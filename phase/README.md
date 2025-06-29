# Notion Database Auto-Merge Project

This project is a **progressive learning journey using the Notion API**, starting from basic read/write operations to
full database merging and synchronization.

The final goal is to build a **Notion tool that automatically merges multiple databases (A, B...) into a central one (C)
**, with proper field normalization, relation handling, and conditional sync logic.

> Built with Python · Notion SDK · Modular Design · Ready for Extension

---

## Learning Phases

Each phase of development was designed to deliberately practice a key skill. Here’s a summary of what I tackled in each
phase:

| Phase | Topic               | Goal Description                                     |
|-------|---------------------|------------------------------------------------------|
| ✅ 1   | Reading data        | Fetch database content using Notion SDK              |
| ✅ 2   | Creating pages      | Understand Notion page format & field types          |
| ✅ 3   | Updating / Deleting | Modify page title and fields programmatically        |
| ✅ 4   | Unconditional Merge | Copy all pages from A/B into C, no filtering         |
| ✅ 5   | Conditional Merge   | Avoid duplicates, set source relations, unify schema |

---

---

## Why This Project Matters

I built this tool not just to automate Notion workflows, but to deeply understand how to:

- Structure and read complex JSON from APIs
- Write clean, maintainable Python code
- Handle real-world issues like schema mismatch, race conditions, data duplication
- Gradually evolve a project from script → tool → product

---

## Useful Snippets

```python
# Creating a new Notion page
notion.pages.create(
    parent={"database_id": DATABASE_ID},
    properties={
        "Name": {
            "title": [{"text": {"content": "My New Page"}}]
        }
    }
)

# Updating a page property
notion.pages.update(
    page_id=page_id,
    properties={
        "Status": {
            "select": {"name": "Completed"}
        }
    }
)


