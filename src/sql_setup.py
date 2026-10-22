import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_PATH = os.path.join(BASE_DIR, "data", "creditcard.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "fraud_detection.db")

print("Loading dataset...")

df = pd.read_csv(CSV_PATH)

print("Dataset loaded!")
print("Rows:", len(df))
print("Columns:", len(df.columns))

conn = sqlite3.connect(DB_PATH)

df.to_sql(
    "credit_card_transactions",
    conn,
    if_exists="replace",
    index=False
)

print("Data successfully loaded into SQLite database!")

result = pd.read_sql_query(
    "SELECT COUNT(*) AS total_transactions FROM credit_card_transactions",
    conn
)

print("\nTotal Transactions:")
print(result)

conn.close()

print("\nSQL database created successfully!")