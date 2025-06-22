import tkinter as tk

import customtkinter as ctk

# 建立主視窗
app = ctk.CTk()
app.geometry("720x480")
app.title("Notion 自動合併工具")

# 儲存組合 ID 與來源 ID 的變數
combination_id_var = ctk.StringVar()  # 儲存 combination database ID

# 儲存 target ID 變數的列表（新增時擴充）
target_vars = []

# ====== Combination ID 輸入欄位（單獨一行） ======
ctk.CTkLabel(app, text="Combination Database ID:").pack(pady=(20, 5))
combination_entry = ctk.CTkEntry(app, textvariable=combination_id_var, width=400, placeholder_text="請輸入 Target ID")
combination_entry.pack(pady=(0, 10))

# ====== Target ID 輸入欄位區域（固定高度，只顯示一個，有滾動條） ======
target_frame_container = ctk.CTkFrame(app, height=60)
target_frame_container.pack(pady=(0, 5), padx=20, fill="x")

canvas = tk.Canvas(target_frame_container, borderwidth=0, background="#2b2b2b", height=50)
scrollbar = ctk.CTkScrollbar(target_frame_container, orientation="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

inner_frame = ctk.CTkFrame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")
inner_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))


# ====== Target ID 清單展開與新增 ======
def add_target_entry():
    var = ctk.StringVar()
    entry = ctk.CTkEntry(inner_frame, textvariable=var, width=400)
    entry.pack(pady=2)
    target_vars.append(var)
    check_enable_merge_button()


# 啟用/停用合併按鈕的檢查
def check_enable_merge_button():
    if combination_id_var.get().strip() and any(v.get().strip() for v in target_vars):
        merge_button.configure(state="normal")
    else:
        merge_button.configure(state="disabled")


# 合併按鈕事件
def on_merge_click():
    combination_id = combination_id_var.get().strip()
    target_ids = [v.get().strip() for v in target_vars if v.get().strip()]
    print("Combination ID:", combination_id)
    print("Target IDs:", target_ids)


# ====== 控制按鈕（新增 target 與合併） ======
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=(10, 5))

add_button = ctk.CTkButton(button_frame, text="➕ 新增 Target ID", command=add_target_entry)
add_button.pack(side="left", padx=10)

merge_button = ctk.CTkButton(app, text="🚀 開始合併", state="disabled", command=on_merge_click)
merge_button.pack(pady=(10, 10))

# 每次輸入 Combination ID 時檢查按鈕啟用狀態
combination_id_var.trace_add("write", lambda *args: check_enable_merge_button())

# 主事件迴圈啟動
app.mainloop()
