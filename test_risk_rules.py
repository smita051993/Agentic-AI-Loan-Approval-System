import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/risk_rules_server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            # See available tools
            tools = await session.list_tools()

            print("Available tools:")

            for tool in tools.tools:
                print(tool.name)

            # Call risk rules tool
            result = await session.call_tool(
                "get_risk_rules",
                arguments={}
            )

            print("\nRisk Rules Result:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())