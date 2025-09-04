import re
from test_llm import Agent

def extract_products_from_text(text: str):
    lines = text.splitlines()
    products = []

    current_product = {}
    skip_keywords = ["Add to Compare", "Hot Deal", "Only", "Bank Offer", "Upto", "Off on Exchange"]

    for line in lines:
        line = line.strip()

        # Match product name (usually starts with "Acer Aspire 7" or similar)
        if line.startswith("Acer Aspire"):
            if current_product:
                if 'item_name' in current_product and 'price' in current_product:
                    products.append(current_product)
                current_product = {}
            current_product["item_name"] = line

        # Match price (₹xx,xxx)
        elif re.match(r"₹\d[\d,]*", line):
            price = re.findall(r"₹[\d,]+", line)
            if price and "price" not in current_product:
                current_product["price"] = price[0]

        # If line is useless, skip
        elif any(keyword in line for keyword in skip_keywords):
            continue

    # Add last product if valid
    if current_product.get("item_name") and current_product.get("price"):
        products.append(current_product)
    data_to_send=str(products) 
    format_query="Extract just the items,quantity and price from the data provided,return in a form which is best for jsonfiy function to work, with keys itemname,quantity,price for each item,most importantly check if the item included is a valid product name and listed in the site with similar features.", data_to_send


    return Agent(format_query)
