import json
import os
import time
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

import base64

import anthropic


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

    def _get_active_models(self) -> list[tuple[str, str]]:
        """
        ConfigService에서 우선순위 목록을 가져와
        현재 사용 가능한(API Key가 있는) (provider, model_name) 리스트를 반환
        """
        from app.services.config_service import config_service

        active_models = []
        priority_list = config_service.get_ocr_config().model_priority

        for model_name in priority_list:
            provider = self._resolve_provider(model_name)

            if provider == "gemini" and self.google_client:
                active_models.append((provider, model_name))
            elif provider == "claude" and self.anthropic_client:
                active_models.append((provider, model_name))
            else:
                # Provider not supported or Client not initialized
                continue

        return active_models

    def _resolve_provider(self, model_name: str) -> str:
        if model_name.startswith("claude"):
            return "claude"
        return "gemini"  # Default to gemini for 'gemini-*' or others

    def _generate_prompt(self) -> str:
        from app.services.config_service import config_service

        # Pydantic model -> dict -> json dump for prompt injection
        prompt_structure_obj = config_service.get_ocr_config().prompt_structure
        json_structure = prompt_structure_obj.model_dump_json(indent=2)

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

        if the image is NOT a business document
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

        1. First, analyze the overall structure (tables, headers, footer).
           - Understand that columns may be miss-aligned. Look for coordinates implicitly.
        2. Perform full OCR.
        3. Transcribe EVERY visible text into "debug_raw_text".
        4. Include:
           - Korean + English mixed text
           - Table headers and row values
           - Repeated values (e.g. 합계금액 appearing multiple times)
           - Parentheses text (예: 공급받는자용)
           - Units (kg, 원, ₩)
           - Stamps or seals (describe existence even if unreadable)
        5. Do NOT summarize.
        6. Preserve line order as much as possible.

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
        STEP 4. KOREAN BUSINESS TERM MAPPING & TYPO CORRECTION
        ────────────────────────────────────────
        Map Korean terms contextually to the schema fields.
        
        [CRITICAL: TYPO CORRECTION]
        - Correct obvious Korean typos based on context (e.g., '코피' -> '커피', '원두명' -> '품명').
        - Do not hallucinate, but fix single-character OCR errors if the meaning is clear.

        Mappings:
        - 거래명세서 = Transaction Statement
        - 등록번호 = Business Registration Number
        - 상호(법인명) = Company Name
        - 성명(대표) = Representative
        - 사업장 = Address
        - 업태 / 종목 = Business Type (put in additional_info or notes if no specific field)
        - 규격 = Specification / Package unit (e.g. 1kg)
        - 수량 = Quantity / Count (Integer). 
          * [WARNING] Do NOT confuse with Total Weight.
          * If value is 1-100 (integer) -> Quantity.
          * If value has 'kg' (e.g. 40kg) -> Total Weight.
        - 중량/총중량 = Total Weight (kg).
          * [CRITICAL] Map '40kg', '20kg' etc. to "total_weight".
          * NEVER map a weight value (e.g. 40kg) to "quantity" (e.g. 2).
          * Do NOT calculate bag count unless explicitly stated.
        - 단가 = Unit Price
        - 공급가액 = Supply Amount (Line Amount EXCLUDING tax)
        - 세액/부가세 = Tax Amount
        - 합계금액 / 총액 = Total Amount (Supply + Tax)
        [SPECIAL RULE: SUPPLIER NAME & BRANDING]
        - The Supplier Name (상호) is commonly the LOGO or HUGE TEXT at the very top.
        - **SPECIFIC OVERRIDE**: If you see "LACIELO", "L A C I E L O", "라씨엘로", or similar, SET "supplier_name" to "LACIELO".
        - If you see "COFFEE ZIP", "커피집", SET "supplier_name" to "COFFEE ZIP".
        - If you see "Almacielo", "알마씨엘로", SET "supplier_name" to "Almacielo".
        - If the document starts with a prominent English or Korean brand name, treat it as the "supplier_name".
        - Do not ignore the header/logo text.
        - If "공급자" section exists, prioritize the "상호(법인명)" value in that section.
        - If no clear "supplier_name" is found, leave it as null.

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
        STEP 5-1. ORDER NUMBER EXTRACTION (CRITICAL)
        ────────────────────────────────────────
        If the document contains MULTIPLE order numbers for different items:

        1. Each item MUST include its corresponding "order_number" field.
        2. Format: YYYYMMDD-XXXXX (e.g., "20251108-8B7C2")
        3. Extract from context (date + identifier pattern).
        4. Look for patterns in:
           - Table columns labeled "주문번호", "Order No", "발주번호"
           - Row headers or item descriptions
           - Sections grouped by order
        5. Validation:
           - Verify format: YYYYMMDD-XXXXX
           - Date must be valid (YYYY=year, MM=01-12, DD=01-31)
        6. Fallback:
           - If no order number found: use null
           - If single order for entire document: extract once and apply to all items
           - When uncertain: prefer null over incorrect extraction

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

    def _post_process_ocr_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        OCR 결과를 후처리하여 주문별로 그룹화 및 누락된 정보 보완
        """
        import re

        # Fallback: Check debug_raw_text for Supplier Name if missing
        supplier_data = result.get("supplier", {})
        if not supplier_data:
            supplier_data = {}
            result["supplier"] = supplier_data
        
        current_name = supplier_data.get("name")
        raw_text = result.get("debug_raw_text", "")

        if not current_name and raw_text:
            # Check for known suppliers in the first few lines of raw text
            # Simply check if the keyword exists in the first 1000 chars to cover headers
            head_text = raw_text[:1000].upper()
            
            if any(k in head_text for k in ["LACIELO", "L A C I E L O", "라씨엘로", "LACIELOR", "LACIEL0"]):
                supplier_data["name"] = "LACIELO"
                result["supplier_name"] = "LACIELO" # Populate top-level as well for convenience
            elif "COFFEE ZIP" in head_text or "커피집" in head_text:
                supplier_data["name"] = "COFFEE ZIP"
            elif "ALMACIELO" in head_text or "알마씨엘로" in head_text:
                supplier_data["name"] = "Almacielo"
            elif "THE MOON" in head_text:
                supplier_data["name"] = "The Moon Coffee"

        items = result.get("items", [])

        if not items:
            result["has_multiple_orders"] = False
            result["total_order_count"] = 0
            result["order_groups"] = []
            return result

        # 주문번호로 그룹화
        order_groups = {}

        for item in items:
            order_num = item.get("order_number") or "UNKNOWN"

            if order_num not in order_groups:
                order_groups[order_num] = {
                    "order_number": order_num,
                    "order_date": None,
                    "items": [],
                    "subtotal": 0,
                }

            order_groups[order_num]["items"].append(item)
            order_groups[order_num]["subtotal"] += item.get("amount", 0)

        # 주문 날짜 추출 (YYYYMMDD-XXXXX 형식에서)
        for group in order_groups.values():
            order_num = group["order_number"]
            # YYYYMMDD-XXXXX 형식 파싱
            match = re.match(r"^(\d{4})(\d{2})(\d{2})", order_num)
            if match:
                year, month, day = match.groups()
                group["order_date"] = f"{year}-{month}-{day}"

        # 결과 enrichment
        order_groups_list = list(order_groups.values())
        result["has_multiple_orders"] = len(order_groups_list) > 1
        result["total_order_count"] = len(order_groups_list)
        result["order_groups"] = order_groups_list

        return result

    def _call_gemini_sync(
        self, model_name: str, image_bytes: bytes, mime_type: str, prompt: str
    ) -> str:
        response = self.google_client.models.generate_content(
            model=model_name,
            contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type), prompt],
        )
        return response.text

    def _call_claude_sync(
        self, model_name: str, image_bytes: bytes, mime_type: str, prompt: str
    ) -> str:
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
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return message.content[0].text

    def analyze_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> Dict[str, Any]:
        models = self._get_active_models()
        if not models:
            raise Exception("No OCR models configured (Missing API Keys)")

        prompt = self._generate_prompt()
        last_exception = None

        for provider, model_name in models:
            print(f"🔄 Trying OCR with [{provider}] model: {model_name}...")
            try:
                text_result = ""
                if provider == "gemini":
                    text_result = self._call_gemini_sync(model_name, image_bytes, mime_type, prompt)
                elif provider == "claude":
                    text_result = self._call_claude_sync(model_name, image_bytes, mime_type, prompt)

                result = self._clean_and_parse_json(text_result)
                print(f"✅ OCR Success with {model_name}")
                return result

            except Exception as e:
                error_str = str(e)
                last_exception = e

                retry_codes = [
                    "429",
                    "503",
                    "500",
                    "529",
                    "RESOURCE_EXHAUSTED",
                    "UNAVAILABLE",
                    "Internal Server Error",
                    "Overloaded",
                ]

                if any(code in error_str for code in retry_codes):
                    print(
                        f"⚠️ Transient Error ({error_str}) for {model_name}. Switching to next model..."
                    )
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
        models = self._get_active_models()
        if not models:
            yield {"status": "error", "message": "No OCR models configured"}
            return

        try:
            prompt = self._generate_prompt()
        except Exception as e:
            yield {"status": "error", "message": f"Failed to load OCR schema: {e}"}
            return

        last_exception = None

        for provider, model_name in models:
            provider_label = "Gemini" if provider == "gemini" else "Claude"
            yield {
                "status": "progress",
                "message": f"{provider_label} ({model_name}) 모델로 분석 중...",
            }

            try:
                text_result = ""
                # Wrap sync calls in asyncio.to_thread to avoid blocking event loop
                import asyncio

                if provider == "gemini":
                    text_result = await asyncio.to_thread(
                        self._call_gemini_sync, model_name, image_bytes, mime_type, prompt
                    )
                elif provider == "claude":
                    text_result = await asyncio.to_thread(
                        self._call_claude_sync, model_name, image_bytes, mime_type, prompt
                    )

                print(
                    f"📄 [OCR Raw] {provider} Response:\n{text_result[:500]}..."
                )  # Log first 500 chars

                result_json = self._clean_and_parse_json(text_result)

                # 🆕 후처리: 주문별 그룹화
                result_json = self._post_process_ocr_result(result_json)

                yield {"status": "complete", "data": result_json}
                return

            except Exception as e:
                error_str = str(e)
                last_exception = e

                retry_codes = [
                    "429",
                    "503",
                    "500",
                    "529",
                    "RESOURCE_EXHAUSTED",
                    "UNAVAILABLE",
                    "Internal Server Error",
                    "Overloaded",
                ]

                if any(code in error_str for code in retry_codes):
                    print(f"⚠️ [OCR Stream] Transient Error for {model_name}: {e}")
                    yield {
                        "status": "progress",
                        "message": f"{provider_label} 일시적 오류. 다음 모델로 전환합니다...",
                    }
                    await asyncio.sleep(1)
                    continue

                print(f"❌ [OCR Stream] Error for {model_name}: {e}")
                yield {
                    "status": "progress",
                    "message": f"{provider_label} 분석 실패: {e}. 다음 모델 시도...",
                }
                continue

        yield {"status": "error", "message": f"모든 분석 모델 시도 실패: {last_exception}"}
