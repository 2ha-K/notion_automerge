from notion_client import Client
import os

# 此method回傳一個dict
def create_new_page(database_id: str, title: str, tag: str):
    notion = Client(auth=os.getenv("NOTION_TOKEN")) # 若環境變數不存在，os.getenv() 回傳 None，需手動檢查避免 auth=None
    # **kwargs 會把所有 key=value 的參數打包成 dict
    # 用來傳入多個命名參數，不需要事先定義每一個
    # ✅ 為什麼使用 **kwargs 而不是傳 dict？
    # - kwargs 是語法糖：呼叫者可以直接傳 title="...", tag="..."
    # - dict 則需要手動包一個物件，不直觀
    # - kwargs 實際上在函式內就是一個 dict，方便用 key 取值
    # - 支援 IDE 自動提示、檢查、傳遞彈性
    # - kwargs 也可以方便轉傳給其他需要命名參數的函式（例如 Notion SDK）

    # ➤ 等同於 dict，但寫法更簡潔、更 Pythonic
    # * → 表示位置參數打包（成 tuple），名字不限，常用 *args
    # ** → 表示命名參數打包（成 dict），名字不限，常用 **kwargs
    # ※ 重點在 * 與 **，不是變數名稱
    response = notion.pages.create(
        # 這裡 response 是 dict
        # ⚠️ Notion SDK 會自動幫你處理 JSON body 的結構
        # 你只需要提供 parent / properties / icon / children 等關鍵欄位
        # 其他像 created_time, id, url... 都是 Notion 回傳的結果
        parent={"database_id": database_id},
        properties={
            "Name": {
                "title": [
                    {
                        "text": {"content": title}
                    }
                ]
            },
            "Tags": {
                "rich_text": [
                    {
                        "text": {"content": tag}
                    }
                ]
            }
            # 📝 Notion 的欄位設計採「可選模式」：
            # 只要寫你想要的欄位就好，沒寫的會自動忽略或填空
            # 例如不寫 children ➜ 頁面不含內容；不寫 icon ➜ 無 icon
            # 若要加粗體等格式，須使用 annotations，例如 bold: True
            # 🧠 為什麼這裡不用寫 "type"？
            # 因為 notion-client SDK 會自動幫你推斷與補上必要欄位格式
            # 若你手動使用 requests 呼叫 Notion API，就必須明確寫出所有欄位
            # 優點：簡潔可讀、快速開發
            # 缺點：對 Notion 資料結構理解有限，較難客製控制細節
        }
    )
    return response

def create_new_page_page(page_id: str, title: str):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
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
#✅ 如果你想在 workspace 建立 page，你必須使用 Public Integration 並啟用 insert_content 權限

# def create_new_page_root(title: str):
#     notion = Client(auth=os.getenv("NOTION_TOKEN"))
#     response = notion.pages.create(
#         parent={"type": "workspace"
#                 ,"workspace": True
#                 },
#         properties={
#             "title": [
#                 {
#                     "text": {"content": title}
#                 }
#             ]
#         }
#     )
#     return response
