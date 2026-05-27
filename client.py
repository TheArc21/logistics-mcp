import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def async_input(prompt):
    print(prompt, end="", flush=True)
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sys.stdin.readline)

async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "server.py"],
        cwd=r"D:\UTD\MCP_Project\logistics-mcp"
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("\n=== Logistics MCP Client ===")
            print("\nAvailable tools:")
            for tool in tools.tools:
                print(f"  [{tool.name}] {tool.description}")

            print("\nType a tool name to run it, or 'query' to run custom SQL.")
            print("Type 'quit' to exit.\n")

            while True:
                choice = (await async_input("Tool: ")).strip().lower()

                if choice in ("quit", "exit", "q"):
                    print("Bye!")
                    break

                elif choice == "query":
                    sql = (await async_input("SQL: ")).strip()
                    result = await session.call_tool("run_query", {"sql": sql})
                    print("\n" + result.content[0].text)

                elif choice == "get_delayed_orders":
                    result = await session.call_tool("get_delayed_orders", {"limit": 10})
                    print("\n" + result.content[0].text)

                elif choice == "get_carrier_performance":
                    result = await session.call_tool("get_carrier_performance", {})
                    print("\n" + result.content[0].text)

                elif choice == "get_warehouse_summary":
                    result = await session.call_tool("get_warehouse_summary", {})
                    print("\n" + result.content[0].text)

                elif choice == "get_top_customers":
                    result = await session.call_tool("get_top_customers", {"limit": 10})
                    print("\n" + result.content[0].text)

                else:
                    print("Unknown tool. Available: get_delayed_orders, get_carrier_performance, get_warehouse_summary, get_top_customers, query")

                print()

asyncio.run(asyncio.wait_for(main(), timeout=300))