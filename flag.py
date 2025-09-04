from pymongo import MongoClient
import pandas as pd

def extract_mongodb_data(connection_string, database_name):
    """
    Extracts data from all specified collections in a MongoDB database.
    
    Args:
        connection_string (str): MongoDB connection string
        database_name (str): Name of the database to connect to
        
    Returns:
        dict: A dictionary where keys are collection names and values are DataFrames
    """
    try:
        # Connect to MongoDB
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
        
        extracted_data = {}
        
        for collection_name in collection_names:
            # Get the collection
            collection = db[collection_name]
            
            # Fetch all documents from the collection
            cursor = collection.find({})
            
            # Convert to DataFrame
            df = pd.DataFrame(list(cursor))
            
            # Store in dictionary
            extracted_data[collection_name] = df
            
            print(f"Extracted {len(df)} records from {collection_name}")
        
        return extracted_data
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
    finally:
        # Close the connection
        if 'client' in locals():
            client.close()
def find(s):
    data=extract_mongodb_data(CONNECTION_STRING, DATABASE_NAME)
    print(data)

# Example usage:
if __name__ == "__main__":
    # Replace with your actual connection string and database name
    CONNECTION_STRING = "mongodb+srv://jsabhiramsuresh:AtUKr9R9r9ozELf4@cluster1.kky8xoc.mongodb.net/"
    DATABASE_NAME = "sample_mflix"
    
    # Extract data
    data = extract_mongodb_data(CONNECTION_STRING, DATABASE_NAME)
    
    # Access the data
    if data:
        for collection_name, df in data.items():
            print(f"\nData from {collection_name}:")
            for x in df.head():
                x=df.head(1)
                if(collection_name=="benchmark_prices"):
                    print(x["itemname"])
                    print(x["quantity"])
                    print(x["price"])
                
                # print(type(df.head(1).to_dict()))

    # find("Hi")

    