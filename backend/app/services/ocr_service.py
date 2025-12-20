import google.generativeai as genai
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class OCRService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            # Gemini 2.0 Flash 모델 사용 (2025년 최신 모델)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
            self.model = None

    def analyze_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> Dict[str, Any]:
        if not self.model:
            raise Exception("OCR Service is not configured (Missing API Key)")

        prompt = """
        You are a meticulous Data Entry Clerk. Read the provided Invoice/Purchase Order image carefully.
        
        Your task is to extracting the following data into a JSON format.
        
        EXTRACT ALL TEXT FIRST for debugging, then find specific fields.

        JSON SCHEMA:
        {
          "debug_raw_text": "TRANSCRIPTION OF ALL TEXT found in the top 30% of the page (Header area). INCLUDE EVERYTHING YOU SEE.",
          "contract_number": "Look for '발주번호', '문서번호', 'Order No', 'Ref No' in the header. It usually starts with 'S' (e.g. S225HY...). Copy it exactly.",
          "supplier_name": "The Supplier Company Name (exclude 'The Moon Coffee').",
          "supplier_phone": "Tel/Mobile number",
          "supplier_email": "Email address",
          "receiver_name": "Receiver Name (default to 'The Moon Coffee' if implied)",
          "invoice_date": "YYYY-MM-DD",
          "total_amount": "Total Amount (Number)",
          "items": "List of {bean_name, quantity, unit_price, amount}"
        }
        
        Return ONLY valid JSON.
        """

        try:
            response = self.model.generate_content([
                {'mime_type': mime_type, 'data': image_bytes},
                prompt
            ])
            
            text = response.text
            # Clean up markdown if present
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            return json.loads(text)
            
        except Exception as e:
            print(f"Error during Gemini OCR analysis: {e}")
            raise e
