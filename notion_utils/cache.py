"""
notion_utils/cache.py

Purpose:
    Implements simple in-memory caching for Notion pages and databases to reduce redundant API calls.
    This improves performance for read-heavy operations such as:
    - Page property lookups
    - Database schema validations
    - Metadata extraction for syncing

Features:
    - Optional cache toggle (`use_cache=True`) for each call
    - Individual release functions for fine-grained control
    - Global cache clearing for reset scenarios (e.g., full sync)

Used in:
    - Phase 4–5: During batch processing and metadata updates
    - All modules that repeatedly access the same pages/databases

Functions:
    - get_page(): Fetch a page, with optional caching
    - get_database(): Fetch a database, with optional caching
    - release_page(): Remove one page from cache
    - release_database(): Remove one database from cache
    - clear_all_cache(): Clear everything from memory
"""

from notion_utils.client import get_notion_client

# Get the Notion client instance
notion = get_notion_client()

# Internal caches for pages and databases
_page_cache = {}
_database_cache = {}


def get_page(page_id, use_cache=True):
    """
    Retrieve a Notion page, optionally using a cache to avoid redundant API calls.

    Args:
        page_id (str): The ID of the page to retrieve.
        use_cache (bool): If True, use the cache if available.

    Returns:
        dict: The page data.
    """
    if use_cache and page_id in _page_cache:
        # Return from cache if available
        return _page_cache[page_id]
    # Retrieve page from Notion API
    page = notion.pages.retrieve(page_id=page_id)
    if use_cache:
        _page_cache[page_id] = page
    return page


def get_database(database_id, use_cache=True):
    """
        Retrieve a Notion database, optionally using a cache to avoid redundant API calls.

        Args:
            database_id (str): The ID of the database to retrieve.
            use_cache (bool): If True, use the cache if available.

        Returns:
            dict: The database data.
        """
    if use_cache and database_id in _database_cache:
        return _database_cache[database_id]
    db = notion.databases.retrieve(database_id=database_id)
    if use_cache:
        _database_cache[database_id] = db
    return db


def release_database(database_id):
    """
    Remove a specific database from the cache.

    Args:
        database_id (str): The ID of the database to remove.
    """
    _database_cache.pop(database_id, None)


def release_page(page_id):
    """
    Remove a specific page from the cache.

    Args:
        page_id (str): The ID of the page to remove.
    """
    _page_cache.pop(page_id, None)


def clear_all_cache():
    """
    Clear all cached pages and databases.
    """
    _page_cache.clear()
    _database_cache.clear()
