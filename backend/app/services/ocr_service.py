import google.generativeai as genai
from app.config import settings
import json
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            logger.warning("GEMINI_API_KEY is not set. OCR service will not function.")
            self.model = None

    async def extract_receipt_data(self, image_content: bytes, mime_type: str = "image/jpeg") -> Dict[str, Any]:
        """
        이미지에서 영수증 데이터를 추출합니다.
        """
        if not self.model:
            # Mock Data for Testing/Dev when Key is missing
            logger.warning("Returning Mock OCR Data (No API Key)")
            return {
                "supplier_name": "Mock Supplier",
                "invoice_number": "MOCK-INV-001",
                "date": "2024-01-01",
                "total_amount": 250000,
                "items": [
                    {
                        "name": "Brazil Cerrado",
                        "quantity": 10,
                        "unit_price": 15000,
                        "total_price": 150000
                    },
                    {
                        "name": "Ethiopia Yirgacheffe",
                        "quantity": 5,
                        "unit_price": 20000,
                        "total_price": 100000
                    }
                ]
            }

        prompt = """
        Analyze this receipt/invoice image and extract the following information in JSON format:
        - supplier_name: Name of the supplier/vendor
        - invoice_number: Invoice number or receipt number (unique identifier)
        - date: Date of transaction (YYYY-MM-DD format if possible)
        - total_amount: Total amount of the receipt
        - items: List of items, each containing:
            - name: Item name (exactly as shown)
            - quantity: Quantity (number)
            - unit_price: Unit price (number)
            - total_price: Total price for this item (number)
        
        If a field is not found, set it to null.
        Ensure the output is valid JSON.
        """

        try:
            image_part = {
                "mime_type": mime_type,
                "data": image_content
            }

            response = self.model.generate_content([prompt, image_part])
            
            # Extract JSON from response text (handle potential markdown code blocks)
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            return json.loads(text.strip())

        except Exception as e:
            logger.error(f"OCR Extraction failed: {e}")
            raise e

ocr_service = OCRService()
