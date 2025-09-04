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
