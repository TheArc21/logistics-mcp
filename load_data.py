import pandas as pd
import sqlite3
import os

# Paths
EXCEL_PATH = r"D:\UTD\MCP_Project\logistics-mcp\data\Supply chain logisitcs problem.xlsx"
DB_PATH = r"D:\UTD\MCP_Project\logistics-mcp\data\supply_chain.db"

# Load all sheets
print("Reading Excel file...")
sheets = pd.read_excel(EXCEL_PATH, sheet_name=None)

print(f"Found {len(sheets)} sheets:")
for name, df in sheets.items():
    print(f"  - {name}: {df.shape[0]} rows x {df.shape[1]} columns")

# Load into SQLite
conn = sqlite3.connect(DB_PATH)

for sheet_name, df in sheets.items():
    # Clean table name — lowercase, replace spaces with underscores
    table_name = sheet_name.strip().lower().replace(" ", "_")
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded '{sheet_name}' -> table '{table_name}'")

conn.close()
print(f"\nDatabase saved to: {DB_PATH}")