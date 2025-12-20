from google import genai
from google.genai import types
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class OCRService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            # 새로운 google.genai Client 사용
            self.client = genai.Client(api_key=api_key)
            # Gemini 2.0 Flash 모델 사용 (2025년 최신 모델)
            self.model_name = 'gemini-2.0-flash-exp'
        else:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
            self.client = None
            self.model_name = None

    def analyze_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> Dict[str, Any]:
        if not self.client:
            raise Exception("OCR Service is not configured (Missing API Key)")

        prompt = """
        You are a meticulous Data Entry Clerk. Read the provided Invoice/Purchase Order image carefully.

        Your task is to extract ALL available information from the invoice into a structured JSON format.

        EXTRACT EVERYTHING YOU CAN SEE, even if some fields are empty or not found.

        JSON SCHEMA (Complete Invoice Data):
        {
          "debug_raw_text": "FULL TRANSCRIPTION of ALL text in the document. Include EVERYTHING visible.",

          "document_info": {
            "document_number": "문서번호, Document No (if different from contract_number)",
            "contract_number": "발주번호, 계약번호, Order No, Ref No (e.g. S225HY...)",
            "issue_date": "발행일, Issue Date (YYYY-MM-DD)",
            "invoice_date": "거래일, Invoice Date (YYYY-MM-DD)",
            "delivery_date": "납품일, 배송일, Delivery Date (YYYY-MM-DD)",
            "payment_due_date": "지급기한, Payment Due Date (YYYY-MM-DD)",
            "invoice_type": "GSC, HACIELO, STANDARD, or UNKNOWN"
          },

          "supplier": {
            "name": "공급자명, Supplier Name",
            "business_number": "사업자등록번호, Business Registration Number",
            "address": "주소, Address",
            "phone": "전화번호, Tel",
            "fax": "팩스, Fax",
            "email": "Email",
            "representative": "대표자명, Representative Name",
            "contact_person": "담당자명, Contact Person"
          },

          "receiver": {
            "name": "수신자명, Receiver Name (default: The Moon Coffee)",
            "business_number": "사업자등록번호",
            "address": "주소",
            "phone": "전화번호",
            "contact_person": "담당자명"
          },

          "amounts": {
            "subtotal": "공급가액, Subtotal (Number)",
            "tax_amount": "세액, Tax Amount (Number)",
            "total_amount": "합계금액, Total Amount (Number)",
            "grand_total": "총합계, Grand Total (Number)",
            "currency": "통화, Currency (KRW, USD, etc.)"
          },

          "items": [
            {
              "item_number": "순번, No",
              "bean_name": "품명, 원두명, Product Name",
              "bean_name_kr": "품명 한글 번역 (if original is English)",
              "specification": "규격, Specification",
              "origin": "원산지, Origin",
              "quantity": "수량 (Number)",
              "unit": "단위 (kg, bag, etc.)",
              "unit_price": "단가 (Number)",
              "amount": "금액, Amount (Number)",
              "note": "비고, Note"
            }
          ],

          "additional_info": {
            "payment_terms": "결제조건, Payment Terms",
            "shipping_method": "배송방법, Shipping Method",
            "notes": "비고, 특이사항, Notes",
            "remarks": "기타 메모, Remarks"
          }
        }

        IMPORTANT RULES:
        1. Extract ALL text visible in the image into debug_raw_text
        2. For each field, try your best to find the information
        3. If a field is not found, use null or empty string ""
        4. Convert all dates to YYYY-MM-DD format
        5. Convert all numbers by removing commas (e.g., "1,500" -> 1500)
        6. For items, extract as many details as possible
        7. Return ONLY valid JSON, no markdown code blocks
        """

        try:
            # 새로운 API: client.models.generate_content() 사용
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                    prompt
                ]
            )

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
