from notion_client import Client
import json
import os

"""
🔍 為什麼要使用 JSON，而不是直接使用 Python 的 dict？

1. 跨語言資料交換：
   Python 的 dict 是 Python 特有的資料結構，無法直接被 JavaScript、Java、C++ 等其他語言理解。
   JSON（JavaScript Object Notation）是一種通用資料交換格式，所有主流程式語言都能讀寫。

2. 儲存與傳輸：
   JSON 是純文字格式，可以用來儲存在檔案中或透過網路傳送。
   如果你要將資料寫入檔案、儲存在資料庫、或用 API 傳送，就必須使用 JSON。
   不能直接把 Python 的 dict 寫入硬碟或網路，因為它是記憶體內的結構。

3. 人與機器皆可讀：
   JSON 是一種結構清晰、易於閱讀的純文字格式。
   將 dict 轉換為 JSON 後可以加上縮排（indent）來美化輸出，方便除錯與查閱。

🔄 dict 與 JSON 互轉方式：

從 JSON ➜ Python dict：
- 使用 json.load(file) 或 json.loads(json_string)

從 Python dict ➜ JSON 字串或檔案：
- 使用 json.dump(dict_obj, file)放到檔案中 或 json.dumps(dict_obj)

📦 額外參數補充：
- indent：控制縮排層級，讓 JSON 看起來更漂亮。通常設為 2 或 4。
- sort_keys：若為 True，JSON 會依照 key 的字母排序輸出。
- ensure_ascii：預設為 True，會將非 ASCII 字元轉為 Unicode 編碼。設為 False 可保留中文等原字。

✅ 總結：
dict 是你在 Python 程式中操作的「活資料」，
JSON 是將資料寫出、儲存、或傳送給其他系統所使用的「標準格式」。
兩者可互相轉換，但使用情境不同。
"""

#輸出json格式到terminal
def print_response(response):#Notion SDK 給你的dict
    print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))
    #Indent: 每一層縮排幾個空格
    # sort_keys: 同層依照字幕排序(預設false: 依照插入順序排序)
    #ensure_ascii:非ASCII字元會被轉為Unicode轉義(預設true)

#輸出json格式到指定檔案(.jsom)
def output_response(response):
    print("目前工作目錄:", os.getcwd())# 確認目前工作目錄
    with open("result.jason", "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False, indent=4)#將dict寫入剛才開的檔案f
        # "w": 寫入模式(如果檔案不存在自動建立)
        #上下文管理器: with能自動關閉檔案，以免忘記關閉(忘記關閉會造成資源為釋放未寫入問題)

#搜id於database，回傳jason
def get_page_response(page_id):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    response = notion.pages.retrieve(page_id=page_id)# query是專門給database用來找pages(可搭配filter, sort, etc)
    return response

def get_database_response(database_id):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    response = notion.databases.retrieve(database_id=database_id)
    return response

#回傳資料庫名稱
def get_database_title(database_id):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    response = notion.databases.retrieve(database_id=database_id)

    title_list = response["title"]
    if title_list:
        title = title_list[0]["plain_text"]
        return title
    else:
        print("沒有此資料庫")
        return None

def get_page_title(page_id, title_property):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    response = notion.pages.retrieve(page_id=page_id)
    title = response["properties"][title_property]["title"][0]["plain_text"]
    if title:
        print("找到title:", title)
        return title
    else:
        print("沒有此頁面")
        return None

#property是否存在
def property_exists(database_id, property_name):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    database = notion.databases.retrieve(database_id=database_id)
    return property_name in database["properties"]

#從database得知這個database title property的名字
def get_title_property_name(database_id):
    notion = Client(auth=os.getenv("NOTION_TOKEN"))
    response = notion.databases.retrieve(database_id=database_id)
    for prop_name, prop_data in response["properties"].items():
        if prop_data["type"] == "title":
            return prop_name
    return None


#搜垃圾桶，回傳id群(無法查詢垃圾桶中的資料，只能判斷是否在垃圾桶)



