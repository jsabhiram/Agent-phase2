from typing import TypedDict, List, Optional, Dict, Any

# -- Define product structure --
class Product(TypedDict):
    itemname: str         
    quantity: int     
    price: float
    country: str
    vendor: str
    hsn: str
    risk:int

class ProductResult(TypedDict):
    product: str
    invoice_price: float
    market_prices: Dict[str, float]  # e.g., {"min": 65000, "max": 70000}
    anomaly: str
    risk:int #risk level
    status: str  # "success" or "retry_success"

# -- Define the LangGraph-compatible state schema --
class GraphState(TypedDict):
    input_file_path: str
    invoice_data: Optional[Dict[str, Any]]  # Changed to include Any for flexibility
    pending_products: List[Product]
    allowed_deviation: float
    results: List[ProductResult]
    final_report: Optional[str]
    failed_once: List[Product]
    failed_final: List[Product]
    # Added new fields needed for the Groq workflow
    monitor: Optional[bool]  # For progress monitoring
    current_step: Optional[str]  # Track current processing step
    error_log: Optional[List[str]]  # Track errors for debugging

# -- Initial state generator function --
def get_initial_state(file_path: str) -> GraphState:
    return {
        "input_file_path": file_path,
        "invoice_data": None,
        "pending_products": [],
        "allowed_deviation":0,   #just added
        "failed_once": [],
        "failed_final": [],
        "results": [],
        "final_report": None,
        # Initialize new fields
        "monitor": False,
        "current_step": None,
        "error_log": []
    }