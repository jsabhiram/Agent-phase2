import os
import json
from groq import Groq

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class GroqDecisionAgent:
    # Default to llama-3.1-8b-instant
    def __init__(self, model_name="llama-3.1-8b-instant"):
        self.model_name = model_name
        self.client = groq_client
    
    def analyze_state_and_decide(self, state, current_node=None):
        """Use Groq Llama to analyze current state and decide next action"""
        
        # Prepare state summary for the LLM
        state_summary = {
            "current_node": current_node,
            "invoice_data_available": bool(state.get("invoice_data")),
            "pending_products_count": len(state.get("pending_products", [])),
            "failed_once_count": len(state.get("failed_once", [])),
            "failed_final_count": len(state.get("failed_final", [])),
            "results_count": len(state.get("results", [])),
            "has_final_report": bool(state.get("final_report"))
        }
        
        # Create detailed prompt for decision making
        prompt = f"""
You are an intelligent workflow coordinator for an invoice processing system. 
Analyze the current state and decide the next best action.
All prices has to be in INR (Indian Rupees).

Current State:
{json.dumps(state_summary, indent=2)}

Available Actions:
1. "extract" - Extract products from invoice (use when no invoice data exists)
2. "process_product" - Process next product from pending list
3. "retry_failed" - Retry products that failed once
4. "process_retry" - Process products in retry queue
5. "report" - Generate final report
6. "continue_processing" - Continue with current processing loop
7. "skip_to_retry" - Skip to retry phase if too many failures

Decision Rules:
- If no invoice data exists, choose "extract"
- If pending products exist and failure rate is low, choose "process_product" 
- If pending products are empty but failed_once has items, choose "retry_failed"
- If retry queue has items, choose "process_retry"
- If all processing is complete, choose "report"
- Consider failure patterns and efficiency

Respond with just the action name and a brief reason.
Format: ACTION: [action_name] | REASON: [brief explanation]
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a workflow decision engine. Be concise and decisive."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=100
            )
            
            # Extract decision text
            if response.choices and response.choices[0].message and response.choices[0].message.content:
                decision_text = response.choices[0].message.content.strip()
            else:
                print("⚠️ No content returned from Groq API")
                return self._fallback_decision(state), "No response from API"
            
            # Parse the decision
            if "ACTION:" in decision_text:
                action = decision_text.split("ACTION:")[1].split("|")[0].strip()
                reason = decision_text.split("REASON:")[1].strip() if "REASON:" in decision_text else "No reason provided"
                
                print(f"🤖 Groq Decision: {action} - {reason}")
                return action, reason
            else:
                print(f"🤖 Groq Raw Response: {decision_text}")
                return self._fallback_decision(state), "Fallback decision used"
                
        except Exception as e:
            print(f"❌ Groq API Error: {e}")
            return self._fallback_decision(state), "Error occurred, using fallback"
    
    def _fallback_decision(self, state):
        """Fallback decision logic when Groq is unavailable"""
        if not state.get("invoice_data"):
            return "extract"
        elif state.get("pending_products"):
            return "process_product"
        elif state.get("failed_once"):
            return "retry_failed"
        else:
            return "report"


# ==========================
# ✅ TESTING BLOCK
# ==========================
if __name__ == "__main__":
    # Example test states
    test_states = [
        {
            "name": "No invoice data (should extract)",
            "state": {
                "invoice_data": None,
                "pending_products": [],
                "failed_once": [],
                "failed_final": [],
                "results": [],
                "final_report": None
            }
        },
        {
            "name": "Pending products (should process_product)",
            "state": {
                "invoice_data": {"id": "INV123"},
                "pending_products": ["item1", "item2"],
                "failed_once": [],
                "failed_final": [],
                "results": [],
                "final_report": None
            }
        },
        {
            "name": "Failed once (should retry_failed)",
            "state": {
                "invoice_data": {"id": "INV456"},
                "pending_products": [],
                "failed_once": ["item3"],
                "failed_final": [],
                "results": [],
                "final_report": None
            }
        },
        {
            "name": "All done (should report)",
            "state": {
                "invoice_data": {"id": "INV789"},
                "pending_products": [],
                "failed_once": [],
                "failed_final": [],
                "results": ["done"],
                "final_report": "Report ready"
            }
        }
    ]

    agent = GroqDecisionAgent(model_name="llama-3.1-8b-instant")

    for case in test_states:
        print(f"\n=== Running Test: {case['name']} ===")
        action, reason = agent.analyze_state_and_decide(case["state"], current_node="test_node")
        print(f"Action: {action}")
        print(f"Reason: {reason}")
