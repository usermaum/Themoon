"""
Google Gemini API 기반 OCR 서비스
이미지를 분석하여 거래 명세서 데이터를 구조화된 JSON으로 추출합니다.
"""

import os
import json
import google.generativeai as genai
from PIL import Image
from typing import Dict, Optional
from datetime import datetime
import streamlit as st

class GeminiOCRService:
    """
    Google Gemini API를 사용한 지능형 OCR 서비스
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: Google API Key (없으면 환경 변수 GOOGLE_API_KEY 사용)
        """
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            # Streamlit secrets에서 시도
            try:
                self.api_key = st.secrets["GOOGLE_API_KEY"]
            except:
                pass
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    def process_invoice(self, image: Image.Image) -> Dict:
        """
        거래 명세서 이미지 처리

        Args:
            image: PIL Image 객체

        Returns:
            Dict: 구조화된 명세서 데이터
        """
        if not self.model:
            return {
                "error": "Google API Key가 설정되지 않았습니다.",
                "invoice_type": "UNKNOWN",
                "items": []
            }

        try:
            # 프롬프트 작성
            prompt = """
            이 이미지는 커피 원두 거래 명세서입니다. 
            이미지에서 다음 정보를 추출하여 정확한 JSON 형식으로 반환해주세요.
            다른 텍스트 없이 오직 JSON만 출력하세요.

            필요한 정보:
            1. supplier: 공급업체명 (예: GSC, HACIELO 등)
            2. invoice_date: 거래일자 (YYYY-MM-DD 형식)
            3. total_amount: 합계금액 (숫자만)
            4. invoice_type: 명세서 타입 ('GSC', 'HACIELO', 'UNKNOWN' 중 하나)
            5. items: 품목 리스트 (배열)
               - bean_name: 원두명 (이미지에 표시된 원본 이름 그대로, 영문이면 영문 그대로)
               - bean_name_kr: 원두명 한글 번역 (영문 원두명을 한글로 번역, 예: "Colombia Supremo" -> "콜롬비아 수프리모")
               - quantity: 수량 (kg 단위 숫자, '10kg' -> 10)
               - unit_price: 단가 (원 단위 숫자)
               - amount: 공급가액 (원 단위 숫자)
               - origin: 원산지 (가능한 경우, 영문)
            
            주의사항:
            - bean_name은 이미지에 표시된 원본 이름을 정확히 그대로 적어주세요 (번역하지 마세요)
            - bean_name_kr은 bean_name을 한글로 번역한 값입니다
            - 날짜 형식을 반드시 지켜주세요 (YYYY-MM-DD)
            - 숫자에 콤마(,)가 있으면 제거하고 숫자형으로 변환하세요
            - 원두명은 가능한 상세하게 적어주세요
            
            예시:
            {
              "supplier": "GSC GREEN COFFEE",
              "invoice_date": "2025-11-19",
              "total_amount": 1500000,
              "invoice_type": "GSC",
              "items": [
                {
                  "bean_name": "Colombia Supremo Huila",
                  "bean_name_kr": "콜롬비아 수프리모 우일라",
                  "quantity": 30,
                  "unit_price": 14500,
                  "amount": 435000,
                  "origin": "Colombia"
                }
              ]
            }
            """

            # Gemini API 호출
            response = self.model.generate_content([prompt, image])

            # finish_reason 확인 (응답 거부 시 처리)
            if not response.candidates or not response.candidates[0].content.parts:
                finish_reason = response.candidates[0].finish_reason if response.candidates else "UNKNOWN"
                return {
                    "error": f"Gemini API가 응답을 생성하지 못했습니다 (finish_reason: {finish_reason}). 이미지 품질을 확인하거나 Claude API를 사용해주세요.",
                    "invoice_type": "UNKNOWN",
                    "items": [],
                    "ocr_text": f"응답 거부 (finish_reason: {finish_reason})",
                    "warnings": ["Gemini API가 이미지를 처리할 수 없습니다. 이미지가 너무 작거나 품질이 낮을 수 있습니다."]
                }

            # 디버그: 원본 응답 저장
            raw_response_text = response.text
            
            # 응답 텍스트 정리 (JSON 코드 블록 제거)
            response_text = raw_response_text
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            # JSON 파싱
            result = json.loads(response_text.strip())
            
            # 결과 보정 및 메타데이터 추가
            result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result['confidence'] = 95.0  # Gemini는 신뢰도 점수를 직접 주지 않으므로 임의 설정
            
            # OCR 원본 텍스트 추가 (디버그용)
            result['ocr_text'] = raw_response_text
            result['ocr_confidence'] = 95.0
            
            # 경고 메시지 생성
            warnings = []
            if not result.get('invoice_date'):
                warnings.append("⚠️ 거래일자를 찾을 수 없습니다")
            if not result.get('supplier'):
                warnings.append("⚠️ 공급업체명을 찾을 수 없습니다")
            if not result.get('items') or len(result.get('items', [])) == 0:
                warnings.append("⚠️ 원두 항목을 찾을 수 없습니다")
            
            result['warnings'] = warnings
            
            # invoice_date 문자열을 date 객체로 변환
            from datetime import date
            invoice_date_str = result.get('invoice_date')
            invoice_date_obj = None
            
            if invoice_date_str:
                try:
                    # YYYY-MM-DD 형식 파싱
                    if isinstance(invoice_date_str, str):
                        parts = invoice_date_str.split('-')
                        if len(parts) == 3:
                            invoice_date_obj = date(int(parts[0]), int(parts[1]), int(parts[2]))
                    elif isinstance(invoice_date_str, date):
                        invoice_date_obj = invoice_date_str
                except Exception as e:
                    warnings.append(f"⚠️ 날짜 변환 실패: {str(e)}")
            
            # invoice_data 구조 생성 (InvoiceService와 호환)
            result['invoice_data'] = {
                'supplier': result.get('supplier'),
                'invoice_date': invoice_date_obj,  # date 객체로 변환됨
                'total_amount': result.get('total_amount'),
                'invoice_type': result.get('invoice_type', 'UNKNOWN')
            }
            
            return result

        except json.JSONDecodeError as e:
            return {
                "error": f"JSON 파싱 오류: {str(e)}",
                "raw_response": raw_response_text if 'raw_response_text' in locals() else "응답 없음",
                "invoice_type": "UNKNOWN",
                "items": [],
                "ocr_text": raw_response_text if 'raw_response_text' in locals() else "응답 없음",
                "warnings": ["JSON 파싱에 실패했습니다. 원본 응답을 확인하세요."]
            }
        except Exception as e:
            return {
                "error": f"Gemini 처리 중 오류 발생: {str(e)}",
                "invoice_type": "UNKNOWN",
                "items": [],
                "ocr_text": f"오류: {str(e)}",
                "warnings": [f"처리 중 오류가 발생했습니다: {str(e)}"]
            }

    def is_configured(self) -> bool:
        """API 키 설정 여부 확인"""
        return bool(self.api_key)
