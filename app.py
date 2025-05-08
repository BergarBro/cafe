import time
import tkinter as tk
import random as rd
import threading

import plotPrices, scraperScript

def startPlotPrices() :
    plotPrices.makePricePlot(["kaffe"])

def startScraperScript() :
    thread1 = threading.Thread(target=scraperScript.runScraperScript, daemon=True)
    thread1.start()

root = tk.Tk()
root.title("Hilbot 2000")
root.geometry("600x600")

timeDelay = tk.StringVar()

label1text = "This is a tool to 'help'/replace mackåsnan..."
label1 = tk.Label(root, text=label1text)
label1.pack(pady=5)

button1 = tk.Button(root, text="Plot Prices over Time",command=startPlotPrices)
button1.pack(pady=5)

button2 = tk.Button(root, text="Scrape Prices from SvenskCater",command=startScraperScript)
button2.pack(pady=5)

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