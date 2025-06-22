"""
__init__.py 是 Python 中用來標示一個資料夾是「套件（package）」的特殊檔案。
當 Python 匯入這個資料夾時，會自動執行 __init__.py 裡的內容。
可以在裡面寫 from .xxx import yyy 來把深層的模組或類別轉出（re-export），
讓使用者可以用更簡潔的方式 import。

例如：
如果某個類別 Client 定義在 notion_client/client.py 中，
可以在 notion_client/__init__.py 中寫：
    from .client import Client
這樣外部就能直接使用：
    from notion_client import Client
而不用寫 from notion_client.client import Client
"""
from notion_client import Client
import os # os 模組提供與作業系統互動的功能，這裡用來讀取 .env 中的環境變數（如 API 金鑰）

def get_database_pages(): # 2 usages 表示這個名稱在你整個專案中被用到兩次，方便你追蹤誰用它
    #程式碼中有任何地方參考到這個符號（symbol）的位置，不管是 import、呼叫、傳入參數、甚至被註解提到，都算 usage
    # 從os中讀取 .env 由 load_dotenv() 存入的特定Token和Database ID 環境變數
    notion = Client(auth=os.getenv("NOTION_TOKEN")) #建立物件等於java的 Client notion = new Clinent(...)
    database_id = os.getenv("PHASE_1_DATABASE_A_ID")

    # API 回傳的是 JSON 格式（字串），但 Python SDK 會自動幫你轉成 dict（字典）
    # 如果用 requests 自己打 API，則會先得到 .text（字串），再用 .json() 或 json.loads() 轉換
    response = notion.databases.query(database_id=database_id) # Python 的 dict 就像 Java 裡的 Map（尤其像 HashMap), 都是 key → value 的對應結構，key 唯一、value 任意

    pages = response["results"]
    print("response type: ", type(response))
    print("response: ", response)
    print("pages type: ", type(pages))
    print("pages: ", pages)

    titles = []
    for page in pages:
        properties = page["properties"]
        print("page type: ", type(page))
        print("page: ", page)
        print("properties type: ", type(properties))
        print("properties: ", properties)
        # 根據 Notion 資料庫欄位名稱調整這行
        # .get("key") 是安全取值，不會報錯，可用於不確定欄位是否存在的情況
        # ["key"] 是直接取值，適合在確認欄位已存在時使用
        title_prop = properties.get("Name") or properties.get("標題") #靠or左的為優先選擇

        # 在 Python 中 if x: 會自動判斷 x 是否為「真值」
        # None、空容器、空字串、0、False 都會被當作 False
        # 所以 if title_prop: 可以檢查它是否有資料，不需要寫 if title_prop != None
        if title_prop and title_prop["type"] == "title": #先檢查是否none的簡化版
            # Notion 的 title 是 list of text objects（每段可能有不同樣式）
            # 常見只會有一段，但保險做法應該是把所有 plain_text 合併
            # ex: title = "".join(t["plain_text"] for t in title_prop["title"]), "分隔符".join(清單) 中的分隔符，會根據「項目數量 - 1」次自動插入。
            # 把所有段落的 plain_text 合併成一整串字串
            # 用的是 Python 的生成器表達式，比 for-loop 更簡潔
            text = title_prop["title"] # 取出title這一欄的檔案
            # Notion 的 title 是 list，內含多個 text object
            # 每段的產生依據是樣式是否不同（如加粗、變色）
            # 所以 text[0], text[1]... 是樣式切段，不是空格或換行
            title = text[0]["plain_text"] if text else "(空白)" #如果text是"title": []"進ELSE
            #1.title = 標題名稱, 有填寫回傳第一部分結構
            #2.title = 空白, 標題為填寫
        else:
            #3.title = 無標題, 沒有title叫做"Name"或者"名稱"或者叫做其二但是不是title項目
            title = "(無標題)"
        titles.append((page["id"], title)) # 一次append一個二元組 => 二元陣列

    return titles
"""
📘 Python 常見內建資料格式（Data Types）完整整理：

1. dict（字典）
   - 格式：{"key": value, "name": "Alice", "age": 25}
   - 說明：以 key-value 儲存資料，key 唯一，value 可為任意型別
   - 用途：儲存 JSON 資料、查找映射關係

2. list（串列）
   - 格式：[1, 2, 3, 4]
   - 說明：有順序、可重複、可變動的元素集合
   - 用途：排序、索引、儲存一組資料

3. set（集合）
   - 格式：{1, 2, 3}
   - 說明：無順序、不可重複元素，不支援索引
   - 用途：去除重複、集合運算（交集、差集）

4. tuple（元組）
   - 格式：(1, 2, 3)
   - 說明：有順序、可重複，但**不可變動**（immutable）
   - 用途：作為鍵、不可修改的資料組

5. str（字串）
   - 格式："hello" 或 'world'
   - 說明：文字型別，支援索引與切片
   - 用途：處理文字、輸出訊息、API 傳輸

6. int（整數）
   - 格式：42, -10
   - 說明：整數數值，可做數學運算
   - 用途：數量、索引、計算

7. float（浮點數）
   - 格式：3.14, -0.5
   - 說明：帶小數點的數值
   - 用途：計算比例、統計數值等

8. bool（布林值）
   - 格式：True, False
   - 說明：表示邏輯值，通常用於條件判斷
   - 用途：if 判斷、布林邏輯

9. NoneType（空值型）
   - 格式：None
   - 說明：代表「無值」，不是 0、不是空字串，而是什麼都沒有
   - 用途：初始化變數、表示缺值或未設定狀態

🎯 小整理表格：

| 類型     | 是否可變 | 是否有順序 | 可重複 | 典型用途           |
|----------|----------|------------|--------|--------------------|
| dict     | ✅        | ✅ (3.7+)   | ❌ key | 儲存映射資料       |
| list     | ✅        | ✅          | ✅     | 一般資料列表       |
| set      | ✅        | ❌          | ❌     | 去重、集合運算     |
| tuple    | ❌        | ✅          | ✅     | 不可變的資料組合   |
| str      | ❌        | ✅          | ✅     | 處理文字           |
| int      | ❌        | -           | -      | 計算、索引         |
| float    | ❌        | -           | -      | 比例、計算         |
| bool     | ❌        | -           | -      | 邏輯條件           |
| NoneType | ❌        | -           | -      | 缺值、初始化       |
"""
