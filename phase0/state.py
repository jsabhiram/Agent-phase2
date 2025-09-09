from typing import TypedDict, List, Optional, Dict

# -- Define product structure --
class Product(TypedDict):
    itemname: str
    quantity: int
    price: float

class ProductResult(TypedDict):
    product: str
    invoice_price: float
    market_prices: Dict[str, float]  # e.g., {"min": 65000, "max": 70000}
    anomaly: str
    status: str  # "success" or "retry_success"

# -- Define the LangGraph-compatible state schema --
# class GraphState(TypedDict):
    # input_file_path: str
    # invoice_data: Optional[Dict]
    # pending_products: List[Product]
    # results: List[ProductResult]
    # final_report: Optional[str]

class GraphState(TypedDict):
    input_file_path: str
    invoice_data: Optional[Dict]
    pending_products: List[Product]
    results: List[ProductResult]
    final_report: Optional[str]
    failed_once: List[Product]
    failed_final: List[Product]

# -- Initial state generator function --
def get_initial_state(file_path: str) -> GraphState:
    return {
        "input_file_path": file_path,
        "invoice_data": None,
        "pending_products": [],  # <- This was commented out
        "failed_once": [],
        "failed_final": [],
        "results": [],
        "final_report": None
    }


# def get_initial_state(file_path: str) -> GraphState:
    # return {
        # "input_file_path": file_path,
        # "invoice_data": None,
        # "pending_products": [],
        # "failed_once": [],              # ✅ Added this line
        # "failed_final": [],
        # "results": [],
        # "final_report": None
    # }