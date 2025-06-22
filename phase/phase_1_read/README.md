# Phase 1: 讀取 Notion 資料庫

這個模組示範如何使用 Notion API 從資料庫中讀取 pages 資料。

## 功能說明

- 使用 `.env` 儲存 API Token 和 Database ID
- 使用 `notion-client` SDK 查詢資料庫
- 抓取每個 page 的標題與 ID

## 執行方式

```bash
pip install -r requirements.txt
python main.py

"""
📦 Phase 1：讀取 Notion 資料庫

這個階段的目標是練習使用 Notion 的 Python SDK（notion-client），成功讀取資料庫中的 page 資料，並了解回傳資料的結構與解析方式。

我完成的項目包括：
- 建立專案結構與 phase_1_read 資料夾
- 設定 .env 檔案與 token/database_id
- 使用 `get_database_pages()` 函式正確取得資料庫內容
- 熟悉 Notion 回傳的巢狀 dict + list 結構
- 正確解析 page 的 title、rich_text 等欄位
- 使用 `"".join(...)` 合併段落文字，安全處理空值與欄位不存在狀況
- 學會用 tuple list 儲存每一筆資料的 (page_id, title)

這個階段我完全理解了 SDK 的讀取邏輯與 JSON 資料的實際結構，接下來可以開始進入資料寫入與更新。
"""
