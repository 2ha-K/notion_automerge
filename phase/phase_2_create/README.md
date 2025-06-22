# 📘 Phase 2: Create Notion Page via API

本階段目標為透過 Notion API 新增一筆資料到指定的資料庫，並學習：

- 如何使用 SDK 建立 page
- 如何新增欄位資料（如 title、tag）
- 如何加上 children 區塊（段落、粗體）
- SDK 如何簡化 JSON 結構
- annotations 格式的控制方式

---

## ✅ 實作概念與架構

### 🔧 使用方法（簡化版）
```python
notion.pages.create(
    parent={"database_id": database_id},
    properties={
        "Title": {
            "title": [
                {"text": {"content": "頁面標題"}}
            ]
        },
        "Tags": {
            "rich_text": [
                {"text": {"content": "分類標籤"}}
            ]
        }
    }
)
