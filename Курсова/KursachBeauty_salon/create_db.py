import sqlite3
from datetime import date
import os

DB_FOLDER = "data"
DB_NAME = "beauty_salon.db"
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)

if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.executescript("""
CREATE TABLE Masters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT,
    contact_info TEXT
);

CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE Services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    master_id INTEGER,
    category_id INTEGER,
    duration_min INTEGER,
    price_usd REAL,
    stock_quantity INTEGER,
    FOREIGN KEY (master_id) REFERENCES Masters(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(id) ON DELETE CASCADE
);

CREATE TABLE Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    address TEXT
);

CREATE TABLE Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT,
    total_price REAL,
    FOREIGN KEY (customer_id) REFERENCES Customers(id) ON DELETE CASCADE
);

CREATE TABLE OrderItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    service_id INTEGER,
    quantity INTEGER,
    unit_price REAL,
    subtotal REAL,
    FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES Services(id) ON DELETE CASCADE
);
""")


masters = [
    ("Ольга Манікюр", "Манікюр, педикюр", "olga@salon.com"),          # ID: 1
    ("Ірина Стрижкова", "Стрижки, фарбування", "ira@salon.com"),      # ID: 2
    ("Андрій Барбер", "Чоловічі стрижки", "andriy@salon.com"),        # ID: 3
    ("Світлана Візажист", "Макіяж", "svitlana@salon.com"),           # ID: 4
    ("Марина Косметолог", "Догляд за обличчям", "maryna@salon.com")  # ID: 5
]
cursor.executemany("INSERT INTO Masters (name, specialty, contact_info) VALUES (?, ?, ?)", masters)

categories = [
    ("Нігтьовий сервіс", "Манікюр, педикюр, покриття"),                # ID: 1
    ("Перукарські послуги", "Стрижка, укладка, фарбування"),           # ID: 2
    ("Додаткові товари", "Професійна косметика та догляд"),           # ID: 3
    ("Косметологія", "Процедури для обличчя та тіла")                 # ID: 4
]
cursor.executemany("INSERT INTO Categories (name, description) VALUES (?, ?)", categories)

services = [
    ('Манікюр + Гель-лак', 1, 1, 90, 25.00, 1000),      # ID: 1
    ('Жіноча стрижка', 2, 2, 60, 35.00, 1000),         # ID: 2
    ('Фарбування (середня довжина)', 2, 2, 180, 80.00, 1000),# ID: 3
    ('Чоловіча стрижка', 3, 2, 45, 20.00, 1000),       # ID: 4
    ('Масло для кутикули (Товар)', 1, 3, 0, 10.00, 50), # ID: 5
    ('Педикюр класичний', 1, 1, 90, 40.00, 1000),      # ID: 6
    ('Денний макіяж', 4, 4, 60, 50.00, 1000),          # ID: 7
    ('Чистка обличчя', 5, 4, 75, 65.00, 1000),         # ID: 8
    ('Корекція бороди', 3, 2, 30, 15.00, 1000),        # ID: 9
    ('Вечірня зачіска', 2, 2, 90, 45.00, 1000),        # ID: 10
    ('Професійний шампунь (Товар)', 2, 3, 0, 22.00, 30),# ID: 11
    ('Французький манікюр', 1, 1, 100, 30.00, 1000)    # ID: 12
]
cursor.executemany("INSERT INTO Services (name, master_id, category_id, duration_min, price_usd, stock_quantity) VALUES (?, ?, ?, ?, ?, ?)", services)

customers = [
    ("Олена Ковальчук", "olena@client.com", "+380509876543", "Київ, вул. Шевченка, 5"), # ID: 1
    ("Віктор Приходько", "viktor@client.com", "+380671234567", "Львів, просп. Свободи, 1"),# ID: 2
    ("Катерина Бондаренко", "kate@example.com", "+380991112233", "Одеса, вул. Дерибасівська, 10"),# ID: 3
    ("Михайло Івасюк", "mykhailo@example.com", "+380934445566", "Чернівці, вул. Головна, 25")# ID: 4
]
cursor.executemany("INSERT INTO Customers (name, email, phone, address) VALUES (?, ?, ?, ?)", customers)

orders = [
    (1, date(2025, 11, 5).isoformat(), "виконане", 0), # ID: 1
    (2, date(2025, 11, 6).isoformat(), "нове", 0),     # ID: 2
    (3, date(2025, 11, 7).isoformat(), "нове", 0),     # ID: 3
    (4, date(2025, 11, 4).isoformat(), "скасоване", 0),# ID: 4
    (1, date(2025, 11, 8).isoformat(), "підтверджене", 0) # ID: 5
]
cursor.executemany("INSERT INTO Orders (customer_id, order_date, status, total_price) VALUES (?, ?, ?, ?)", orders)

order_items = [
    # Замовлення 1 (виконане)
    (1, 1, 1, 25.00, 25.00),
    (1, 5, 2, 10.00, 20.00),
    # Замовлення 2 (нове)
    (2, 4, 1, 20.00, 20.00),
    # Замовлення 3 (нове)
    (3, 7, 1, 50.00, 50.00),
    (3, 8, 1, 65.00, 65.00),
    # Замовлення 4 (скасоване)
    (4, 2, 1, 35.00, 35.00),
    # Замовлення 5 (підтверджене)
    (5, 10, 1, 45.00, 45.00),
    (5, 11, 1, 22.00, 22.00)
]
cursor.executemany("INSERT INTO OrderItems (order_id, service_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)", order_items)

for order_id in range(1, len(orders) + 1):
    cursor.execute(f"UPDATE Orders SET total_price = (SELECT SUM(subtotal) FROM OrderItems WHERE order_id = {order_id}) WHERE id = {order_id}")

conn.commit()
conn.close()

print("База даних 'beauty_salon.db' успішно створена та заповнена розширеними даними.")
print("Загалом вставлено 3 Майстри, 3 Категорії, 6 Послуг, 2 Клієнти та 2 Замовлення.")
