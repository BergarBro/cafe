# -- CREATE TABLE IF NOT EXISTS products (
# --     id INT PRIMARY KEY,
# --     name TEXT NOT NULL,
# --     brand TEXT,
# --     category TEXT
# -- );

# -- CREATE TABLE IF NOT EXISTS prices (
# --     id INTEGER PRIMARY KEY AUTOINCREMENT,
# --     productId INT NOT NULL,
# --     price DECIMAL(10,2) NOT NULL,
# --     unit TEXT NOT NULL,
# --     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
# --     FOREIGN KEY (productId) REFERENCES products(id) ON DELETE CASCADE
# -- );

import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.widgets import Slider
import numpy as np
import random as rn
import datetime

def main():
    print("Main")
    # test()
    # makePricePlot(["Gurka", "Tomat Bas", "Kaffe"])
    # makeRandomPlot()
    

def makeRandomPlot() :
    print("Here is funny plot!")
    c = ['r','g','b','c','m','y','k']
    x = range(50)
    y = []
    z = []
    for i in x :
        y.append(rn.randrange(0,10))
        z.append(rn.randrange(0,10))
    
    # print(z[1:1+2])
    for i in range(len(z)-1) :
        plt.plot(z[i:i+2],y[i:i+2], color = c[rn.randrange(0,len(c))])
    plt.show()

def makePricePlot(productsName) :
    conn = sqlite3.connect("hilbertDatabase.db")
    cursor = conn.cursor()
    units = []

    for productName in productsName :
        search = f"%{productName.lower()}%"
        cursor.execute('''
            -- SELECT price, DATE(timestamp) FROM prices
            -- WHERE ProductId = 49553;
                       
            SELECT pri.price, pri.unit, DATE(pri.timestamp) 
            FROM prices pri
            JOIN products p ON pri.productId = p.id
            WHERE LOWER(p.name) LIKE ?;
        ''', (search,))

        elems = cursor.fetchall()

        if elems != [] :

            price, unit, date = list(zip(*elems))
            time = list(map(makeDateObj, date))
            units.append(unit[0])

            # print(price)
            # print(time)

            plt.plot(time, price, marker = '.')
            plt.xticks(rotation=45)

            plt.xlabel("Time")
            plt.title("Product Prices over Time")
        else :
            productsName.remove(productName)
            print("Could not find product in list:", productName)
    plt.legend(productsName, loc="upper left")
    if len(set(units)) == 1 :
        plt.ylabel(units[0], rotation=0)
    else :
        print("Products have different units, could not compare")

    plt.tight_layout() 
    plt.show()
    cursor.close()

    # hej = "2024-04-23"
    # datehej = makeDateObj(hej)
    # print(datehej)

def test() :
    # Sample data
    dates = [datetime.date(2024, 1, i + 1) for i in range(31)]
    values = [(-2)**i + 10 for i in range(31)]

    # Initial range
    start = 0
    end = 10

    # Plot setup
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    line, = ax.plot(dates[start:end], values[start:end], marker='o')
    ax.set_title('Interactive Date Range')

    # Slider for range
    ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
    slider = Slider(ax_slider, 'Start Index', 0, len(dates) - 10, valinit=start, valstep=1)

    # Update function
    def update(val):
        idx = int(slider.val)
        line.set_xdata(dates[idx:idx*10])
        line.set_ydata(values[idx:idx*10])
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

def makeDateObj(str) :
    d = str.split('-')
    return datetime.date(int(d[0]), int(d[1]), int(d[2]))

main()