import tkinter as tk
from tkinter import *
from tkinter import ttk

### Global Helper Functions ###
def make_treeview_with_search(current_frame, heading_names, heading_width = [], tree_names = ["0"]) :
    if heading_width == [] :
        heading_width = [-1] * len(heading_names)

    frame_search = tk.Frame(current_frame)
    frame_search.pack(pady=5)
    
    label_search = tk.Label(frame_search, text="Search:")
    label_search.pack(side="left")

    search_var = tk.StringVar()
    entry_search = ttk.Entry(frame_search, textvariable=search_var)
    entry_search.pack(side="left")

    frame_tree = tk.Frame(current_frame)
    frame_tree.pack(pady=5)

    tree_frames = {}
    trees = {}
    for j in range(len(tree_names)) :
        temp_frame = tk.Frame(frame_tree)
        temp_tree = ttk.Treeview(temp_frame, columns=heading_names, show="headings", selectmode="browse")

        for i in range(len(heading_names)) :
            temp_tree.heading(heading_names[i], text=heading_names[i])
            if heading_width[i] > 0 :
                temp_tree.column(heading_names[i], width=heading_width[i])

        scrollbar = ttk.Scrollbar(temp_frame) 
        scrollbar.pack(side = "right", fill = "both")

        temp_tree.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = temp_tree.yview)

        temp_tree.pack(expand=True)

        tree_frames[tree_names[j]] = temp_frame
        trees[tree_names[j]] = temp_tree

    tree_frames[tree_names[0]].pack()

    return (frame_search, label_search, search_var, trees, tree_frames)

def update_search_in_tree(tree, search_var, list_of_items, index_of_items = []) :
    search_term = search_var.get().lower()
    # print(search_term)
    for i in tree.get_children() :
        tree.delete(i)

    if index_of_items == [] :
        index_of_items = range(len(list_of_items[0]))

    for item in list_of_items :
        if search_term in item[0].lower() :
            tree.insert("", tk.END, values=tuple(item[i] for i in index_of_items))

def make_entry_with_label(current_frame, label_text) :
    frame = ttk.Frame(current_frame)

    label = tk.Label(frame, text=label_text)
    label.pack(side="left")
    
    str_var = tk.StringVar()
    entry = ttk.Entry(frame, textvariable=str_var)
    entry.pack(side="left")

    return (frame, str_var)

def make_popup_window(current_fame, title_text, info_text) :
    def on_ok() :
        window.destroy()

    window = tk.Toplevel(current_fame)
    window.title(title_text)
    window.geometry("300x100")

    label_info = tk.Label(window, text=info_text)
    label_info.pack(pady=5)

    ok_button = ttk.Button(window, text="OK", command=on_ok)
    ok_button.pack(pady=5)


