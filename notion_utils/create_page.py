from notion_utils.client import get_notion_client

# Initialize the Notion client
notion = get_notion_client()


def create_new_page(database_id: str, property_title, property_rich_text, title: str, tag: str) -> dict | None:
    """
    Create a new page in a Notion database with title and rich_text fields.

    Args:
        database_id (str): The ID of the target Notion database.
        property_title (str): Name of the title property in the database.
        property_rich_text (str): Name of the rich_text property in the database.
        title (str): The page title to insert.
        tag (str): The tag or rich text content to insert.

    Returns:
        dict | None: The created page as a dictionary, or None if failed.
    """
    try:
        # Create a new page in the specified database with title and tag
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties={
                property_title: {
                    "title": [
                        {
                            "text": {"content": title}
                        }
                    ]
                },
                property_rich_text: {
                    "rich_text": [
                        {
                            "text": {"content": tag}
                        }
                    ]
                }
            }
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to create page in database") from e


def create_new_page_page(page_id: str, title: str) -> dict | None:
    """
    Create a sub-page under a given Notion page.

    Args:
        page_id (str): The ID of the parent Notion page.
        title (str): The title of the new sub-page.

    Returns:
        dict | None: The created page dictionary, or None if failed.
    """
    try:
        # Create a new sub-page under the specified page
        response = notion.pages.create(
            parent={"page_id": page_id},
            properties={
                "title": [
                    {
                        "text": {"content": title}
                    }
                ]
            }
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to create sub-page in page '{page_id}'") from e


def create_new_page_root(title: str) -> dict | None:
    """
    Create a page in the root workspace.

    Args:
        title (str): The title of the new root-level page.

    Returns:
        dict | None: The created page dictionary, or None if failed.
    """
    try:
        # Create a new top-level page directly in the workspace
        response = notion.pages.create(
            parent={"type": "workspace"
                , "workspace": True
                    },
            properties={
                "title": [
                    {
                        "text": {"content": title}
                    }
                ]
            }
        )
        return response
    except Exception as e:
        raise RuntimeError("Failed to create page at root") from e
