from PIL import Image
from customtkinter import *

app = CTk()
app.geometry("720x480")

form_frame = CTkFrame(app)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)


def click_handler():
    print(target_ID_list_combobox.get())


combination_label = CTkLabel(master=form_frame, text="Combination Database ID:")
combination_entry = CTkEntry(master=form_frame, placeholder_text="Type combination database ID...", width=300)
image = CTkImage(Image.open("your_image.png"), size=(200, 150))

target_label = CTkLabel(master=form_frame, text="Target Database ID List:")
target_database_list = ["Type type database ID..."]  # 獲得
target_ID_list_combobox = CTkComboBox(master=form_frame, values=target_database_list, width=300)
target_add_button = CTkButton(master=form_frame, text="Add", width=10, command=click_handler)
target_delete_button = CTkButton(master=form_frame, text="Delete", width=10)

validation_button = CTkButton(master=form_frame, text="Validation", width=10, command=click_handler)
merge_button = CTkButton(master=form_frame, text="Auto Merge!", width=10, command=click_handler)

combination_label.grid(row=0, column=0, padx=10, pady=10)
combination_entry.grid(row=0, column=1, padx=10, pady=10)

target_label.grid(row=1, column=0, padx=10, pady=10)
target_ID_list_combobox.grid(row=1, column=1, padx=10, pady=10)
target_add_button.grid(row=1, column=2, padx=10, pady=10)
target_delete_button.grid(row=1, column=3, padx=10, pady=10)

validation_button.grid(row=2, column=0, padx=10, pady=10)
merge_button.grid(row=2, column=1, padx=10, pady=10)

app.mainloop()
