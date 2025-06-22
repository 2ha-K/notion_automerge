from notion_utils.client import get_notion_client

notion = get_notion_client()


def property_relation_id_exists(combination_database_id, target_database_id):
    """
    Checks whether a relation property linking to the target database exists
    in the specified combination database.

    Args:
        combination_database_id (str): The ID of the combination Notion database.
        target_database_id (str): The ID of the target Notion database to check for relations.

    Returns:
        bool: True if a relation to the target database exists, False otherwise.
    """
    try:
        database = notion.databases.retrieve(database_id=combination_database_id)

        for prop in database["properties"].values():
            if prop["type"] == "relation":
                relation = prop["relation"]
                # Normalize UUID format for comparison (Notion returns hyphenated UUIDs, but some APIs might not)
                if normalize_uuid(relation["database_id"]) == target_database_id:
                    return True
        return False
    except Exception as e:
        raise RuntimeError("Failed to check relation property existence.") from e


def normalize_uuid(uuid_str):
    """
    Normalizes a UUID string by removing hyphens.

    Args:
        uuid_str (str): UUID string with hyphens.

    Returns:
        str: Normalized UUID string without hyphens.
    """
    return uuid_str.replace("-", "")
