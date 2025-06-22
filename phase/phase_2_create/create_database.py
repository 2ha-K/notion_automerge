"""
在 Notion 中，workspace page ID 通常是你帳號底下的某個「頂層頁面」的 ID（也就是 Notion 根目錄下直接顯示的頁面）。
你不能直接把 database 建在「完全沒有 parent 的 root」，但可以放在某個「你的 Notion 首頁」裡。
"""
from notion_client import Client
import os

def create_new_database(page_id: str, db_title: str):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    return notion.databases.create(
        parent={"type": "page_id", "page_id": page_id},
        title=[{"type": "text", "text": {"content": db_title}}],
        properties={
            "Name": {"title": {}},
            "Category": {"rich_text": {}}
        }
    )
