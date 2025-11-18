# DeepSeek-OCR 통합 플랜

> **작성일**: 2025-11-18
> **버전**: 1.0.0
> **상태**: 검토 중 (Constitution 단계)

---

## 📋 목차

1. [Constitution (원칙)](#1-constitution-원칙)
2. [Specify (명세)](#2-specify-명세)
3. [Clarify (명확화)](#3-clarify-명확화)
4. [Plan (계획)](#4-plan-계획)
5. [Tasks (작업 분해)](#5-tasks-작업-분해)
6. [Implement (구현)](#6-implement-구현)
7. [Analyze (검증)](#7-analyze-검증)
8. [참고 자료](#참고-자료)

---

## 1. Constitution (원칙)

### 1.1 프로젝트 목표

거래 명세서(한글/영문 혼합) OCR 인식 정확도를 향상시키기 위해 DeepSeek-OCR을 통합하여 현재 EasyOCR 대비 성능을 개선한다.

### 1.2 기본 원칙

- **비교 우선**: 실제 명세서로 EasyOCR vs DeepSeek-OCR 정확도 비교 후 결정
- **호환성 유지**: 기존 OCRService API 인터페이스 유지 (하위 호환성)
- **점진적 전환**: 기존 EasyOCR 제거 금지 (옵션으로 선택 가능하게)
- **비용 고려**: DeepSeek-OCR API 호출 비용 vs 로컬 실행 성능 비교
- **한글 최적화**: 한국어 거래 명세서(GSC, HACIELO) 인식 정확도 우선

### 1.3 제약사항

| 제약 | 내용 |
|------|------|
| **환경** | WSL2, Python 3.12.3, ./venv 사용 필수 |
| **기존 시스템** | EasyOCR 기반 OCRService 유지 |
| **API 호출** | 외부 API 사용 시 비용/속도 고려 |
| **오프라인** | 로컬 실행 가능한 방법 우선 검토 |
| **데이터** | GSC/HACIELO 명세서 형식 지원 |

### 1.4 기술 스택 결정 원칙

- **검증 우선**: POC 테스트 후 기술 스택 확정
- **오픈소스 우선**: 가능하면 로컬 실행 가능한 오픈소스 모델
- **성능 측정**: CER/WER, 파싱 정확도, 처리 속도 정량적 비교
- **비용 분석**: API 호출 비용 vs GPU 로컬 실행 비용

---

## 2. Specify (명세)

### 2.1 기능 요구사항

#### FR-1: OCR 엔진 선택 옵션
- 사용자가 OCR 엔진 선택 가능 (EasyOCR / DeepSeek-OCR)
- 설정 페이지에서 기본 엔진 변경 가능

#### FR-2: DeepSeek-OCR 통합
- DeepSeek-OCR 모델을 로컬 또는 API로 사용
- 한글/영문 혼합 텍스트 추출
- 테이블 구조 인식 및 Markdown 출력 지원

#### FR-3: 성능 비교 리포트
- 동일 이미지에 대해 EasyOCR vs DeepSeek-OCR 결과 비교
- 인식 정확도, 신뢰도, 처리 시간 비교
- 파싱 성공률 비교

#### FR-4: 하위 호환성
- 기존 `OCRService.extract_text_from_image()` API 유지
- 기존 코드 수정 최소화

### 2.2 입출력 명세

#### 입력
- **이미지**: PIL.Image 객체 (거래 명세서 사진)
- **OCR 엔진**: 'easyocr' | 'deepseek'
- **전처리 옵션**: bool (이미지 전처리 수행 여부)

#### 출력
```python
{
    'text': str,           # 추출된 전체 텍스트
    'words': List[Dict],   # 단어별 상세 정보 (bbox, confidence)
    'confidence': float,   # 평균 신뢰도 (0~100)
    'engine': str,         # 사용된 OCR 엔진
    'processing_time': float  # 처리 시간 (초)
}
```

### 2.3 데이터 구조

#### DeepSeek-OCR 설정
```python
# .env 파일 추가
DEEPSEEK_OCR_MODE=local  # 'local' | 'api'
DEEPSEEK_API_KEY=your_api_key_here  # API 모드일 때만
DEEPSEEK_MODEL_PATH=./models/deepseek-ocr  # 로컬 모드일 때
```

#### 비교 리포트 구조
```python
{
    'image_path': str,
    'engines': {
        'easyocr': {
            'text': str,
            'confidence': float,
            'processing_time': float,
            'parsed_data': Dict,
            'success': bool
        },
        'deepseek': {
            'text': str,
            'confidence': float,
            'processing_time': float,
            'parsed_data': Dict,
            'success': bool
        }
    },
    'comparison': {
        'text_similarity': float,  # 텍스트 유사도 (0~1)
        'parsing_match': bool,     # 파싱 결과 일치 여부
        'winner': str              # 'easyocr' | 'deepseek' | 'tie'
    }
}
```

---

## 3. Clarify (명확화)

### 3.1 사용자에게 확인 필요한 사항

#### Q1: DeepSeek-OCR 실행 방식
**질문**: DeepSeek-OCR을 어떻게 실행하시겠습니까?

**옵션**:
1. **로컬 실행** (Transformers + vLLM)
   - 장점: API 비용 없음, 오프라인 가능, 무제한 사용
   - 단점: GPU 필요 (추론 속도), 초기 모델 다운로드 (~수GB)
   - 요구사항: CUDA GPU (권장: RTX 3060 이상)

2. **API 호출** (Replicate / Clarifai)
   - 장점: GPU 불필요, 빠른 시작, 관리 편리
   - 단점: 호출당 비용, 인터넷 필요, 속도 제한
   - 비용 예상: 이미지당 $0.01~0.05

3. **하이브리드** (로컬 + API 백업)
   - 장점: 로컬 우선 사용, 실패 시 API 백업
   - 단점: 구현 복잡도 증가

#### Q2: 성능 테스트 범위
**질문**: POC 테스트 시 어떤 명세서로 테스트하시겠습니까?

**옵션**:
1. **GSC 명세서** (5~10장)
2. **HACIELO 명세서** (5~10장)
3. **둘 다** (10~20장)

#### Q3: 기준 정확도
**질문**: DeepSeek-OCR이 EasyOCR보다 얼마나 더 정확해야 전환하시겠습니까?

**옵션**:
1. **5% 이상** 정확도 향상
2. **10% 이상** 정확도 향상
3. **파싱 성공률** 기준 (80% → 90%)

---

## 4. Plan (계획)

### 4.1 아키텍처 설계

#### 4.1.1 OCR 엔진 추상화

```
OCRService (기존)
├── EasyOCREngine (기존)
│   └── easyocr.Reader
└── DeepSeekOCREngine (신규)
    ├── LocalEngine (Transformers + vLLM)
    └── APIEngine (Replicate / Clarifai)
```

#### 4.1.2 클래스 다이어그램

```python
# app/services/ocr_engines/base.py
class BaseOCREngine(ABC):
    @abstractmethod
    def extract_text(self, image: Image.Image) -> Dict:
        pass

# app/services/ocr_engines/easyocr_engine.py
class EasyOCREngine(BaseOCREngine):
    def __init__(self):
        self.reader = easyocr.Reader(['ko', 'en'])

    def extract_text(self, image: Image.Image) -> Dict:
        # 기존 로직

# app/services/ocr_engines/deepseek_engine.py
class DeepSeekOCREngine(BaseOCREngine):
    def __init__(self, mode='local'):
        if mode == 'local':
            self.engine = LocalDeepSeekEngine()
        else:
            self.engine = APIDeepSeekEngine()

    def extract_text(self, image: Image.Image) -> Dict:
        # DeepSeek-OCR 로직

# app/services/ocr_service.py (수정)
class OCRService:
    def __init__(self, db: Session, engine='easyocr'):
        if engine == 'easyocr':
            self.engine = EasyOCREngine()
        elif engine == 'deepseek':
            self.engine = DeepSeekOCREngine()
```

### 4.2 DB 스키마 변경 (선택)

#### 신규 테이블: `ocr_comparison_logs`

```sql
CREATE TABLE ocr_comparison_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT NOT NULL,
    engine_name TEXT NOT NULL,  -- 'easyocr' | 'deepseek'
    ocr_text TEXT,
    confidence REAL,
    processing_time REAL,
    success BOOLEAN,
    parsed_data TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4.3 파일 구조

```
TheMoon_Project/
├── app/
│   ├── services/
│   │   ├── ocr_service.py (수정)
│   │   └── ocr_engines/
│   │       ├── __init__.py
│   │       ├── base.py (신규)
│   │       ├── easyocr_engine.py (신규)
│   │       └── deepseek_engine.py (신규)
│   ├── pages/
│   │   └── OCRComparison.py (신규 - 비교 테스트 페이지)
│   └── models/
│       └── database.py (OCRComparisonLog 모델 추가)
├── data/
│   ├── test_invoices/  (신규 - POC 테스트용)
│   │   ├── gsc_*.png
│   │   └── hacielo_*.png
│   └── ocr_comparison_reports/  (신규 - 비교 리포트)
├── Documents/
│   └── Planning/
│       └── DEEPSEEK_OCR_INTEGRATION_PLAN.md (이 문서)
└── .env (수정)
```

---

## 5. Tasks (작업 분해)

### Phase 1: 환경 설정 및 POC (1~2일)

- [ ] **Task 1.1**: DeepSeek-OCR 기술 검증
  - [ ] Hugging Face 모델 다운로드 테스트
  - [ ] 로컬 추론 테스트 (GPU 사용 시)
  - [ ] API 접근 테스트 (Replicate / Clarifai)
  - [ ] 한글 텍스트 인식 테스트

- [ ] **Task 1.2**: POC 테스트 데이터 준비
  - [ ] GSC 명세서 5장 수집
  - [ ] HACIELO 명세서 5장 수집
  - [ ] `data/test_invoices/` 폴더 생성 및 저장

- [ ] **Task 1.3**: 간단한 비교 스크립트 작성
  - [ ] `scripts/compare_ocr_engines.py` 작성
  - [ ] EasyOCR vs DeepSeek-OCR 결과 비교
  - [ ] 정확도, 신뢰도, 처리 시간 측정
  - [ ] 리포트 생성 (JSON/Markdown)

### Phase 2: 통합 설계 (1일)

- [ ] **Task 2.1**: OCR 엔진 추상화
  - [ ] `app/services/ocr_engines/base.py` 작성
  - [ ] `BaseOCREngine` 추상 클래스 정의

- [ ] **Task 2.2**: EasyOCR 리팩토링
  - [ ] `app/services/ocr_engines/easyocr_engine.py` 작성
  - [ ] 기존 OCRService 로직 이동

- [ ] **Task 2.3**: DeepSeek-OCR 엔진 구현
  - [ ] `app/services/ocr_engines/deepseek_engine.py` 작성
  - [ ] 로컬 모드 구현 (Transformers)
  - [ ] API 모드 구현 (Replicate 또는 Clarifai)

### Phase 3: OCRService 업데이트 (1일)

- [ ] **Task 3.1**: OCRService 수정
  - [ ] 엔진 선택 파라미터 추가
  - [ ] `extract_text_from_image()` 수정 (엔진 선택 지원)
  - [ ] 하위 호환성 테스트

- [ ] **Task 3.2**: 설정 파일 업데이트
  - [ ] `.env`에 DeepSeek-OCR 설정 추가
  - [ ] `app/config.py` 업데이트 (있을 경우)

### Phase 4: UI 추가 (1일)

- [ ] **Task 4.1**: OCR 비교 페이지 추가
  - [ ] `app/pages/OCRComparison.py` 작성
  - [ ] 이미지 업로드 → 두 엔진 동시 실행 → 결과 비교
  - [ ] 신뢰도, 처리 시간, 파싱 결과 시각화

- [ ] **Task 4.2**: 설정 페이지 업데이트
  - [ ] `app/pages/Settings.py` 수정
  - [ ] 기본 OCR 엔진 선택 옵션 추가

### Phase 5: 테스트 및 검증 (1일)

- [ ] **Task 5.1**: 단위 테스트 작성
  - [ ] `app/tests/test_ocr_engines.py` 작성
  - [ ] EasyOCR / DeepSeek-OCR 각각 테스트

- [ ] **Task 5.2**: 통합 테스트
  - [ ] 실제 명세서 10장으로 비교 테스트
  - [ ] 정확도 리포트 생성

- [ ] **Task 5.3**: 성능 테스트
  - [ ] 100장 처리 시간 측정
  - [ ] 메모리 사용량 측정

### Phase 6: 문서화 및 배포 (0.5일)

- [ ] **Task 6.1**: 문서 업데이트
  - [ ] `README.md` 업데이트 (DeepSeek-OCR 설정 안내)
  - [ ] `Documents/Architecture/SYSTEM_ARCHITECTURE.md` 업데이트
  - [ ] `Documents/Guides/OCR_SETUP_GUIDE.md` 작성

- [ ] **Task 6.2**: 버전 관리
  - [ ] `logs/CHANGELOG.md` 업데이트
  - [ ] 버전 업데이트 (Minor: 0.50.0 → 0.51.0)

---

## 6. Implement (구현)

### 6.1 POC 스크립트 예시

```python
# scripts/compare_ocr_engines.py
import time
from PIL import Image
from pathlib import Path

# EasyOCR
import easyocr
reader_easy = easyocr.Reader(['ko', 'en'])

# DeepSeek-OCR (Transformers)
from transformers import AutoProcessor, AutoModel
processor = AutoProcessor.from_pretrained("deepseek-ai/DeepSeek-OCR")
model = AutoModel.from_pretrained("deepseek-ai/DeepSeek-OCR")

def test_easyocr(image_path):
    img = Image.open(image_path)
    start = time.time()
    results = reader_easy.readtext(np.array(img))
    elapsed = time.time() - start
    text = '\n'.join([r[1] for r in results])
    return {'text': text, 'time': elapsed}

def test_deepseek(image_path):
    img = Image.open(image_path)
    start = time.time()
    inputs = processor(images=img, text="<image>\nFree OCR.", return_tensors="pt")
    outputs = model.generate(**inputs)
    text = processor.decode(outputs[0], skip_special_tokens=True)
    elapsed = time.time() - start
    return {'text': text, 'time': elapsed}

# 비교 실행
for img_path in Path('data/test_invoices').glob('*.png'):
    result_easy = test_easyocr(img_path)
    result_deepseek = test_deepseek(img_path)

    print(f"\n=== {img_path.name} ===")
    print(f"EasyOCR: {len(result_easy['text'])} chars, {result_easy['time']:.2f}s")
    print(f"DeepSeek: {len(result_deepseek['text'])} chars, {result_deepseek['time']:.2f}s")
```

### 6.2 DeepSeek-OCR 엔진 구현 예시

```python
# app/services/ocr_engines/deepseek_engine.py
from typing import Dict
from PIL import Image
import numpy as np
import time

class DeepSeekOCREngine:
    def __init__(self, mode='local'):
        self.mode = mode
        if mode == 'local':
            from transformers import AutoProcessor, AutoModel
            self.processor = AutoProcessor.from_pretrained("deepseek-ai/DeepSeek-OCR")
            self.model = AutoModel.from_pretrained("deepseek-ai/DeepSeek-OCR")
        else:
            # API 모드 (Replicate 등)
            import replicate
            self.replicate = replicate

    def extract_text(self, image: Image.Image) -> Dict:
        """
        DeepSeek-OCR로 텍스트 추출

        Returns:
            {
                'text': str,
                'words': List[Dict],
                'confidence': float,
                'processing_time': float
            }
        """
        start = time.time()

        if self.mode == 'local':
            # 로컬 추론
            inputs = self.processor(
                images=image,
                text="<image>\nFree OCR.",
                return_tensors="pt"
            )
            outputs = self.model.generate(**inputs)
            text = self.processor.decode(outputs[0], skip_special_tokens=True)
        else:
            # API 호출 (Replicate)
            output = self.replicate.run(
                "lucataco/deepseek-ocr",
                input={"image": image}
            )
            text = output

        elapsed = time.time() - start

        return {
            'text': text,
            'words': [],  # DeepSeek-OCR은 bbox 정보 없음
            'confidence': 95.0,  # 임시 값 (실제 신뢰도는 별도 계산)
            'processing_time': elapsed
        }
```

---

## 7. Analyze (검증)

### 7.1 검증 기준

#### 정확도 검증
- **CER/WER**: Character Error Rate / Word Error Rate
- **파싱 성공률**: 전체 명세서 중 정상 파싱 비율
- **필드 정확도**: 날짜, 금액, 원두명 인식 정확도

#### 성능 검증
- **처리 시간**: 이미지당 평균 처리 시간 (초)
- **메모리 사용량**: 최대 메모리 사용량 (MB)
- **GPU 사용량**: GPU 메모리 사용량 (로컬 실행 시)

#### 비용 검증 (API 모드)
- **API 호출 비용**: 이미지당 비용
- **월 예상 비용**: 월 1000장 처리 시 예상 비용

### 7.2 검증 체크리스트

- [ ] POC 테스트 완료 (10장 이상)
- [ ] EasyOCR 대비 정확도 비교 완료
- [ ] 처리 시간 비교 완료
- [ ] 메모리/비용 분석 완료
- [ ] 사용자 결정: DeepSeek-OCR 도입 여부 확정

### 7.3 예상 결과 시나리오

#### 시나리오 A: DeepSeek-OCR 승리
- **조건**: 파싱 성공률 10% 이상 향상
- **Action**: Phase 2~6 진행 (통합 구현)

#### 시나리오 B: EasyOCR 승리
- **조건**: DeepSeek-OCR이 5% 미만 향상 또는 더 나쁨
- **Action**: 통합 중단, 현재 시스템 유지

#### 시나리오 C: 비슷함
- **조건**: 차이 5% 이내
- **Action**: 비용/속도 고려하여 최종 결정

---

## 참고 자료

### 공식 문서
- [DeepSeek-OCR GitHub](https://github.com/deepseek-ai/DeepSeek-OCR)
- [DeepSeek-OCR Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- [DeepSeek-OCR Paper (arXiv)](https://arxiv.org/html/2510.18234v1)

### API 서비스
- [Replicate API](https://replicate.com/lucataco/deepseek-ocr)
- [Clarifai API](https://www.clarifai.com/blog/run-deepseek-ocr-with-an-api)

### 기술 리뷰
- [DeepSeek-OCR vs Traditional OCR Tools (2025)](https://skywork.ai/blog/llm/deepseek-ocr-vs-traditional-ocr-tools-which-one-is-better-2025/)
- [12 Best DeepSeek-OCR Use Cases (2025)](https://skywork.ai/blog/ai-agent/deepseek-ocr-use-cases-2025/)
- [DeepSeek-OCR in Invoice Processing](https://skywork.ai/blog/llm/deepseek-ocr-in-invoice-processing-automating-finance-workflows/)

### 현재 시스템 문서
- `app/services/ocr_service.py` - 현재 OCR 서비스 (EasyOCR 기반)
- `Documents/Architecture/SYSTEM_ARCHITECTURE.md` - 시스템 아키텍처
- `Documents/Architecture/DEVELOPMENT_GUIDE.md` - 개발 가이드

---

## 변경 이력

| 날짜 | 버전 | 내용 |
|------|------|------|
| 2025-11-18 | 1.0.0 | 초안 작성 (Constitution ~ Tasks 단계) |

---

**다음 단계**: 사용자 확인 후 POC 테스트 진행 (Phase 1)
