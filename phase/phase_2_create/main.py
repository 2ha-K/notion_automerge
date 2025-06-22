from dotenv import load_dotenv

from create_database import create_new_database
from create_page import *

load_dotenv()
# 在database增加一個page
database_id = os.getenv("PHASE_2_DATABASE_A_ID")
title = "自動新增測試"
tag = "完成囉"
response = create_new_page(database_id, title, tag)
if response: print("✅ 新增一頁筆記到資料庫成功！Page ID:", response["id"])
# 在page中增加一個page
page_id = os.getenv("PHASE_2_PAGE_ID")
response = create_new_page_page(page_id, title)
if response: print("✅ 新增一頁筆記到一頁筆記成功！Page ID:", response["id"])
# 在page中增加一個database
response = create_new_database(page_id, title)
if response: print("✅ 新增資料庫到一頁筆記成功！Database ID:", response["id"])
# 在workspace增加一個page
# response = create_new_page_root(title)
# if response: print("✅ 新增一頁筆記到根目錄成功！Page ID:", response["id"])
