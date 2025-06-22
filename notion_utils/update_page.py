from notion_utils.cache import get_page
from notion_utils.client import get_notion_client

notion = get_notion_client()


def update_page_property(page_id, property_name, new_value, property_type):
    """
    Update a specific property of a Notion page.

    Args:
        page_id (str): The ID of the page to update.
        property_name (str): The name of the property to update.
        new_value (Any): The new value to assign.
        property_type (str): The type of the property (e.g., 'title', 'rich_text', 'checkbox', 'number', 'select').

    Returns:
        dict: The updated page object from Notion API.

    Raises:
        ValueError: If the property_type is not supported.
    """

    # Build the property value format based on the type
    if property_type == "title":
        property_value = {
            # Title requires a list of text objects
            property_name: {
                "title": [
                    {
                        "text": {"content": new_value},
                    }
                ]
            }
        }
    elif property_type == "rich_text":
        # Rich text block for paragraph-style text content
        property_value = {
            property_name: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": new_value},
                    }
                ]
            }
        }
    elif property_type == "checkbox":
        # Boolean property (converted explicitly)
        property_value = {
            property_name: {
                "checkbox": bool(new_value)  # Converts any value to boolean
            }
        }
    elif property_type == "number":
        # Numeric field
        property_value = {
            property_name: {
                "number": new_value
            }
        }
    elif property_type == "select":
        # Select property with predefined option
        property_value = {
            property_name: {
                "select": {
                    "name": new_value,
                }
            }
        }
    else:
        # Unknown property type
        raise ValueError(f"Unsupported property type: {property_type}")

    try:
        # Update the page with new property
        response = notion.pages.update(
            page_id=page_id,
            properties=property_value
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to update page property '{property_name}' ({property_type})")


def delete_page(page_id):
    """
    Archive (soft delete) a Notion page.

    Note:
        Notion does not support true deletion via API. This function marks the page as archived,
        which is the recommended way to remove it from the workspace view.

    Args:
        page_id (str): The ID of the page to archive.

    Returns:
        dict: The updated page object from Notion API, or None if failed.
    """
    try:
        page = get_page(page_id)
        if page.get("archived"):
            return page  # Already archived, skip
        # Soft delete by setting `archived` to True
        response = notion.pages.update(
            page_id=page_id,
            archived=True
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to delete (archive) page: {page_id}")
