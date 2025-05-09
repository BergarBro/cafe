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

    products = []
    categorys = []
    for cat, prod in elems :
        try :
            ind = categorys.index(cat)
        except :
            prodList = [prod]
            products.append(prodList)
            categorys.append(cat)
        else :
            products[ind].append(prod)

    return (products, categorys)


