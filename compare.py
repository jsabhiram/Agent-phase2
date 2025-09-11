from dotenv import load_dotenv
load_dotenv()
# from flagged import source
from groq import Groq
from slider_value import get_value
def decide(invoice_entry, benchmark_entry):
    print("Deciding...")
    """
    General-purpose price comparison between an invoice item and a benchmark listing.

    Args:
        invoice_entry (str): Description + price from invoice.
        benchmark_entry (str): Description + price from benchmark.

    Returns:
        str: A reasoned verdict on price fairness.
    """
    print(invoice_entry ,"AND"  ,benchmark_entry)

    print(type(invoice_entry) ,"AND"  ,type(benchmark_entry))

    prompt = f"""
Compare two product listings for type, specs, and price fairness.

Invoice Entry: {invoice_entry}  
Benchmark Entry: {benchmark_entry}  

Rules:
- Allowed deviation: {get_value()}%
- Check if items are the same or different.
- Decide if invoice price is FAIR, OVERPRICED, UNDERPRICED, or MISMATCHED.
- Keep response concise.

Output format:
1. Similarity: [Yes/No]  
2. Price: [Fair/Overpriced/Underpriced]  
3. Reason: short one-liner  
4. Verdict: [FAIR | OVERPRICED | UNDERPRICED | MISMATCHED]
"""

    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
def mark(dct):
    # source(dct)
    pass



    

# Example use
if __name__ == "__main__":
    invoice = "Samsung 7kg Fully Automatic Washing Machine, Inverter Motor, price 18490"
    benchmark = "Samsung 7kg Inverter Fully Automatic Washing Machine, price 15990"
    print(decide(invoice, benchmark))
    print(get_value())
