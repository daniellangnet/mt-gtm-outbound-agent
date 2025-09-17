import os
from openai import OpenAI
from dotenv import load_dotenv

def create_openai_client():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)
