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

def getProductsAndCategorys(active_database) :
    conn = sqlite3.connect(active_database)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT category_name, product_name, ingredient_name FROM products;
    ''')
    elems = cursor.fetchall()
    conn.close()

    products = {}
    categorys = []

    categorys.append("All Products")
    products["All Products"] = []

    for cat, prod, ingr in elems :
        try :
            categorys.index(cat)
        except :
            products[cat] = []
            categorys.append(cat)

        products[cat].append((prod,ingr))
        products["All Products"].append((prod,ingr))
    

    categorys.sort()

    for cat in categorys :
        products[cat].sort()

    return (products, categorys)

def get_ingredients(active_database) :
    conn = sqlite3.connect(active_database)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT ingredient_name, ingredient_comment FROM ingredients;
    ''')
    elems = cursor.fetchall()
    conn.close()

    # print(elems)
    # print([item[0] for item in elems if item[0] == "test"])

    elems.sort()

    return elems

def add_ingredient(active_database, ingredient_name, ingredient_comment) :
    with sqlite3.connect(active_database) as conn :
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO ingredients (ingredient_name, ingredient_comment)
            VALUES(?,?)
        ''',(ingredient_name, ingredient_comment))

def remove_ingredient(active_database, ingredient_name) :
    with sqlite3.connect(active_database) as conn :
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM ingredients
            WHERE ingredient_name = ?
        ''',(ingredient_name,))

def link_product_ingredient(active_database, product_name, ingredient_name) :
    with sqlite3.connect(active_database) as conn :
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE products
            SET ingredient_name = ?
            WHERE product_name = ?
        ''',(ingredient_name, product_name))

def unlink_product_ingredient(active_database, product_name) :
    with sqlite3.connect(active_database) as conn :
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE products
            SET ingredient_name = ''
            WHERE product_name = ?
        ''',(product_name,))

def get_mixtures(active_database) :
    conn = sqlite3.connect(active_database)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT mixture_name, nbr_of_sandwiches, mixture_instruction FROM mixtures;
    ''')
    elems = cursor.fetchall()
    conn.close()

    # print(elems)
    # print([item[0] for item in elems if item[0] == "test"])

    elems.sort()

    return elems

def add_mixture(active_database, mixture_name, nbr_of_sandwiches) :
    with sqlite3.connect(active_database) as conn :
        cursor = conn.cursor()

        # print(mixture_name)

        cursor.execute('''
            INSERT OR REPLACE INTO mixtures (mixture_name, nbr_of_sandwiches, mixture_instruction)
            VALUES(?,?,'')
        ''',(mixture_name,nbr_of_sandwiches))

def remove_mixture(active_database, mixture_name) :
    with sqlite3.connect(active_database) as conn :
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM mixtures
            WHERE mixture_name = ?
        ''',(mixture_name,))

def update_mixture(active_database, mixture_name_old, mixture_name_new, nbr_of_sandwiches, mixture_instructions) :
    with sqlite3.connect(active_database) as conn :
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE mixtures
            SET mixture_name = ?, nbr_of_sandwiches = ?, mixture_instruction = ?
            WHERE mixture_name = ?
        ''',(mixture_name_new, nbr_of_sandwiches, mixture_instructions,mixture_name_old))
