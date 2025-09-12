from dotenv import load_dotenv
load_dotenv()
from test_llm import Agent

def gr(data: str):
    message = f"Write a report on as a price comparison report on {data}"
    return Agent(message)

def generate_report(state):
    print("Generating report...")
    print(state['results'])
    
    # Categorize results by status
    successful_products = []
    removed_products = []
    low_risk_warnings = []
    medium_risk_approved = []
    
    for item in state["results"]:
        if item["status"] == "removed_high_risk":
            removed_products.append(item)
        elif item["status"] == "success_low_risk_warning":
            low_risk_warnings.append(item)
        elif item["status"] == "success_medium_risk_approved":
            medium_risk_approved.append(item)
        else:  # regular success or retry_success
            successful_products.append(item)
    
    # Build comprehensive report structure
    report = {
        "total_products": len(state['results']),
        "successful_processed": len(successful_products),
        "removed_high_risk": len(removed_products),
        "low_risk_warnings": len(low_risk_warnings),
        "medium_risk_approved": len(medium_risk_approved),
        "failed_final": len(state["failed_final"]),
        "summary": f"{len(successful_products + low_risk_warnings + medium_risk_approved)} products processed successfully. {len(removed_products)} removed due to high risk. {len(state['failed_final'])} failed processing.",
        
        "processed_products": [],
        "removed_products": [],
        "failed_products": state["failed_final"]
    }

    # Add successfully processed products
    for item in successful_products + low_risk_warnings + medium_risk_approved:
        p = {
            "product": item["product"],
            "invoice_price": item["invoice_price"],
            "market_prices": item["market_prices"],
            "anomaly": item["anomaly"],
            "status": item["status"],
            "risk_level": item.get("risk", "N/A")
        }
        if "warning_details" in item:
            p["warning_details"] = item["warning_details"]
        report["processed_products"].append(p)

    # Add removed products with detailed reasons
    for item in removed_products:
        r = {
            "product": item["product"],
            "invoice_price": item["invoice_price"],
            "risk_level": item["risk"],
            "removal_reason": item["removal_details"]["removal_reason"],
            "risk_details": item["removal_details"]["risk_details"],
            "timestamp": item["removal_details"]["timestamp"]
        }
        report["removed_products"].append(r)

    # Create detailed prompt for LLM
    prompt = f"""
    Generate a comprehensive price comparison and risk analysis report based on the following data:

    SUMMARY:
    - Total products analyzed: {report['total_products']}
    - Successfully processed: {report['successful_processed']}
    - Low risk warnings: {report['low_risk_warnings']}
    - Medium risk (user approved): {report['medium_risk_approved']}
    - High risk products removed: {report['removed_high_risk']}
    - Failed processing: {report['failed_final']}

    PROCESSED PRODUCTS:
    {report['processed_products']}

    REMOVED HIGH-RISK PRODUCTS:
    {report['removed_products']}

    FAILED PRODUCTS:
    {report['failed_products']}

    Please provide:
    1. Executive summary of the price analysis
    2. Risk assessment findings
    3. Savings opportunities identified
    4. Products flagged for concern
    5. Recommendations for next steps

    Keep it professional but highlight significant savings or overpricing. Be concise but thorough.
    """

    final_summary = Agent(prompt)
    return final_summary

if __name__ == "__main__":
    # Test with your sample data
    state = {
        "results": [
            {
                'product': 'Sadow LAN Cable 25 m', 
                'invoice_price': 480.0, 
                'market_prices': {}, 
                'anomaly': 'PRODUCT_REMOVED_HIGH_RISK', 
                'risk': 3, 
                'status': 'removed_high_risk', 
                'removal_details': {
                    'product_name': 'Sadow LAN Cable 25 m', 
                    'invoice_price': 480.0, 
                    'risk_level': 3, 
                    'removal_reason': 'High risk product automatically removed', 
                    'risk_details': 'Exact match in vendor watchlist-SADOW TECHNOLOGIES \nQuantity limit exceeded by 1 units\nCountry is flagged IN\n ', 
                    'timestamp': '2025-09-12 10:31:56', 
                    'action_taken': 'Product removed from processing queue'
                }
            }
        ],
        "failed_final": []
    }
    print(generate_report(state))