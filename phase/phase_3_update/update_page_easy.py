from notion_client import Client
import os

def update_rich_text_property(page_id, property_name, new_text):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))

    response = notion.pages.update(
        page_id=page_id,
        properties={
            property_name: {
                "rich_text": [
                    {
                        "text": {
                            "content": new_text
                        }
                    }
                ]
            }
        }
    )

    return response
