import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Multi-column List Example")

test_frame = tk.Frame(root)
test_frame.pack(pady=5)

tree = ttk.Treeview(root, columns=("Name", "Price", "Stock"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Price", text="Price")
tree.heading("Stock", text="Stock")

# Optional: Set column widths
tree.column("Name", width=150)
tree.column("Price", width=100)
tree.column("Stock", width=80)

# Example data
data = [
    ("Milk", "$1.50", "In Stock"),
    ("Bread", "$2.00", "Out of Stock"),
    ("Butter", "$3.25", "In Stock"),
]

for item in data:
    tree.insert("", tk.END, values=item)

tree.pack(expand=True, fill="both")

root.mainloop()
