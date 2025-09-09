# reference for risk analysis node 
def assess_risk(invoice, watchlists, benchmark_prices, quantity_limits):
    risks = []
    
    # Vendor Risk
    vendor = invoice['vendor']
    if vendor in watchlists['vendors']:
        risks.append({"field": "vendor", "value": vendor, "risk": "High", "reason": "Exact match in vendor watchlist"})
    elif any(v.lower() in vendor.lower() for v in watchlists['vendors']):
        risks.append({"field": "vendor", "value": vendor, "risk": "Medium", "reason": "Partial match in vendor watchlist"})

    # Country Risk
    country = invoice['country']
    if country in watchlists['countries']:
        risks.append({"field": "country", "value": country, "risk": "High", "reason": "Country is sanctioned"})

    # HSN Risk
    hsn = invoice['hsn']
    if hsn in watchlists['hsn']:
        risks.append({"field": "hsn", "value": hsn, "risk": "Medium", "reason": "HSN code flagged"})

    # Price Risk
    item = invoice['item']
    price = invoice['unit_price']
    benchmark = benchmark_prices.get(item)
    if benchmark:
        if price > 1.5 * benchmark:
            risks.append({"field": "unit_price", "value": price, "risk": "High", "reason": f"Price 50% above benchmark ({benchmark})"})
        elif price > 1.2 * benchmark:
            risks.append({"field": "unit_price", "value": price, "risk": "Medium", "reason": f"Price slightly above benchmark ({benchmark})"})

    # Quantity Risk
    quantity = invoice['quantity']
    unit = invoice['unit']
    limit = quantity_limits.get((item, unit))
    if limit:
        if quantity > 1.5 * limit:
            risks.append({"field": "quantity", "value": quantity, "risk": "High", "reason": f"Quantity exceeds limit by 50% (Limit: {limit} {unit})"})
        elif quantity > 1.2 * limit:
            risks.append({"field": "quantity", "value": quantity, "risk": "Medium", "reason": f"Quantity slightly above limit (Limit: {limit} {unit})"})

    return risks



# recovered code from file step-core.py
from groq import Groq
# from dotenv import load_dotenv
import os
from dotenv import load_dotenv
load_dotenv()
def decide_tool_usage(state):
    llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
You are an intelligent invoice reasoning agent. Given the extracted invoice data:

Products:
{state['invoice_data'] if state['invoice_data'] else 'No data'}

Determine if the invoice products are valid, if any need retry, and if price comparison should be done. Respond with:
- action: [process|retry|skip]
- reason: your justification
"""
    completion = llm.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

if __name__ =="__main__":
    print(decide_tool_usage({"input_file_path":'',
            "invoice_data": None,
            "pending_products":None,
            "results": [],
            # "failed_once": [],
            # "failed_final": [],
            "final_report": None})
            )
    



#simulate NOLLM Comaprison

# {'itemname': 'Acer Aspire 7 (2023) Intel Core i5 12th Gen 12450H - (16 GB/512 GB SSD/Windows 11 Home/4 GB Graphics/NVIDIA GeForce RTX 3050/144 Hz) A715-76G Gaming Laptop', 'quantity': 1, 'price': 50990.0}







from slider_value import get_value




def decide(str1, str2):
    val1 = None
    x1 = None
    x2 = None
    val2 = None

    # Extract item name
    start = str1.find("'itemname': '") + len("'itemname': '")
    end = str1.find("', 'quantity'")
    item = str1[start:end]

    # Extract bought price
    for x in str1.split(" "):
        if x == "'price':":
            var = (str1.split(" ")[str1.split(" ").index(x) + 1])
            val1 = float(var[0:(len(var) - 1)])

    # Extract market min/max
    for x in str2.split(" "):
        if x == "'min':":
            var = (str2.split(" ")[str2.split(" ").index(x) + 1])
            x1 = float(var[0:(len(var) - 1)])
        if x == "'max':":
            var = (str2.split(" ")[str2.split(" ").index(x) + 1])
            x2 = float(var[0:(len(var))])

    # Average market price
    val2 = (x1 + x2) / 2
    result = None

    # print(item)
    # print(val1, val2)

    if val1 <= val2:
        result = "The products are decently priced"
    else:
        chg = val1 - val2
        calc = int((chg / val2) * 100)
        result = f"The products are {calc}% more expensive than the average price"

        if (get_value() != None and calc <= get_value()):
            result = "The products are priced within the accepted range"
        else:
            result = "The products are priced outside the accepted range, extremely overpriced!!! 🤷‍♂️"

    return(item+result)


if __name__ == "__main__":

    str1="{'itemname': 'Acer Aspire 7 (2023) Intel Core i5 12th Gen 12450H - (16 GB/512 GB SSD/Windows 11 Home/4 GB Graphics/NVIDIA GeForce RTX 3050/144 Hz) A715-76G Gaming Laptop', 'quantity': 1, 'price': 150990.0}"
    str2="'min': 70427, 'max': 70990"

    decide(str1, str2)




# code refractord from human.py


def get_user_input():
    from app import get_slider_value
    slider_value = get_slider_value()
    return slider_value

import time


def waiting(state):
    time.sleep(3)
    if(get_user_input()!=None):
        state['slider_value'] = get_user_input()

    return state





#something related to matching flagged vendors and products
#file name modified.py
from pymongo import MongoClient
import pandas as pd
from typing import Dict, Optional, Union
from typing import Mapping
def extract_mongodb_data(connection_string: str, database_name: str) -> Optional[Dict[str, pd.DataFrame]]:
    try:
        client = MongoClient(connection_string)
        db = client[database_name]

        # List of collections to extract
        collection_names = [
            'benchmark_prices',
            'quantity_limits',
            'watchlist_countries',
            'watchlist_hsn',
            'watchlist_vendors'
        ]

        available_collections = db.list_collection_names()
        extracted_data = {}

        for collection_name in collection_names:
            if collection_name not in available_collections:
                print(f"Collection '{collection_name}' does not exist in database '{database_name}'")
                continue

            collection = db[collection_name]
            cursor = collection.find({})
            df = pd.DataFrame(list(cursor))

            if df.empty:
                print(f"No data found in collection: {collection_name}")

            extracted_data[collection_name] = df
            print(f"Extracted {len(df)} records from {collection_name}")

        return extracted_data

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
    finally:
        if 'client' in locals():
            client.close()


def find_matches(product: str, price: float, vendor: str, quantity: int,
                 data: Dict[str, pd.DataFrame]) -> Dict[str, Union[str, pd.DataFrame]]:
    matches: Mapping[str,str | [pd.DataFrame]] = {
    'benchmark_price_matches': None,
    'quantity_limit_matches': None,
    'vendor_watchlist_matches': None,
    'product_watchlist_matches': None
}
    
    
    

    # Benchmark price check
    if 'benchmark_prices' in data:
        benchmark_df = data['benchmark_prices']
        if 'product' in benchmark_df.columns and 'benchmark_price' in benchmark_df.columns:
            product_matches = benchmark_df[benchmark_df['product'].str.contains(product, case=False, na=False)]
            price_matches = product_matches[product_matches['benchmark_price'] >= price]
            if not price_matches.empty:
                matches['benchmark_price_matches'] = price_matches
                print(f"Found {len(price_matches)} price benchmark matches")

    # Quantity limits check
    if 'quantity_limits' in data:
        quantity_df = data['quantity_limits']
        if all(col in quantity_df.columns for col in ['product', 'min_quantity', 'max_quantity']):
            quantity_matches = quantity_df[
                quantity_df['product'].str.contains(product, case=False, na=False) &
                (quantity_df['min_quantity'] <= quantity) &
                (quantity_df['max_quantity'] >= quantity)
            ]
            if not quantity_matches.empty:
                matches['quantity_limit_matches'] = quantity_matches
                print(f"Found {len(quantity_matches)} quantity limit matches")

    # Vendor watchlist check
    if 'watchlist_vendors' in data:
        vendor_df = data['watchlist_vendors']
        if 'vendor_name' in vendor_df.columns:
            vendor_matches = vendor_df[vendor_df['vendor_name'].str.contains(vendor, case=False, na=False)]
            if not vendor_matches.empty:
                matches['vendor_watchlist_matches'] = vendor_matches
                print(f"Found {len(vendor_matches)} vendor watchlist matches")

    # Product (HSN) watchlist check
    if 'watchlist_hsn' in data:
        hsn_df = data['watchlist_hsn']
        if 'product' in hsn_df.columns:
            hsn_matches = hsn_df[hsn_df['product'].str.contains(product, case=False, na=False)]
            if not hsn_matches.empty:
                matches['product_watchlist_matches'] = hsn_matches
                print(f"Found {len(hsn_matches)} product watchlist matches")

    return matches


# Example usage
if __name__ == "__main__":
    CONNECTION_STRING = "mongodb+srv://jsabhiramsuresh:AtUKr9R9r9ozELf4@cluster1.kky8xoc.mongodb.net/"
    DATABASE_NAME = "sample_mflix"  # Make sure your collections are actually in this DB

    data = extract_mongodb_data(CONNECTION_STRING, DATABASE_NAME)

    if data:
        product_name = "laptop"
        product_price = 999.99
        vendor_name = "TechCorp"
        quantity = 5

        results = find_matches(
            product=product_name,
            price=product_price,
            vendor=vendor_name,
            quantity=quantity,
            data=data
        )

        print("\nSearch Results:")
        for match_type, match_data in results.items():
            if match_data is not None:
                print(f"\n{match_type.replace('_', ' ').title()}:")
                print(match_data)
            else:
                print(f"\nNo {match_type.replace('_', ' ')} found")
