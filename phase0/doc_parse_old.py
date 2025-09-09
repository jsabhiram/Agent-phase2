import os
from test_llm import Agent
import check 
def extract_invoice_data(file_path):
    if file_path.endswith(".docx"):
        return parse_docx_invoice(file_path)
    elif file_path.endswith(".pdf"):
        return parse_pdf_invoice(file_path)
    # elif file_path.endswith(".xls") or file_path.endswith(".xlsx"):
        # return parse_excel_invoice(file_path)
    else:
        raise ValueError("Unsupported file format")
# from docx import Document
import json
def parse_docx_invoice(path):
    meta=check.main(path)
    output_str = json.dumps(meta, indent=2)
    return {"products":{output_str}}
    """
    Extracts text from all pages and elements of a DOCX invoice.
    
    Args:
        path (str): Path to the DOCX file
        
    Returns:
        list: All text elements from the document
    """



import fitz,re
import time
def parse_pdf_invoice(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        # print(page)
        textpage = page.get_textpage()
        text += textpage.extractText()
        # print(text)
    lines = text.split('\n')
    # items = []
    return lines


# import pandas as pd
# def parse_excel_invoice(path):
    # df = pd.read_excel(path)
    # items = df.to_dict('records')
# 
    # return items
# 
# 
# print(extract_invoice_data("invoice.pdf"))
import re
import json
import ast
def form(data):
    match=re.search(r'(\[.*\])', data, re.DOTALL)
    if match:
        result = match.group(0)
        items_list = json.loads(result)
        result=items_list
        # print(result)
    else:
        result="[No match found]"
    return result
def some(s):
    data_str = s
    vendors=None
    data_list = ast.literal_eval(data_str)
    #Extract vendors
    # if("vendor" in data_list):
    vendors = [entry['vendor'] for entry in data_list]
    from share import add_vendor
    add_vendor(vendors)
    print(vendors)   # ['STS ENTERPRIES']

def admin(file_path):
    print("Extracting invoice data...")
    data_to_send=extract_invoice_data(file_path) #calls the doc_parse.py
    # print(data_to_send)
    # time.sleep(5)
    format_query="Extract the items,quantity,vendor(if any otherwise return vendor:unknown), goods/HSN, price and country from the invoice of products[analyze the content and then decide product price include brand and features also in name] and neglect services like handling or platform fee ,return in a form which is best for jsonfiy function to work, with keys itemname,quantity,price for each item,most importantly check if the item included is a valid product name and not ambiguous.|If there is no products or service found with a price then return the message no useful invoice data found", data_to_send
    response = Agent(format_query)
    print(response)
    data_str = str(form(response))
    # some(data_str)


# E



    return form(response)
if __name__ == "__main__":
    # print(extract_invoice_data("uploads\\OD334580468490515100.pdf"))
    print(admin("uploads\\OD328509323961361100.pdf"))
    # print(admin("uploads\\OD330976234110643100.pdf"))