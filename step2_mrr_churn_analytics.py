import sqlite3

# Connect to our 3-table SaaS billing warehouse
conn = sqlite3.connect("saas_billing.db")
cursor = conn.cursor()

print("=== EXECUTIVE SAAS REVENUE & CHURN REPORT ===\n")

# QUERY 1: Total Active Monthly Recurring Revenue (MRR)
cursor.execute("""
SELECT COUNT(*), SUM(monthly_price_usd)
FROM subscriptions
WHERE status = 'active'
""")
active_row = cursor.fetchone()
print(f"1. ACTIVE SUBSCRIPTIONS: {active_row[0]} clients | TOTAL ACTIVE MRR: ${active_row[1]:,.2f}/month\n")

# QUERY 2: Revenue Attribution by Marketing Channel (2-Table INNER JOIN)
print("2. ACTIVE MRR BY MARKETING CHANNEL:")
cursor.execute("""
SELECT c.signup_channel, COUNT(s.sub_id) as active_clients, SUM(s.monthly_price_usd) as channel_mrr
FROM customers c
INNER JOIN subscriptions s ON c.customer_id = s.customer_id
WHERE s.status = 'active'
GROUP BY c.signup_channel
ORDER BY channel_mrr DESC
""")
for row in cursor.fetchall():
    print(f" - {row[0]:15} | {row[1]} active client(s) | ${row[2]:,.2f}/mo")

# QUERY 3: Failed Payment & Churn Recovery Alert (3-Table INNER JOIN)
print("\n3. HIGH-PRIORITY CHURN ALERTS (FAILED PAYMENTS ON PAST-DUE ACCOUNTS):")
cursor.execute("""
SELECT c.company_name, c.country, s.plan_tier, s.monthly_price_usd, p.payment_date
FROM customers c
INNER JOIN subscriptions s ON c.customer_id = s.customer_id
INNER JOIN payments p ON s.sub_id = p.sub_id
WHERE s.status = 'past_due' AND p.payment_status = 'failed'
ORDER BY s.monthly_price_usd DESC
""")
at_risk_rows = cursor.fetchall()
total_at_risk = 0.0
for row in at_risk_rows:
    total_at_risk += row[3]
    print(f" - ALERT: {row[0]} ({row[1]}) | {row[2]} Plan | ${row[3]:,.2f}/mo at risk (Failed on {row[4]})")

print(f"\nTOTAL REVENUE AT RISK TO RECOVER: ${total_at_risk:,.2f}/month")

conn.close()