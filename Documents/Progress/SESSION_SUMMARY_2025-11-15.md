# 세션 요약 - 2025년 11월 15일

## 📊 세션 정보
- **날짜**: 2025-11-15
- **시작 버전**: v0.41.0
- **종료 버전**: v0.43.0
- **작업 시간**: ~2시간
- **주요 작업**: OCR 방식 개선 (image_to_data 도입)

---

## 🎯 작업 내용

### 1. OCR 텍스트 분석 및 문제 진단
**문제점 발견:**
- 사용자가 업로드한 이미지가 명세서 전체가 아닌 표 일부만 촬영됨
- "거래명세서" 헤더, 날짜 정보, 표 헤더 누락
- GSC 타입 및 날짜 인식 실패

**OCR 텍스트 분석 결과:**
- `922507661582` - 사업자번호 숫자 발견
- `사업장`, `우스` - GSC 명세서 특징 키워드
- 표 형식 데이터만 일부 포함

### 2. GSC 타입 감지 로직 강화 (v0.42.0)
**파일**: `app/utils/text_parser.py`

**추가된 패턴:**
```python
gsc_indicators = [
    'GSC' in ocr_upper,
    'COFFEEGSC' in ocr_upper,
    '197-04-00506' in ocr_text,
    '922507661582' in ocr_text,  # ✅ 새로 추가 (사업자번호 OCR 오인식)
    '157-04' in ocr_text,
    '197-04' in ocr_text,
    '거래명세서' in ocr_text,
    ('사업장' in ocr_text and '우스' in ocr_text)  # ✅ 새로 추가
]
```

**개선사항:**
- 단일 사업자번호(`922507661582`)만으로도 GSC 판정 가능
- "사업장" + "우스" 조합 패턴 추가

### 3. 날짜 추출 로직 개선 (v0.42.0)
**파일**: `app/utils/text_parser.py`

**변경사항:**
```python
# 이전: 한글 패턴 → dateparser → YYYY-MM-DD 패턴
# 현재: YYYY-MM-DD 패턴 우선 → 한글 패턴 → dateparser
```

**이유:**
- 표 데이터와 날짜가 혼재될 때 정확도 향상
- OCR이 표 전체를 읽으면 날짜가 다른 숫자와 섞일 수 있음

### 4. OCR image_to_data 방식 도입 (v0.43.0) ⭐
**파일**: `app/services/ocr_service.py`, `app/pages/ImageInvoiceUpload.py`

**주요 변경:**

#### 4.1. OCR 서비스 개선
```python
# 이전 방식 (텍스트만)
text = pytesseract.image_to_string(image, lang='kor+eng')

# 현재 방식 (텍스트 + 신뢰도 + 좌표)
data = pytesseract.image_to_data(
    image,
    lang='kor+eng',
    output_type=Output.DICT
)
# 반환: {
#   'text': ['단어1', '단어2', ...],
#   'conf': [95.2, 87.3, ...],  # 신뢰도
#   'left': [10, 50, ...],       # x 좌표
#   'top': [20, 30, ...]         # y 좌표
# }
```

#### 4.2. 신뢰도 기반 필터링
```python
def extract_text_from_image(..., return_data: bool = False):
    if return_data:
        # 단어별 정보 추출 (신뢰도 > 0인 것만)
        words = []
        confidences = []

        for i in range(len(data['text'])):
            word_text = data['text'][i].strip()
            conf = float(data['conf'][i])

            if word_text and conf > 0:
                words.append({
                    'text': word_text,
                    'confidence': conf,
                    'left': data['left'][i],
                    'top': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i]
                })
                confidences.append(conf)

        avg_confidence = sum(confidences) / len(confidences)

        return {
            'text': text,
            'words': words,
            'confidence': avg_confidence
        }
```

#### 4.3. UI 개선
**OCR 신뢰도 표시:**
- 🟢 80% 이상: 우수
- 🟡 60~80%: 보통
- 🔴 60% 미만: 낮음 (경고)

**단어별 신뢰도 디버깅:**
```python
# 디버그 정보 (OCR 원본 텍스트 + 단어별 신뢰도)
with st.expander("🔍 디버그: OCR 상세 정보"):
    # 원본 텍스트
    st.text_area("OCR 추출 텍스트", ocr_text, height=200)

    # 단어별 신뢰도 (낮은 순으로 정렬)
    low_conf_words = sorted(ocr_words, key=lambda x: x['confidence'])[:20]

    for word in low_conf_words:
        conf = word['confidence']
        text = word['text']
        color = "🟢" if conf >= 80 else "🟡" if conf >= 60 else "🔴"
        st.write(f"{color} `{text}` - {conf:.1f}%")
```

---

## 📈 버전 히스토리

### v0.41.0
- feat: OCR 디버그 expander 추가

### v0.42.0
- feat: OCR 인식 개선 (사업자번호 패턴 추가)
- GSC 타입 감지: `922507661582` 패턴 추가
- GSC 타입 감지: "사업장" + "우스" 조합 패턴 추가
- 날짜 추출: YYYY-MM-DD 패턴 우선 처리

### v0.43.0
- feat: OCR image_to_data 방식으로 개선
- pytesseract.image_to_data() 추가: 단어별 좌표 + 신뢰도 제공
- extract_text_from_image(): return_data 옵션 추가
- process_image(): OCR 평균 신뢰도 + 단어별 정보 반환
- UI: OCR 신뢰도 표시 (🟢🟡🔴)
- UI: 단어별 신뢰도 디버그 섹션 추가 (낮은 순 20개)
- 신뢰도 < 60% 경고 메시지 추가

---

## 🔧 기술적 개선사항

### OCR 엔진 설정
```python
custom_config = '--oem 3 --psm 6 -c preserve_interword_spaces=1'
# --oem 3: LSTM 엔진 (최신, 정확도 높음)
# --psm 6: 균일한 텍스트 블록 (표 형식에 적합)
# preserve_interword_spaces=1: 단어 간 공백 유지
```

### 신뢰도 계산
- **OCR 신뢰도**: Tesseract가 제공하는 단어별 신뢰도 평균
- **파싱 신뢰도**: 기존 로직 (필수 필드 존재 여부 + 원두명 매칭 점수)

---

## 📝 문서 업데이트

### 버전 동기화
- ✅ `logs/VERSION`: 0.43.0
- ✅ `logs/CHANGELOG.md`: 업데이트 완료
- ✅ `README.md`: v0.43.0으로 동기화
- ✅ `.claude/CLAUDE.md`: v0.43.0으로 동기화

---

## 💡 사용자 피드백 및 권장사항

### 발견된 이슈
- 업로드된 이미지가 명세서 전체가 아닌 표 일부분만 촬영됨
- 헤더, 날짜 정보, 표 헤더가 누락되어 인식 실패

### 권장사항
**전체 명세서를 촬영해야 합니다:**
1. 상단 헤더 포함 (거래명세서, GSC 로고 등)
2. 표 전체 (NO., 품목, 규격, 수량, 중량, 단가, 공급가액)
3. 하단 정보 포함 (계약일자, 총 중량, 합계금액)

**또는:**
- 현재 이미지로 테스트 시 "🔍 디버그: OCR 상세 정보"에서 신뢰도 확인
- 낮은 신뢰도 단어 확인하여 수동 수정

---

## 🎯 다음 세션 계획

### 필요 작업
1. **전체 명세서 이미지로 테스트**
   - GSC 타입 인식 확인
   - 날짜 추출 확인
   - 항목 파싱 확인

2. **OCR 정확도 개선** (필요시)
   - 좌표 기반 표 파싱 구현 (복잡, 나중에)
   - 전처리 옵션 추가 테스트

3. **성능 테스트**
   - 다양한 명세서 타입으로 테스트
   - 신뢰도 임계값 조정

---

## 📊 통계

- **커밋 수**: 3개
- **변경된 파일**: 4개
  - `app/services/ocr_service.py`
  - `app/utils/text_parser.py`
  - `app/pages/ImageInvoiceUpload.py`
  - `README.md`, `.claude/CLAUDE.md`
- **추가된 코드 라인**: ~110줄
- **삭제된 코드 라인**: ~25줄

---

## ✅ 완료된 작업
- [x] OCR 텍스트 분석 및 문제점 파악
- [x] GSC 타입 감지 로직 개선
- [x] 날짜 추출 로직 개선
- [x] pytesseract.image_to_data() 방식 도입
- [x] 신뢰도 점수 기반 필터링 추가
- [x] UI에 OCR 신뢰도 표시
- [x] 단어별 신뢰도 디버깅 섹션 추가
- [x] 문서 버전 동기화 (README, CLAUDE.md)
- [x] 세션 요약 작성

---

**세션 종료 시각**: 2025-11-15 (한국시간 기준)
**다음 세션**: 전체 명세서 이미지로 테스트 예정
