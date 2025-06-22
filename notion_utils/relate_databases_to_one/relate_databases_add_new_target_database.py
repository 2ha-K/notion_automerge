from notion_utils.log import log_print_yellow
from notion_utils.relate_databases_to_one.relate_databases_search import get_notion_client, property_relation_id_exists
from notion_utils.search_database import get_target_database_title
from notion_utils.update_database import property_exists

notion = get_notion_client()


def add_new_relate_database_property(new_target_databases_id, combination_database_id):
    """
    Adds a new relation field to the combination database.
    If the relation already exists, it will not be added again.

    Args:
        new_target_databases_id (str): ID of the newly selected target database to relate.
        combination_database_id (str): ID of the combination database to update.

    Returns:
        dict: The updated combination database dictionary.
    """
    # Get the intended relation field name based on the target database's title
    new_property_title = get_target_database_title(new_target_databases_id)
    print(f"Checking relation field: {new_property_title}")

    # Skip adding if a relation to the target database already exists
    if property_relation_id_exists(combination_database_id, target_database_id=new_target_databases_id):
        log_print_yellow(f"Relation to target database '{new_property_title}' already exists.")
        return
    # If a non-relation property already uses the intended field name, force exit (to prevent conflict)
    elif property_exists(combination_database_id, new_property_title):
        raise ValueError(
            f"Field name conflict: '{new_property_title}' already exists. Please rename the target database.")

    # Add new relation field linking to the specified target database
    notion.databases.update(
        database_id=combination_database_id,
        properties={
            new_property_title: {
                "type": "relation",
                "relation": {
                    "database_id": new_target_databases_id,
                    "type": "single_property",
                    "single_property": {
                    }
                }
            }
        }
    )
    log_print_yellow(f"New relation field created: {new_property_title}")
    return
