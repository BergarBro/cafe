import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random as rd
import multiprocessing

import plotPrices, scraperScript, getFunctions, makeBackupDB
from tooltip import ListboxTooltip

def open_popup_scraper():
    popup_scraper = tk.Toplevel(root)
    popup_scraper.title("Scraping Prices")
    popup_scraper.geometry("300x300")
    
    label_scraper_info = tk.Label(popup_scraper, text="Options for Scraping Prices on SvenskCater:")
    label_scraper_info.pack(pady=10)
    
    # Radio buttons for mutually exclusive choices
    option_vars = {}
    options = ["Fetch Products", "Fetch Prices", "Fetch Bread and Breadprices"]
    for opt in options:
        var = tk.BooleanVar(value=True)
        tk.Checkbutton(popup_scraper, text=opt, variable=var).pack(pady=5)
        option_vars[opt] = var

    def on_ok():
        selected = [var.get() for opt, var in option_vars.items()]

        multiproc_scraper = multiprocessing.Process(
            target=scraperScript.run_scraper_script,
            args=(selected, active_database)
            )
        multiproc_scraper.start()
        popup_scraper.destroy()

    def on_cancel():
        print("You canceled the Scraper")
        popup_scraper.destroy()

    frame_select = tk.Frame(popup_scraper)
    frame_select.pack(pady=5)

    button_scraper_ok = tk.Button(frame_select, text="SCRAPE!", command=on_ok)
    button_scraper_ok.pack(side=tk.LEFT, padx=10)

    button_scraper_cancel = tk.Button(frame_select, text="CANCEL", command=on_cancel)
    button_scraper_cancel.pack(side=tk.LEFT, padx=10)

def open_popup_plotter() :
    global categorys, products, listOfListBoxes, scrollbar
    global activeCategory, activeProducts, search_var, search_entry

    def plot_prices() :
        global categorys, activeCategory, activeProducts
        selectedProductsIndex = listOfListBoxes[activeCategory].curselection()
        selectedProducts = []
        for index in selectedProductsIndex :
            selectedProducts.append(activeProducts[index])

        plotPrices.makePricePlot(selectedProducts, active_database)

    def change_category(newCategory) :
        global activeCategory, listOfListBoxes, categorys, activeProducts, scrollbar
        listOfListBoxes[activeCategory].pack_forget()
        listOfListBoxes[newCategory].pack(pady=5)
        activeCategory = newCategory
        activeProducts = products[activeCategory]
        # search_entry.delete(0, tk.END)
        # print(listOfListBoxes[activeCategory].size())
        listOfListBoxes[activeCategory].config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listOfListBoxes[activeCategory].yview)

    def select_all() :
        global activeCategory, listOfListBoxes
        listOfListBoxes[activeCategory].selection_set(0,listOfListBoxes[activeCategory].size())

    def deselect_all() :
        global activeCategory, listOfListBoxes
        listOfListBoxes[activeCategory].selection_clear(0,listOfListBoxes[activeCategory].size())

    def update_search_category_list() :
        global activeProducts, listOfListBoxes, activeProducts, activeCategory
        search_term = search_entry.get().lower()
        # print(search_term)
        listOfListBoxes[activeCategory].delete(0,tk.END)
        activeProducts = []
        for prod in products[activeCategory] :
            if search_term in prod.lower() :
                listOfListBoxes[activeCategory].insert(tk.END, prod)
                activeProducts.append(prod)

    def on_close():
        print("You canceled the Plotter.")
        popup_plotter.destroy()

    popup_plotter = tk.Toplevel(root)
    popup_plotter.title("Plotting Prices")
    popup_plotter.geometry("500x500")

    label_plotter_info = tk.Label(popup_plotter, text="Choose products to plot the price over time.")
    label_plotter_info.pack(pady=5)

    # button3 = tk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)

    frame_search = tk.Frame(popup_plotter)
    frame_search.pack(pady=5)  # You can also use padx here

    # Dropdown options  
    products, categorys = getFunctions.getProductsAndCategorys(active_database)

    # Selected option variable  
    opt = StringVar(value=categorys[0])  

    # Dropdown menu  
    dropdown_categorys = tk.OptionMenu(frame_search, opt, *categorys, command=change_category)
    dropdown_categorys.pack(side=tk.LEFT, padx=5)

    search_var = tk.StringVar()
    search_entry = tk.Entry(frame_search, textvariable=search_var)
    # search_entry.insert(0, "Search...")
    search_entry.pack(side=tk.LEFT, padx=5)

    # Buttons packed inside the frame side-by-side
    button_select_all = tk.Button(frame_search, text="Select All", command=select_all)
    button_select_all.pack(side=tk.LEFT, padx=5)

    button_deselect_all = tk.Button(frame_search, text="Deselect All", command=deselect_all)
    button_deselect_all.pack(side=tk.LEFT, padx=5)

    listBox_frame = tk.Frame(popup_plotter)
    listBox_frame.pack(pady=5)

    style = ttk.Style(popup_plotter)
    style.theme_use("clam")

    scrollbar = ttk.Scrollbar(listBox_frame) 
    scrollbar.pack(side = RIGHT, fill = BOTH) 

    listOfListBoxes = {}
    for cat in categorys :
        tempListBox = tk.Listbox(listBox_frame, selectmode='multiple', height=14, width=50)
        for item in products[cat] :
            tempListBox.insert(tk.END, item)
        listOfListBoxes[cat] = tempListBox

    activeCategory = categorys[0]
    activeProducts = products[activeCategory]
    listOfListBoxes[activeCategory].pack(side=tk.LEFT)

    listOfListBoxes[activeCategory].config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = listOfListBoxes[activeCategory].yview)

    search_var.trace_add("write", lambda *args: update_search_category_list())

    frame_plot = tk.Frame(popup_plotter)
    frame_plot.pack(pady=5)

    button_plot_prices = tk.Button(frame_plot, text="PLOT!",command=plot_prices)
    button_plot_prices.pack(side=tk.LEFT, padx=10)

    button_plotter_cancel = tk.Button(frame_plot, text="CANCEL", command=on_close)
    button_plotter_cancel.pack(side=tk.LEFT, pady=10)

def create_backup() :
    makeBackupDB.create_backup_of_DB(active_database)

def open_popup_ingredient() :
    global categorys, products, listOfListBoxes, scrollbar
    global activeCategory, activeProducts, search_var, search_entry

    def change_category(newCategory) :
        global activeCategory, listOfListBoxes, categorys, activeProducts, scrollbar
        listOfListBoxes[activeCategory].pack_forget()
        listOfListBoxes[newCategory].pack(pady=5)
        activeCategory = newCategory
        activeProducts = products[activeCategory]
        # search_entry.delete(0, tk.END)
        # print(listOfListBoxes[activeCategory].size())
        listOfListBoxes[activeCategory].config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listOfListBoxes[activeCategory].yview)

    def update_search_category_list() :
        global activeProducts, listOfListBoxes, activeProducts, activeCategory
        search_term = search_entry.get().lower()
        # print(search_term)
        listOfListBoxes[activeCategory].delete(0,tk.END)
        activeProducts = []
        for prod in products[activeCategory] :
            if search_term in prod.lower() :
                listOfListBoxes[activeCategory].insert(tk.END, prod)
                activeProducts.append(prod)

    def on_ingredient() :
        print(tree.selection())

    def on_close():
        print("You closed the Ingredient Editor.")
        popup_ingredient.destroy()


    popup_ingredient = tk.Toplevel(root)
    popup_ingredient.title("Ingredient Editor")
    popup_ingredient.geometry("1000x500")

    label_ingredient_info = tk.Label(popup_ingredient, text="Choose a product in the left field, " \
    "then choose an ingredient in the right field, then link them together.\n" \
    "If the ingredient does not exist, create a new one.")
    label_ingredient_info.pack(pady=5)

    # button3 = tk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)

    frame_search = tk.Frame(popup_ingredient)
    frame_search.pack(pady=5)  # You can also use padx here

    # Dropdown options  
    products, categorys = getFunctions.getProductsAndCategorys(active_database) # categorys and porducts include an "All Products" item

    # Selected option variable  
    opt = StringVar(value=categorys[0])  

    # Dropdown menu  
    dropdown_categorys = tk.OptionMenu(frame_search, opt, *categorys, command=change_category)
    dropdown_categorys.pack(side=tk.LEFT, padx=5)

    search_var = tk.StringVar()
    search_entry = tk.Entry(frame_search, textvariable=search_var)
    # search_entry.insert(0, "Search...")
    search_entry.pack(side=tk.LEFT, padx=5)

    listBox_frame = tk.Frame(popup_ingredient)
    listBox_frame.pack(pady=5)

    style = ttk.Style(popup_ingredient)
    style.theme_use("clam")

    scrollbar = ttk.Scrollbar(listBox_frame) 
    scrollbar.pack(side = RIGHT, fill = BOTH) 

    listOfListBoxes = {}
    for cat in categorys :
        tempTreeview = ttk.Treeview(listBox_frame, columns=("Name", "Price"), show="headings") 
        tempListBox = tk.Listbox(listBox_frame, selectmode='multiple', height=14, width=50)
        for item in products[cat] :
            tempListBox.insert(tk.END, item)
        listOfListBoxes[cat] = tempListBox

    activeCategory = categorys[0]
    activeProducts = products[activeCategory]
    listOfListBoxes[activeCategory].pack(side=tk.LEFT)

    listOfListBoxes[activeCategory].config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = listOfListBoxes[activeCategory].yview)

    search_var.trace_add("write", lambda *args: update_search_category_list())

    frame_plot = tk.Frame(popup_ingredient)
    frame_plot.pack(pady=5)

    button_plot_prices = tk.Button(frame_plot, text="INGREDIENT!", command=on_ingredient)
    button_plot_prices.pack(side=tk.LEFT, padx=10)

    button_ingredient_cancel = tk.Button(frame_plot, text="CANCEL", command=on_close)
    button_ingredient_cancel.pack(side=tk.LEFT, pady=10)

    tree = ttk.Treeview(popup_ingredient, columns=("Name", "Price", "Stock"), show="headings")
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

    for item in products[activeCategory]:
        tree.insert("", tk.END, values=(activeCategory,item,"hej"))

    tree.pack(expand=True)
    tree.pack(pady=5)


if __name__ == "__main__" :
    active_database = "hilbertDatabase.db" # Name of active database

    root = tk.Tk()
    root.title("Hilbot 2000")
    root.geometry("600x600")

    label_info_text = "This is a tool to 'help'/replace mackåsnan..."
    label_info = tk.Label(root, text=label_info_text)
    label_info.pack(pady=5)

    button_open_scraper = tk.Button(root, text="Open Scraper",command=open_popup_scraper)
    button_open_scraper.pack(pady=5)

    button_open_plotter = tk.Button(root, text="Open Plotter",command=open_popup_plotter)
    button_open_plotter.pack(pady=5)

    button_open_backup = tk.Button(root, text="Create Backup of Database", command=create_backup)
    button_open_backup.pack(pady=5)

    button_open_ingredient_editor = tk.Button(root, text="Open Ingredient Editor",command=open_popup_ingredient)
    button_open_ingredient_editor.pack(pady=5)

    # button3 = tk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)



    # tooltip = ListboxTooltip(listOfListBoxes[activeCategory], get_tooltip_text=lambda i: str(i) + "hej")

    # label2 = tk.Label(root, text="Recored Movment")
    # label2.pack(pady=5)

    # label3 = tk.Label(root, text="Nummber of Clicks: " + str(clickCount))
    # label3.pack(pady=0)

    # button2 = tk.Button(root, text="Start",command=startRecored)
    # button2.pack(pady=5)

    # label4 = tk.Label(root, text="Time Between Clicks: (sek)")
    # label4.pack(pady=0)

    # entry1 = tk.Entry(root, textvariable=timeDelay)
    # #entry1.pack(pady=5)


    root.mainloop()