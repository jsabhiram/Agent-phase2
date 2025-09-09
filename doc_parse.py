import os
import re
import json
import ast
import time
import fitz  # PyMuPDF
from test_llm import Agent
import check


def extract_invoice_data(file_path):
    """
    Dispatch function to extract invoice data based on file type.
    """
    if file_path.endswith(".docx"):
        return parse_docx_invoice(file_path)
    elif file_path.endswith(".pdf"):
        return parse_pdf_invoice(file_path)
    # elif file_path.endswith((".xls", ".xlsx")):
    #     return parse_excel_invoice(file_path)
    else:
        raise ValueError("Unsupported file format")


def parse_docx_invoice(path):
    """
    Extracts structured invoice metadata from a DOCX file.
    """
    meta = check.main(path)
    output_str = json.dumps(meta, indent=2)
    return {"products": output_str}


def parse_pdf_invoice(path):
    """
    Extracts text from all pages of a PDF invoice using PyMuPDF.
    """
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text("text")  # modern PyMuPDF API
    doc.close()

    lines = text.split('\n')
    return lines


# def parse_excel_invoice(path):
#     df = pd.read_excel(path)
#     items = df.to_dict('records')
#     return items


def form(data):
    """
    Extract JSON-like list from a string and return parsed Python object.
    """
    match = re.search(r'(\[.*\])', data, re.DOTALL)
    if match:
        result = match.group(0)
        try:
            items_list = json.loads(result)
            return items_list
        except json.JSONDecodeError:
            return "[Invalid JSON found]"
    return "[No match found]"


def some(s):
    """
    Extract vendor list and call share.add_vendor
    """
    try:
        data_list = ast.literal_eval(s)
    except Exception as e:
        print("Error parsing string to list:", e)
        return

    vendors = [entry.get('vendor', 'unknown') for entry in data_list if isinstance(entry, dict)]
    if vendors:
        from share import add_vendor
        add_vendor(vendors)
        print(vendors)   # e.g. ['STS ENTERPRISES']


def admin(file_path):
    """
    Orchestrator: extract invoice data, query Agent, parse response.
    """
    print("Extracting invoice data🔎...")  #added debugging part
    data_to_send = extract_invoice_data(file_path)

    format_query = (
        "Extract the items, quantity, vendor (if any otherwise return vendor:unknown), "
        "goods/HSN, price and country from the invoice of products. "
        "Analyze the content and then decide product price; include brand and features "
        "also in name. Neglect services like handling or platform fee. "
        "Return in a form which is best for jsonify function to work, "
        "with keys itemname, quantity, price for each item. "
        "Most importantly check if the item included is a valid product name "
        "and not ambiguous. If there are no products or services found with a price, "
        "then return the message: 'no useful invoice data found'."
    ), data_to_send

    response = Agent(format_query)
    # print(response)

    data_str = str(form(response))
    # some(data_str)  # Uncomment if vendor processing is needed
    return form(response)


if __name__ == "__main__":
    # Example test
    c=admin("uploads\\OD328509323961361100.pdf")
    print((c[0]))
    # print(admin("uploads\\OD330976234110643100.pdf"))
