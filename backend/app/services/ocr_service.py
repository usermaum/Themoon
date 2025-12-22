from google import genai
from google.genai import types
import os
import json
import time
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

import anthropic
import base64

class OCRService:
    def __init__(self):
        # 1. Google Gemini Init
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if google_api_key:
            self.google_client = genai.Client(api_key=google_api_key)
        else:
            print("Warning: GOOGLE_API_KEY not found.")
            self.google_client = None

        # 2. Anthropic Claude Init
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        else:
            print("Warning: ANTHROPIC_API_KEY not found.")
            self.anthropic_client = None

        # 3. Model Priority List (Provider, Model Name)
        # 우선순위: 
        # 1) Claude 4.5 Sonnet (최고 성능, 복잡한 문서 분석/한글에 강함)
        # 2) Gemini 2.5 Flash (빠르고 안정적, Quota 넉넉함)
        # 3) Gemini Flash Latest (레거시, 안정적)
        self.models = []
        
        if self.anthropic_client:
            self.models.append(('claude', 'claude-sonnet-4-5')) # Latest available Sonnet model
        
        if self.google_client:
            self.models.append(('gemini', 'gemini-2.5-flash'))
            self.models.append(('gemini', 'gemini-flash-latest'))
            self.models.append(('gemini', 'gemini-2.0-flash'))

    def _load_prompt_schema(self) -> str:
        try:
            from pathlib import Path
            schema_path = Path(__file__).parent.parent / "schemas" / "ocr_prompt_structure.json"
            with open(schema_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error loading OCR schema file: {e}")
            raise Exception(f"Failed to load OCR prompt schema: {e}")

    def _generate_prompt(self) -> str:
        json_structure = self._load_prompt_schema()
        return f"""
        You are an OCR and Business Document Intelligence Agent
        specialized in Korean transaction statements (거래명세서),
        coffee green bean invoices, and mixed Korean–English tables.

        You must prioritize ACCURATE recognition of Korean (Hangul),
        especially business terms, table headers, and contextual labels.

        ────────────────────────────────────────
        STEP 1. DOCUMENT TYPE VERIFICATION
        ────────────────────────────────────────
        Carefully inspect the image.

        If the image is NOT a business document
        (invoice, transaction statement, tax invoice, delivery note, purchase order),
        return ONLY the following JSON:
        {{
          "error": "INVALID_DOCUMENT"
        }}

        Do not explain.
        Do not add anything else.

        ────────────────────────────────────────
        STEP 2. FULL OCR TRANSCRIPTION (NO LOSS)
        ────────────────────────────────────────
        If the image IS a business document:

        1. Perform full OCR.
        2. Transcribe EVERY visible text into "debug_raw_text".
        3. Include:
           - Korean + English mixed text
           - Table headers and row values
           - Repeated values (e.g. 합계금액 appearing multiple times)
           - Parentheses text (예: 공급받는자용)
           - Units (kg, 원, ₩)
           - Stamps or seals (describe existence even if unreadable)
        4. Do NOT summarize.
        5. Preserve line order as much as possible.

        ────────────────────────────────────────
        STEP 3. ROLE INTERPRETATION (VERY IMPORTANT)
        ────────────────────────────────────────
        Korean transaction documents may reverse roles or place them horizontally/vertically.
        
        Interpret carefully based on labels:
        - "공급자", "매도인", "Seller" -> Supplier
        - "공급받는자", "매수인", "Buyer", "Receiver" -> Receiver

        DO NOT assume sender/receiver based on visual position alone (e.g. Left/Right varies).
        Follow the Korean labels exactly.
        
        *Self-Correction*: If 'The Moon Coffee' appears, it is likely the Receiver (us).

        ────────────────────────────────────────
        STEP 4. KOREAN BUSINESS TERM MAPPING
        ────────────────────────────────────────
        Map Korean terms contextually to the schema fields:

        - 거래명세서 = Transaction Statement
        - 등록번호 = Business Registration Number
        - 상호(법인명) = Company Name
        - 성명(대표) = Representative
        - 사업장 = Address
        - 업태 / 종목 = Business Type (put in additional_info or notes if no specific field)
        - 규격 = Specification / Package unit (e.g. 1kg)
        - 수량 = Quantity (Count of packages)
        - 중량 = Total Weight (if distinct from quantity)
        - 단가 = Unit Price
        - 공급가액 = Supply Amount (Line Amount EXCLUDING tax)
        - 세액/부가세 = Tax Amount
        - 합계금액 / 총액 = Total Amount (Supply + Tax)
        - 배송비 = Shipping cost (add as a line item or in additional_info)
        - 계약번호 / 계약일자 = Contract Number / Date

        ────────────────────────────────────────
        STEP 5. ITEM (COFFEE BEAN) INTELLIGENCE
        ────────────────────────────────────────
        Coffee item names often contain:
        - Origin (Colombia, Ethiopia)
        - Grade (G2, G4, Supremo, SHB)
        - Region (Huila, Sidamo, Yirgacheffe)
        - Process (Natural, Washed, Decaf)

        Rules:
        - "bean_name": Preserve original text (English/Korean mixed).
        - "bean_name_kr": Provide a clean Korean translation/transliteration if the original is English.
        - "origin": Extract country if inferable (e.g. 'Colombia' from 'Colombia Supremo').
        - "unit_price": Ensure this is the price PER UNIT, not the total line amount.

        ────────────────────────────────────────
        STEP 6. NORMALIZATION RULES
        ────────────────────────────────────────
        - Dates -> YYYY-MM-DD
        - Numbers -> Remove commas (1,000 -> 1000). Handle '0' vs 'null' correctly.
        - Currency -> Infer from context (₩, 원, KRW). Default to KRW if Korean text present.

        ────────────────────────────────────────
        FINAL OUTPUT (STRICT)
        ────────────────────────────────────────
        Return ONLY valid JSON using the following schema.
        Do NOT wrap the code in markdown blocks (```json ... ```).

        JSON SCHEMA:
        {json_structure}
        """

    def _clean_and_parse_json(self, text_result: str) -> Dict[str, Any]:
        import re
        text_result = text_result.strip()
        
        # Pattern to find a JSON block enclosed in triple backticks with optional language identifier
        code_block_pattern = r"```(?:json)?\s*({[\s\S]*?})\s*```"
        match = re.search(code_block_pattern, text_result)
        
        if match:
            json_str = match.group(1)
        else:
            # If no code block, try to find the outermost JSON object
            # This handles cases where the model returns just raw JSON but might have some noise
            # or if the markdown formatting is malformed.
            json_pattern = r"{[\s\S]*}"
            match_json = re.search(json_pattern, text_result)
            if match_json:
                json_str = match_json.group(0)
            else:
                # Last resort: try parsing the whole string (user might get a decode error if invalid)
                json_str = text_result

        return json.loads(json_str)

    def _call_gemini_sync(self, model_name: str, image_bytes: bytes, mime_type: str, prompt: str) -> str:
        response = self.google_client.models.generate_content(
            model=model_name,
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                prompt
            ]
        )
        return response.text

    def _call_claude_sync(self, model_name: str, image_bytes: bytes, mime_type: str, prompt: str) -> str:
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        message = self.anthropic_client.messages.create(
            model=model_name,
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,
                                "data": b64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ]
        )
        return message.content[0].text

    def analyze_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> Dict[str, Any]:
        if not self.models:
            raise Exception("No OCR models configured (Missing API Keys)")

        prompt = self._generate_prompt()
        last_exception = None

        for provider, model_name in self.models:
            print(f"🔄 Trying OCR with [{provider}] model: {model_name}...")
            try:
                text_result = ""
                if provider == 'gemini':
                    text_result = self._call_gemini_sync(model_name, image_bytes, mime_type, prompt)
                elif provider == 'claude':
                    text_result = self._call_claude_sync(model_name, image_bytes, mime_type, prompt)

                result = self._clean_and_parse_json(text_result)
                print(f"✅ OCR Success with {model_name}")
                return result

            except Exception as e:
                error_str = str(e)
                last_exception = e
                
                retry_codes = ["429", "503", "500", "529", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "Internal Server Error", "Overloaded"]
                
                if any(code in error_str for code in retry_codes):
                    print(f"⚠️ Transient Error ({error_str}) for {model_name}. Switching to next model...")
                    time.sleep(1)
                    continue
                
                print(f"❌ Error during OCR analysis ({model_name}): {e}")
                continue

        if last_exception:
            print("❌ All models exhausted quotas or failed.")
            raise Exception(f"OCR Failed on all providers: {last_exception}")

    async def analyze_image_stream(self, image_bytes: bytes, mime_type: str = "image/jpeg"):
        """
        Async Generator that yields status updates and finally the result.
        """
        if not self.models:
            yield {"status": "error", "message": "No OCR models configured"}
            return

        try:
            prompt = self._generate_prompt()
        except Exception as e:
            yield {"status": "error", "message": f"Failed to load OCR schema: {e}"}
            return

        last_exception = None

        for provider, model_name in self.models:
            provider_label = "Gemini" if provider == 'gemini' else "Claude"
            yield {"status": "progress", "message": f"{provider_label} ({model_name}) 모델로 분석 중..."}
            
            try:
                text_result = ""
                # Wrap sync calls in asyncio.to_thread to avoid blocking event loop
                import asyncio
                
                if provider == 'gemini':
                    text_result = await asyncio.to_thread(
                        self._call_gemini_sync, model_name, image_bytes, mime_type, prompt
                    )
                elif provider == 'claude':
                    text_result = await asyncio.to_thread(
                        self._call_claude_sync, model_name, image_bytes, mime_type, prompt
                    )

                print(f"📄 [OCR Raw] {provider} Response:\n{text_result[:500]}...") # Log first 500 chars

                result_json = self._clean_and_parse_json(text_result)
                yield {"status": "complete", "data": result_json}
                return

            except Exception as e:
                error_str = str(e)
                last_exception = e
                
                retry_codes = ["429", "503", "500", "529", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "Internal Server Error", "Overloaded"]
                
                if any(code in error_str for code in retry_codes):
                    print(f"⚠️ [OCR Stream] Transient Error for {model_name}: {e}")
                    yield {"status": "progress", "message": f"{provider_label} 일시적 오류. 다음 모델로 전환합니다..."}
                    await asyncio.sleep(1)
                    continue
                
                print(f"❌ [OCR Stream] Error for {model_name}: {e}")
                yield {"status": "progress", "message": f"{provider_label} 분석 실패: {e}. 다음 모델 시도..."}
                continue

        yield {"status": "error", "message": f"모든 분석 모델 시도 실패: {last_exception}"}
