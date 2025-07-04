"""
notion_utils/search_database.py

Purpose:
    Provides utility functions to query, validate, and extract metadata from Notion databases and pages.
    These functions are primarily used to support dynamic schema resolution, validation, and data retrieval
    across the entire database merging pipeline.

Features:
    - Fetch full database or page objects
    - Extract display titles from Notion databases and pages
    - Dynamically resolve the name of the 'title' property in any database
    - Check for the existence of specific properties
    - Validate database ID existence via safe access

Used in:
    - Phase 2–5: During conditional merge, schema validation, and page generation
    - Metadata syncing, GUI inspection, and error handling

Functions:
    - get_target_database_dict(): Return full database schema
    - get_target_database_title(): Extract the display title of a database
    - get_target_database_title_property_name(): Find the name of the 'title' property field
    - property_exists(): Check if a property exists in a database
    - get_target_page_title(): Get plain-text title of a page
    - get_target_page_dict(): Return full page metadata
    - is_valid_database(): Validate a database ID (returns True/False)
"""

from notion_utils.cache import get_page, get_database
from notion_utils.client import get_notion_client

# Initialize the Notion client using the auth token
notion = get_notion_client()


def get_target_database_dict(database_id):
    """
    Retrieve the full database object by ID.
    """
    try:
        return notion.databases.retrieve(database_id=database_id)  # Fetch the database metadata
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve database '{database_id}'") from e


def get_target_database_title(database_id):
    """
    Get the display title of a Notion database.
    """
    try:
        response = get_database(database_id, True)  # Retrieve database info
        title_list = response["title"]  # Get the list of rich text title blocks
        if title_list:
            return title_list[0]["plain_text"]  # Extract plain text from the first block
        raise ValueError(f"Failed to get title of database '{database_id}'")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve title for database '{database_id}'") from e


def get_target_database_title_property_name(database_id):
    """
    Get the name of the 'title' property field in a database.
    """
    try:
        response = notion.databases.retrieve(database_id=database_id)  # Get full schema
        for prop_name, prop_data in response["properties"].items():  # Check if this property is of type 'title'
            if prop_data["type"] == "title":
                return prop_name
        raise ValueError(f"Failed to find 'title' property in database '{database_id}'")
    except Exception as e:
        raise RuntimeError(f"Failed to get title property name from database '{database_id}'") from e


def property_exists(database_id, property_name):
    """
    Check if a property exists in a database.

    Returns:
        bool: True if property exists, False otherwise.
    """
    try:
        database = notion.databases.retrieve(database_id=database_id)
        return property_name in database["properties"]  # Check for existence of the property
    except Exception as e:
        raise RuntimeError(f"Failed to check property '{property_name}' in database '{database_id}'")from e


def get_target_page_title(page_id, title_property):
    """
    Retrieve the title value from a page using the specified title property.
    """
    try:
        response = get_page(page_id, True)
        title = response["properties"][title_property]["title"][0]["plain_text"]  # Extract title plain text
        return title
    except Exception as e:
        raise RuntimeError(f"Failed to get title from page '{page_id}'") from e


def get_target_page_dict(page_id):
    """
    Retrieve the full page object by ID.
    """
    try:
        response = get_page(page_id, True)  # Get all page metadata
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to get page '{page_id}'") from e


def is_valid_database(database_id):
    try:
        notion.databases.retrieve(database_id=database_id)
        return True
    except Exception:
        print(f"[!] Invalid database ID: {database_id}")
        return False
