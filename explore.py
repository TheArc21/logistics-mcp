import sqlite3

conn = sqlite3.connect(r"D:\UTD\MCP_Project\logistics-mcp\data\supply_chain.db")
cursor = conn.cursor()

tables = ["orderlist", "freightrates", "whcosts", "whcapacities"]
for t in tables:
    cursor.execute(f"PRAGMA table_info({t})")
    cols = [row[1] for row in cursor.fetchall()]
    print(f"\n{t}: {cols}")

conn.close()