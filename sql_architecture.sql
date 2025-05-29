-- Active Tables in Database

CREATE TABLE IF NOT EXISTS categorys (
    category_name TEXT,
    PRIMARY KEY (category_name)
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT,
    product_name TEXT,
    product_brand TEXT DEFAULT ('Not Found'),
    category_name TEXT,
    ingredient_name TEXT,
    PRIMARY KEY (product_id),
        FOREIGN KEY (category_name) REFERENCES categorys(category_name),
        FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name)
);

CREATE TABLE IF NOT EXISTS price_offers (
    offer_id TEXT DEFAULT (lower(hex(randomblob(8)))),
    offer_price DECIMAL,
    offer_timestamp DATETIME,
    offer_unit TEXT,
    product_id INT,
    PRIMARY KEY (offer_id, product_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_name TEXT,
    ingredient_comment TEXT, -- Like if one cheese slice is 15g, information for the user
    PRIMARY KEY (ingredient_name)
);

CREATE TABLE IF NOT EXISTS mixtures (
    mixture_name TEXT,
    nbr_of_sandwiches INT, -- The amount of sandwhiches one batch mixture will make
    mixture_instruction TEXT,
    PRIMARY KEY (mixture_name)
);

CREATE TABLE IF NOT EXISTS mixture_amounts (
    ingredient_amount DECIMAL,
    ingredient_unit TEXT,
    ingredient_name TEXT,
    mixture_name TEXT,
    PRIMARY KEY (ingredient_name, mixture_name),
        FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name),
        FOREIGN KEY (mixture_name) REFERENCES mixtures(mixture_name)
);

CREATE TABLE IF NOT EXISTS sandwiches (
    sandwich_name TEXT,
    vegan BOOLEAN,  -- True means the it is vegan, vegetarian respectively
    vegatarian BOOLEAN,
    bread_type TEXT,
    prep_info TEXT,
    mixture_name TEXT,
    PRIMARY KEY (sandwich_name),
        FOREIGN KEY (mixture_name) REFERENCES mixtures(mixture_name)
);

CREATE TABLE IF NOT EXISTS sandwich_amounts (
    ingredient_amount DECIMAL,
    ingredient_unit TEXT,
    ingredient_name TEXT,
    sandwich_name TEXT,
    PRIMARY KEY (ingredient_name, sandwich_name),
        FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name),
        FOREIGN KEY (sandwich_name) REFERENCES sandwiches(sandwich_name)
);

CREATE TABLE IF NOT EXISTS weekdays (
    weekday_id TEXT DEFAULT (lower(hex(randomblob(8)))),
    weekday_name TEXT, -- = monday/tuseday/...
    weekday_date DATETIME,
    PRIMARY KEY (weekday_id)
);

CREATE TABLE IF NOT EXISTS day_schedules (
    sandwich_ratio DECIMAL DEFAULT (1.0), -- The ratio of how many times the recepie the sandwich is suppose to be, default 1:1
    day_info TEXT, -- Lay a comment for why we are making 4 "satser" hummus, because "lunchföreläsning"
    sandwich_name TEXT,
    weekday_id TEXT,
    PRIMARY KEY (sandwich_name, weekday_id),
        FOREIGN KEY (sandwich_name) REFERENCES sandwiches(sandwich_name),
        FOREIGN KEY (weekday_id) REFERENCES weekdays(weekday_id)
);

-- SELECT p.category, p.name, p.id, pri.price, pri.unit, pri.timestamp 
-- FROM prices pri
-- JOIN products p ON pri.productId = p.id
-- WHERE p.category = 'Frukt och Grönt'
-- ORDER BY p.name ASC;

-- SELECT p.category, SUM(price) as totSum
-- FROM products p
-- JOIN (
--     SELECT productId, price, MAX(timestamp) AS max_ts
--     FROM prices
--     WHERE price < 20
--     GROUP BY productId
-- ) AS pp 
-- ON p.id = pp.productId
-- GROUP BY p.category


-- SELECT p.category, SUM(pp.price) AS totSum --, pp.unit, pp.max_ts
-- FROM products p
-- JOIN (
--     SELECT productId, price, unit, MAX(timestamp) AS max_ts
--     FROM prices
--     GROUP BY productId
-- ) pp ON p.id = pp.productId
-- GROUP BY p.category
-- HAVING totSum > 1000
-- ORDER BY p.category ASC, pp.price DESC;

-- SELECT * FROM products;