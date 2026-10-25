"""Simulate an MCP client connecting over STDIO to test tools and record transcripts."""
import asyncio
import json
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = str(Path(__file__).parent / "server.py")
PYTHON_BIN = str(Path(__file__).parent / ".venv" / "bin" / "python")


async def run_client_simulation():
    server_params = StdioServerParameters(
        command=PYTHON_BIN,
        args=[SERVER_SCRIPT],
    )

    transcript = []
    print("Connecting to Data Explorer MCP server over STDIO...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Initialize
            init_res = await session.initialize()
            print("Server initialized:", init_res.serverInfo.name)
            transcript.append({
                "step": "initialize",
                "server": init_res.serverInfo.name,
                "version": init_res.serverInfo.version
            })

            # 2. List tools
            tools = await session.list_tools()
            tool_names = [t.name for t in tools.tools]
            print("Available tools:", tool_names)
            transcript.append({
                "step": "list_tools",
                "tools": tool_names
            })

            # 3. Call search_countries (normal)
            query1 = "turkey"
            res1 = await session.call_tool("search_countries", arguments={"query": query1, "limit": 2})
            content1 = json.loads(res1.content[0].text)
            print(f"Call search_countries('{query1}'):", content1)
            transcript.append({
                "step": "call_tool",
                "tool": "search_countries",
                "arguments": {"query": query1, "limit": 2},
                "result": content1
            })

            # 4. Call get_country_details (normal)
            country_name = "Germany"
            res2 = await session.call_tool("get_country_details", arguments={"name": country_name})
            content2 = json.loads(res2.content[0].text)
            print(f"Call get_country_details('{country_name}'):", content2)
            transcript.append({
                "step": "call_tool",
                "tool": "get_country_details",
                "arguments": {"name": country_name},
                "result": content2
            })

            # 5. Call search_countries with empty query (error handling)
            res3 = await session.call_tool("search_countries", arguments={"query": ""})
            content3 = json.loads(res3.content[0].text)
            print("Call search_countries(''):", content3)
            transcript.append({
                "step": "call_tool",
                "tool": "search_countries",
                "arguments": {"query": ""},
                "result": content3
            })

            # 6. Call get_country_details with nonexistent country (error handling)
            invalid_name = "AtlantisCity99"
            res4 = await session.call_tool("get_country_details", arguments={"name": invalid_name})
            content4 = json.loads(res4.content[0].text)
            print(f"Call get_country_details('{invalid_name}'):", content4)
            transcript.append({
                "step": "call_tool",
                "tool": "get_country_details",
                "arguments": {"name": invalid_name},
                "result": content4
            })

    output_path = Path(__file__).parent / "mcp_client_transcript.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, indent=2, ensure_ascii=False)
    print(f"Transcript written to {output_path}")


if __name__ == "__main__":
    asyncio.run(run_client_simulation())
