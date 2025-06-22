from notion_utils.log import log_error
from notion_utils.log import log_print_green, log_print_yellow
from notion_utils.search_database import get_target_database_title
from notion_utils.update_database import update_database_property_type, get_notion_client

notion = get_notion_client()


def update_standard_database_property(combination_database_id):
    """
    Ensure standard structure in the combination database for dynamic data synchronization.
    Required fields: Name, Database Location, Created Time, Last Edited Time.

    Args:
        combination_database_id (str): The ID of the combination Notion database.
    """
    try:
        # Ensure the title field is named 'Name'

        rename_title_to_name(combination_database_id)
        log_print_yellow("Title field verified: Name")

        update_database_property_type(combination_database_id, "rich_text", "Database Location")
        log_print_yellow("Field verified: Database Location")

        update_database_property_type(combination_database_id, "date", "Created Time")
        log_print_yellow("Field verified: Created Time")

        update_database_property_type(combination_database_id, "date", "Last Edited Time")
        log_print_yellow("Field verified: Last Edited Time")
    except RuntimeError as re:
        log_error("Failed to update standard database properties.")
        raise RuntimeError("Failed to update standard database properties.") from re


def sync_relation_names_with_database_titles(combination_database_id):
    """
    Ensure all relation field names in the combination database match the corresponding source database titles.

    Args:
        combination_database_id (str): ID of the combination Notion database.
    """
    try:
        database = notion.databases.retrieve(database_id=combination_database_id)
        updates = {}

        for prop_name, prop in database["properties"].items():
            if prop["type"] == "relation":
                target_id = prop["relation"]["database_id"]
                correct_name = get_target_database_title(target_id)
                if prop_name != correct_name:
                    log_print_yellow(f"Renaming field '{prop_name}' to '{correct_name}'...")
                    updates[prop_name] = {
                        "name": correct_name,
                    }

        if updates:
            notion.databases.update(
                database_id=combination_database_id,
                properties=updates
            )
            log_print_green("All relation field names updated successfully.")
        else:
            log_print_green("All relation field names are up to date.")
    except Exception as e:
        log_error("Failed to sync relation field names with database titles.")
        raise RuntimeError("Failed to sync relation field names with database titles.") from e


def check_combination_database_pages_format(combination_database_id):
    """
    Validate page format rules in the combination database:
    - No duplicate relation field names
    - No multiple relations pointing to the same target database
    - Each page should relate to at most one source page

    Args:
        combination_database_id (str): ID of the combination Notion database.
    """
    try:
        database = notion.databases.retrieve(database_id=combination_database_id)
        properties = database["properties"]

        # Check for duplicate relation field names in schema
        seen_names = set()
        for name, prop in properties.items():
            if prop["type"] == "relation":
                if name in seen_names:
                    raise ValueError(f"Duplicate relation field name detected: {name}")
                seen_names.add(name)

        # Check if multiple relation fields point to the same target database
        seen_targets = set()
        for prop in properties.values():
            if prop["type"] == "relation":
                target_id = prop["relation"]["database_id"]
                if target_id in seen_targets:
                    raise ValueError(f"Multiple relations point to the same target database ID: {target_id}")
                seen_targets.add(target_id)

        has_more = True
        start_cursor = None
        while has_more:
            response = notion.databases.query(
                database_id=combination_database_id,
                start_cursor=start_cursor
            )
            pages = response["results"]
            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor", None)

            # Collect all non-empty relation fields for this page
            for page in pages:
                props = page["properties"]
                related = {}
                for name, prop in props.items():
                    if name in properties and properties[name]["type"] == "relation":
                        rel_data = prop["relation"]
                        if rel_data:
                            related[name] = len(rel_data)

                # Each page should relate to only one source; reject if more than one
                if len(related) >= 2:
                    raise ValueError(f"Page {page['id']} has multiple relation links: {list(related.keys())}")

                if len(related) == 1:
                    rel_name, count = next(iter(related.items()))
                    if count > 1:
                        raise ValueError(
                            f"Page {page['id']} relation '{rel_name}' links to more than one page ({count})")
        log_print_green("Page format validation passed successfully.")
    except Exception as e:
        log_error("Failed to validate page format rules in the combination database")
        raise RuntimeError("Failed to sync relation field names with database titles.") from e


def rename_title_to_name(database_id: str):
    """
    Rename the database's title property to 'Name' if not already named.

    Args:
        database_id (str): ID of the Notion database.
    """
    try:
        db = notion.databases.retrieve(database_id=database_id)
        properties = db["properties"]

        title_prop_name = None
        # Find the first field of type 'title' (usually there's only one)
        for prop_name, prop_info in properties.items():
            if prop_info["type"] == "title":
                title_prop_name = prop_name
                break

        if not title_prop_name:
            raise ValueError("No title field found in the database.")

        if title_prop_name != "Name":
            log_print_yellow(f"Renaming title field '{title_prop_name}' to 'Name'...")
            notion.databases.update(
                database_id=database_id,
                properties={
                    title_prop_name: {
                        "name": "Name",
                    }
                }
            )
        else:
            log_print_yellow("Title field already named 'Name'. No change required.")
    except Exception as e:
        raise RuntimeError("Failed to rename title field to 'Name'.") from e
