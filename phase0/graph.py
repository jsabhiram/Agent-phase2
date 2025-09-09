from langchain.agents import Tool
from phase0.doc_parse_old import admin
from search import search
from compare import decide
from report import generate_report
from langgraph.graph import StateGraph
# from test_llm import Agent
from mdb import get_vendor_names
from phase0.state import get_initial_state
tools = [
    Tool(name="ExtractInvoice", func=admin, description="Extracts products from invoice"),
    Tool(name="SearchPrices", func=search, description="Finds product prices online"),
    Tool(name="ComparePrices", func=decide, description="Compares invoice and market prices"),
    Tool(name="GenerateReport", func=generate_report, description="Generates a report on price anomalies")
]


def get_tools():
    return tools



def run_graph(state):
    print("I will take it from here")
    def extract_node(state):
        result = admin(state["input_file_path"])
        print(result)
        state["invoice_data"] = {"products": result}

        state["pending_products"] =result   #result["products"].copy()
        print(state['invoice_data'])
        print("Something is not here")
        print(state["pending_products"])
        return state

    def process_product_node(state):
        product = state["pending_products"].pop(0)
     
        # print(str(product)+"def process_product_node\n")
        print(product["itemname"])
        try:
            prices = search(product["itemname"])
            anomaly = decide(product, prices)
            state["results"].append({
                "product": product["itemname"],
                "invoice_price": product["price"],
                "market_prices": prices,
                "anomaly": anomaly,
                "status": "success"
            })
        except Exception:
            state["failed_once"].append(product)
        return state

    def retry_failed_node(state):
        # state["pending_products"] = state["failed_once"]
        # state["failed_once"] = []
        state["pending_products"] = state["failed_once"].copy()
        state["failed_once"] = []

        return state

    def process_failed_retry_node(state):
        a=""
        try:
            a=state['pending_products'][0]
            product = state["pending_products"].pop(0)
            
            prices = search(product["itemname"])
            invoice_entry= f"{product['itemname']} {product['price']}"
            benchmark_entry= f"{product['itemname']} {prices}"
            anomaly = decide(invoice_entry, benchmark_entry)
            state["results"].append({
                "product": product["itemname"],
                "invoice_price": product["price"],
                "market_prices": prices,
                "anomaly": anomaly,
                "status": "retry_success"
            })
        except Exception:
            print("Something went wrong")
            state["failed_final"].append(a)
        return state

    def report_node(state):
        final_report = generate_report(state)
        # final_report = generate_report(state["results"], state["failed_final"])

        state["final_report"] = final_report
        return state
    # def flagged(state):
        # stage=state['final_report']
        # stat=get

        # prompt=stage+

    # Build the graph
    graph = StateGraph(dict)

    graph.add_node("extract", extract_node)
    graph.add_node("process_product", process_product_node)
    graph.add_node("retry_failed", retry_failed_node)
    graph.add_node("process_retry", process_failed_retry_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("extract")

    # Main loop: process → retry → re-process → report
    graph.add_edge("extract", "process_product")
    graph.add_conditional_edges(
        "process_product",
        lambda s: "process_product" if s["pending_products"] else "retry_failed"
    )
    graph.add_edge("retry_failed", "process_retry")
    graph.add_conditional_edges(
        "process_retry",
        lambda s: "process_retry" if s["pending_products"] else "report"
    )
    graph.set_finish_point("report")

    # Compile and run
    compiled = graph.compile()
    return compiled.invoke(state)


if __name__ =="__main__":
    state = get_initial_state("uploads\\OD328509323961361100.pdf")
    run_graph(state)