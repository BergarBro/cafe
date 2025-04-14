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
import numpy as np
import random as rn

def main():
    makeRandomPlot()

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

def makePricePlot(category) :
    print("hi")



main()