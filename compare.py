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
You are a smart pricing evaluator AI that compares two product listings based on their features and prices.

**Listing 1: Invoice Entry**
{invoice_entry}

**Listing 2: Benchmark Entry**
{benchmark_entry}

Task:
- Analyze the product type, key specifications, and features.
- Compare both listings even if the wording is different.
- Focus on price fairness—determine if the invoice price is reasonable based on the benchmark and allowed deviaition or overpricing is {get_value()}%.
- Consider upgrades/downgrades in specs if any.
- If the products are significantly different, mention that too.

Your final output should include:
1. Are the products similar or not?
2. Is the invoice item overpriced, underpriced, or fairly priced?
3. A short, clear justification.
4. Final verdict label: one of ["FAIR", "OVERPRICED", "UNDERPRICED", "MISMATCHED"]
"""

    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
def mark(dct):
    # source(dct)
    passs



    

# Example use
if __name__ == "__main__":
    invoice = "Samsung 7kg Fully Automatic Washing Machine, Inverter Motor, price 18490"
    benchmark = "Samsung 7kg Inverter Fully Automatic Washing Machine with Smart Features, price 15990"
    print(decide(invoice, benchmark))
