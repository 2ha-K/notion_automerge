"""
UNDO:
Notion token 的處理
"""
import re

from customtkinter import *
from dotenv import load_dotenv

load_dotenv()
from notion_utils.search_database import is_valid_database

app = CTk()
app.geometry("720x480")

form_frame = CTkFrame(app)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# List for collect target database ids
target_database_list = []


def on_click_add():
    def is_valid_lowercase_alnum(s):
        return re.fullmatch(r'[a-z0-9]+', s) is not None

    new_target = target_ID_list_combobox.get().strip().lower()
    # First, check if already in the list and not empty
    if new_target and new_target not in target_database_list:
        # Second, use API to check is the database id valid or not (more time)
        if re.fullmatch(r'[a-z0-9]+', new_target):
            if is_valid_database(new_target):
                target_database_list.append(new_target)
                target_ID_list_combobox.configure(values=target_database_list)
                error_label.configure(text="New target database id added successfully.", text_color="green")
            else:
                error_label.configure(text="[!] Invalid ID", text_color="red")
        else:
            print("[!] Invalid input format")
            error_label.configure(text="[!] Invalid input format (Only Accept Alphabet and Number).", text_color="red")
    else:
        print("[!] Empty or Repeated Input")
        error_label.configure(text="[!] Invalid Format or Repeated Input", text_color="red")


def on_click_delete():
    pass


def on_click_ensure():
    pass


def on_click_sync():
    pass


combination_label = CTkLabel(master=form_frame, text="Combination Database ID:")
combination_entry = CTkEntry(master=form_frame, width=300)

target_label = CTkLabel(master=form_frame, text="Target Database ID List:")

target_ID_list_combobox = CTkComboBox(master=form_frame, values=target_database_list, width=300)
target_ID_list_combobox.set("")
target_add_button = CTkButton(master=form_frame, text="Add", width=10, command=on_click_add)
target_delete_button = CTkButton(master=form_frame, text="Delete", width=10, command=on_click_delete)

error_label = CTkLabel(master=form_frame, text="", text_color="red")

validation_button = CTkButton(master=form_frame, text="Ensure Standard Fields", width=10, command=on_click_ensure)
merge_button = CTkButton(master=form_frame, text="Sync & Merge Databases", width=10, command=on_click_sync)

combination_label.grid(row=0, column=0, padx=10, pady=10)
combination_entry.grid(row=0, column=1, padx=10, pady=10)

target_label.grid(row=1, column=0, padx=10, pady=10)
target_ID_list_combobox.grid(row=1, column=1, padx=10, pady=10)
target_add_button.grid(row=1, column=2, padx=10, pady=10)
target_delete_button.grid(row=1, column=3, padx=10, pady=10)

error_label.grid(row=2, column=1, padx=10, pady=10)

validation_button.grid(row=3, column=0, padx=10, pady=10)
merge_button.grid(row=3, column=1, padx=10, pady=10)

app.mainloop()
