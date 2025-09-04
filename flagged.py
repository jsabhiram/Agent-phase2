from mdb import confuse

def search_items(data, query):
    """
    Search for items in the data dictionary that match the query (case-insensitive).
    
    Args:
        data (dict): Dictionary of items with details.
        query (str): The search keyword.
    
    Returns:
        dict: Matching items with details.
    """
    query = query.lower()
    result = {}
    
    for item, details in data.items():
        if query in item.lower():  # match in item name
            result[item] = details
        else:
            # also check in details (unit or max_quantity as string)
            if any(query in str(value).lower() for value in details.values()):
                result[item] = details
    
    return result


# Example usage
inventory = {
    'High-Precision Gear': {'unit': 'units', 'max_quantity': 100},
    'Industrial Lubricant': {'unit': 'kg', 'max_quantity': 500},
    'Thermal Sensor Unit': {'unit': 'units', 'max_quantity': 50},
    'Steel Beams': {'unit': 'ton', 'max_quantity': 25}
}
def source(dct):
    for x in dct.keys():
        print(dct[x])
        
        


print(search_items(inventory, "beams"))   # match by item name   # match by unit     # match by quantity
source(confuse())


