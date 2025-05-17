# tooltip.py

import tkinter as tk

class ListboxTooltip:
    def __init__(self, listbox, get_tooltip_text):
        self.listbox = listbox
        self.get_tooltip_text = get_tooltip_text

        self.tooltip = tk.Toplevel(listbox)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        self.tooltip.attributes("-topmost", True)
        self.tooltip.attributes("-disabled", True)
        self.label = tk.Label(self.tooltip, bg="white", relief="solid", borderwidth=1, padx=4)
        self.label.pack()

        listbox.bind("<Motion>", self.on_hover)
        listbox.bind("<Leave>", lambda e: self.tooltip.withdraw())

    def on_hover(self, event):
        index = self.listbox.nearest(event.y)
        if index < 0:
            self.tooltip.withdraw()
            return

        text = self.get_tooltip_text(index)
        self.label.config(text=text)

        x = self.listbox.winfo_pointerx() + 10
        y = self.listbox.winfo_pointery() + 10
        self.tooltip.geometry(f"+{x}+{y}")
        self.tooltip.wm_attributes("-topmost", True)
        self.tooltip.deiconify()
