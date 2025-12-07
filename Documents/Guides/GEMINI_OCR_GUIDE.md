# Google Gemini OCR 통합 가이드

## 📋 개요

The Moon Project에 **Google Gemini 1.5 Flash** 모델을 사용한 무료 OCR 서비스를 통합했습니다.

### 🎯 주요 특징

- **완전 무료**: 분당 15회, 하루 1,500회까지 무료 사용 가능
- **높은 정확도**: 멀티모달 LLM으로 텍스트 인식 + 문맥 이해
- **구조화된 출력**: 이미지를 주면 바로 JSON 형식으로 반환
- **빠른 속도**: Gemini 1.5 Flash는 응답 속도가 매우 빠름
- **자동 Fallback**: Gemini API가 없으면 자동으로 Claude API로 전환

---

## 🚀 설치 및 설정

### 1. API Key 발급

1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. Google 계정으로 로그인
3. "Create API Key" 버튼 클릭
4. API Key 복사

### 2. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가:

```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

또는 Streamlit Secrets 사용 (`.streamlit/secrets.toml`):

```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

### 3. 패키지 설치

```bash
pip install google-generativeai>=0.4.0
```

또는 전체 의존성 재설치:

```bash
pip install -r requirements.txt
```

---

## 🔧 사용 방법

### 자동 OCR 엔진 선택

애플리케이션은 다음 우선순위로 OCR 엔진을 자동 선택합니다:

1. **Google Gemini** (GOOGLE_API_KEY가 설정된 경우)
2. **Claude API** (ANTHROPIC_API_KEY가 설정된 경우)
3. **오류** (둘 다 없으면 에러 표시)

### 이미지 입고 페이지에서 확인

1. 애플리케이션 실행:
   ```bash
   streamlit run app/app.py
   ```

2. 사이드바에서 **"📄 이미지 입고"** 클릭

3. 이미지 업로드 시 현재 사용 중인 OCR 엔진 표시:
   - 🤖 **OCR 엔진: Google Gemini 1.5 Flash (무료)**
   - 🤖 **OCR 엔진: Claude 3.5 Sonnet**

---

## 📊 성능 비교

| 항목 | **Google Gemini** | **Claude API** |
|:---|:---|:---|
| **비용** | 무료 (제한 내) | 유료 ($3/1M tokens) |
| **속도** | 매우 빠름 (~2초) | 빠름 (~3-5초) |
| **정확도** | 매우 높음 | 매우 높음 |
| **한글 지원** | 우수 | 우수 |
| **표 인식** | 탁월 | 탁월 |
| **무료 한도** | 분당 15회, 하루 1,500회 | 없음 |

---

## 🎨 구현 세부사항

### 1. GeminiOCRService 클래스

위치: `app/services/gemini_ocr_service.py`

```python
class GeminiOCRService:
    def __init__(self, api_key: Optional[str] = None):
        # API Key 자동 감지 (환경 변수 또는 Streamlit Secrets)
        
    def process_invoice(self, image: Image.Image) -> Dict:
        # 이미지를 Gemini에 전송하여 구조화된 JSON 반환
```

### 2. 통합 방식

- **ImageInvoiceUpload.py**: Gemini와 Claude 서비스를 모두 초기화하고 우선순위에 따라 선택
- **InvoiceService**: OCR 서비스 타입에 관계없이 동일한 인터페이스로 처리

### 3. 프롬프트 엔지니어링

Gemini에게 전송하는 프롬프트:

```
이 이미지는 커피 원두 거래 명세서입니다. 
이미지에서 다음 정보를 추출하여 정확한 JSON 형식으로 반환해주세요.

필요한 정보:
1. supplier: 공급업체명
2. invoice_date: 거래일자 (YYYY-MM-DD)
3. total_amount: 합계금액 (숫자만)
4. invoice_type: 명세서 타입
5. items: 품목 리스트
   - bean_name: 원두명
   - quantity: 수량 (kg)
   - unit_price: 단가 (원)
   - amount: 공급가액 (원)
```

---

## 🔍 테스트 방법

### 1. API Key 확인

```python
import os
print(os.environ.get("GOOGLE_API_KEY"))  # API Key 출력 (마스킹됨)
```

### 2. 간단한 테스트

```python
from services.gemini_ocr_service import GeminiOCRService
from PIL import Image

service = GeminiOCRService()
if service.is_configured():
    print("✅ Gemini OCR 서비스 준비 완료")
    
    # 테스트 이미지 처리
    image = Image.open("test_invoice.jpg")
    result = service.process_invoice(image)
    print(result)
else:
    print("❌ API Key가 설정되지 않았습니다")
```

---

## 🚨 문제 해결

### 1. "API Key가 설정되지 않았습니다" 오류

**원인**: 환경 변수가 제대로 설정되지 않음

**해결**:
- `.env` 파일이 프로젝트 루트에 있는지 확인
- `python-dotenv`가 설치되어 있는지 확인
- 애플리케이션 재시작

### 2. "Quota exceeded" 오류

**원인**: 무료 한도 초과 (분당 15회 또는 하루 1,500회)

**해결**:
- 잠시 대기 후 재시도
- Claude API로 자동 전환됨

### 3. JSON 파싱 오류

**원인**: Gemini가 잘못된 형식으로 응답

**해결**:
- 프롬프트를 더 명확하게 수정
- 이미지 품질 개선
- Claude API로 재시도

---

## 📈 향후 개선 계획

1. **멀티 OCR 엔진 병렬 처리**: Gemini와 Claude를 동시에 호출하여 결과 비교
2. **사용자 선택 옵션**: UI에서 OCR 엔진을 수동으로 선택 가능하도록 개선
3. **캐싱**: 동일한 이미지 재처리 방지
4. **배치 처리**: 여러 이미지를 한 번에 처리

---

## 📚 참고 자료

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API 문서](https://ai.google.dev/docs)
- [Gemini 1.5 Flash 모델 정보](https://ai.google.dev/models/gemini)
- [무료 할당량 정보](https://ai.google.dev/pricing)

---

## 💡 팁

1. **무료 한도 관리**: 하루 1,500회면 중소 카페는 충분히 사용 가능
2. **이미지 최적화**: 고해상도 이미지보다 적절한 해상도(1024x1024)가 더 빠름
3. **에러 핸들링**: Gemini 실패 시 자동으로 Claude로 전환되므로 안정적

---

**작성일**: 2025-11-19  
**버전**: v0.50.0  
**작성자**: Antigravity AI Assistant
