"""
notion_utils/create_database.py

Purpose:
    Provides a utility function to programmatically create a new Notion database under a given parent page.
    This is commonly used in tools that auto-generate merged or combined databases during setup.

Features:
    - Uses Notion API to create a database with customizable `title` and `rich_text` properties
    - Designed to support dynamic database generation from the GUI or sync logic

Used in:
    - Phase 6+: GUI-based one-click creation of combination databases
    - Setup process for merged database pipelines

Function:
    - create_new_database(): Create a new database with specified structure under a Notion page
"""

from notion_utils.client import get_notion_client

# Initialize Notion client
notion = get_notion_client()


def create_new_database(page_id: str, db_title: str, property_title: str, property_rich_text: str) -> dict | None:
    """
    Create a new Notion database under the given page.

    Args:
        page_id (str): ID of the parent Notion page.
        db_title (str): Title of the new database.
        property_title (str): Name of the 'title' property.
        property_rich_text (str): Name of the 'rich_text' property.

    Returns:
        dict | None: The created database object, or None if creation fails.
    """
    try:
        # Use Notion API to create a new database with title and rich_text fields
        return notion.databases.create(
            parent={"type": "page_id", "page_id": page_id},
            title=[{"type": "text", "text": {"content": db_title}}],
            properties={
                property_title: {"title": {}},
                property_rich_text: {"rich_text": {}}
            }
        )
    except Exception as e:
        raise RuntimeError(f"Failed to create new database") from e
