"""
notion_utils/update_all_target_database_to_combi.py

Purpose:
    This module acts as the core controller to synchronize and integrate multiple source Notion databases
    into a centralized combination database. It handles syncing page content, relations, metadata,
    and removes orphaned pages. All major actions are multi-threaded for performance.

Key Features:
    - Merge multiple target databases into one central database.
    - Deduplicate entries via relation checking.
    - Auto-update metadata: creation time, last edited time, source database, and page title.
    - Remove pages with no valid source reference (orphan cleanup).
    - Multithreaded for high performance across all page operations.

Used in:
    - Phase 5: Conditional Merge
    - Final Integration Layer (sync engine)
    - GUI-triggered synchronization

Core Functions:
    - update_all_target_database_to_combi(): Main entrypoint to sync all target DBs into the combination DB.
    - update_single_target_database_to_combi(): Syncs one target DB with relation-based deduplication.
    - update_page_to_combi(): Adds or skips a page based on whether it already exists.
    - delete_no_relation_pages(): Deletes pages that lack source linkage.
    - update_all_pages_properties(): Copies metadata from source pages into merged records.
    - update_page_properties(): Updates a single page's metadata (title, timestamps, origin).
    - Helper functions like add_new_page(), is_page_id_in_combi_relation_id() assist in structure & validation.
"""

from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed

import notion_utils.search_database as search_database
from notion_utils.cache import get_page
from notion_utils.log import log_print_yellow, log_print_green, log_error
from notion_utils.search_page import get_parent_of_page_id, get_page_title, get_page_create_time, \
    get_page_last_edited_time

notion = search_database.get_notion_client()


def update_all_target_database_to_combi(target_databases_id_list, combination_database_id):
    """
    Main controller: Synchronize all target databases into the combination database.

    Args:
        target_databases_id_list (List[str]): List of Notion database IDs to merge from.
        combination_database_id (str): The ID of the destination (merged) Notion database.
    """
    target_databases_title_list = []
    # Merge each target database into the combination database
    for target_database_id in target_databases_id_list:
        update_single_target_database_to_combi(target_database_id, combination_database_id)
        target_databases_title_list.append(search_database.get_target_database_title(target_database_id))

    log_print_green("All target databases merged.")

    # Delete pages that are no longer linked to any source
    print("Removing orphan pages...")
    delete_no_relation_pages(combination_database_id, target_databases_title_list)
    log_print_green("Orphan pages removed.")

    # Update metadata like creation time, last edited time, etc.
    print("Updating metadata...")
    update_all_pages_properties(combination_database_id, target_databases_title_list)
    log_print_green("Metadata updated.")


def update_single_target_database_to_combi(target_database_id, combination_database_id):
    """
    Synchronize a single target database into the combination database.

    Args:
        target_database_id (str): The ID of the target Notion database.
        combination_database_id (str): The ID of the combination Notion database.
    """
    try:
        pages_id = get_page_id_list(target_database_id)
        target_database_title = search_database.get_target_database_title(target_database_id)
        #     for page in pages_id["results"]:
        #         # Update each page
        #         update_page_to_combi(page["id"], combination_database_id, target_database_title, target_database_id)
        #     log_print_green(f"Database '{target_database_title}' merged.")
        # except Exception as e:
        #     log_error(f"Error merging database {target_database_id}.", e)
        pages = pages_id["results"]

        def update_one(page):
            try:
                update_page_to_combi(page["id"], combination_database_id, target_database_title, target_database_id)
            except Exception as e:
                log_error(f"Failed to update page {page['id']} from '{target_database_title}'", e)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(update_one, page) for page in pages]
            for future in as_completed(futures):
                future.result()
        log_print_green(f"Database '{target_database_title}' merged.")
    except Exception as e:
        log_error(f"Error full merging database {target_database_id}.", e)
        raise


def update_page_to_combi(page_id, combination_database_id, target_database_title, target_database_id):
    """
    Add or update a page from target database into the combination database.

    Args:
        page_id (str): The page ID from target database.
        combination_database_id (str): The combination database ID.
        target_database_title (str): The title of the target database.
        target_database_id (str): The ID of the target database.
    """
    try:
        title_property = search_database.get_target_database_title_property_name(target_database_id)
        # Check if page already exists in the combination database
        if not is_page_id_in_combi_relation_id(page_id, combination_database_id, target_database_title):
            # Add new page to the combination database
            add_new_page_helper(page_id, combination_database_id, target_database_title, title_property)
            log_print_yellow(
                "Page '%s' has been added to the combination database." % search_database.get_target_page_title(page_id,
                                                                                                                title_property))
        else:
            # Page already linked, no update needed
            log_print_yellow("Page has no updates: %s" % search_database.get_target_page_title(page_id, title_property))

    except RuntimeError as e:
        log_error(f"Failed to update page {page_id}.", e)
        raise RuntimeError(f"Failed to update page {page_id}.") from e


def get_page_id_list(database_id):
    """
    Retrieves all page IDs from the specified Notion database.

    Args:
        database_id (str): The ID of the Notion database.

    Returns:
        List[str]: List of page IDs.
    """
    try:
        all_page_ids = []
        response = notion.databases.query(database_id=database_id)
        # for page in response["results"]:
        #     # Collect page IDs
        #     all_page_ids.append(page["id"])
        #
        # print("Retrieved %d pages for a database." % len(all_page_ids))
        # return all_page_ids
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve pages from database {database_id}.") from e


def is_page_id_in_combi_relation_id(page_id, combination_database_id, target_database_title):
    """
    Checks if the given page ID is already related in the combination database.

    Args:
        page_id (str): ID of the page to check.
        combination_database_id (str): ID of the destination database.
        target_database_title (str): Property name used for the relation.

    Returns:
        bool: True if already linked, False otherwise.
    """
    try:
        response = notion.databases.query(database_id=combination_database_id)

        for page in response["results"]:
            # Check if relation field is not empty
            if not page["properties"][target_database_title]["relation"] == []:
                # Compare relation ID with source page ID
                if page_id == page["properties"][target_database_title]["relation"][0]["id"]:
                    return True
        return False
    except Exception as e:
        raise RuntimeError(f"Failed to check relation for page {page_id}.") from e


def add_new_page(page_id, database_id, database_title_property_name, database_relation_property_name, title_property):
    """
    Creates a new page in the destination database with appropriate title and relation.

    Args:
        page_id (str): ID of the source page.
        database_id (str): ID of the target Notion database.
        database_title_property_name (str): Name of the title property in the target database.
        database_relation_property_name (str): Name of the relation property in the target database.
        title_property (str): Name of the title property in the source page.
    """
    try:
        page_title = search_database.get_target_page_title(page_id, title_property)

        # Construct new page payload
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                database_title_property_name: {
                    "type": "title",
                    "title": [
                        {
                            "text": {"content": page_title}
                        }
                    ]
                },
                database_relation_property_name: {
                    "type": "relation",
                    "relation": [
                        {
                            "id": page_id
                        }
                    ]
                }
            }
        )
    except Exception as e:
        raise RuntimeError(f"Failed to add new page {page_id}.") from e


def add_new_page_helper(page_id, database_id, target_database_title, title_property):
    """
    Helper to prepare correct property names and delegate page creation.

    Args:
        page_id (str): ID of the page.
        database_id (str): ID of the destination database.
        target_database_title (str): Title of the source database used as relation field.
        title_property (str): Name of the page title property.
    """
    try:
        # Get the title field name for the combination database
        database_title_property_name = search_database.get_target_database_title_property_name(database_id)
        database_relation_property_name = target_database_title
        add_new_page(page_id, database_id, database_title_property_name, database_relation_property_name,
                     title_property)
    except Exception as e:
        log_error(f"Failed to invoke page helper for {page_id}.", e)
        raise RuntimeError(f"Failed to invoke page helper for {page_id}.") from e


def delete_page(page_id):
    """
    Archives a page in Notion (soft delete).

    Args:
        page_id (str): ID of the page to archive.
    """
    try:
        page = get_page(page_id)
        if page.get("archived"):
            return  # Already archived, skip
        notion.pages.update(
            page_id=page_id,
            archived=True
        )
    except Exception as e:
        raise RuntimeError(f"Failed to archive page {page_id}.") from e


def delete_no_relation_pages(combination_database_id, relation_property_name_list):
    """
    Multithreaded: Delete pages in the combination database that have no relation.

    Args:
        combination_database_id (str): The ID of the destination database.
        relation_property_name_list (List[str]): List of relation property names to check.
    """
    try:
        pages_id_list = get_page_id_list(combination_database_id)
        pages = pages_id_list["results"]

        def process_single_page(page):
            try:
                full_page = get_page(page["id"])
                for relation_property_name in relation_property_name_list:
                    if full_page["properties"].get(relation_property_name, {}).get("relation"):
                        log_print_yellow(f"Keep page: {get_page_title(page["id"])}")
                        return  # Page has at least one relation → skip

                delete_page(page["id"])
                log_print_yellow(f"Deleted page: {get_page_title(page['id'])}")
            except Exception as e:
                log_error(f"Failed to process/delete page {page['id']}", e)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_single_page, page) for page in pages]
            for future in as_completed(futures):
                future.result()


    except Exception as e:
        raise RuntimeError(f"Failed to delete all unlinked pages.") from e


def update_all_pages_properties(combination_database_id, relation_property_name_list):
    """
    Multithreaded: Update metadata fields for all pages in the combination database.

    Args:
        combination_database_id (str): ID of the merged database.
        relation_property_name_list (List[str]): Relation properties to check for mapping.
    """
    try:
        pages_id_list = get_page_id_list(combination_database_id)
        pages = pages_id_list["results"]

        def update_single_page(page):
            # for page in pages_id_list["results"]:
            try:
                for relation_property_name in relation_property_name_list:
                    # Find the related source page via relation
                    response = get_page(page["id"], True)
                    if response["properties"][relation_property_name]["relation"]:
                        relate_page_id = response["properties"][relation_property_name]["relation"][0]["id"]

                        # Extract metadata from source page
                        create_time = get_page_create_time(relate_page_id)

                        last_edited_time = get_page_last_edited_time(relate_page_id)

                        database_id = get_parent_of_page_id(relate_page_id)
                        database_title = search_database.get_target_database_title(database_id)

                        page_title = get_page_title(relate_page_id)

                        # Apply metadata to combined page
                        update_page_properties(page["id"], create_time, last_edited_time, database_title, page_title)
                        log_print_yellow("Page properties updated: %s." % page_title)
                        return
            except Exception as e:
                log_error(f"Failed to update page metadata: {page['id']}", e)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(update_single_page, page) for page in pages]
            for future in as_completed(futures):
                future.result()

    except Exception as e:
        raise RuntimeError("Failed to update page properties.", e)


def update_page_properties(page_id, create_time, update_time, location, title):
    """
    Applies metadata updates (creation time, last edited time, source location, and title) to a page.

    Args:
        page_id (str): ID of the page to update.
        create_time (str): ISO timestamp of page creation.
        update_time (str): ISO timestamp of last edit.
        location (str): Source database title.
        title (str): Title of the original page.
    """
    try:
        # Send update to Notion
        notion.pages.update(
            page_id=page_id,
            properties={
                "Created Time": {
                    "date": {
                        "start": create_time
                    }
                },
                "Last Edited Time": {
                    "date": {
                        "start": update_time
                    }
                },
                "Database Location": {
                    "rich_text": [
                        {
                            "text": {
                                "content": location
                            }
                        }
                    ]
                },
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            }
        )
    except Exception as e:
        raise RuntimeError(f"Failed to update properties for page {page_id}.") from e
