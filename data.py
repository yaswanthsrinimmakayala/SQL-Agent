import sqlite3
def actual_data():
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()
    cursor.executescript("""

    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;
    DROP TABLE IF EXISTS categories;
    DROP TABLE IF EXISTS customers;

    CREATE TABLE customers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        city TEXT
    );

    CREATE TABLE categories (
        id INTEGER PRIMARY KEY,
        name TEXT
    );

    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category_id INTEGER,
        price REAL,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    );

    CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        status TEXT,
        payment_method TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    );

    CREATE TABLE order_items (
        id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    );

    """)

    # Customers
    customers = [
        (1, "Ravi Kumar", "ravi.kumar@gmail.com", "Bangalore"),
        (2, "Priya Sharma", "priya.sharma@yahoo.com", "Mumbai"),
        (3, "Arjun Reddy", "arjun.reddy@outlook.com", "Hyderabad"),
        (4, "Neha Verma", "neha.verma@gmail.com", "Delhi"),
        (5, "Karan Mehta", "karan.mehta@gmail.com", "Pune"),
        (6, "Sneha Iyer", "sneha.iyer@yahoo.com", "Chennai"),
    ]

    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?)", customers
    )

    # Categories
    categories = [
        (1, "Electronics"),
        (2, "Clothing"),
        (3, "Books"),
        (4, "Home & Kitchen")
    ]

    cursor.executemany(
        "INSERT INTO categories VALUES (?, ?)", categories
    )

    # Products
    products = [
        (1, "iPhone 14", 1, 70000),
        (2, "Samsung Galaxy S22", 1, 65000),
        (3, "Dell Inspiron Laptop", 1, 85000),
        (4, "Men's T-Shirt", 2, 799),
        (5, "Women's Kurti", 2, 1200),
        (6, "Blue Jeans", 2, 2000),
        (7, "Python Programming Book", 3, 599),
        (8, "Data Science Handbook", 3, 899),
        (9, "Mixer Grinder", 4, 3000),
        (10, "Cookware Set", 4, 4500),
    ]

    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?)", products
    )

    # Orders
    orders = [
        (1, 1, "2026-03-01", "Delivered", "UPI"),
        (2, 2, "2026-03-03", "Delivered", "Credit Card"),
        (3, 3, "2026-03-05", "Pending", "UPI"),
        (4, 1, "2026-03-07", "Delivered", "Debit Card"),
        (5, 4, "2026-03-10", "Cancelled", "COD"),
        (6, 5, "2026-03-12", "Delivered", "UPI"),
        (7, 6, "2026-03-15", "Delivered", "Credit Card"),
    ]

    cursor.executemany(
        "INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders
    )

    # Order Items
    order_items = [
        (1, 1, 1, 1),   
        (2, 1, 7, 2),   
        (3, 2, 2, 1),  
        (4, 2, 4, 3),  
        (5, 3, 3, 1),  
        (6, 4, 5, 2),
        (7, 5, 8, 1),   
        (8, 6, 9, 1),   
        (9, 7, 10, 1),  
    ]

    cursor.executemany(
        "INSERT INTO order_items VALUES (?, ?, ?, ?)", order_items
    )

    conn.commit()
    conn.close()

    print("Database created with realistic data!")