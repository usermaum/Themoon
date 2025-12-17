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
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
            self.model = None

    def analyze_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> Dict[str, Any]:
        if not self.model:
            raise Exception("OCR Service is not configured (Missing API Key)")

        prompt = """
        Analyze this coffee bean invoice/receipt image and extract the following data in JSON format:
        
        1. supplier_name: String (Name of the vendor/supplier)
        2. contract_number: String (Order No, Estimate No, Document No, or '발주번호', '견적번호'. If not found, null)
        3. supplier_phone: String (Vendor's phone number, e.g., 'Tel', 'Phone', 'H.P')
        4. supplier_email: String (Vendor's email)
        5. receiver_name: String (Name of the receiver/buyer)
        6. invoice_date: String (YYYY-MM-DD format)
        7. total_amount: Number (Total sum of the invoice)
        8. items: List of objects, each containing:
           - bean_name: String (Name of the bean/product)
           - quantity: Number (Weight in kg or count)
           - unit_price: Number (Price per unit)
           - amount: Number (Total price for this line item)
           
        If a field is missing, use null. ensure the output is valid JSON without markdown code blocks.
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
