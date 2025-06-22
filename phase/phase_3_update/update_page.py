from notion_client import Client
import os


def update_page_property(page_id, property_name, new_value, property_type):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))

    if property_type == "title":
        property_value = {
            property_name: {
                "title": [
                    {
                        "text": {"content": new_value},
                    }
                ]
            }
        }
    elif property_type == "rich_text":
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
        property_value = {
            property_name: {
                "checkbox": bool(new_value) #這是甚麼?這是 Python 的 型別轉換，會將value 轉成一切可能的布林值：
            }
        }
    elif property_type == "number":
        property_value = {
            property_name: {
                "number": new_value
            }
        }
    elif property_type == "select":
        property_value = {
            property_name: {
                "select": {
                    "name": new_value,
                }
            }
        }
    else:
        raise ValueError(f"Property type {property_type} not supported or do not code at here lol!")
    response = notion.pages.update(
        page_id=page_id,
        properties=property_value
    )
    return response


def delete_page(page_id):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    response = notion.pages.update(
        page_id=page_id,
        archived = True
    )
    return response