from notion_client import Client
import os

def property_exists(database_id, property_name):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    database = notion.databases.retrieve(database_id=database_id)
    return property_name in database["properties"]

#更改欄位名(都可以包含主欄位)
def update_database(database_id, old_context, new_context):
    notion = Client(auth=os.getenv('NOTION_TOKEN'))  # ✅ 統一變數名稱
    response = notion.databases.update(
        database_id=database_id,
        properties={
            # ⚠️ Notion API 不允許你直接改變欄位的 type
            # ✅ 你可以改欄位的 name（名稱）來達到「改名」的目的
            # ❌ 不能同時修改 name + type，否則會噴錯
            # Notion 的 databases.update() API 是「資料驅動」而非「顯式聲明導向」的。也就是說，它會根據你提供的欄位內容，自動推斷並設定 type。
            old_context: {
                "name": new_context,
                # "type": "rich_text" 錯誤
            }
        }
    )
    print(response)
    return response

def update_property(database_id, new_property):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    response = notion.databases.update(
        database_id=database_id,
        properties={
            "婚姻狀況": {
                new_property: {},  # ✅ 指定欄位型別
                # "type": "select"
                #🔍 小知識：大部分 property type 都只需要像 "rich_text": {} 這樣，Notion SDK 自動會補上 type，但你也可以顯式加上 "type": "rich_text" 幫助閱讀。
            }
        }
    )
    return response
"""
| 欄位型別           | JSON 結構                                |
| -------------- | -------------------------------------- |
| `title`        | `"title": {}`                          |
| `rich_text`    | `"rich_text": {}`                      |
| `number`       | `"number": { "format": "number" }`     |
| `select`       | `"select": { "options": [...] }`       |
| `multi_select` | `"multi_select": { "options": [...] }` |
| `checkbox`     | `"checkbox": {}`                       |
| `date`         | `"date": {}`                           |
"""
def add_new_property(database_id, new_property, new_property_type):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    if property_exists(database_id, new_property):
        update_database(database_id, new_property, new_property+"1")
        response = notion.databases.update(
            database_id=database_id,
            properties={
                new_property: {
                    new_property_type: {}
                }
            }
        )
        update_database(database_id, new_property+"1", new_property)
    else:
        response = notion.databases.update(
            database_id=database_id,
            properties={
                new_property: {
                    new_property_type: {}
                }
            }
        )
    return response

