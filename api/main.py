from fastapi import FastAPI
from pydantic import BaseModel
from orchestration.graph import loan_graph
app = FastAPI(
   title="Agentic AI Loan Approval System"
)

class LoanApplication(BaseModel):
   applicant_id: str
   name: str
   age: int
   income: float
   credit_score: int
   employment_type: str
   loan_amount: float
   debt_obligations: float

@app.get("/")
def home():
   return {
       "message": "Agentic AI Loan Approval System is running"
   }

@app.post("/loan/apply")
async def apply_loan(application: LoanApplication):
   initial_state = {
       "application": application.model_dump()
   }
   result = await loan_graph.ainvoke(initial_state)
   return {
       "status": "success",
       "result": result
   }