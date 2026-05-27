import asyncio
import sys
import anthropic
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

            # Get tools from MCP server and convert to Anthropic format
            mcp_tools = await session.list_tools()
            tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                }
                for tool in mcp_tools.tools
            ]

            claude = anthropic.Anthropic()

            print("\n=== Supply Chain NLP Analytics ===")
            print("Ask any question about the logistics data in plain English.")
            print("Type 'quit' to exit.\n")

            while True:
                question = (await async_input("Your question: ")).strip()

                if question.lower() in ("quit", "exit", "q"):
                    print("Bye!")
                    break

                if not question:
                    continue

                messages = [{"role": "user", "content": question}]

                # Agentic loop
                while True:
                    response = claude.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=1000,
                        system="You are a supply chain analyst. You have access to a logistics database with order, carrier, warehouse, and freight data. Answer the user's question using the available tools. Be concise and highlight the most important insight.",
                        tools=tools,
                        messages=messages
                    )

                    if response.stop_reason == "tool_use":
                        messages.append({"role": "assistant", "content": response.content})

                        tool_results = []
                        for block in response.content:
                            if block.type == "tool_use":
                                print(f"  [querying: {block.name}...]")
                                result = await session.call_tool(block.name, block.input)
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": result.content[0].text
                                })

                        messages.append({"role": "user", "content": tool_results})

                    elif response.stop_reason == "end_turn":
                        for block in response.content:
                            if hasattr(block, "text"):
                                print(f"\n{block.text}\n")
                        break

asyncio.run(asyncio.wait_for(main(), timeout=300))