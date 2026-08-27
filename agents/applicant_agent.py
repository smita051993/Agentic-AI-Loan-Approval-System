#
import os
import json
import asyncio
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from models.schemas import ApplicantProfileResult

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv(override=True)


# --------------------------------------------------
# Claude Client
# --------------------------------------------------
client = AsyncAnthropic(
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
   result = await client.messages.create(
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

   result_text = ""

   for block in result.content:

      if hasattr(block, "text") and block.text:

         result_text += block.text

   
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
 
