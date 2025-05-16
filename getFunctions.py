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

def getProductsAndCategorys() :
    conn = sqlite3.connect("hilbertDatabase.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT category, name FROM products;
    ''')
    elems = cursor.fetchall()
    conn.close()

    products = {}
    categorys = []

    categorys.append("All Products")
    products["All Products"] = []

    for cat, prod in elems :
        try :
            categorys.index(cat)
        except :
            products[cat] = []
            categorys.append(cat)

        products[cat].append(prod)
        products["All Products"].append(prod)
    

    categorys.sort()

    for cat in categorys :
        products[cat].sort()

    return (products, categorys)


