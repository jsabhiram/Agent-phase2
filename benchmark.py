from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient
import urllib.parse
# from clean_json import clean

# from clean_json import clean
from fetch_html_price import extract_products_from_text as fhp
def crawl():
# To install: pip install tavily-python
    client = TavilyClient('TAVILY_API_KEY')
    response = client.extract(
        urls=["https://www.flipkart.com/infinix-gt-30-pro-5g/p/itmd4bc1852572b9"]
    )
    print(response)





def generate_flipkart_search_url(query: str) -> str:
    """
    Generates a Flipkart search URL for the given query.

    Args:
        query (str): Product name or search keywords.

    Returns:
        str: Flipkart search URL.
    """
    base_url = "https://www.flipkart.com/search?q="
    encoded_query = urllib.parse.quote(query)
    return base_url + encoded_query
import urllib.parse

def generate_amazon_search_url(query: str) -> str:  #not implemented
    """
    Generates an Amazon search URL for the given query.

    Args:
        query (str): Product name or keywords to search.
        country_code (str): Amazon domain (e.g., 'in' for India, 'com' for US).

    Returns:
        str: Amazon search URL.
    """
    base_url = f"https://www.amazon.in/s?k="
    encoded_query = urllib.parse.quote(query)
    return base_url + encoded_query


def main():
    query = "BRUTON Trendy Sports Running Shoes For Men"
    flipkart_search_url = generate_flipkart_search_url(query)
    # print(generate_amazon_search_url("Washing machine"))
    print(flipkart_search_url)
    # uam=generate_amazon_search_url("Washing machine")
    print(fetch_page_text(flipkart_search_url))
 
import requests
from bs4 import BeautifulSoup

def fetch_page_text(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator='\n', strip=True)
        print(text)
        return (fhp(text))
    except Exception as e:
        return f"Error: {e}"
# 

#new fetch function

if __name__ == "__main__":
    main()