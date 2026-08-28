import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/decision_synthesis_server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")

            for tool in tools.tools:
                print(tool.name)

            result = await session.call_tool(
                "make_loan_decision",
                arguments={
                    "risk_score": 80,
                    "compliance_ok": True,
                    "credit_score": 750
                }
            )

            print("\nResult:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())