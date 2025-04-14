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

SELECT p.category, p.name, p.id, pri.price, pri.unit, pri.timestamp 
FROM prices pri
JOIN products p ON pri.productId = p.id
WHERE p.category = 'Bröd'
ORDER BY p.name ASC;

-- SELECT p.category, p.name, pp.price, pp.unit, pp.max_ts
-- FROM products p
-- JOIN (
--     SELECT productId, price, unit, MAX(timestamp) AS max_ts
--     FROM prices
--     GROUP BY productId
-- ) pp ON p.id = pp.productId
-- ORDER BY p.category ASC, pp.price DESC;
