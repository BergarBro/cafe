import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random as rd
import threading

import plotPrices, scraperScript, getFunctions
from tooltip import ListboxTooltip

def open_popup_scraper():
    popup_scraper = tk.Toplevel(root)
    popup_scraper.title("Scraping Prices")
    popup_scraper.geometry("300x300")
    
    label_scraper_info = tk.Label(popup_scraper, text="Options for Scraping Prices:")
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

        thread_scraper = threading.Thread(
            target=lambda: scraperScript.run_scraper_script(optionsList=selected), 
            daemon=True
            )
        thread_scraper.start()
        popup_scraper.destroy()

    def on_cancel():
        print("You canceled the Scraper")
        popup_scraper.destroy()

    button_scraper_ok = tk.Button(popup_scraper, text="OK", command=on_ok)
    button_scraper_ok.pack(padx=10)

    button_scraper_cancel = tk.Button(popup_scraper, text="CANCEL", command=on_cancel)
    button_scraper_cancel.pack(pady=10)

def open_popup_plotter() :
    global categorys, products, listOfListBoxes, scrollbar
    global activeCategory, activeProducts, search_var, search_entry

    def plot_prices() :
        global categorys, activeCategory, activeProducts
        selectedProductsIndex = listOfListBoxes[activeCategory].curselection()
        selectedProducts = []
        for index in selectedProductsIndex :
            selectedProducts.append(activeProducts[index])

        plotPrices.makePricePlot(selectedProducts)

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
        print("You canceled the Plotter")
        popup_plotter.destroy()

    popup_plotter = tk.Toplevel(root)
    popup_plotter.title("Plotting Prices")
    popup_plotter.geometry("500x500")

    label_plotter_info = tk.Label(popup_plotter, text="Choose products to plot the price over time.")
    label_plotter_info.pack(pady=5)
    
    button_plot_prices = tk.Button(popup_plotter, text="Plot!",command=plot_prices)
    button_plot_prices.pack(pady=5)

    # button3 = tk.Button(root, text="Pop-Up",command=test)
    # button3.pack(pady=5)

    search_frame = tk.Frame(popup_plotter)
    search_frame.pack(pady=5)  # You can also use padx here

    # Dropdown options  
    products, categorys = getFunctions.getProductsAndCategorys()

    # Selected option variable  
    opt = StringVar(value=categorys[0])  

    # Dropdown menu  
    dropdown_categorys = tk.OptionMenu(search_frame, opt, *categorys, command=change_category)
    dropdown_categorys.pack(side=tk.LEFT, padx=5)

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var)
    # search_entry.insert(0, "Search...")
    search_entry.pack(side=tk.LEFT, padx=5)

    # Buttons packed inside the frame side-by-side
    button_select_all = tk.Button(search_frame, text="Select All", command=select_all)
    button_select_all.pack(side=tk.LEFT, padx=5)

    button_deselect_all = tk.Button(search_frame, text="Deselect All", command=deselect_all)
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

    button_scraper_cancel = tk.Button(popup_plotter, text="CLOSE", command=on_close)
    button_scraper_cancel.pack(pady=10)

root = tk.Tk()
root.title("Hilbot 2000")
root.geometry("600x600")

label_info_text = "This is a tool to 'help'/replace mackåsnan..."
label_info = tk.Label(root, text=label_info_text)
label_info.pack(pady=5)

button_open_scraper = tk.Button(root, text="Scrape Prices from SvenskCater",command=open_popup_scraper)
button_open_scraper.pack(pady=5)

button_open_plotter = tk.Button(root, text="Plot Prices over Time",command=open_popup_plotter)
button_open_plotter.pack(pady=5)

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