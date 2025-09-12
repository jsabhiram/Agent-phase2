'''
# enhanced_graph.py

This module contains the enhanced graph implementation for the application.

## Imports

- `from langchain.agents import Tool`: Imports the `Tool` class from the `langchain.agents` module.
- `from phase0.doc_parse_old import admin`: Imports the `admin` function from the `phase0.doc_parse_old` module.
- `from search import search`: Imports the `search` function from the `search` module.
- `from compare import decide`: Imports the `decide` function from the `compare` module.
- `from old_report import generate_report`: Imports the `generate_report` function from the `old_report` module.
- `from langgraph.graph import StateGraph`: Imports the `StateGraph` class from the `langgraph.graph` module.
- `from enhanced_state import get_initial_state`: Imports the [get_initial_state](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/enhanced_state.py:38:0-52:5) function from the `enhanced_state` module.
- `import json`: Imports the `json` module.
- `from groq import Groq`: Imports the `Groq` class from the `groq` module.
- `import os`: Imports the `os` module.
- `from dotenv import load_dotenv`: Imports the `load_dotenv` function from the `dotenv` module.
- `from side_bar_hover import get_side,change_side`: Imports the `get_side` and `change_side` functions from the `side_bar_hover` module.
- `from slider_value import get_value,send_value,semaphore`: Imports the `get_value`, `send_value`, and `semaphore` functions from the `slider_value` module.
- `import time`: Imports the `time` module.
- `from risk_data import organize`: Imports the `organize` function from the `risk_data` module.

## Global Variables

- [rebundant](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/enhanced_graph.py:17:0-22:19): A global variable used to track the state of the [rebundant](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/enhanced_graph.py:17:0-22:19) flag.

## Functions

- [change_rebundant()](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/enhanced_graph.py:17:0-22:19): A function that toggles the value of the [rebundant](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/enhanced_graph.py:17:0-22:19) flag.
- [check_product(state, product)](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/enhanced_graph.py:25:0-26:8): A function that checks a product in the given state.
- [get_tools()](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/enhanced_graph.py:135:0-136:16): A function that returns a list of tools.

## Classes

- `GroqDecisionAgent`: A class that represents the Groq decision agent.

## Initialization

- `groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))`: Initializes the `groq_client` variable with the Groq client using the API key from the environment variables.

## Dependencies

- `langchain.agents`: A module that provides the `Tool` class.
- `phase0.doc_parse_old`: A module that provides the `admin` function.
- `search`: A module that provides the `search` function.
- `compare`: A module that provides the `decide` function.
- `old_report`: A module that provides the `generate_report` function.
- `langgraph.graph`: A module that provides the `StateGraph` class.
- `enhanced_state`: A module that provides the [get_initial_state](cci:1://file:///c:/Users/jsabh/OneDrive/Desktop/Agent-phase2/enhanced_state.py:38:0-52:5) function.
- `json`: A built-in Python module for working with JSON data.
- `groq`: A module that provides the `Groq` class.
- `os`: A built-in Python module for working with the operating system.
- `dotenv`: A module that provides the `load_dotenv` function for loading environment variables from a `.env` file.
- `side_bar_hover`: A module that provides the `get_side` and `change_side` functions.
- `slider_value`: A module that provides the `get_value`, `send_value`, and `semaphore` functions.
- `risk_data`: A module that provides the `organize` function.
'''

from langchain.agents import Tool
from phase0.doc_parse_old import admin
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
from slider_value import get_value,send_value,semaphore
import time
from risk_data import organize
rebundant=0
def change_rebundant():
    global rebundant
    if (rebundant==0):
        rebundant=1
    else:
        rebundant=0
# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def check_product(state, product):
    pass
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
        global rebundant
        print(state['pending_products'])
        if not state["pending_products"]:
            return state
            
        pre_product = state["pending_products"].pop(0)
        # print("🔎🔎🔎🔎🔎Debugging",product)
        
        product=organize(pre_product)
        print(product['risk'])
        if product['risk']<2:
            print("🔎🔎🔎🔎🔎Debugging",product)
            print(f"🔍 Processing: {product['itemname'][:22:]}")
            #do nothing but just log
            try:
                prices = search(product["itemname"])
                print("Debug prices:", prices)
                anomaly = decide(product, prices)
                state["results"].append({
                "product": product["itemname"],
                "invoice_price": product["price"],
                "market_prices": prices,
                "anomaly": anomaly,
                "risk": product["risk"],
                "status": "success_low_risk_warning",
                "warning_details": f"Low risk warning ignored: {product['risk_details']}"
            })
                print(f"✅ Successfully processed with low risk warning: {product['itemname']}")
            except Exception as e:
                print(f"❌ Failed to process {product['itemname']}: {e}")
                state["failed_once"].append(product)
            return state
        
        elif product['risk']>=2 and product['risk']<4:
            
            send_value(True,"Medium Warning triggered for "+product['itemname'][:10:],product['risk_details'])
            
            while semaphore():
                print(' Waiting for user response🤖')
                print(semaphore())
                time.sleep(2)
                pass
            if rebundant==1:
                print("Product rejected")
                rebundant=0
                state["results"].append({
                "product": product["itemname"],
                "invoice_price": product["price"],
                "market_prices": {},  # No market prices since not processed
                "anomaly": "PRODUCT_REMOVED_BY_USER",
                "risk": product["risk"],
                "status": "removed_high_risk"
})
                return state
            print("🔎🔎🔎🔎🔎Debugging",product)
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


            
        else:
            removal_log = {
            "product_name": product["itemname"],
            "invoice_price": product["price"],
            "risk_level": product["risk"],
            "removal_reason": "High risk product automatically removed",
            "risk_details": product["risk_details"],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action_taken": "Product removed from processing queue"
        }
            state["error_log"].append(f"HIGH RISK REMOVAL: {product['itemname']} - Risk Level {product['risk']} - {product['risk_details']}")

            state["results"].append({
            "product": product["itemname"],
            "invoice_price": product["price"],
            "market_prices": {},  # No market prices since not processed
            "anomaly": "PRODUCT_REMOVED_HIGH_RISK",
            "risk": product["risk"],
            "status": "removed_high_risk",
            "removal_details": removal_log
        })
            print(f"🗑️  Product {product['itemname']} removed due to high risk (Level {product['risk']})")
            print(f"   Reason: {product['risk_details']}")
            return state
        


        # product['risk']=3    
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