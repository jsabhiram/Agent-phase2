import json
import re

def clean(raw_text: str) -> list:
    """
    Cleans and parses LLM-generated JSON-like output.
    
    Args:
        raw_text (str): Raw string from LLM (can include ```json ... ```).

    Returns:
        list[dict]: Parsed and normalized list of item dictionaries.
    """
    # Step 1: Remove code block markers
    raw_text = raw_text.strip()
    raw_text = re.sub(r"^```json", "", raw_text)
    raw_text = re.sub(r"```$", "", raw_text)
    raw_text = raw_text.strip()

    # Step 2: Attempt to parse JSON
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return []

    # Step 3: Normalize keys and fill defaults
    normalized = []
    for item in data:
        norm_item = {
            "item_name": item.get("itemname") or item.get("item_name") or "",
            "quantity": (item.get("quantity", 1)),
            "price": (item.get("price", 0.0)),
            # "discount": float(item.get("discount", 0.0))  # optional
        }
        normalized.append(norm_item)

    return normalized
