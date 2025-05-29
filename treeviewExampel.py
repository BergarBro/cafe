import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Treeview Example")
root.geometry("400x300")

style = ttk.Style(root)
style.theme_use("clam")

# Define columns (identifiers)
columns = ("Name", "Age", "Job")
lengths = (100, 50, 100)

# Create the Treeview widget
tree1 = ttk.Treeview(root, columns=columns, show='headings')

# Define the headings and column formatting
for i in range(len(columns)) :
    tree1.heading(columns[i], text=columns[i])
    tree1.column(columns[i], width=lengths[i], anchor="center")


# Add data (rows)
tree1.insert("", "end", values=("Alice", 30, "Engineer"))
tree1.insert("", "end", values=("Bob", 25, "Designer"))
tree1.insert("", "end", values=("Charlie", 28, "Doctor"))

# Place the Treeview in the window
tree1.pack(expand=True)

tree = ttk.Treeview(root)
tree.pack(expand=True)

# Parent item
parent = tree.insert("", "end", text="Parent Item")

# Child items
tree.insert(parent, "end", text="Child 1")
tree.insert(parent, "end", text="Child 2")

# Run the application
root.mainloop()
