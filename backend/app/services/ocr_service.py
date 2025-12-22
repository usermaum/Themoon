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
            # Gemini 2.0 Flash 모델 사용
            self.model_name = 'gemini-2.0-flash-exp'
        else:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
            self.client = None
            self.model_name = None

    def analyze_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> Dict[str, Any]:
        if not self.client:
            raise Exception("OCR Service is not configured (Missing API Key)")

        prompt = """
        You are a meticulous Data Entry Clerk. 
        
        CRITICAL RULE: First, check if the provided image is a business document (Invoice, Purchase Order, Receipt, Delivery Note, etc.). 
        If it is NOT a business document (e.g., it's a person, a landscape, a screenshot of a video, a meme, etc.), 
        you MUST return ONLY this JSON and NOTHING ELSE:
        {
          "error": "INVALID_DOCUMENT"
        }

        If it IS a business document, extract ALL available information from the invoice into a structured JSON format.

        JSON SCHEMA:
        {
          "error": null,
          "debug_raw_text": "FULL TRANSCRIPTION of ALL text in the document. Include EVERYTHING visible.",

          "document_info": {
            "document_number": "문서번호, Document No",
            "contract_number": "발주번호, 계약번호, Order No, Ref No",
            "issue_date": "발행일 (YYYY-MM-DD)",
            "invoice_date": "거래일 (YYYY-MM-DD)",
            "delivery_date": "납품일 (YYYY-MM-DD)",
            "payment_due_date": "지급기한 (YYYY-MM-DD)",
            "invoice_type": "GSC, HACIELO, STANDARD, or UNKNOWN"
          },

          "supplier": {
            "name": "공급자명, Supplier Name",
            "business_number": "사업자등록번호",
            "address": "주소",
            "phone": "대표 전화번호",
            "fax": "팩스",
            "email": "Email",
            "representative": "대표자명",
            "contact_person": "담당자명",
            "contact_phone": "담당자 전화번호"
          },

          "receiver": {
            "name": "수신자명 (default: The Moon Coffee)",
            "business_number": "사업자등록번호",
            "address": "주소",
            "phone": "전화번호",
            "contact_person": "담당자명"
          },

          "amounts": {
            "subtotal": "공급가액 (Number)",
            "tax_amount": "세액 (Number)",
            "total_amount": "합계금액 (Number)",
            "total_amount_kr": "합계금액 (Number, if total_amount is unclear)",
            "grand_total": "총합계 (Number)",
            "currency": "통화 (KRW, USD, etc.)"
          },

          "items": [
            {
              "item_number": "순번, No",
              "bean_name": "품명, 원두명",
              "bean_name_kr": "품명 한역",
              "specification": "규격",
              "origin": "원산지",
              "quantity": "수량 (Number)",
              "unit": "단위 (kg, bag, etc.)",
              "unit_price": "단가 (Number)",
              "amount": "금액 (Number)",
              "note": "비고"
            }
          ],

          "additional_info": {
            "payment_terms": "결제조건",
            "shipping_method": "배송방법",
            "notes": "비고, 특이사항",
            "remarks": "기타 메모"
          }
        }

        IMPORTANT RULES:
        1. Extract ALL text visible in the image into debug_raw_text.
        2. If a field is not found, use null or empty string "".
        3. Convert all dates to YYYY-MM-DD format.
        4. Convert all numbers by removing commas.
        5. Return ONLY valid JSON, no markdown code blocks.
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
            if text.strip().startswith("```json"):
                text = text.strip()[7:]
                if text.endswith("```"):
                    text = text[:-3]
            elif text.strip().startswith("```"):
                text = text.strip()[3:]
                if text.endswith("```"):
                    text = text[:-3]

            return json.loads(text.strip())

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print(f"⚠️ Gemini API Quota Exceeded: {e}")
                # Raise a specific error message that can be caught by the endpoint
                raise Exception("GEMINI_QUOTA_EXCEEDED")
            print(f"Error during Gemini OCR analysis: {e}")
            raise e
