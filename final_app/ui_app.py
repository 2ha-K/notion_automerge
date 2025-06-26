"""
UNDO:
Notion token 的處理
"""
import re
import threading

from customtkinter import *
from dotenv import load_dotenv

from final_app.main import ensure_standard_fields, sync_relation_field_names

load_dotenv()
from notion_utils.search_database import is_valid_database

app = CTk()
app.title("Notion Auto Merge Tool")
app.resizable(False, False)
app.geometry("720x445")

main_frame = CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=20, pady=(10, 0))

form_frame = CTkFrame(master=main_frame)
form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=0)
main_frame.grid_columnconfigure(0, weight=1)

# List for collect target database ids
target_database_list_test = ["205b82c9b09480a79deaec0b8c3a6369", "206b82c9b09480fe862def4512afcb78",
                             "206b82c9b09480e9b8d5e5bdfef9b9cc"]
target_database_list = target_database_list_test


def on_click_add():
    new_target = target_ID_list_combobox.get().strip().lower()
    # First, check if already in the list and not empty
    if new_target and new_target not in target_database_list:
        # Second, use API to check is the database id valid or not (more time)
        if re.fullmatch(r'[a-z0-9]+', new_target):
            if is_valid_database(new_target):
                target_database_list.append(new_target)
                target_ID_list_combobox.configure(values=target_database_list)
                error_label.configure(text="New target database id have been added successfully.", text_color="green")
                target_ID_list_combobox.set("")
                target_ID_list_combobox.configure(text_color="white")
                flash_progressbar_color(progress, color="#00FF7F")

            else:
                error_label.configure(text="[!] Invalid ID", text_color="red")
                target_ID_list_combobox.configure(text_color="red")
                flash_progressbar_color(progress)
        else:
            print("[!] Invalid input format")
            error_label.configure(text="[!] Invalid input format (Only Accept Alphabet and Number).", text_color="red")
            target_ID_list_combobox.configure(text_color="red")
            flash_progressbar_color(progress)
    else:
        print("[!] Empty or Repeated Input")
        error_label.configure(text="[!] Empty or Repeated Input", text_color="red")
        if new_target:
            target_ID_list_combobox.configure(text_color="red")
        flash_progressbar_color(progress)


# Decide when delete function can be valid
def on_select_to_valid(event=None):
    target_ID_list_combobox.configure(text_color="white")
    selected = combo_var.get()
    if selected and selected in target_database_list:
        target_delete_button.configure(state="normal")
        return
    elif target_delete_button.cget("state") != "disabled":
        target_delete_button.configure(state="disabled")


# Delete target database id
def on_click_delete():
    select_target = target_ID_list_combobox.get().strip().lower()
    target_database_list.remove(select_target)
    target_ID_list_combobox.set("")
    target_ID_list_combobox.configure(values=target_database_list)
    flash_progressbar_color(progress, color="#00FF7F")
    error_label.configure(text="Selected target database id have been deleted successfully.", text_color="green")


def run_sync_in_thread():
    threading.Thread(target=on_click_sync).start()


def on_click_sync():
    combination_database_id = "206b82c9b094809bbec9c31069f10050"  # combination_entry.get().strip().lower()
    # First, check id not empty
    if combination_database_id:
        # Second, use API to check is the database id valid or not (more time)
        if re.fullmatch(r'[a-z0-9]+', combination_database_id):
            if is_valid_database(combination_database_id):
                if len(target_database_list) > 0:
                    combination_entry.configure(state="disabled")
                    target_ID_list_combobox.configure(state="disabled", text_color="white")
                    merge_button.configure(state="disabled")
                    target_add_button.configure(state="disabled")
                    target_delete_button.configure(state="disabled")
                    status_check_button.configure(state="disabled")
                    try:
                        progress.configure(progress_color="#1f6aa5")
                        progress.set(0.0)
                        error_label.configure(
                            text="SYNC Started... Please do not close the program, or the database may be corrupted.",
                            text_color="gray")
                        # progress.start()
                        ensure_standard_fields(combination_database_id=combination_database_id,
                                               target_database_list=target_database_list,
                                               update_callback=update_progress)
                        sync_relation_field_names(combination_database_id=combination_database_id,
                                                  target_database_list=target_database_list,
                                                  update_callback=update_progress)
                        # progress.stop()
                        progress.configure(progress_color="#00FF7F")
                        error_label.configure(text="SYNC Completed", text_color="green")
                        combination_entry.configure(state="normal")
                        target_ID_list_combobox.configure(state="normal")
                        merge_button.configure(state="normal")
                        target_add_button.configure(state="normal")
                        status_check_button.configure(state="normal")
                    except Exception as e:
                        flash_progressbar_color(progress, color="red")
                        progress.configure(progress_color="red")
                        error_label.configure(text=e, text_color="red")
                        combination_entry.configure(state="red")
                        target_ID_list_combobox.configure(state="red")
                        merge_button.configure(state="normal")
                        target_add_button.configure(state="normal")
                        status_check_button.configure(state="normal")
                else:
                    print("[!] At least one target database id is required")
                    flash_progressbar_color(progress, color="red")
                    error_label.configure(text="[!] At least one target database id is required", text_color="red")

            else:
                flash_progressbar_color(progress, color="red")
                error_label.configure(text="[!] Invalid Combination ID", text_color="red")
        else:
            print("[!] Invalid Combination Database ID Format")
            flash_progressbar_color(progress, color="red")
            error_label.configure(text="[!] Invalid Combination Database ID Format (Only Accept Alphabet and Number).",
                                  text_color="red")
    else:
        print("[!] Not Allowed Empty Combination Database ID")
        flash_progressbar_color(progress, color="red")
        error_label.configure(text="[!] Not Allowed Empty Combination Database ID", text_color="red")


def is_valid_combination_database():
    id = combination_entry.get().strip().lower()
    if id and is_valid_database(id):
        error_label.configure(text="Combination database id is exist", text_color="green")
        flash_progressbar_color(progress, color="#00FF7F")
    else:
        error_label.configure(text="[!] Invalid Combination Database ID", text_color="red")
        flash_progressbar_color(progress, color="red")


def update_progress(percent):
    progress.set(percent / 100)  # 例如 30% 就傳入 30
    app.update_idletasks()  # 確保即時更新 UI


def flash_progressbar_color(progressbar, color="red", count=3, delay=300):
    progress.set(100)
    print("變色了")

    def toggle(i=0):
        if i >= count * 2:
            progressbar.configure(progress_color="#3B8ED0")  # 恢復預設色
            return
        if i % 2 == 0:
            progressbar.configure(progress_color=color)
        else:
            progressbar.configure(progress_color="#3B8ED0")  # 原本藍色
        progressbar.after(delay, lambda: toggle(i + 1))

    toggle()


combination_label = CTkLabel(master=form_frame, text="Combination Database ID:")
combi_var = StringVar()
combination_entry = CTkEntry(master=form_frame, width=300, textvariable=combi_var)
status_check_button = CTkButton(master=form_frame, text="Check", command=is_valid_combination_database)

target_label = CTkLabel(master=form_frame, text="Target Database ID List:")

combo_var = StringVar()  # String Variable
target_ID_list_combobox = CTkComboBox(master=form_frame, values=target_database_list, width=300, variable=combo_var)
target_ID_list_combobox.set("")
target_add_button = CTkButton(master=form_frame, text="Add", width=10, command=on_click_add)
target_delete_button = CTkButton(master=form_frame, text="Delete", width=10, command=on_click_delete, state="disabled")

error_label = CTkLabel(master=form_frame, text="(・ω・)I'm just a little bot waiting for orders!(・ω・)",
                       fg_color="#4d4d4d", corner_radius=4)

merge_button = CTkButton(master=form_frame, text="Sync & Merge Databases", width=10, command=run_sync_in_thread,
                         corner_radius=6, )

combination_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
combination_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
status_check_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

target_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
target_ID_list_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
button_width = 67
# 建立按鈕群組框架
button_group_frame = CTkFrame(form_frame, fg_color="transparent")
button_group_frame.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="w")

# 將 Add / Delete 放入群組內
target_add_button = CTkButton(master=button_group_frame, text="Add", width=button_width, command=on_click_add)
target_add_button.pack(side="left", padx=(0, 5))
target_delete_button = CTkButton(master=button_group_frame, text="Delete", width=button_width, command=on_click_delete,
                                 state="disabled")
target_delete_button.pack(side="left")

error_label.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
error_label.configure(anchor="center", justify="center")

progress = CTkProgressBar(master=form_frame, width=450, height=13, progress_color="#1f6aa5")
progress.grid(row=3, column=0, columnspan=4, pady=10)
progress.set(100)

merge_button.grid(row=4, column=0, columnspan=4, pady=10)

combo_var.trace_add("write", lambda *args: on_select_to_valid())

# ============ Instruction Section ============
instruction_frame = CTkFrame(master=main_frame, fg_color="#f0f0f0", corner_radius=8)
instruction_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

instruction_text = CTkLabel(
    master=instruction_frame,
    text=(
        "Instructions:\n"
        "1. This tool comes with a built-in Notion integration token (already configured).\n"
        "2. Before starting, please ensure the integration **My Python Bot** is connected to all target and combination Notion databases.\n"
        "3. Enter a valid Combination Database ID and click 'Check' to verify it.\n"
        "4. Add at least one valid Target Database ID to the list using the 'Add' button.\n"
        "5. Click 'Sync & Merge Databases' to begin merging pages from the target databases into the combination database.\n"
        "6. ⚠️ If any target database is not properly linked, its pages will be skipped.\n"
        "7. ⚠️ Warning: Do NOT close the program while syncing, or database corruption may occur.\n"
        "8. ⚠️ Please **do not manually edit** the combination or target databases in Notion during the sync process to prevent inconsistencies or potential data loss.\n\n"
        "© 2025/6/26  |  All rights reserved by 2ha"
    ),
    justify="left",
    anchor="w",
    wraplength=680,
    font=CTkFont(size=12),
    text_color="black"
)
instruction_text.pack(padx=10, pady=6, anchor="w")

app.mainloop()
