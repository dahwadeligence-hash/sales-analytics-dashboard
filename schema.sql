-- schema.sql: creates sales table and inserts sample seed data

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price REAL NOT NULL DEFAULT 0,
    sales_rep TEXT,
    region TEXT,
    notes TEXT
);

-- Sample seed data
INSERT INTO sales(date, product, quantity, unit_price, sales_rep, region, notes) VALUES
('2026-08-01', 'Widget A', 10, 9.99, 'Alice', 'North', 'First batch'),
('2026-08-03', 'Widget B', 5, 19.99, 'Bob', 'South', ''),
('2026-08-05', 'Widget A', 7, 9.99, 'Carol', 'East', 'Promotion'),
('2026-08-10', 'Widget C', 3, 29.99, 'Alice', 'North', ''),
('2026-08-12', 'Widget B', 2, 19.99, 'Dave', 'West', 'Large client'),
('2026-08-15', 'Widget A', 1, 9.99, 'Eve', 'North', 'Sample');
