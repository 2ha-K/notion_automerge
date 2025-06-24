"""
UNDO:
Notion token 的處理
"""
import re

from customtkinter import *
from dotenv import load_dotenv

from final_app.main import ensure_standard_fields, sync_relation_field_names

load_dotenv()
from notion_utils.search_database import is_valid_database

app = CTk()
app.geometry("720x480")

form_frame = CTkFrame(app, width=720, height=480)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
form_frame.grid_propagate(False)

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
            else:
                error_label.configure(text="[!] Invalid ID", text_color="red")
        else:
            print("[!] Invalid input format")
            error_label.configure(text="[!] Invalid input format (Only Accept Alphabet and Number).", text_color="red")
    else:
        print("[!] Empty or Repeated Input")
        error_label.configure(text="[!] Invalid Format or Repeated Input", text_color="red")


# Decide when delete function can be valid
def on_select_to_valid(event=None):
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
    error_label.configure(text="Selected target database id have been deleted successfully.", text_color="green")


def on_click_sync():
    combination_database_id = combination_entry.get().strip().lower()
    # First, check id not empty
    if combination_database_id:
        # Second, use API to check is the database id valid or not (more time)
        if re.fullmatch(r'[a-z0-9]+', combination_database_id):
            if is_valid_database(combination_database_id):
                if len(target_database_list) > 0:
                    combination_entry.configure(state="disabled")
                    target_ID_list_combobox.configure(state="disabled")
                    try:
                        ensure_standard_fields(combination_database_id=combination_database_id,
                                               target_database_list=target_database_list)
                        sync_relation_field_names(combination_database_id=combination_database_id,
                                                  target_database_list=target_database_list)
                        error_label.configure(text="SYNC Completed", text_color="green")
                        combination_entry.configure(state="normal")
                        target_ID_list_combobox.configure(state="normal")
                    except:
                        error_label.configure(text="SYNC Fail", text_color="red")
                        combination_entry.configure(state="red")
                        target_ID_list_combobox.configure(state="red")
                else:
                    print("[!] At least one target database id is required")
                    error_label.configure(text="[!] At least one target database id is required", text_color="red")

            else:
                error_label.configure(text="[!] Invalid Combination ID", text_color="red")
        else:
            print("[!] Invalid Combination Database ID Format")
            error_label.configure(text="[!] Invalid Combination Database ID Format (Only Accept Alphabet and Number).",
                                  text_color="red")
    else:
        print("[!] Not Allowed Empty Combination Database ID")
        error_label.configure(text="[!] Not Allowed Empty Combination Database ID", text_color="red")


combination_label = CTkLabel(master=form_frame, text="Combination Database ID:")
combination_entry = CTkEntry(master=form_frame, width=300)

target_label = CTkLabel(master=form_frame, text="Target Database ID List:")

combo_var = StringVar()  # String Variable
target_ID_list_combobox = CTkComboBox(master=form_frame, values=target_database_list, width=300, variable=combo_var)
target_ID_list_combobox.set("")
target_add_button = CTkButton(master=form_frame, text="Add", width=10, command=on_click_add)
target_delete_button = CTkButton(master=form_frame, text="Delete", width=10, command=on_click_delete, state="disabled")

error_label = CTkLabel(master=form_frame, text="", text_color="red")

merge_button = CTkButton(master=form_frame, text="Sync & Merge Databases", width=10, command=on_click_sync)

combination_label.grid(row=0, column=0, padx=10, pady=10)
combination_entry.grid(row=0, column=1, padx=10, pady=10)

target_label.grid(row=1, column=0, padx=10, pady=10)
target_ID_list_combobox.grid(row=1, column=1, padx=10, pady=10)
target_add_button.grid(row=1, column=2, padx=10, pady=10)
target_delete_button.grid(row=1, column=3, padx=10, pady=10)

error_label.grid(row=2, column=1, padx=10, pady=10)

merge_button.grid(row=3, column=1, padx=10, pady=10)

combo_var.trace_add("write", lambda *args: on_select_to_valid())
app.mainloop()
