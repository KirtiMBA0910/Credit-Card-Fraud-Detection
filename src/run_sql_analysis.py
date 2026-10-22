import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "fraud_detection.db")

conn = sqlite3.connect(DB_PATH)

print("\n========== 1. TOTAL TRANSACTIONS ==========")

query1 = """
SELECT COUNT(*) AS total_transactions
FROM credit_card_transactions;
"""

print(pd.read_sql_query(query1, conn))


print("\n========== 2. FRAUD VS GENUINE ==========")

query2 = """
SELECT
    Class,
    COUNT(*) AS transaction_count
FROM credit_card_transactions
GROUP BY Class;
"""

print(pd.read_sql_query(query2, conn))


print("\n========== 3. FRAUD PERCENTAGE ==========")

query3 = """
SELECT
    SUM(CASE WHEN Class = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
    AS fraud_percentage
FROM credit_card_transactions;
"""

print(pd.read_sql_query(query3, conn))


print("\n========== 4. AVERAGE AMOUNT BY CLASS ==========")

query4 = """
SELECT
    Class,
    AVG(Amount) AS average_amount
FROM credit_card_transactions
GROUP BY Class;
"""

print(pd.read_sql_query(query4, conn))


print("\n========== 5. MAXIMUM AMOUNT BY CLASS ==========")

query5 = """
SELECT
    Class,
    MAX(Amount) AS maximum_amount
FROM credit_card_transactions
GROUP BY Class;
"""

print(pd.read_sql_query(query5, conn))


conn.close()

print("\nSQL ANALYSIS COMPLETED SUCCESSFULLY!")