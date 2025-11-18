# 세션 요약 - 2025-11-18

> **버전**: v0.50.0
> **세션 시작**: 2025-11-18
> **세션 종료**: 2025-11-18
> **작업 시간**: ~1시간

---

## 🎯 오늘 한 일

### 주요 작업: DeepSeek-OCR 통합 가능성 검토 및 플랜 작성

오늘은 거래 명세서 OCR 인식 정확도를 개선하기 위해 DeepSeek-OCR 기술을 조사하고 통합 플랜을 작성했습니다.

---

## ✅ 완료된 작업

### 1. DeepSeek-OCR 기술 조사
- **WebSearch**: DeepSeek-OCR API 문서 및 한글 지원 여부 조사
- **주요 발견사항**:
  - 한글 포함 100개 이상 언어 지원 (자동 감지)
  - 약 96~97% 정확도 (압축률에 따라)
  - 테이블 구조를 Markdown으로 변환 가능
  - 30M 페이지로 학습된 대규모 모델
  - 거래 명세서(invoice) 처리에 특화된 사례 다수

### 2. EasyOCR vs DeepSeek-OCR 비교 분석
- **현재 시스템**: EasyOCR 기반 (app/services/ocr_service.py)
- **비교 결과**:
  - DeepSeek-OCR: 테이블 인식 우수, 복잡한 레이아웃 처리 가능
  - EasyOCR: 로컬 실행 안정적, 검증된 시스템
  - **문제**: 한글 명세서에 대한 직접적인 비교 데이터 없음
  - **결론**: POC 테스트 필수 (실제 GSC/HACIELO 명세서로 비교)

### 3. DeepSeek-OCR 통합 플랜 작성
- **문서**: `Documents/Planning/DEEPSEEK_OCR_INTEGRATION_PLAN.md`
- **방법론**: 7단계 개발 방법론 적용
  1. Constitution (원칙) ✅
  2. Specify (명세) ✅
  3. Clarify (명확화) ✅ - 사용자 결정 필요
  4. Plan (계획) ✅
  5. Tasks (작업 분해) ✅
  6. Implement (구현) - 대기
  7. Analyze (검증) - 대기

---

## 🔧 기술 세부사항

### DeepSeek-OCR 실행 방식 (3가지)

#### 1. 로컬 실행 (Transformers + vLLM)
```python
from transformers import AutoProcessor, AutoModel
processor = AutoProcessor.from_pretrained("deepseek-ai/DeepSeek-OCR")
model = AutoModel.from_pretrained("deepseek-ai/DeepSeek-OCR")
```
- **장점**: API 비용 없음, 무제한 사용, 오프라인 가능
- **단점**: GPU 필요, 초기 모델 다운로드 (~수GB)

#### 2. API 호출 (Replicate / Clarifai)
```python
import replicate
output = replicate.run(
    "lucataco/deepseek-ocr",
    input={"image": image}
)
```
- **장점**: GPU 불필요, 빠른 시작
- **단점**: 이미지당 $0.01~0.05 비용

#### 3. 하이브리드
- 로컬 우선 사용, 실패 시 API 백업

### 통합 아키텍처 설계

```
OCRService (기존)
├── EasyOCREngine (기존 유지)
│   └── easyocr.Reader
└── DeepSeekOCREngine (신규)
    ├── LocalEngine (Transformers + vLLM)
    └── APIEngine (Replicate / Clarifai)
```

### 통합 플랜 (6 Phase)

- **Phase 1**: POC 테스트 (1~2일)
  - DeepSeek-OCR 기술 검증
  - 10장 명세서로 비교 테스트
  - 정확도/속도/비용 분석

- **Phase 2**: 통합 설계 (1일)
  - OCR 엔진 추상화
  - EasyOCR 리팩토링

- **Phase 3**: OCRService 업데이트 (1일)
  - 엔진 선택 파라미터 추가
  - 하위 호환성 유지

- **Phase 4**: UI 추가 (1일)
  - OCR 비교 페이지 추가
  - 설정 페이지 업데이트

- **Phase 5**: 테스트 및 검증 (1일)
  - 단위 테스트, 통합 테스트
  - 성능 테스트

- **Phase 6**: 문서화 및 배포 (0.5일)
  - README, 아키텍처 문서 업데이트

---

## ⏳ 다음 세션에서 할 일

### 📌 사용자 결정 필요 (Phase 1 시작 전)

다음 3가지 질문에 답변 후 진행:

#### Q1: DeepSeek-OCR 실행 방식
- 로컬 실행 (GPU) vs API 호출 vs 하이브리드?

#### Q2: POC 테스트 범위
- GSC 명세서 5~10장?
- HACIELO 명세서 5~10장?
- 둘 다?

#### Q3: 전환 기준
- 5% 이상 정확도 향상?
- 10% 이상 정확도 향상?
- 파싱 성공률 기준 (80% → 90%)?

### 📋 답변 후 진행 계획

1. **POC 테스트 데이터 준비**
   - GSC/HACIELO 명세서 수집
   - `data/test_invoices/` 폴더 생성

2. **비교 스크립트 작성**
   - `scripts/compare_ocr_engines.py`
   - EasyOCR vs DeepSeek-OCR 정확도 비교

3. **결과 분석 및 최종 결정**
   - 정확도, 속도, 비용 비교
   - 통합 진행 여부 결정

---

## 🛠️ 현재 설정 & 규칙

### 프로젝트 정보
- **버전**: v0.50.0
- **환경**: WSL2, Python 3.12.3, ./venv
- **스택**: Streamlit + SQLite
- **현재 OCR**: EasyOCR (한글+영문)

### 문서 위치
- **플랜 문서**: `Documents/Planning/DEEPSEEK_OCR_INTEGRATION_PLAN.md`
- **세션 체크리스트**:
  - `Documents/Progress/SESSION_START_CHECKLIST.md`
  - `Documents/Progress/SESSION_END_CHECKLIST.md`

### 참고 문서
- [DeepSeek-OCR GitHub](https://github.com/deepseek-ai/DeepSeek-OCR)
- [DeepSeek-OCR Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- [Replicate API](https://replicate.com/lucataco/deepseek-ocr)

---

## 📊 통계

- **작성된 문서**: 1개
  - `DEEPSEEK_OCR_INTEGRATION_PLAN.md` (35KB, 500+ 줄)
- **WebSearch 쿼리**: 2회
- **조사된 리소스**: 10+ 링크

---

## 💡 인사이트

### 발견한 점
1. **DeepSeek-OCR의 강점**:
   - 테이블 구조 인식 및 Markdown 변환 (GSC 명세서에 유리)
   - 대규모 학습 데이터 (30M 페이지)
   - 거래 명세서 처리 사례 다수

2. **검증 필요 사항**:
   - 한글 명세서 인식 정확도 (EasyOCR과 직접 비교 데이터 없음)
   - 로컬 실행 시 GPU 요구사항 및 속도
   - API 비용 vs 로컬 실행 비용

3. **리스크**:
   - POC 테스트 결과가 기대에 못 미칠 수 있음
   - 로컬 실행 시 GPU 환경 필요
   - API 비용이 예상보다 높을 수 있음

### 다음 세션을 위한 노트
- 사용자 답변 받은 후 POC 테스트 먼저 진행
- 테스트 결과가 좋으면 통합 구현 진행 (Phase 2~6)
- 테스트 결과가 나쁘면 현재 EasyOCR 시스템 유지

---

## 🔗 관련 파일

### 신규 파일
- `Documents/Planning/DEEPSEEK_OCR_INTEGRATION_PLAN.md` (신규)

### 참조 파일
- `app/services/ocr_service.py` (현재 EasyOCR 기반)
- `Documents/Architecture/SYSTEM_ARCHITECTURE.md`
- `Documents/Architecture/DEVELOPMENT_GUIDE.md`

---

**마지막 업데이트**: 2025-11-18
**다음 세션 예정**: 2025-11-19 (사용자 답변 후 POC 테스트)
