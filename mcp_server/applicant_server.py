from mcp.server import MCPServer
mcp = MCPServer("ApplicantDB")
APPLICANTS = {
    "AP001": {"name": "John Doe","age": 35,"income": 85000,
        "employment_type": "FULL_TIME","credit_score": 720
    },

    "AP002": {

        "name": "Jane Smith",
        "age": 29, "income": 45000, "employment_type": "CONTRACT", "credit_score": 650
    }
}


@mcp.tool()

def get_applicant(applicant_id: str) -> dict:

    """Retrieve applicant information from ApplicantDB."""

    applicant = APPLICANTS.get(applicant_id)

    if not applicant:

        return {

            "error": "Applicant not found"

        }

    return applicant


if __name__ == "__main__":

    mcp.run()
 