
-- CREATE TABLE users (
--     id INTERGER PRIMARY KEY,
--     name TEXT NOT NULL,
--     username TEXT NOT NULL UNIQUE,
--     email TEXT,
--     age INTEGER,
--     created_at_time DATETIME DEFAULT CURRENT_TIMESTAMP
-- );

-- INSERT INTO users (id, name, username, email)
-- VALUES (1,'Axel Berg', 'BergarBro', 'axel.berg@gmail.com');

-- SELECT * FROM users;

-- INSERT INTO users (id, name, username, email, age)
-- VALUES (2, 'Arvid Berg', 'Zany', 'arvid.berg@gmail.com', 24);

-- INSERT INTO users (id, name, username, email, age)
-- VALUES (3, 'Jörgen Granten', 'Jorg', 'jorg.grant@fuktcom.com', 60), (4, 'Karin Granten', 'Karen', 'karin.granten@sweco.com', 57);

-- UPDATE users SET age = 26 WHERE id = 1;
-- UPDATE users SET age = 24 WHERE id = 2;
-- UPDATE users SET age = 60 WHERE id = 3;
-- UPDATE users SET age = 56 WHERE id = 4;

SELECT * FROM users;
