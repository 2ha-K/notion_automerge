import customtkinter as ctk

# 初始化
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Notion 合併工具")
app.geometry("600x600")

# ========== UI 元件 ==========

# 標題
title_label = ctk.CTkLabel(app, text="🔗 合併 Notion 資料庫", font=("Helvetica", 20))
title_label.pack(pady=20)

# Combination database ID
combi_id_var = ctk.StringVar()
combi_entry = ctk.CTkEntry(app, placeholder_text="輸入合併資料庫 C ID", textvariable=combi_id_var, width=400)
combi_entry.pack(pady=10)

# Target database frame
target_frame = ctk.CTkFrame(app)
target_frame.pack(pady=10)
target_entries = []


# ✅ 合併按鈕功能
def on_merge_click():
    combi_id = combi_id_var.get()
    target_ids = [v.get() for v in target_entries if v.get().strip()]
    print(f"✅ 合併：{target_ids} → {combi_id}")
    # TODO: 呼叫你的 Notion 合併邏輯


# ✅ 是否啟用按鈕的邏輯
def check_enable_merge_button(*args):
    combi_ok = combi_id_var.get().strip() != ""
    target_ok = any(v.get().strip() != "" for v in target_entries)
    if combi_ok and target_ok:
        merge_button.configure(state="normal")
    else:
        merge_button.configure(state="disabled")


# ✅ 新增 target 輸入欄位
def add_target_entry():
    target_var = ctk.StringVar()
    entry = ctk.CTkEntry(target_frame, placeholder_text="輸入來源資料庫 ID", textvariable=target_var, width=400)
    entry.pack(pady=5)
    target_entries.append(target_var)
    target_var.trace_add("write", check_enable_merge_button)
    check_enable_merge_button()


# 合併按鈕（一開始是 disabled）
merge_button = ctk.CTkButton(app, text="🚀 開始合併", command=on_merge_click, state="disabled")
merge_button.pack(pady=20)

# 新增 target ID 按鈕
add_target_button = ctk.CTkButton(app, text="➕ 新增來源資料庫", command=add_target_entry)
add_target_button.pack(pady=5)

# 初始化加一筆 target
add_target_entry()

# 監聽 combi id 的輸入
combi_id_var.trace_add("write", check_enable_merge_button)

# ========== 執行 UI ==========
app.mainloop()
