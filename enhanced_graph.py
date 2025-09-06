from langchain.agents import Tool
from doc_parse import admin
from search import search
from compare import decide
from report import generate_report
from langgraph.graph import StateGraph
from enhanced_state import get_initial_state
import json
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
from side_bar_hover import get_side,change_side
from slider_value import get_value
import time
# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class GroqDecisionAgent:
    # llama-3.1-8b-instant
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
All prices has to be in INR(Indian Rupees).

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
            
            # decision_text = response.choices[0].message.content.strip()
            if response.choices and response.choices[0].message and response.choices[0].message.content:
                decision_text = response.choices[0].message.content.strip()
    # ... rest of your code ...
            else:
                print("No content returned from Groq API")
    # ... handle the case where no content is returned ...
            
            
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

# Initialize the decision agent
decision_agent = GroqDecisionAgent()

tools = [
    Tool(name="ExtractInvoice", func=admin, description="Extracts products from invoice"),
    Tool(name="SearchPrices", func=search, description="Finds product prices online"),
    Tool(name="ComparePrices", func=decide, description="Compares invoice and market prices"),
    Tool(name="GenerateReport", func=generate_report, description="Generates a report on price anomalies"),
    Tool(name="HumanDecision", func=decision_agent.analyze_state_and_decide, description="Decides the maximum price deviation permittable")
]

def get_tools():
    return tools

def run_graph(state):
    print("🚀 Starting intelligent workflow with Groq Llama decision making...")
    
    def extract_node(state):
        print("📄 Extracting invoice data...")
        result = admin(state["input_file_path"])
        state["invoice_data"] = {"products": result}
        if(state["invoice_data"]!="no useful invoice data found"):
            
            #show the side bar now
       
            print(get_side())
            change_side()
            print(get_side())
            while(get_value()==None):
                print("Waiting for user to set variation!🐱‍💻")
                time.sleep(1)
            print("Value recieved",get_value())
            change_side()

        state["pending_products"] = result
        
        print(f"✅ Extracted {len(result)} products")
        return state

    def process_product_node(state):
        print(state['pending_products'])
        if not state["pending_products"]:
            return state
            
        product = state["pending_products"].pop(0)
        print(f"🔍 Processing: {product['itemname'][:22:]}")
        
        try:
            prices = search(product["itemname"])
            print("Debug prices:", prices)
            anomaly = decide(product, prices)
            state["results"].append({
                "product": product["itemname"],
                "invoice_price": product["price"],
                "market_prices": prices,
                "anomaly": anomaly,
                "status": "success"
            })
            print(f"✅ Successfully processed: {product['itemname']}")
        except Exception as e:
            print(f"❌ Failed to process {product['itemname']}: {e}")
            state["failed_once"].append(product)
        
        return state

    def retry_failed_node(state):
        print(f"🔄 Preparing to retry {len(state['failed_once'])} failed products...")
        state["pending_products"] = state["failed_once"].copy()
        state["failed_once"] = []
        return state

    def process_failed_retry_node(state):
        if not state["pending_products"]:
            return state
            
        product = state["pending_products"].pop(0)
        print(f"🔄 Retrying: {product['itemname']}")
        
        try:
            prices = search(product["itemname"])
            invoice_entry = f"{product['itemname']} {product['price']}"
            benchmark_entry = f"{product['itemname']} {prices}"
            anomaly = decide(invoice_entry, benchmark_entry)
            
            state["results"].append({
                "product": product["itemname"],
                "invoice_price": product["price"],
                "market_prices": prices,
                "anomaly": anomaly,
                "status": "retry_success"
            })
            print(f"✅ Retry successful: {product['itemname']}")
        except Exception as e:
            print(f"❌ Retry failed: {product['itemname']}: {e}")
            state["failed_final"].append(product)
        
        return state

    def report_node(state):
        print("📊 Generating final report...")
        state["final_report"]= generate_report(state)
        #  = final_report
        print(state['final_report'])
        print("✅ Report generated successfully")
        return state

    # Intelligent routing functions using Groq
    def smart_route_from_extract(state):
        action, reason = decision_agent.analyze_state_and_decide(state, "extract")
        return "process_product" if action == "process_product" else "process_product"

    def smart_route_from_process(state):
        action, reason = decision_agent.analyze_state_and_decide(state, "process_product")
        
        if action == "continue_processing" and state["pending_products"]:
            return "process_product"
        elif action == "retry_failed" or (not state["pending_products"] and state["failed_once"]):
            return "retry_failed"
        elif action == "report" or (not state["pending_products"] and not state["failed_once"]):
            return "report"
        else:
            # Default logic with LLM insight
            return "process_product" if state["pending_products"] else "retry_failed"

    def smart_route_from_retry(state):
        action, reason = decision_agent.analyze_state_and_decide(state, "retry_failed")
        return "process_retry"

    def smart_route_from_process_retry(state):
        action, reason = decision_agent.analyze_state_and_decide(state, "process_retry")
        
        if action == "continue_processing" and state["pending_products"]:
            return "process_retry"
        elif action == "report" or not state["pending_products"]:
            return "report"
        else:
            return "process_retry" if state["pending_products"] else "report"

    # Build the graph with intelligent routing
    graph = StateGraph(dict)

    graph.add_node("extract", extract_node)
    graph.add_node("process_product", process_product_node)
    graph.add_node("retry_failed", retry_failed_node)
    graph.add_node("process_retry", process_failed_retry_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("extract")

    # Add intelligent edges
    graph.add_edge("extract", "process_product")
    
    graph.add_conditional_edges(
        "process_product",
        smart_route_from_process
    )
    
    graph.add_conditional_edges(
        "retry_failed",
        smart_route_from_retry
    )
    
    graph.add_conditional_edges(
        "process_retry",
        smart_route_from_process_retry
    )
    
    graph.set_finish_point("report")

    # Compile and run
    compiled = graph.compile()
    
    print("🧠 Graph compiled with Groq Llama intelligence")
    return compiled.invoke(state)


# Enhanced state monitoring
def monitor_workflow_progress(state):
    """Monitor and log workflow progress"""
    progress = {
        "total_products": len(state.get("invoice_data", {}).get("products", [])),
        "processed_successfully": len([r for r in state.get("results", []) if r["status"] == "success"]),
        "retry_successes": len([r for r in state.get("results", []) if r["status"] == "retry_success"]),
        "pending": len(state.get("pending_products", [])),
        "failed_once": len(state.get("failed_once", [])),
        "failed_final": len(state.get("failed_final", [])),
        "completion_rate": 0.0
    }
    
    if progress["total_products"] > 0:
        progress["completion_rate"] = (progress["processed_successfully"] + progress["retry_successes"]) / progress["total_products"] * 100
    
    print(f"📈 Progress: {progress['completion_rate']:.1f}% complete")
    print(f"   ✅ Success: {progress['processed_successfully']}, 🔄 Retry Success: {progress['retry_successes']}")
    print(f"   ⏳ Pending: {progress['pending']}, ❌ Failed: {progress['failed_final']}")
    
    return progress


if __name__ == "__main__":
    # Make sure to set your Groq API key
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  Warning: GROQ_API_KEY not found in environment variables")
        print("   Please set your Groq API key: export GROQ_API_KEY='your_api_key_here'")
    
    state = get_initial_state("uploads\\OD328509323961361100.pdf")
    
    # Add progress monitoring
    state["monitor"] = True
    
    result = run_graph(state)
    
    # Final progress report
    print("\n🎉 Workflow Complete!")
    final_progress = monitor_workflow_progress(result)
    
    if result.get("final_report"):
        print(f"\n📋 Final Report Generated: {len(result['final_report'])} characters")