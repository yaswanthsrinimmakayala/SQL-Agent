import sqlite3
from datetime import datetime,timedelta
import random
# connection to database
conn = sqlite3.connect("mydb.db")

# cursor object
cursor = conn.cursor()


# Creating a tables

cursor.executescript("""
CREATE TABLE IF NOT EXISTS customers(
               id INTEGER PRIMARY KEY,
               name TEXT,
               email TEXT,
               city TEXT
    );

CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY,
            name TEXT
    );

CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category_id INTEGER,
            price REAL,
            FOREIGN KEY(category_id) REFERENCES categories(id)
);


CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date TEXT,
            FOREIGN KEY(customer_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
);                  
""")
# Insertion of data

customers = [
    ("Alice", "alice@email.com", "Bangalore"),
    ("Bob", "bob@email.com", "Mumbai"),
    ("Charlie", "charlie@email.com", "Delhi"),
    ("David", "david@email.com", "Chennai"),
]

cursor.executemany(
    "INSERT INTO customers (name, email, city) VALUES (?, ?, ?)",
    customers
)

categories = [("Electronics",), ("Clothing",), ("Books",)]
cursor.executemany("INSERT INTO categories (name) VALUES (?)", categories)

products = [
    ("Laptop", 1, 80000),
    ("Phone", 1, 40000),
    ("T-Shirt", 2, 500),
    ("Jeans", 2, 1500),
    ("Novel", 3, 300),
]

cursor.executemany(
    "INSERT INTO products (name, category_id, price) VALUES (?, ?, ?)",
    products
)

orders = [(1, 1, '2026-03-01'),
(2, 2, '2026-03-05'),
(3, 1, '2026-03-10'),
(4, 3, '2026-03-15'),
(5, 4, '2026-03-20')]
cursor.executemany(
    "INSERT INTO orders (id, customer_id, order_date) VALUES(?,?,?)",orders
)

order_items = [
    (1, 1, 1, 1),  
    (2, 1, 5, 2), 
    (3, 2, 2, 1),  
    (4, 2, 3, 3),  
    (5, 3, 4, 2),
    (6, 4, 5, 5),
    (7, 5, 1, 1),  
    (8, 5, 3, 2)]
cursor.executemany("INSERT INTO order_items (id, order_id, product_id, quantity) VALUES(?,?,?,?)",
                   order_items
)
conn.commit()
conn.close()