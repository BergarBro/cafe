import tkinter as tk

OPTIONS = ["Apples", "Bananas", "Cherries", "Dates", "Elderberries"]

class DynamicSelector(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.option_vars = []
        self.option_menus = []
        self.used_options = set()
        self.add_selector()

    def add_selector(self):
        var = tk.StringVar()
        var.set("Select...")

        menu = tk.OptionMenu(self, var, *OPTIONS, command=lambda value, v=var: self.on_select(v, value))
        menu.pack(anchor="w", pady=2)

        self.option_vars.append(var)
        self.option_menus.append(menu)

    def on_select(self, var, value):
        if value != "Select..." and var == self.option_vars[-1]:
            self.add_selector()

    def get_selections(self):
        return [v.get() for v in self.option_vars if v.get() != "Select..."]

# ---- Main App ----
root = tk.Tk()
root.title("Dynamic Dropdowns")

selector_frame = DynamicSelector(root)
selector_frame.pack(padx=20, pady=20)

def print_selections():
    print("Selected items:", selector_frame.get_selections())

submit_btn = tk.Button(root, text="Print Selections", command=print_selections)
submit_btn.pack(pady=10)

root.mainloop()
