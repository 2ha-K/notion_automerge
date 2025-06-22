# cache.py

from notion_utils.client import get_notion_client

notion = get_notion_client()
_page_cache = {}
_database_cache = {}


def get_page(page_id, use_cache=True):
    if use_cache and page_id in _page_cache:
        return _page_cache[page_id]
    page = notion.pages.retrieve(page_id=page_id)
    if use_cache:
        _page_cache[page_id] = page
    return page


def get_database(database_id, use_cache=True):
    if use_cache and database_id in _database_cache:
        return _database_cache[database_id]
    db = notion.databases.retrieve(database_id=database_id)
    if use_cache:
        _database_cache[database_id] = db
    return db


def release_database(database_id):
    _database_cache.pop(database_id, None)


def release_page(page_id):
    _page_cache.pop(page_id, None)


def clear_all_cache():
    _page_cache.clear()
    _database_cache.clear()
