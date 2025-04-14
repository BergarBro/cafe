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

def importBread ():
    conn = sqlite3.connect("hilberDatabase.db")
    cursor = conn.cursor()

    breads = [
        ( 200001 , "Fruit"  , 10.50 ),
        ( 200002 , "Fruit"  , 5.75  ),
        ( 200003 , "Bakery" , 22.00 )
    ]

    cursor.executemany("INSERT OR REPLACE INTO products (id, name, brand, category) VALUES (?, ?, ?)", breads)

    conn.commit()
    conn.close()


