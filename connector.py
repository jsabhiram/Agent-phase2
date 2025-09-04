from flag import get_mongo_collections
def fetch_watchlists_and_benchmarks():
    collections = get_mongo_collections()

    watchlists = {
        "vendors": [doc['name'] for doc in collections["vendors"].find()],
        "countries": [doc['name'] for doc in collections["countries"].find()],
        "hsn": [doc['code'] for doc in collections["hsn"].find()]
    }

    benchmark_prices = {
        doc['item']: doc['price'] for doc in collections["benchmarks"].find()
    }

    quantity_limits = {
        (doc['item'], doc['unit']): doc['max_quantity']
        for doc in collections["quantity_limits"].find()
    }

    return watchlists, benchmark_prices, quantity_limits
