import sqlite3
from datetime import datetime

# Connect to our new SaaS billing warehouse database
conn = sqlite3.connect("saas_billing.db")
cursor = conn.cursor()

# Enable Foreign Key enforcement in SQLite (critical for real relational integrity!)
cursor.execute("PRAGMA foreign_keys = ON;")

# TABLE 1: Customers (Who signed up and which marketing channel brought them)
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    signup_channel TEXT NOT NULL,
    country TEXT NOT NULL
)
""")

# TABLE 2: Subscriptions (Which plan they are on and monthly price in USD)
cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    sub_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    plan_tier TEXT NOT NULL,
    monthly_price_usd REAL NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
""")

# TABLE 3: Payments (Actual invoice attempts — succeeded vs. failed charges)
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    sub_id INTEGER NOT NULL,
    amount_usd REAL NOT NULL,
    payment_status TEXT NOT NULL,
    payment_date TEXT NOT NULL,
    FOREIGN KEY (sub_id) REFERENCES subscriptions(sub_id)
)
""")

# Seed realistic SaaS startup records (idempotent with INSERT OR REPLACE)
customers_data = [
    (1, "Acme Cloud AI", "LinkedIn", "USA"),
    (2, "FinFlow Labs", "Google Search", "USA"),
    (3, "ScaleOps Data", "Referral", "UK"),
    (4, "NovaPay Systems", "LinkedIn", "Canada"),
    (5, "PulseMetrics", "Cold Email", "USA"),
    (6, "Veloce Freight", "Google Search", "Germany")
]

subscriptions_data = [
    (101, 1, "Enterprise", 1200.00, "active"),
    (102, 2, "Pro", 450.00, "active"),
    (103, 3, "Enterprise", 1200.00, "past_due"),
    (104, 4, "Starter", 150.00, "cancelled"),
    (105, 5, "Pro", 450.00, "active"),
    (106, 6, "Enterprise", 1200.00, "past_due")
]

payments_data = [
    (5001, 101, 1200.00, "succeeded", "2026-11-01"),
    (5002, 102, 450.00, "succeeded", "2026-11-03"),
    (5003, 103, 1200.00, "failed", "2026-11-05"),
    (5004, 104, 150.00, "succeeded", "2026-10-10"),
    (5005, 105, 450.00, "succeeded", "2026-11-12"),
    (5006, 106, 1200.00, "failed", "2026-11-15")
]

cursor.executemany("INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?)", customers_data)
cursor.executemany("INSERT OR REPLACE INTO subscriptions VALUES (?, ?, ?, ?, ?)", subscriptions_data)
cursor.executemany("INSERT OR REPLACE INTO payments VALUES (?, ?, ?, ?, ?)", payments_data)

conn.commit()
conn.close()

print("SUCCESS: 3-table relational SaaS warehouse (customers -> subscriptions -> payments) built in saas_billing.db!")