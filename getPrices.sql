-- CREATE TABLE IF NOT EXISTS products (
--     id INT PRIMARY KEY,
--     name TEXT NOT NULL,
--     brand TEXT
-- );

-- CREATE TABLE IF NOT EXISTS prices (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     productId INT NOT NULL,
--     price DECIMAL(10,2) NOT NULL,
--     unit TEXT NOT NULL,
--     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (productId) REFERENCES products(id) ON DELETE CASCADE
-- );

SELECT p.name, p.id, pri.price, pri.unit, pri.timestamp 
FROM prices pri
JOIN products p ON pri.productId = p.id
WHERE p.id = 49553
ORDER BY pri.timestamp DESC;
