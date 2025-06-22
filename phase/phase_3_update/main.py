from dotenv import load_dotenv

from update_database import *
from update_page import *

load_dotenv()
database_id = os.getenv("PHASE_3_DATABASE_A_ID")

old_context = "大名稱"
new_context = "大名稱"
new_property = "rich_text"
#
# 1. 更改一個欄位名稱
response = update_database(database_id, old_context, new_context)
if response: print("✅ 更改資料庫的標題項成功！Database ID:", response["id"])
#
# #2.更改一個欄位狀態(在鎖定的欄位名或ID輸入)
# if response: response = update_property(database_id, new_property)
# if response: print("✅ 更改資料庫的標題項類型成功！Database ID:", response["id"])
# #3.新增一個欄位 (我改成先改成其他名字再改回來)
# response = add_new_property(database_id, "大福興", "rich_text")
# if response: print("✅ 新增資料庫的標題項成功！Database ID:", response["id"])
# 4.刪除一個欄位(無法)
# 5.更改一個page的內容
# page_id = os.getenv("PHASE_3_PAGE_ID")
# # property_name = "婚姻狀況"
# # new_value = "熱戀期"
# # property_type = "rich_text"
# # # response = update_rich_text_property(page_id, property_name, new_value)
# # response = update_page_property(page_id, property_name, new_value, property_type)
# # if response: print("✅ 更改頁面成功！page ID:", response["id"])
# #6.刪除資個page的內容
# response = delete_page(page_id)
# if response: print("✅ 刪除頁面成功！page ID:", response["id"])
