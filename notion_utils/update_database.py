"""
notion_utils/update_database.py

Purpose:
    Provides utility functions for modifying Notion database schemas, including:
    - Renaming properties
    - Changing property types
    - Adding new properties safely (with name conflict resolution)

Features:
    - Safe property name updates with conflict avoidance
    - Automatic type update only when necessary
    - Add property with rollback support if name collision occurs
    - Built-in checks using `property_exists` and current schema inspection

Used in:
    - Phase 3–5: To prepare combination database schema before syncing
    - GUI schema validation or pre-sync formatting
    - Standardizing structure across merged databases

Functions:
    - update_database_property_name(): Rename an existing property
    - update_database_property_type(): Change the type of a property
    - add_new_property(): Add new property with collision-safe fallback
"""

from notion_utils.cache import get_database
from notion_utils.client import get_notion_client
from notion_utils.search_database import property_exists

notion = get_notion_client()


def update_database_property_name(database_id, target_context, new_context):
    """
    Rename a property in a Notion database.

    Args:
        database_id (str): The ID of the Notion database.
        target_context (str): The current property name to rename.
        new_context (str): The new name to assign.

    Returns:
        dict or None: Updated database object if successful, otherwise None.
    """

    try:
        database = get_database(database_id, False)
        if target_context not in database["properties"]:
            raise ValueError(f"Property '{target_context}' not found.")
        if target_context == new_context:
            return database  # No change needed
        response = notion.databases.update(
            database_id=database_id,
            properties={
                target_context: {
                    "name": new_context,  # Cannot change "name" and "type" at the same time
                }
            }
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to rename property '{target_context}'") from e


def update_database_property_type(database_id, new_property_type, target_property_name):
    """
    Change the type of a property in a Notion database.

    Args:
        database_id (str): The ID of the Notion database.
        new_property_type (str): Type to apply (e.g., 'rich_text', 'number').
        target_property_name (str): The name of the property to modify.

    Returns:
        dict or None: Updated database object if successful, otherwise None.
    """
    schema = notion.databases.retrieve(database_id=database_id)["properties"]
    if target_property_name in schema:
        current_type = schema[target_property_name]["type"]
        if current_type == new_property_type:
            return
    try:
        notion.databases.update(
            database_id=database_id,
            properties={
                target_property_name: {
                    new_property_type: {},  # Notion API will automatically detect type from the property format
                }
            }
        )
        return
    except Exception as e:
        raise RuntimeError(f"Failed to update type for property '{target_property_name}'") from e


def add_new_property(database_id, new_property_name, new_property_type):
    """
    Add a new property to a Notion database. If it already exists, temporarily rename it to avoid conflict.

    Args:
        database_id (str): The ID of the Notion database.
        new_property_name (str): The name of the property to add.
        new_property_type (str): The type of the property to add.

    Returns:
        dict or None: Updated database object if successful, otherwise None.
    """

    try:
        if property_exists(database_id, new_property_name):
            # Rename existing conflicting property temporarily
            update_database_property_name(database_id, new_property_name, new_property_name + "1")

            # Add the new property with the desired name
            response = notion.databases.update(
                database_id=database_id,
                properties={
                    new_property_name: {
                        new_property_type: {}
                    }
                }
            )

            # Restore the original name to the temporarily renamed property
            update_database_property_name(database_id, new_property_name + "1", new_property_name)  # 再改回原本的名字
        else:
            # Property doesn't exist; directly add the new property
            response = notion.databases.update(
                database_id=database_id,
                properties={
                    new_property_name: {
                        new_property_type: {}
                    }
                }
            )
        return response

    except Exception as e:
        raise RuntimeError(f"Failed to add property '{new_property_name}'") from e
