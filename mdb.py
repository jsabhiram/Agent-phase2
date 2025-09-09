from pymongo import MongoClient

uri = "mongodb+srv://jsabhiramsuresh:AtUKr9R9r9ozELf4@cluster1.kky8xoc.mongodb.net/"

def extract_all_details():
    client = MongoClient(uri)
    db = client["sample_mflix"]

    # Extract vendors → list of names
    vendors = [doc["name"] for doc in db["watchlist_vendors"].find({}, {"_id": 0, "name": 1})]

    # Extract countries → list of names
    countries = [doc["name"] for doc in db["watchlist_countries"].find({}, {"_id": 0, "name": 1})]

    # Extract hsn codes → list of codes
    hsn_codes = [doc["code"] for doc in db["watchlist_hsn"].find({}, {"_id": 0, "code": 1})]

    # Extract benchmark items → dictionary {item: price}
    benchmark_prices = {doc["item"]: doc["price"] for doc in db["benchmark_prices"].find({}, {"_id": 0})}

    # Extract quantity limits → dictionary {item: {"unit": unit, "max_quantity": value}}
    quantity_limits = {
        doc["item"]: {"unit": doc["unit"], "max_quantity": doc["max_quantity"]}
        for doc in db["quantity_limits"].find({}, {"_id": 0})
    }

    client.close()

    return {
        "vendors": vendors,
        "countries": countries,
        "hsn_codes": hsn_codes,
        # "benchmark_prices": benchmark_prices,
        "quantity_limits": quantity_limits
    }

# Example
c=extract_all_details()['quantity_limits']
print(c['High-Precision Gear']['unit'])