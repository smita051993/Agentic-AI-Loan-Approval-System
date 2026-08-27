# import os
# import json
# from dotenv import load_dotenv
# from anthropic import Anthropic
# from pydantic import BaseModel


# # -----------------------------
# # Loan Application Model
# # -----------------------------

# class LoanApplication(BaseModel):

#     applicant_id: str
#     age: int
#     income: float
#     employment_type: str
#     credit_score: int
#     loan_amount: float
#     loan_tenure: int
#     existing_liabilities: float
#     location: str


# class ApplicantProfileResult(BaseModel):
#    income_stability_score: int
#    employment_risk: str
#    credit_history_summary: str
#    application_complete: bool
#    risk_score: int
#    rationale: str


# # -----------------------------

# # Claude Configuration

# # -----------------------------

# load_dotenv(override=True)

# api_key = os.getenv("ANTHROPIC_API_KEY")

# if not api_key:

#     raise ValueError("ANTHROPIC_API_KEY not found")

# client = Anthropic(api_key=api_key)


# # -----------------------------

# # Sample Application

# # -----------------------------

# application = LoanApplication(

#     applicant_id="APP1001",

#     age=32,

#     income=80000,

#     employment_type="Salaried",

#     credit_score=780,

#     loan_amount=2000000,

#     loan_tenure=10,

#     existing_liabilities=10000,

#     location="Bangalore"

# )


# # -----------------------------
# # Applicant Profile Agent
# # -----------------------------

# def analyze_applicant(application):

#     prompt = f"""

# You are the Applicant Profile Agent

# in an intelligent loan approval system.

# Analyze this loan application:

# {json.dumps(application, indent=2)}

# Evaluate:

# 1. Income stability

# 2. Employment risk

# 3. Credit history

# 4. Application completeness

# 5. Overall applicant profile risk

# Return ONLY valid JSON.

# The JSON MUST contain exactly these fields:

# {{

#     "income_stability_score": 0,

#     "employment_risk": "LOW",

#     "credit_history_summary": "",

#     "application_complete": true,

#     "risk_score": 0,

#     "rationale": ""

# }}

# Rules:

# - income_stability_score must be between 0 and 100.

# - risk_score must be between 0 and 100.

# - employment_risk must be LOW, MEDIUM, or HIGH.

# - application_complete must be true or false.

# - Do not include markdown.

# - Do not include ```json.

# - Do not make the final loan decision.

# - Only analyze the applicant profile.

# """
 
#     response = client.messages.create(

#         model="claude-sonnet-4-6",

#         max_tokens=500,

#         messages=[

#             {
#                 "role": "user",
#                 "content": prompt
#             }

#         ]

#     )

#     result= response.content[0].text
#     return ApplicantProfileResult.model_validate_json(result)


# # -----------------------------
# # Run
# # -----------------------------

# if __name__ == "__main__":

#     result = analyze_applicant(application)
#     print("\n===== APPLICANT PROFILE AGENT =====")
#     print(result)
#     print("\n===== AS DICTIONARY =====")
#     print(result.model_dump())



import os
import json
import asyncio
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv(override=True)

# --------------------------------------------------
# Applicant Models
# --------------------------------------------------
class ApplicantProfileResult(BaseModel):
   income_stability_score: int
   employment_risk: str
   credit_history_summary: str
   application_complete: bool
   risk_score: int
   rationale: str

# --------------------------------------------------
# Claude Client
# --------------------------------------------------
client = Anthropic(
   api_key=os.getenv("ANTHROPIC_API_KEY")
)

# --------------------------------------------------
# Applicant Agent
# --------------------------------------------------
async def analyze_applicant(state):
   # --------------------------------------------------
   # 1. Start Applicant MCP Server
   # --------------------------------------------------
   server_params = StdioServerParameters(
       command="python",
       args=["mcp_server/applicant_server.py"],
       env=os.environ.copy()
   )
   # --------------------------------------------------
   # 2. Connect to MCP Server
   # --------------------------------------------------
   async with stdio_client(server_params) as (read, write):
       async with ClientSession(read, write) as session:
           # Initialize MCP connection
           await session.initialize()
           # --------------------------------------------------
           # 3. Call MCP Tool
           # --------------------------------------------------
           application = state["application"]
           response = await session.call_tool(
            "get_applicant",
            arguments={
               "applicant_id": application["applicant_id"]
            }
         )
           
           # --------------------------------------------------
           # 4. Extract Applicant Data
           # --------------------------------------------------
           applicant_data = response.content[0].text
           applicant = json.loads(applicant_data)

           # --------------------------------------------------
           # 5. Create Prompt for Claude
           # --------------------------------------------------
           prompt = f"""
 You are the Applicant Profile Agent in an intelligent loan
 approval system.
 Analyze the following applicant information:
 {json.dumps(applicant, indent=2)}
 Evaluate:
 1. Income stability
 2. Employment risk
 3. Credit history
 4. Whether the application is complete
 5. Overall applicant risk score from 0 to 100
 6. Give a short rationale
 Return ONLY valid JSON in exactly this format:
 {{
    "income_stability_score": 0,
    "employment_risk": "LOW",
    "credit_history_summary": "",
    "application_complete": true,
    "risk_score": 0,
    "rationale": ""
 }}
 """
   # --------------------------------------------------
   # 6. Call Claude
   # --------------------------------------------------
   result = client.messages.create(
                 model="claude-sonnet-4-6",
                 max_tokens=500,
                 messages=[
                     {
                         "role": "user",
                         "content": prompt
                     }
                 ]
             )
   # --------------------------------------------------
   # 7. Get Claude Response
   # --------------------------------------------------
   # result_text = result.content[0].text
   # print("\n===== CLAUDE RAW RESPONSE =====")
   # print(repr(result_text))
   # --------------------------------------------------
   # 8. Convert Claude JSON → Pydantic Model
   # --------------------------------------------------
   # result_json = json.loads(result_text)
   # applicant_result = ApplicantProfileResult.model_validate(result_json)
   # return applicant_result

   # --------------------------------------------------

# 7. Get Claude Response

# --------------------------------------------------

   result_text = ""

   for block in result.content:

      if hasattr(block, "text") and block.text:

         result_text += block.text

   # print("\n===== CLAUDE RAW RESPONSE =====")

   # print(repr(result_text))

   # --------------------------------------------------

   # 8. Clean Claude JSON

   # --------------------------------------------------

   result_text = result_text.strip()

   if not result_text:

      raise ValueError("Claude returned an empty response")

   # Remove ```json and ``` if Claude added them

   if result_text.startswith("```json"):

      result_text = result_text[len("```json"):].strip()

   if result_text.endswith("```"):

      result_text = result_text[:-3].strip()

   # print("\n===== CLEAN JSON =====")

   # print(repr(result_text))

   # --------------------------------------------------

   # 9. Convert Claude JSON → Pydantic Model

   # --------------------------------------------------

   result_json = json.loads(result_text)

   applicant_result = ApplicantProfileResult.model_validate(

      result_json

   )

   return applicant_result
 

# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":
   result = asyncio.run(
       analyze_applicant()
   )
   print("\n===== APPLICANT PROFILE AGENT RESULT =====")
   print(result.model_dump_json(indent=2))
 