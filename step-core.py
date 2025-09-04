from groq import Groq
# from dotenv import load_dotenv
import os
def decide_tool_usage(state):
    llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""
You are an intelligent invoice reasoning agent. Given the extracted invoice data:

Products:
{state['invoice_data'] if state['invoice_data'] else 'No data'}

Determine if the invoice products are valid, if any need retry, and if price comparison should be done. Respond with:
- action: [process|retry|skip]
- reason: your justification
"""
    completion = llm.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

if __name__ =="__main__":
    print(decide_tool_usage({"input_file_path":'',
            "invoice_data": None,
            "pending_products":None,
            "results": [],
            # "failed_once": [],
            # "failed_final": [],
            "final_report": None})
            )