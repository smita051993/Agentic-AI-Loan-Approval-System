from datetime import datetime
import uuid

def compliance_agent(state):
   """
   Compliance & Action Orchestrator Agent
   Responsible for:
   - Taking action based on the final loan decision
   - Generating case ID
   - Recording timestamp
   - Preparing notification information
   - Creating an audit summary
   """
   application = state.get("application", {})
   # Get the final decision
   decision=state["decision"]
   classification = decision.classification
   # Generate Case ID
   case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
   # Timestamp
   timestamp = datetime.now().isoformat()
   # Decide action
   if classification == "APPROVE":
       action_taken = "Loan application approved"
       notification_sent = True
   elif classification == "REJECT":
       action_taken = "Loan application rejected"
       notification_sent = True
   else:
       action_taken = "Loan application sent for manual review"
       notification_sent = True
   # Create summary
   summary = (
       f"Loan application {classification}. "
       f"Action taken: {action_taken}. "
       f"Case ID: {case_id}."
   )
   compliance_result = {
       "action_taken": action_taken,
       "notification_sent": notification_sent,
       "case_id": case_id,
       "timestamp": timestamp,
       "summary": summary
   }
   return {
       "compliance_result": compliance_result
   }