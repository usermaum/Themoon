# 세션 요약 - 2025년 11월 15일 (세션 2)

## 📊 세션 정보
- **날짜**: 2025-11-15
- **시작 버전**: v0.44.0
- **종료 버전**: v0.46.0
- **작업 시간**: ~2시간
- **주요 작업**: EasyOCR 성능 최적화 및 파싱 로직 개선

---

## 🎯 작업 내용

### 1. EasyOCR 성능 최적화 (v0.44.0 → v0.45.0)

#### 1.1. Reader 캐싱 구현
**파일**: `app/services/ocr_service.py`

**문제**: 페이지 새로고침마다 EasyOCR 모델 재로드 (~20-30초)

**해결**:
```python
@st.cache_resource
def get_easyocr_reader():
    """EasyOCR Reader 싱글톤 (캐싱)"""
    return easyocr.Reader(['ko', 'en'], gpu=False)

class OCRService:
    def __init__(self, db: Session, learning_service: Optional['LearningService'] = None):
        self.reader = get_easyocr_reader()  # 캐시된 인스턴스 재사용
```

**성능 개선**:
| 상황 | 이전 | 현재 | 개선 |
|------|------|------|------|
| 첫 페이지 로드 | ~20-30초 | ~20-30초 | 동일 |
| 페이지 새로고침 | ~20-30초 | **<1초** | 🚀 **20배 빠름** |
| 이미지 업로드 | ~20-30초 + OCR | **OCR만** | 🚀 로딩 시간 제거 |

#### 1.2. EasyOCR 전용 전처리 함수 추가
**파일**: `app/utils/image_utils.py`

**기존 문제**: `preprocess_image()`는 Tesseract용 (이진화 방식)
- EasyOCR은 딥러닝 기반 → 컬러 이미지에서 더 정확
- 이진화는 세부 정보 손실 → 인식률 저하

**새로운 함수**: `preprocess_for_easyocr()`
```python
def preprocess_for_easyocr(image: Image.Image, enhance: bool = True) -> Image.Image:
    """
    EasyOCR 최적화 전처리

    처리 순서:
    1. RGB 모드 유지 (이진화 ❌)
    2. 해상도 업스케일 (<1000px → 2배)
    3. LAB 색공간 CLAHE (밝기만 향상)
    4. 약한 Gaussian Blur (디테일 유지)
    """
```

**처리 과정**:
```python
# 1. RGB 모드 확인 (그레이스케일 → RGB 변환)
if len(img_array.shape) == 2:
    img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)

# 2. 해상도 업스케일 (최소 1000px)
if height < 1000 or width < 1000:
    img_array = cv2.resize(img_array, (width * 2, height * 2),
                           interpolation=cv2.INTER_CUBIC)

# 3. LAB 색공간에서 밝기 채널만 CLAHE
lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
l, a, b = cv2.split(lab)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
l_enhanced = clahe.apply(l)
img_array = cv2.cvtColor(cv2.merge([l_enhanced, a, b]), cv2.COLOR_LAB2RGB)

# 4. 약한 노이즈 제거
img_array = cv2.GaussianBlur(img_array, (3, 3), 0)
```

**적용**:
```python
# app/services/ocr_service.py
def extract_text_from_image(..., preprocess: bool = False):
    if preprocess:
        image = preprocess_for_easyocr(image, enhance=True)  # ✅ 새로운 함수 사용
```

---

### 2. EasyOCR 오인식 패턴 대응 (v0.45.0 → v0.46.0)

#### 2.1. 사용자 제공 OCR 결과 분석
**실제 EasyOCR 출력**:
```
ESL                          # GSC 로고 오인식
거 래 명 세 서                # 공백 포함
197-04-00506                # 사업자번호 정확!
2025 = 109 29일             # 날짜 오인식
학계금9 : 18-5000 원        # 금액 키워드 + 숫자 오인식
Colombia Supremo Huila      # 원두명 인식
Ethiopia G_ Sidsmo Natural  # 일부 철자 오류
```

#### 2.2. GSC 타입 감지 강화
**파일**: `app/utils/text_parser.py` (Line 507-518)

**추가된 패턴**:
```python
gsc_indicators = [
    'GSC' in ocr_upper,
    'ESL' in ocr_upper,  # ✅ NEW: EasyOCR "GSC" 오인식
    'COFFEEGSC' in ocr_upper,
    '197-04-00506' in ocr_text,
    '922507661582' in ocr_text,
    '157-04' in ocr_text,
    '197-04' in ocr_text,
    '거래명세서' in ocr_text or '거 래 명 세 서' in ocr_text,  # ✅ NEW: 공백 포함
    ('사업장' in ocr_text and '우스' in ocr_text),
    'coffeegsc' in ocr_text.lower()  # ✅ NEW: 이메일 도메인
]
```

#### 2.3. 날짜 추출 개선
**파일**: `app/utils/text_parser.py` (Line 184-200)

**새로운 패턴 추가**:
```python
# "YYYY년 MM월 DD일" 또는 "YYYY = MM9 DD일" (OCR 오인식)
korean_full_date_pattern = r'(\d{4})\s*[년=\-]\s*(\d{1,3})\s*[월9oO]\s*(\d{1,2})\s*일'

if match:
    year_str, month_str, day_str = match.groups()
    year = int(year_str)
    # OCR 오인식: "109" → "10" (끝 2자리 사용)
    month = int(month_str[-2:]) if len(month_str) > 2 else int(month_str)
    day = int(day_str)
```

**처리 예시**:
- `2025 = 109 29일` → `2025-10-29` ✅
- `2025년 10월 29일` → `2025-10-29` ✅
- "월" → "9", "o", "O" 오인식 허용

#### 2.4. 금액 추출 개선
**파일**: `app/utils/text_parser.py` (Line 366-386)

**새로운 키워드**:
```python
keywords = ['합계금액', '총액', '합계', 'Total', 'TOTAL',
            '학계금액', '학계금9']  # ✅ OCR 오인식 포함
```

**새로운 패턴**:
```python
# 괄호, 하이픈, 공백 처리
pattern = rf'{keyword}\s*[:：]?\s*[₩￦]?\s*(\d+(?:[,\-\s]\d{{3,}})*)\s*[)）]?\s*원?'

if match:
    amount_str = match.group(1)
    # 쉼표, 하이픈, 공백 제거
    amount_str = amount_str.replace(',', '').replace('-', '').replace(' ', '')
    return float(amount_str)
```

**처리 예시**:
- `학계금9 : 18-5000 원` → `185000` ✅
- `합계금액: 1,845,000원` → `1845000` ✅
- `1825003)` → `1825003` (괄호 제거)

---

## 📈 버전 히스토리

### v0.45.0
- feat: EasyOCR 전용 전처리 함수 추가
- EasyOCR Reader 캐싱으로 페이지 로딩 20배 단축
- preprocess_for_easyocr() 함수: 컬러 이미지 유지, 해상도 업스케일, LAB CLAHE

### v0.46.0
- feat: EasyOCR 오인식 패턴 대응 강화
- GSC 타입 감지: ESL, 거 래 명 세 서, coffeegsc 패턴 추가
- 날짜 추출: "2025 = 109 29일" 패턴 처리
- 금액 추출: 학계금9, 18-5000 패턴 처리

---

## 🔧 기술적 세부사항

### EasyOCR vs Tesseract 비교

| 항목 | Tesseract | EasyOCR |
|------|-----------|---------|
| **엔진** | 전통적 OCR | 딥러닝 (LSTM) |
| **이미지 입력** | 이진화 선호 | 컬러 선호 |
| **한글 인식** | 보통 | 우수 |
| **초기 로드** | 빠름 (~1초) | 느림 (~20초) |
| **인식 속도** | 빠름 | 보통 |
| **정확도** | 70-80% | 85-95% |

### 캐싱 전략
```python
# Streamlit의 @st.cache_resource
# - 함수 호출 결과를 메모리에 저장
# - 같은 인자로 호출 시 캐시된 결과 반환
# - 앱 재시작 시에도 유지 (세션 독립적)

@st.cache_resource
def get_easyocr_reader():
    return easyocr.Reader(['ko', 'en'], gpu=False)
```

### 전처리 파이프라인
```
원본 이미지 (PNG/JPG)
    ↓
RGB 모드 확인 (RGBA/Grayscale → RGB)
    ↓
해상도 체크 (<1000px → 2배 업스케일)
    ↓
LAB 색공간 변환
    ↓
L 채널만 CLAHE 적용 (대비 향상)
    ↓
LAB → RGB 변환
    ↓
Gaussian Blur (3x3, 약함)
    ↓
EasyOCR 입력
```

---

## 📝 문서 업데이트

### 커밋 로그
```bash
# v0.44.0 → v0.45.0
92af20f9 feat: EasyOCR 전용 전처리 함수 추가

# v0.45.0 → v0.46.0
500dae69 feat: EasyOCR 오인식 패턴 대응 강화
```

### 변경된 파일
- `app/services/ocr_service.py` (83줄 추가, 7줄 삭제)
- `app/utils/image_utils.py` (57줄 추가)
- `app/utils/text_parser.py` (35줄 추가, 7줄 삭제)

---

## 💡 인사이트 및 교훈

### 1. OCR 엔진 선택의 중요성
- **Tesseract**: 전통적, 빠르지만 한글 인식률 낮음
- **EasyOCR**: 딥러닝 기반, 느리지만 한글 인식률 높음
- **결론**: 정확도 > 속도 → EasyOCR 선택

### 2. 전처리의 중요성
- 이진화는 Tesseract용
- EasyOCR은 컬러 이미지에서 더 정확
- **교훈**: OCR 엔진마다 최적의 전처리 다름

### 3. 캐싱의 효과
- 첫 로드: 20-30초
- 이후 로드: <1초
- **20배 성능 향상!**

### 4. 오인식 패턴 학습
- "GSC" → "ESL"
- "월" → "9", "o", "O"
- "합" → "학"
- **교훈**: 실제 OCR 결과로 패턴 학습 필요

---

## 🎯 다음 세션 계획

### 필요 작업
1. **실제 명세서로 종합 테스트**
   - GSC 타입 인식률 확인
   - 날짜 추출 정확도 측정
   - 항목 파싱 성공률 확인

2. **추가 오인식 패턴 수집**
   - 다양한 명세서로 테스트
   - 오인식 패턴 데이터베이스 구축

3. **성능 모니터링**
   - OCR 평균 신뢰도 추적
   - 파싱 성공률 측정
   - 사용자 피드백 수집

---

## 📊 통계

- **커밋 수**: 2개
- **변경된 파일**: 3개
  - `app/services/ocr_service.py`
  - `app/utils/image_utils.py`
  - `app/utils/text_parser.py`
- **추가된 코드 라인**: ~175줄
- **삭제된 코드 라인**: ~14줄
- **성능 개선**: 페이지 로드 20배 단축

---

## ✅ 완료된 작업
- [x] EasyOCR Reader 캐싱 구현
- [x] EasyOCR 전용 전처리 함수 추가
- [x] 사용자 제공 OCR 결과 분석
- [x] GSC 타입 감지 패턴 강화
- [x] 날짜 추출 로직 개선
- [x] 금액 추출 로직 개선
- [x] 커밋 및 푸시 (v0.45.0, v0.46.0)
- [x] 세션 요약 작성

---

**세션 종료 시각**: 2025-11-15 (한국시간 기준)
**다음 세션**: 실제 명세서로 종합 테스트 예정
