
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def list_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not found.")
        return

    client = genai.Client(api_key=api_key)
    
    print("Found models:")
    try:
        # Paging is handled by the SDK usually, but let's just print simple list first
        # Usually client.models.list() returns an iterable
        for m in client.models.list():
             if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
