import sqlite3
from mcp.server.fastmcp import FastMCP

DB_PATH = r"D:\UTD\MCP_Project\logistics-mcp\data\supply_chain.db"

mcp = FastMCP("logistics-server")

def query_db(sql: str) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def format_results(rows: list[dict]) -> str:
    if not rows:
        return "No results found."
    headers = list(rows[0].keys())
    lines = [" | ".join(headers)]
    lines.append("-" * len(lines[0]))
    for row in rows:
        lines.append(" | ".join(str(row[h]) for h in headers))
    return "\n".join(lines)

@mcp.tool()
def run_query(sql: str) -> str:
    """Run any SQL query against the supply chain database and return results."""
    try:
        rows = query_db(sql)
        return format_results(rows)
    except Exception as e:
        return f"Query error: {str(e)}"

@mcp.tool()
def get_delayed_orders(limit: int = 10) -> str:
    """Get orders with the worst shipping delays, sorted by delay days descending."""
    sql = f"""
        SELECT "Order ID", "Carrier", "Origin Port", "Destination Port",
               "Customer", "Ship Late Day count"
        FROM orderlist
        WHERE "Ship Late Day count" > 0
        ORDER BY "Ship Late Day count" DESC
        LIMIT {limit}
    """
    rows = query_db(sql)
    return format_results(rows)

@mcp.tool()
def get_carrier_performance() -> str:
    """Get summary of each carrier — total orders, average delay, and late shipment count."""
    sql = """
        SELECT "Carrier",
               COUNT(*) as total_orders,
               ROUND(AVG("Ship Late Day count"), 2) as avg_delay_days,
               SUM(CASE WHEN "Ship Late Day count" > 0 THEN 1 ELSE 0 END) as late_shipments
        FROM orderlist
        GROUP BY "Carrier"
        ORDER BY late_shipments DESC
    """
    rows = query_db(sql)
    return format_results(rows)

@mcp.tool()
def get_warehouse_summary() -> str:
    """Get all warehouses with their daily capacity and cost per unit."""
    sql = """
        SELECT wc."Plant ID", wc."Daily Capacity ", wh."Cost/unit"
        FROM whcapacities wc
        LEFT JOIN whcosts wh ON wc."Plant ID" = wh."WH"
        ORDER BY wc."Daily Capacity " DESC
    """
    rows = query_db(sql)
    return format_results(rows)

@mcp.tool()
def get_top_customers(limit: int = 10) -> str:
    """Get customers ranked by total order volume and total weight shipped."""
    sql = f"""
        SELECT "Customer",
               COUNT(*) as total_orders,
               SUM("Unit quantity") as total_units,
               ROUND(SUM("Weight"), 2) as total_weight
        FROM orderlist
        GROUP BY "Customer"
        ORDER BY total_orders DESC
        LIMIT {limit}
    """
    rows = query_db(sql)
    return format_results(rows)

if __name__ == "__main__":
    mcp.run()