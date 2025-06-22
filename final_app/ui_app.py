import customtkinter as ctk

# 初始化樣式
ctk.set_appearance_mode("System")  # 或 "Dark", "Light"
ctk.set_default_color_theme("blue")

# 建立主視窗
app = ctk.CTk()
app.title("Notion 資料庫合併工具")
app.geometry("600x400")

# === 元件區塊 ===

# 標題
title_label = ctk.CTkLabel(app, text="🔗 合併 Notion 資料庫", font=("Helvetica", 20))
title_label.pack(pady=20)

# 輸入：來源資料庫 A
source_a_entry = ctk.CTkEntry(app, placeholder_text="輸入資料庫 A ID")
source_a_entry.pack(pady=10)

# 輸入：來源資料庫 B
source_b_entry = ctk.CTkEntry(app, placeholder_text="輸入資料庫 B ID")
source_b_entry.pack(pady=10)

# 輸入：合併資料庫 C
combi_entry = ctk.CTkEntry(app, placeholder_text="輸入合併資料庫 C ID")
combi_entry.pack(pady=10)


# 按鈕：開始合併
def on_merge_click():
    db_a = source_a_entry.get()
    db_b = source_b_entry.get()
    db_c = combi_entry.get()
    print(f"合併 A: {db_a} + B: {db_b} → C: {db_c}")
    # 這裡之後會呼叫你原本的合併邏輯


merge_button = ctk.CTkButton(app, text="🚀 開始合併", command=on_merge_click)
merge_button.pack(pady=20)

# === 執行 UI ===
app.mainloop()
