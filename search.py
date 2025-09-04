from tavily import TavilyClient
import os

from test_llm import Agent
def context(data):
        query= 'strictly give a one word or one sentence description of the given products category if you can find that otherwise give empty string:product itemname:{data}'
        return{Agent(query)}

def search(name:str):
    print("Searching online...")
    print(name)
    # To install: pip install tavily-python
    c=context(name)
    client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    response = client.search(
        query=f"what is the price of {name}-{c} in india in Indian rupee?",
        search_depth="advanced",
        max_results=15,
        time_range="day",
        include_answer="basic",
        country="india"

    )

    # print(response)

    prompt=f"this is the online search result about the price of a product or service\nGather the product price range making sure the product name and characteristic is same\ngive the result as one line strictly(nothing else other than this) in this format 'min': lowest price, 'max':highest price.this is the search result {response}"

    print("Debugging part:" ,Agent(prompt))
   
   
    return(Agent(prompt))

#just added but configuration pending
# def dev():
     
     
# def config(state):
    #   Pass slider value to the state if available
        # if SLIDER_VALUE is not None:
            # state['slider_value'] = SLIDER_VALUE

if __name__ == "__main__":
    search("portonics vader 7 button wired mouse")
    # print("This is from search",get_user_input())