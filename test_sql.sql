-- CREATE TABLE IF NOT EXISTS products (
--     id INT PRIMARY KEY,
--     name TEXT NOT NULL,
--     brand TEXT,
--     category TEXT
-- );

-- CREATE TABLE IF NOT EXISTS prices (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     productId INT NOT NULL,
--     price DECIMAL(10,2) NOT NULL,
--     unit TEXT NOT NULL,
--     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (productId) REFERENCES products(id) ON DELETE CASCADE
-- );


-- CREATE TABLE IF NOT EXISTS categorys (
--     category_name TEXT,
--     PRIMARY KEY (category_name)
-- );

-- CREATE TABLE IF NOT EXISTS products (
--     product_id INT,
--     product_name TEXT,
--     product_brand TEXT DEFAULT ('Not Found'),
--     category_name TEXT,
--     ingredient_name TEXT,
--     PRIMARY KEY (product_id),
--         FOREIGN KEY (category_name) REFERENCES categorys(category_name),
--         FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name)
-- );

-- CREATE TABLE IF NOT EXISTS price_offers (
--     offer_id TEXT DEFAULT (lower(hex(randomblob(8)))),
--     offer_price DECIMAL,
--     offer_timestamp DATETIME,
--     offer_unit TEXT,
--     product_id INT,
--     PRIMARY KEY (offer_id, product_id),
--         FOREIGN KEY (product_id) REFERENCES products(product_id)
-- );

-- CREATE TABLE IF NOT EXISTS ingredients (
--     ingredient_name TEXT,
--     ingredient_comment TEXT, -- Like if one cheese slice is 15g, information for the user
--     PRIMARY KEY (ingredient_name)
-- );

-- CREATE TABLE IF NOT EXISTS mixtures (
--     mixture_name TEXT,
--     nbr_of_sandwiches INT, -- The amount of sandwhiches one batch mixture will make
--     mixture_instructions TEXT,
--     PRIMARY KEY (mixture_name)
-- );

-- CREATE TABLE IF NOT EXISTS mixture_amounts (
--     ingredient_amount DECIMAL,
--     ingredient_unit TEXT,
--     ingredient_name TEXT,
--     mixture_name TEXT,
--     PRIMARY KEY (ingredient_name, mixture_name),
--         FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name),
--         FOREIGN KEY (mixture_name) REFERENCES mixtures(mixture_name)
-- );

-- CREATE TABLE IF NOT EXISTS sandwiches (
--     sandwich_name TEXT,
--     vegan BOOLEAN,
--     vegatarian BOOLEAN, -- True means the it is vegan, vegetarian respectively
--     bread_type TEXT,
--     prep_info TEXT,
--     mixture_name TEXT,
--     PRIMARY KEY (sandwich_name),
--         FOREIGN KEY (mixture_name) REFERENCES mixtures(mixture_name)
-- );

-- CREATE TABLE IF NOT EXISTS sandwich_amounts (
--     ingredient_amount DECIMAL,
--     ingredient_unit TEXT,
--     ingredient_name TEXT,
--     sandwich_name TEXT,
--     PRIMARY KEY (ingredient_name, sandwich_name),
--         FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name),
--         FOREIGN KEY (sandwich_name) REFERENCES sandwiches(sandwich_name)
-- );

-- CREATE TABLE IF NOT EXISTS weekdays (
--     weekday_id TEXT DEFAULT (lower(hex(randomblob(16)))),
--     weekday_name TEXT, -- = monday/tuseday/...
--     weekday_date DATETIME,
--     PRIMARY KEY (weekday_id)
-- );

-- CREATE TABLE IF NOT EXISTS day_schedules (
--     sandwich_ratio DECIMAL DEFAULT (1.0), -- The ratio of how many times the recepie the sandwich is suppose to be, default 1:1
--     day_info TEXT, -- Lay a comment for why we are making 4 "satser" hummus, because "lunchföreläsning"
--     sandwich_name TEXT,
--     weekday_id TEXT,
--     PRIMARY KEY (sandwich_name, weekday_id),
--         FOREIGN KEY (sandwich_name) REFERENCES sandwiches(sandwich_name),
--         FOREIGN KEY (weekday_id) REFERENCES weekdays(weekday_id)
-- );


--------------------------------------------------------------------------------------------------------------------
BEGIN TRANSACTION;

-- INSERT INTO products_test (product_id, product_name, product_brand, product_unit, category_name)
-- SELECT p.id, p.name, p.brand, pri.unit, p.category
-- FROM products p
-- JOIN (
--     SELECT unit, productId
--     FROM prices
--     GROUP BY productId
-- ) pri ON pri.productId = p.id;

-- INSERT INTO price_offers (offer_price, offer_timestamp, product_id)
-- SELECT price, timestamp, productId
-- FROM prices;

-- INSERT INTO categorys(category_name)
-- SELECT DISTINCT(category_name) from products_test;

-- INSERT INTO products SELECT * FROM products_test;

-- SELECT count(*) from price_offers;

-- SELECT pri.offer_price, p.product_unit, DATE(pri.offer_timestamp) 
-- FROM price_offers pri
-- JOIN products p USING (product_id)
-- WHERE p.product_name = 'Tomat Bas Lösvikt';

-- INSERT INTO products_new (product_id, product_name, product_brand, category_name)
-- SELECT product_id, product_name, product_brand, category_name from products;

INSERT INTO price_offers_new (offer_price, offer_timestamp, offer_unit, product_id)
SELECT pri.offer_price, pri.offer_timestamp, p.product_unit, pri.product_id
FROM products p
JOIN price_offers pri USING (product_id);

COMMIT;