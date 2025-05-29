import tkinter as tk
from tkinter import ttk

# Sample options to choose from
OPTIONS = ["Apples", "Bananas", "Cherries", "Dates", "Elderberries"]

def add_combobox(parent_frame, previous_var=None):
    """Create a new combobox inside the parent_frame."""
    var = tk.StringVar()
    combobox = ttk.Combobox(parent_frame, textvariable=var, values=OPTIONS, state="readonly")
    combobox.pack(pady=5, anchor="w")

    def on_select(event):
        # Only add another combobox if this is the last one (avoid duplicates)
        if var.get() and combobox == combobox_list[-1]:
            add_combobox(parent_frame)

    combobox.bind("<<ComboboxSelected>>", on_select)
    combobox_list.append(combobox)

# --- Main UI ---
root = tk.Tk()
root.title("Dynamic Option Selector")

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack()

combobox_list = []  # Keep track of comboboxes
add_combobox(main_frame)  # Add the first one

root.mainloop()