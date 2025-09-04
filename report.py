from dotenv import load_dotenv
load_dotenv()
from test_llm import Agent

def gr(data:str):
    message = f"Write a report on as a price comparison report on {data}"
    return Agent(message)



def generate_report(state):
    print("Generating report...")
    report = {
        "summary": f"{len(state['results'])} products processed successfully. {len(state['failed_final'])} failed.",
        "products": [],
        "failed": state["failed_final"]
    }

    for item in state["results"]:
        p = {
            "product": item["product"],
            "invoice_price": item["invoice_price"],
            "market_prices": item["market_prices"],
            "anomaly": item["anomaly"],
            "status": item["status"]
        }
        report["products"].append(p)

    final_summary = Agent(f"Write a report as a price comparison agent referring the following data:{report},respond short and sweet way with strictly product name,invoice price and market price and your observation about the pricing,get excited about huge savings and recommend future steps a product was overpriced but just two or three sentences for all that.") # Gemini or LLaMA3

    return final_summary

    # print(final_summary)
    # return state


if __name__ == "__main__":
    state = {
    "invoice_data": [...],         # raw extracted data (product, qty, price)
    "pending_products": [...],     # queue of product dicts
    "results": [],                 # successful comparisons
    "failed_once": [],             # items to retry once
    "failed_final": [],            # items failed even after retry
}
    print(generate_report(state))