import asyncio
from agents.compliance_agent import compliance_agent


async def main():

    state = {
        "application": {
            "applicant_id": "AP002"
        },

        "decision": type(
            "Decision",
            (),
            {"classification": "APPROVE"}
        )()
    }

    result = await compliance_agent(state)

    print("\n===== COMPLIANCE AGENT RESULT =====")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())