# logistics-mcp

A natural language supply chain analytics tool built on MCP (Model Context Protocol) and Claude API. Ask plain English questions about carrier performance, warehouse costs, shipping delays, and customer order volumes — and get analyst-quality answers backed by live SQL queries.

> "Which carrier should I avoid for on-time delivery?" → Claude queries the database → returns ranked analysis with a recommendation.

Built as a portfolio project demonstrating NLP-to-SQL architecture, MCP tool integration, and supply chain domain knowledge.

---

## What This Project Demonstrates

- **NLP-to-SQL** — natural language questions translated to live database queries via Claude API agentic loop
- **MCP architecture** — custom AI tool server exposing structured data to LLMs using Anthropic's Model Context Protocol
- **SQL analytics** — multi-table JOIN queries, aggregations, and grouping on a normalized relational database
- **Supply chain domain knowledge** — carrier performance, warehouse capacity, shipment delays, freight routing
- **ETL pipeline** — raw Excel ingested, normalized, and loaded into SQLite across 7 relational tables
- **Python async programming** — asyncio-based MCP client-server communication over stdio transport

---

## How It Works

```
User asks plain English question
        ↓
Claude API receives question + tool definitions
        ↓
Claude decides which tool to call (or writes SQL)
        ↓
MCP client executes tool against SQLite database
        ↓
Raw results returned to Claude
        ↓
Claude generates analyst-quality natural language answer
```

---

## Example Session

```
=== Supply Chain NLP Analytics ===
Ask any question about the logistics data in plain English.

Your question: Which carrier should I avoid for on-time delivery?

  [querying: get_carrier_performance...]

Avoid V444_0 — it has 183 late shipments, accounting for 95%+ of all
late deliveries. V44_3 has a perfect record (0 late shipments across
854 orders) and is the most reliable option.

Your question: Which warehouses are most expensive to operate?

  [querying: get_warehouse_summary...]

PLANT18 is the most expensive at $2.04/unit with only 111 units/day
capacity — poor value. PLANT16 is the bigger concern: $1.92/unit but
457 units/day capacity, making total daily costs significantly high.
Recommend auditing both for consolidation or cost reduction.

Your question: quit
Bye!
```

---

## The Dataset

**Source:** Brunel University London — Supply Chain Logistics Problem Dataset  
**Size:** 9,215 orders across 7 relational tables

| Table | Rows | Description |
|-------|------|-------------|
| orderlist | 9,215 | Orders, carriers, ports, quantities, delays |
| freightrates | 1,540 | Carrier rates by lane and weight band |
| whcapacities | 19 | Daily order capacity per warehouse |
| whcosts | 19 | Cost per unit per warehouse |
| productsperplant | 2,036 | Warehouse-product support matrix |
| plantports | 22 | Warehouse to shipping port mappings |
| vmicustomers | 14 | Special warehouse-customer restrictions |

---

## MCP Tools

| Tool | What it does |
|------|-------------|
| `get_carrier_performance` | Orders, average delay, and late shipment count per carrier |
| `get_delayed_orders` | Top N orders with worst shipping delays |
| `get_warehouse_summary` | Warehouses with daily capacity and cost per unit |
| `get_top_customers` | Customers ranked by order volume, units, and weight |
| `run_query` | Execute any custom SQL — Claude uses this for ad-hoc questions |

---

## Project Structure

```
logistics-mcp/
├── nlp_client.py    # NLP-to-SQL client — plain English → Claude API → MCP tools → answer
├── client.py        # Direct interactive client — tool menu + custom SQL
├── server.py        # MCP server — 5 supply chain analytics tools
├── load_data.py     # ETL script — Excel to SQLite
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

**3. Set your Anthropic API key**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."   # Mac/Linux
$env:ANTHROPIC_API_KEY="sk-ant-..."     # Windows PowerShell
```

**4. Run the NLP client**
```bash
uv run nlp_client.py
```

**Or run the direct tool client (no API key needed)**
```bash
uv run client.py
```

---

## Key Insights from the Data

- **V444_0** handles 68% of orders but accounts for 95%+ of late shipments — primary reliability risk
- **PORT04** processes 98% of all shipments — extreme concentration and single point of failure
- **PLANT18** is the most expensive warehouse ($2.04/unit) with only 111 units/day capacity
- **V44_3** has zero late shipments across 854 orders — most reliable carrier in the network
- **V55555_2** ranks 3rd in order count but ships the most units (1.5M) and heaviest freight (18,717 kg)

---

## Related Project

[news-mcp](https://github.com/TheArc21/news-mcp) — Live news feed MCP server using Google News RSS