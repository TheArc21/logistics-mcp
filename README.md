# logistics-mcp

A supply chain analytics tool built on MCP (Model Context Protocol) that enables natural language querying of a real logistics database. Ask questions about carrier performance, warehouse efficiency, shipping delays, and customer order volumes — and get live answers from structured SQL data.

Built as a portfolio project to demonstrate AI tool integration, SQL analytics, and Python development skills relevant to Product Analyst and Data Analyst roles.

---

## What This Project Demonstrates

- **MCP architecture** — building a custom AI tool server from scratch using Anthropic's Model Context Protocol
- **SQL analytics** — querying a normalized 7-table relational database with JOINs and aggregations
- **Supply chain domain knowledge** — carrier performance, warehouse capacity, shipment delays, freight routing
- **Python async programming** — asyncio-based client-server communication over stdio transport
- **End-to-end data pipeline** — raw Excel → SQLite → MCP tools → interactive CLI

---

## The Dataset

**Source:** Brunel University London — Supply Chain Logistics Problem Dataset  
**Size:** 9,215 orders across 7 relational tables  
**Coverage:** Orders, freight rates, warehouse capacities, warehouse costs, plant-port mappings, product-plant assignments, VMI customers

| Table | Rows | Description |
|-------|------|-------------|
| orderlist | 9,215 | Core fact table — orders, carriers, ports, quantities, delays |
| freightrates | 1,540 | Carrier rates by lane, weight band, and service level |
| whcapacities | 19 | Daily order capacity per warehouse |
| whcosts | 19 | Cost per unit for each warehouse |
| productsperplant | 2,036 | Warehouse-product support matrix |
| plantports | 22 | Warehouse to shipping port mappings |
| vmicustomers | 14 | Special warehouse-customer restrictions |

---

## Key Insights Surfaced

- **V444_0** handles 68% of all orders (6,264 of 9,215) and accounts for 183 late shipments — the dominant carrier and primary delay risk
- **PORT04** processes 98% of shipments (9,041 of 9,215) — a single point of failure in the network
- **PLANT16 and PLANT18** have the highest cost/unit despite mid-range capacity — candidates for cost optimization
- **V44_3** has zero late shipments across 854 orders — highest reliability carrier in the network

---

## MCP Tools

| Tool | What it does |
|------|-------------|
| `get_carrier_performance` | Total orders, average delay days, and late shipment count per carrier |
| `get_delayed_orders` | Top N orders with worst shipping delays |
| `get_warehouse_summary` | All warehouses with daily capacity and cost per unit |
| `get_top_customers` | Customers ranked by order volume, units, and weight |
| `run_query` | Execute any custom SQL against the database |

---

## Project Structure

```
logistics-mcp/
├── server.py        # MCP server — 5 supply chain analytics tools
├── client.py        # Interactive Python MCP client
├── load_data.py     # One-time ETL script — Excel to SQLite
├── explore.py       # Schema exploration utility
├── data/
│   ├── supply_chain.db                        # SQLite database (7 tables)
│   └── Supply chain logisitcs problem.xlsx    # Source dataset
└── pyproject.toml
```

---

## Setup

**1. Install uv**
```bash
pip install uv
```

**2. Clone and install dependencies**
```bash
git clone https://github.com/TheArc21/logistics-mcp.git
cd logistics-mcp
uv sync
```

**3. Run the interactive client**
```bash
uv run client.py
```

---

## Example Session

```
=== Logistics MCP Client ===

Available tools:
  [run_query] Run any SQL query against the supply chain database
  [get_delayed_orders] Get orders with the worst shipping delays
  [get_carrier_performance] Carrier summary — orders, delays, late shipments
  [get_warehouse_summary] Warehouse capacity and cost per unit
  [get_top_customers] Customers ranked by order volume

Tool: get_carrier_performance

Carrier | total_orders | avg_delay_days | late_shipments
--------------------------------------------------------
V444_0  | 6264         | 0.05           | 183
V444_1  | 2097         | 0.01           | 9
V44_3   | 854          | 0.0            | 0

Tool: query
SQL: SELECT "Origin Port", COUNT(*) as total_orders FROM orderlist
     GROUP BY "Origin Port" ORDER BY total_orders DESC

Origin Port | total_orders
--------------------------
PORT04      | 9041
PORT09      | 173
PORT05      | 1

Tool: quit
Bye!
```

---

## How It Works

1. `load_data.py` reads the Excel file and loads each sheet into a SQLite table
2. `server.py` starts an MCP server exposing 5 analytics tools over stdio transport
3. `client.py` launches the server as a subprocess, performs the MCP handshake, and enters an interactive loop
4. User selects a tool or types custom SQL — results returned live from the database

---

## Related Project

[news-mcp](https://github.com/TheArc21/news-mcp) — Live news feed MCP server using Google News RSS