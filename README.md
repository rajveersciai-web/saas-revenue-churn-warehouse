# 📊 SaaS Revenue & Customer Churn Warehouse

A multi-table relational SQL and Python data engineering pipeline designed to track SaaS Monthly Recurring Revenue (MRR), marketing channel attribution, and failed-payment churn risks.

## 🏗️ Architecture & Pipeline Stages
* **`step1_build_warehouse.py`**: Builds a normalized 3-table SQLite warehouse (`customers` -> `subscriptions` -> `payments`) with `PRAGMA foreign_keys = ON` and parameterized SQL inserts.
* **`step2_mrr_churn_analytics.py`**: Executes multi-table `INNER JOIN` queries to calculate Active MRR (`$2,100/mo`), revenue by acquisition channel, and high-priority churn alerts (`$2,400/mo` at risk from failed Enterprise payments).
* **`step3_quality_check.py`**: Automated data quality gatekeeper using `LEFT JOIN` orphan detection and `assert` checks to verify referential and pricing integrity.

## ▶️ Quick Start
```bash
python step1_build_warehouse.py
python step2_mrr_churn_analytics.py
python step3_quality_check.py
```
