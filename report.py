from dotenv import load_dotenv
load_dotenv()
from test_llm import Agent

def gr(data: str):
    message = f"Write a price comparison report on {data}"
    return Agent(message)


def generate_report(state):
    print("Generating report...")
    print(state['results'])
    
    # Containers
    processed_products = []
    removed_products = []
    failed_products = state.get("failed_final", [])
    unknown_status = []

    # Categorize dynamically
    for item in state["results"]:
        status = item.get("status", "unknown")
        
        entry = {"status": status}
        # Capture all available keys
        for key, value in item.items():
            if key != "status":
                entry[key] = value
        
        if status.startswith("success"):
            processed_products.append(entry)
        elif "removed" in status:
            removed_products.append(entry)
        elif "failed" in status:
            failed_products.append(entry)
        else:
            unknown_status.append(entry)

    report = {
        "total_products": len(state["results"]),
        "processed_products": processed_products,
        "removed_products": removed_products,
        "failed_products": failed_products,
        "unknown_status": unknown_status
    }

    # LLM prompt (strict, field-based)
    prompt = f"""
    Generate a professional price comparison and risk analysis report.

    DATA SUMMARY:
    - Total products: {report['total_products']}
    - Processed: {len(processed_products)}
    - Removed: {len(removed_products)}
    - Failed: {len(failed_products)}
    - Unknown: {len(unknown_status)}

    PRODUCT DETAILS:
    - Processed Products: {processed_products}
    - Removed Products: {removed_products}
    - Failed Products: {failed_products}
    - Unknown Status: {unknown_status}

    Guidelines:
    1. Analyze each product entry strictly based on the fields provided (keys and values).
    2. Do not assume missing fields; if data is not present, exclude it.
    3. Summarize per-product findings clearly (product name, invoice price, anomalies, risk, etc.).
    4. Provide a professional executive summary, risk insights, and recommendations.
    5. Keep the tone factual, avoid speculation or casual expressions.

    make all this within 150 characters
    """

    final_summary = Agent(prompt)
    return final_summary





if __name__ == "__main__":
    state = {
        "results":[{'product': 'Sadow LAN Cable 25 m', 'invoice_price': 480.0, 'market_prices': {}, 'anomaly': 'PRODUCT_REMOVED_BY_USER', 'risk': 3, 'status': 'removed_high_risk'}],
        "failed_final": []
    }
    print(generate_report(state))
