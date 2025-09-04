from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
def Agent(data):
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=data
    )
    return response.text



if __name__ == "__main__":
    print(Agent("Write a report on NVIDIA"))