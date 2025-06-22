from notion_utils.cache import get_page
from notion_utils.client import get_notion_client
from notion_utils.log import log_error

notion = get_notion_client()


def get_target_page_title(page_id, title_property):
    """
    Retrieve the plain-text title from a specific property of a page.

    Args:
        page_id (str): The ID of the Notion page.
        title_property (str): The property name that holds the title.

    Returns:
        str or None: The title text, or None if not found.
    """

    try:
        response = get_page(page_id, True)
        title = response["properties"][title_property]["title"][0]["plain_text"]
        return title
    except Exception as e:
        raise RuntimeError(f"Failed to get title from page '{page_id}'") from e


def get_target_page_dict(page_id):
    """
    Retrieve the full page object from Notion.

    Args:
        page_id (str): The ID of the Notion page.

    Returns:
        dict or None: Page object, or None if not found or error.
    """

    try:
        response = get_page(page_id, True)  # query is design for a database can work with filter, sort, etc.
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve page '{page_id}'") from e


def is_page_id_exist(page_id):
    """
    Check if a Notion page ID exists.

    Args:
        page_id (str): The page ID to check.

    Returns:
        bool: True if exists, False otherwise.
    """

    try:
        page = get_page(page_id, True)  # If this doesn't raise, the page exists
        if page:
            return True
        return False
    except Exception as e:
        print(str(e))
        return False


def get_page_create_time(page_id):
    """
    Get the created time of a page.

    Args:
        page_id (str): The ID of the page.

    Returns:
        str or None: ISO timestamp string, or None on error.
    """

    try:
        response = get_page(page_id, True)
        return response["created_time"]  # ISO 8601 format
    except Exception as e:
        log_error(f"Failed to get created time for page '{page_id}'", e)
        return None


def get_page_last_edited_time(page_id):
    """
    Get the last edited time of a page.

    Args:
        page_id (str): The ID of the page.

    Returns:
        str or None: ISO timestamp string, or None on error.
    """

    try:
        response = get_page(page_id, True)
        return response["last_edited_time"]  # ISO 8601 format
    except Exception as e:
        log_error(f"Failed to get last edited time for page '{page_id}'", e)
        return None


def get_parent_of_page_id(page_id):
    """
    Get the database ID that owns the page (if applicable).

    Args:
        page_id (str): The ID of the page.

    Returns:
        str or None: Database ID if parent is a database, else None.
    """

    try:
        page = get_page(page_id, True)
        parent = page["parent"]  # Get parent info
        if parent["type"] == "database_id":
            return parent["database_id"]
        raise ValueError("Failed to find parent id")
    except Exception as e:
        raise RuntimeError(f"Failed to get parent of page '{page_id}'") from e


def get_page_title(page_id):
    """
    Auto-detect and return the title of a Notion page.

    Args:
        page_id (str): The ID of the page.

    Returns:
        str or None: The title string, or None if not found.
    """

    try:
        page = get_page(page_id, True)
        properties = page["properties"]  # All fields in the page
        for name, prop in properties.items():
            if prop["type"] == "title":  # Look for the field with type 'title'
                title_list = prop["title"]
                if title_list:
                    return title_list[0]["text"]["content"]  # Return raw title string
        raise ValueError(f"Failed to get title from page '{page_id}'")
    except Exception as e:
        raise RuntimeError(f"Failed to auto-detect title for page '{page_id}'") from e
