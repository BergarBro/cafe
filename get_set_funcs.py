
# CREATE TABLE IF NOT EXISTS categorys (
#     category_name TEXT,
#     PRIMARY KEY (category_name)
# );

# CREATE TABLE IF NOT EXISTS products (
#     product_id INT,
#     product_name TEXT,
#     product_brand TEXT DEFAULT ('Not Found'),
#     category_name TEXT,
#     ingredient_name TEXT,
#     PRIMARY KEY (product_id),
#         FOREIGN KEY (category_name) REFERENCES categorys(category_name),
#         FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name)
# );

# CREATE TABLE IF NOT EXISTS price_offers (
#     offer_id TEXT DEFAULT (lower(hex(randomblob(8)))),
#     offer_price DECIMAL,
#     offer_timestamp DATETIME,
#     offer_unit TEXT,
#     product_id INT,
#     PRIMARY KEY (offer_id, product_id),
#         FOREIGN KEY (product_id) REFERENCES products(product_id)
# );

# CREATE TABLE IF NOT EXISTS ingredients (
#     ingredient_name TEXT,
#     ingredient_comment TEXT, -- Like if one cheese slice is 15g, information for the user
#     PRIMARY KEY (ingredient_name)
# );

# CREATE TABLE IF NOT EXISTS mixtures (
#     mixture_name TEXT,
#     nbr_of_sandwiches INT, -- The amount of sandwhiches one batch mixture will make
#     mixture_instruction TEXT,
#     PRIMARY KEY (mixture_name)
# );

# CREATE TABLE IF NOT EXISTS mixture_amounts (
#     ingredient_amount DECIMAL,
#     ingredient_unit TEXT,
#     ingredient_name TEXT,
#     mixture_name TEXT,
#     PRIMARY KEY (ingredient_name, mixture_name),
#         FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name),
#         FOREIGN KEY (mixture_name) REFERENCES mixtures(mixture_name)
# );

# CREATE TABLE IF NOT EXISTS sandwiches (
#     sandwich_name TEXT,
#     vegan BOOLEAN,  -- True means the it is vegan, vegetarian respectively
#     vegatarian BOOLEAN,
#     bread_type TEXT,
#     prep_info TEXT,
#     mixture_name TEXT,
#     PRIMARY KEY (sandwich_name),
#         FOREIGN KEY (mixture_name) REFERENCES mixtures(mixture_name)
# );

# CREATE TABLE IF NOT EXISTS sandwich_amounts (
#     ingredient_amount DECIMAL,
#     ingredient_unit TEXT,
#     ingredient_name TEXT,
#     sandwich_name TEXT,
#     PRIMARY KEY (ingredient_name, sandwich_name),
#         FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name),
#         FOREIGN KEY (sandwich_name) REFERENCES sandwiches(sandwich_name)
# );

# CREATE TABLE IF NOT EXISTS weekdays (
#     weekday_id TEXT DEFAULT (lower(hex(randomblob(8)))),
#     weekday_name TEXT, -- = monday/tuseday/...
#     weekday_date DATETIME,
#     PRIMARY KEY (weekday_id)
# );

# CREATE TABLE IF NOT EXISTS day_schedules (
#     sandwich_ratio DECIMAL DEFAULT (1.0), -- The ratio of how many times the recepie the sandwich is suppose to be, default 1:1
#     day_info TEXT, -- Lay a comment for why we are making 4 "satser" hummus, because "lunchföreläsning"
#     sandwich_name TEXT,
#     weekday_id TEXT,
#     PRIMARY KEY (sandwich_name, weekday_id),
#         FOREIGN KEY (sandwich_name) REFERENCES sandwiches(sandwich_name),
#         FOREIGN KEY (weekday_id) REFERENCES weekdays(weekday_id)
# );

import sqlite3

def get_products_and_categorys(active_database) :
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

def get_max_date(active_database) :
    conn = sqlite3.connect(active_database)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT DATE(MAX(offer_timestamp)) FROM price_offers;
    ''')
    max_date = cursor.fetchall()[0][0]
    conn.close()

    return max_date
