import sqlite3

conn = sqlite3.connect("saas_billing.db")
cursor = conn.cursor()

print("=== RUNNING SAAS WAREHOUSE DATA QUALITY GATES ===\n")

# CHECK 1: Referential Integrity — Zero orphan subscriptions without a valid customer
cursor.execute("""
SELECT COUNT(*)
FROM subscriptions s
LEFT JOIN customers c ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL
""")
orphan_subs = cursor.fetchone()[0]
assert orphan_subs == 0, f"FAIL: Found {orphan_subs} orphan subscriptions with no customer!"
print("[PASS] Check 1 — Referential Integrity: 0 orphan subscriptions found.")

# CHECK 2: Pricing Integrity — Zero $0.00 or negative subscription prices
cursor.execute("SELECT COUNT(*) FROM subscriptions WHERE monthly_price_usd <= 0 OR monthly_price_usd IS NULL")
invalid_prices = cursor.fetchone()[0]
assert invalid_prices == 0, f"FAIL: Found {invalid_prices} invalid subscription prices!"
print("[PASS] Check 2 — Pricing Integrity: All subscription plans have valid positive USD pricing.")

# CHECK 3: Payment Completeness — Every payment maps to a valid subscription
cursor.execute("""
SELECT COUNT(*)
FROM payments p
LEFT JOIN subscriptions s ON p.sub_id = s.sub_id
WHERE s.sub_id IS NULL
""")
orphan_payments = cursor.fetchone()[0]
assert orphan_payments == 0, f"FAIL: Found {orphan_payments} orphan payments!"
print("[PASS] Check 3 — Payment Ledger Integrity: 0 orphan payment records found.")

conn.close()
print("\nALL SAAS QUALITY GATES PASSED: Multi-table billing warehouse verified!")