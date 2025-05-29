import tkinter as tk

class AutocompleteEntry(tk.Entry):
    def __init__(self, master, valid_values, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.valid_values = valid_values
        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace_add("write", self.on_change)

        self.listbox = None

    def on_change(self, *args):
        typed = self.var.get()
        if typed == "":
            self.hide_suggestions()
            return

        matches = [v for v in self.valid_values if typed.lower() in v.lower()]

        if matches:
            self.show_suggestions(matches)
        else:
            self.hide_suggestions()

    def show_suggestions(self, suggestions):
        if self.listbox:
            self.listbox.destroy()

        self.listbox = tk.Listbox()
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        for item in suggestions:
            self.listbox.insert(tk.END, item)

        # Position just below the entry
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.listbox.place(x=x, y=y, width=self.winfo_width())

    def hide_suggestions(self):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None

    def on_select(self, event):
        if not self.listbox:
            return
        selected = self.listbox.get(tk.ACTIVE)
        self.var.set(selected)
        self.hide_suggestions()

# Example use
root = tk.Tk()
root.geometry("300x150")

valid_items = ["Apple", "Apricot", "Banana", "Blackberry", "Blueberry", "Cherry", "Date", "Grape", "Honeydew"]
entry = AutocompleteEntry(root, valid_items)
entry.pack(padx=10, pady=10)

root.mainloop()
