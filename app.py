import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
import random as rd
import threading

import plotPrices, scraperScript, getFunctions

def startPlotPrices() :
    global categorys, activList
    productList = products[activList]
    selectedProductsIndex = listOfListBoxes[activList].curselection()
    selectedProducts = []
    for index in selectedProductsIndex :
        selectedProducts.append(productList[index])

    plotPrices.makePricePlot(selectedProducts)

def startScraperScript() :
    thread1 = threading.Thread(target=scraperScript.runScraperScript, daemon=True)
    thread1.start()

def test() :
    print(opt.get())
    # print(listbox1.curselection())

def changeCategory(cat) :
    global activList, listOfListBoxes, categorys
    catIndex = categorys.index(cat)
    listOfListBoxes[activList].pack_forget()
    listOfListBoxes[catIndex].pack(pady=5)
    activList = catIndex


root = tk.Tk()
root.title("Hilbot 2000")
root.geometry("600x600")

timeDelay = tk.StringVar()

label1text = "This is a tool to 'help'/replace mackåsnan..."
label1 = tk.Label(root, text=label1text)
label1.pack(pady=5)

button2 = tk.Button(root, text="Scrape Prices from SvenskCater",command=startScraperScript)
button2.pack(pady=5)

button1 = tk.Button(root, text="Plot Prices over Time",command=startPlotPrices)
button1.pack(pady=5)

button3 = tk.Button(root, text="Test",command=test)
# button3.pack(pady=5)

# Dropdown options  
products, categorys = getFunctions.getProductsAndCategorys()
for l in products :
    l.sort()

# Selected option variable  
opt = StringVar(value=categorys[0])  

# Dropdown menu  
dropdown1 = tk.OptionMenu(root, opt, *categorys, command=changeCategory)
dropdown1.pack(pady=5)

scrollbar = Scrollbar(root) 
scrollbar.pack(side = RIGHT, fill = BOTH) 

listOfListBoxes = []
for i in range(len(categorys)) :
    tempListBox = tk.Listbox(root, selectmode='multiple', height=10, width=50)
    for item in products[i] :
        tempListBox.insert(tk.END, item)
    listOfListBoxes.append(tempListBox)

activList = 0
listOfListBoxes[0].pack(pady=5)

listOfListBoxes[0].config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listOfListBoxes[0].yview) 

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