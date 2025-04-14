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
import datetime

def importBread ():
    conn = sqlite3.connect("hilbertDatabase.db")
    cursor = conn.cursor()

    breads = [ # ( Id , Category , Name , Brand , Price , Unit )
        ( 200001 , "Bröd" , "Bagle"     , "MORMORS BAGERI" , 8.57   , "kr / st"),   # Säljs som en bagle
        ( 200002 , "Bröd" , "Baugette"  , "MORMORS BAGERI" , 15.71  , "kr / st"),   # Säljs som tredjedels baugetter
        ( 200003 , "Bröd" , "Ciabatta"  , "MORMORS BAGERI" , 6.43   , "kr / st"),   # Säljs som en ciabatta
        ( 200004 , "Bröd" , "Halvfralla", "MORMORS BAGERI" , 5.00   , "kr / st"),   # Säljs som halva frallor
        ( 200005 , "Bröd" , "Ostbulle"  , "MORMORS BAGERI" , 7.14   , "kr / st"),   # Säljs som en bulle/fralla
        ( 200006 , "Bröd" , "Rågbröd"   , "MORMORS BAGERI" , 25.00  , "kr / st"),   # Säljs som ca 12:te dels rågbröd
    ]
    for breadInfo in breads :
        id = breadInfo[0]
        category = breadInfo[1]
        name = breadInfo[2]
        brand = breadInfo[3]
        price = breadInfo[4]
        unit = breadInfo[5]
        timestamp = datetime.datetime.now().isoformat()

        cursor.execute('''
            INSERT OR REPLACE INTO products (id, category, name, brand)
            VALUES (?, ?, ?, ?)
            ''', (id, category, name, brand))
        
        cursor.execute('''
            INSERT INTO prices (productId, price, unit, timestamp)
            VALUES (?, ?, ?, ?)
            ''', (id, price, unit, timestamp))

    conn.commit()
    conn.close()


