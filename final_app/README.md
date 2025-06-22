# 🧠 Notion Database Merger Tool

A Python tool to **automatically merge multiple Notion databases** into one combination database.

---

## ✅ Features

- 🔄 One-click sync of multiple target databases into a central one
- 🔗 Automatically adds relation fields if missing (avoids duplicates)
- 📝 Synchronizes relation field names with target database titles
- 🧾 Adds metadata fields:
    - `Name`
    - `Database Source`
    - `Created Time`
    - `Last Edited Time`
- 🧪 Validates format:
    - No duplicate relation field names
    - No page with multiple active relations
- 🖨 Clean, color-coded logs using `[green]success[/green]`, `[yellow]warning[/yellow]`, and `[red]error[/red]`

---

## 🗂 Project Structure

```
notion_utils/
├── client.py                            # Load Notion client
├── log.py                               # Colored logging utils
├── search_database.py                   # Get database name, properties, title
├── search_page.py                       # Get page info and content
├── update_database.py                   # Update schema/structure
├── relate_databases_to_one/
│   ├── relate_databases_add_new_target_database.py
│   ├── relate_databases_format.py
│   ├── relate_databases_to_one_update.py
│   └── relate_databases_search.py
main.py                                  # Entry point
```

---

## ⚙️ Setup Instructions

### 1. Install dependencies

```bash
pip install notion-client python-dotenv rich
```

### 2. Create a `.env` file

Place this in the same directory as `main.py`:

```env
NOTION_TOKEN=your_secret_token
PHASE_5_COMBINATION_DATABASE_C_ID=your_combination_database_id
PHASE_4_TARGET_DATABASE_A_ID=your_first_target_id
PHASE_4_TARGET_DATABASE_B_ID=your_second_target_id
```

---

## 🚀 How to Run

```bash
python main.py
```

---

## 🧠 How It Works

1. Load environment variables and initialize Notion client
2. Rename title field to `"Name"` if needed
3. Ensure metadata fields exist:
    - `資料庫地址`
    - `建立時間`
    - `最後編輯時間`
4. Add missing relation fields for each target database
5. Validate format rules:
    - No duplicate relation names
    - Each page has at most one active relation
6. Sync all page content from targets to the combination database
7. Update metadata properties

---

## 🖨 Sample Log Output

```bash
[yellow]Checking relation field: 目標資料庫A[/yellow]
[green]Relation to target database '目標資料庫A' already exists.[/green]
[green]New relation field created: 目標資料庫B[/green]
✅ Format check passed.
✅ All fields created.
✅ Merge complete.
```

---

## 👤 Author

**PO-YI LIN**  
Part of _暑假無實習 軟體工程前進_ project  
ASU Computer Science | 2025 Summer Portfolio Project

---

## 🪪 License

MIT
