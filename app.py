import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random as rd
import threading

import plotPrices, scraperScript, getFunctions

def startPlotPrices() :
    global categorys, activeCategory, activeProducts
    selectedProductsIndex = listOfListBoxes[activeCategory].curselection()
    selectedProducts = []
    for index in selectedProductsIndex :
        selectedProducts.append(activeProducts[index])

    plotPrices.makePricePlot(selectedProducts)

def test() :
    print(opt.get())
    # print(listbox1.curselection())

def changeCategory(newCategory) :
    global activeCategory, listOfListBoxes, categorys, activeProducts, scrollbar
    listOfListBoxes[activeCategory].pack_forget()
    listOfListBoxes[newCategory].pack(pady=5)
    activeCategory = newCategory
    activeProducts = products[activeCategory]
    # search_entry.delete(0, tk.END)
    # print(listOfListBoxes[activeCategory].size())
    listOfListBoxes[activeCategory].config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = listOfListBoxes[activeCategory].yview)

def open_popup_scraper():
    popup = tk.Toplevel(root)
    popup.title("Scraping Prices")
    popup.geometry("300x300")
    
    popLabel = tk.Label(popup, text="Options for Scraping Prices:")
    popLabel.pack(pady=10)
    
    # Radio buttons for mutually exclusive choices
    option_vars = {}
    options = ["Fetch Products", "Fetch Prices", "Fetch Bread and Breadprices"]
    for opt in options:
        var = tk.BooleanVar()
        ttk.Checkbutton(popup, text=opt, variable=var).pack(pady=5)
        option_vars[opt] = var

    def on_ok():
        selected = [var.get() for opt, var in option_vars.items()]

        thread1 = threading.Thread(
            target=lambda: scraperScript.runScraperScript(optionsList=selected), 
            daemon=True
            )
        thread1.start()
        popup.destroy()

    def on_cancel():
        print("You canceled the Scraper")
        popup.destroy()

    popButton1 = ttk.Button(popup, text="OK", command=on_ok)
    popButton1.pack(padx=10)

    popButton2 = ttk.Button(popup, text="CANCEL", command=on_cancel)
    popButton2.pack(pady=10)

def selectAll() :
    global activeCategory, listOfListBoxes
    listOfListBoxes[activeCategory].selection_set(0,listOfListBoxes[activeCategory].size())

def deselectAll() :
    global activeCategory, listOfListBoxes
    listOfListBoxes[activeCategory].selection_clear(0,listOfListBoxes[activeCategory].size())

def updateSearchCategoryList() :
    global activeProducts, listOfListBoxes, activeProducts, activeCategory
    search_term = search_entry.get().lower()
    # print(search_term)
    listOfListBoxes[activeCategory].delete(0,tk.END)
    activeProducts = []
    for prod in products[activeCategory] :
        if search_term in prod.lower() :
            listOfListBoxes[activeCategory].insert(tk.END, prod)
            activeProducts.append(prod)

root = tk.Tk()
root.title("Hilbot 2000")
root.geometry("600x600")

label1text = "This is a tool to 'help'/replace mackåsnan..."
label1 = tk.Label(root, text=label1text)
label1.pack(pady=5)

button2 = tk.Button(root, text="Scrape Prices from SvenskCater",command=open_popup_scraper)
button2.pack(pady=5)

button1 = tk.Button(root, text="Plot Prices over Time",command=startPlotPrices)
button1.pack(pady=5)

button3 = tk.Button(root, text="Pop-Up",command=test)
# button3.pack(pady=5)

search_frame = tk.Frame(root)
search_frame.pack(pady=5)  # You can also use padx here

# Dropdown options  
products, categorys = getFunctions.getProductsAndCategorys()

# Selected option variable  
opt = StringVar(value=categorys[0])  

# Dropdown menu  
dropdown1 = tk.OptionMenu(search_frame, opt, *categorys, command=changeCategory)
dropdown1.pack(side=tk.LEFT, padx=5)

search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var)
# search_entry.insert(0, "Search...")
search_entry.pack(side=tk.LEFT, padx=5)

# Buttons packed inside the frame side-by-side
btn1 = tk.Button(search_frame, text="Select All", command=selectAll)
btn1.pack(side=tk.LEFT, padx=5)

btn2 = tk.Button(search_frame, text="Deselect All", command=deselectAll)
btn2.pack(side=tk.LEFT, padx=5)

search_var.trace_add("write", lambda *args: updateSearchCategoryList())

listBox_frame = tk.Frame(root)
listBox_frame.pack(pady=5)

style = ttk.Style()
style.theme_use("clam")

scrollbar = ttk.Scrollbar(listBox_frame) 
scrollbar.pack(side = RIGHT, fill = BOTH) 

listOfListBoxes = {}
for cat in categorys :
    tempListBox = tk.Listbox(listBox_frame, selectmode='multiple', height=10, width=50)
    for item in products[cat] :
        tempListBox.insert(tk.END, item)
    listOfListBoxes[cat] = tempListBox

activeCategory = categorys[0]
activeProducts = products[activeCategory]
listOfListBoxes[activeCategory].pack(side=tk.LEFT)

listOfListBoxes[activeCategory].config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listOfListBoxes[activeCategory].yview)


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