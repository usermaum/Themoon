# 세션 요약 - 2025년 11월 16일

**날짜**: 2025-11-16
**버전**: v0.46.0 → [Unreleased]
**주요 작업**: GSC 명세서 OCR 파싱 로직 개선 (수량 유무 패턴 모두 지원)
**작업 시간**: 약 1시간

---

## 📋 작업 개요

이번 세션에서는 어제 (2025-11-15) 작업이 사용제한으로 중단된 부분을 이어서 진행했습니다. IMG_1651.PNG 테스트 중 발견된 새로운 테이블 패턴 (수량 없음)을 지원하기 위해 파싱 로직을 개선했고, IMG_1650.PNG 회귀 테스트에서 문제를 발견하여 두 가지 패턴을 모두 지원하도록 수정했습니다.

---

## ✅ 완료된 작업

### 1. 어제 작업 이어서 진행

**배경:**
- 2025-11-15 세션에서 IMG_1650.PNG OCR 파싱 로직 개선 완료
- IMG_1651.PNG 테스트를 위해 새로운 파싱 로직 개발 중 사용제한 발생
- test_pattern.py → v2 → v3 → v4 로 패턴 개선
- 최종 전략을 text_parser.py에 적용한 상태로 중단

### 2. IMG_1651.PNG 테스트 실행

**테스트 결과:**
- ✅ 날짜: 2025-09-26 (`099 → 09` 변환)
- ✅ 총 금액: 305,300원 (`한계금액` 오인식 대응)
- ✅ 총 중량: 140kg
- ✅ 4개 항목 모두 파싱 (`Sk9 → 5kg` 변환 성공)
- ✅ 전체 신뢰도: **100.0%**

### 3. IMG_1650.PNG 회귀 테스트 실패 발견

**문제:**
- ❌ 원두명에 이전 금액이 붙음: "235.009 Colombia Supremo..."
- ❌ 단가/중량 값이 잘못 파싱됨

**원인 분석:**
두 이미지의 테이블 구조가 다름:
- **IMG_1650**: `품목 규격 수량 중량 단가 금액` (6개 필드, 수량 있음)
- **IMG_1651**: `품목 규격 중량 단가 금액` (5개 필드, 수량 없음)

현재 로직이 IMG_1651에만 맞춰져 있어서 IMG_1650 파싱 실패.

### 4. 파싱 로직 개선 (text_parser.py:703-773)

**개선 내용:**
```python
# 두 가지 패턴 정의
# 패턴 1 (6개 필드): (규격) (수량) (중량) (단가) (금액)
item_pattern_with_qty = rf'({spec_pattern})\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+([\d,\.\)\-]+)\s+([\d,\.\)\-]+)'

# 패턴 2 (5개 필드): (규격) (중량) (단가) (금액)
item_pattern_no_qty = rf'({spec_pattern})\s+(\d+(?:\.\d+)?)\s+([\d,\.\)\-]+)\s+([\d,\.\)\-]+)'

# 자동 감지: 패턴 1로 2개 미만 매칭 시 패턴 2 시도
matches = list(re.finditer(item_pattern_with_qty, table_text_flat))
has_quantity = True

if len(matches) < 2:
    matches = list(re.finditer(item_pattern_no_qty, table_text_flat))
    has_quantity = False

# 원두명 앞 숫자 제거 (이전 항목 금액 오인식 대응)
bean_name = re.sub(r'^[\d,\.\)\-]+\s+', '', bean_name)
```

**주요 개선사항:**
1. **두 가지 패턴 자동 감지**: 먼저 패턴 1 시도, 실패 시 패턴 2 사용
2. **원두명 정리**: 앞에 붙은 숫자 자동 제거
3. **규격 정리 확장**: `Sk9 → 5kg` 변환 추가

### 5. 최종 테스트 결과

**IMG_1650.PNG (패턴 1: 수량 있음)**
- ✅ 날짜: 2025-10-29
- ✅ 총 금액: 1,825,003원
- ✅ 4개 항목 파싱 (수량 30개씩)
- ✅ 전체 신뢰도: **100.0%**

**IMG_1651.PNG (패턴 2: 수량 없음)**
- ✅ 날짜: 2025-09-26
- ✅ 총 금액: 305,300원
- ✅ 4개 항목 파싱 (수량 0개, 중량 20kg씩)
- ✅ 전체 신뢰도: **100.0%**

### 6. 테스트 파일 정리

**삭제한 파일:**
- `test_pattern.py`
- `test_pattern2.py`
- `test_pattern3.py`
- `test_pattern4.py`
- `test_ocr_debug.py`

(어제 패턴 개선 과정에서 생성된 임시 파일들)

### 7. 추가 이미지 테스트 (IMG_1652~1659)

**테스트 방법:**
- `test_quick_check.py` 생성하여 9개 이미지 일괄 테스트

**테스트 결과:**
- IMG_1650/1651: ✅ 완벽 (4개 항목, 100% 신뢰도)
- IMG_1652~1659: ❌ 대부분 실패 (0~6개 항목, 낮은 신뢰도)

**원인 분석:**
- 저품질 이미지 → OCR 인식 신뢰도 40~60%
- 텍스트 인식 오류로 인한 파싱 실패

### 8. Enhanced 전처리 모드 시도 (실험)

**목표:**
- 저품질 이미지의 OCR 인식률 향상

**구현 내용:**
- `image_utils.py`: `preprocess_for_easyocr()` 함수에 `mode='enhanced'` 추가
  - 3배 업스케일링
  - 강력한 노이즈 제거 (fastNlMeansDenoisingColored)
  - 강화된 CLAHE (clipLimit=3.0)
  - Unsharp Mask 선명화
- `ocr_service.py`: OCR 신뢰도 < 60% 시 자동 재시도

**테스트 결과:**
- ❌ 불안정한 결과
  - IMG_1652: 3→0개 (더 나빠짐)
  - IMG_1653: 0→2개 (개선됨)
- 결론: **Enhanced 모드는 신뢰할 수 없음**

### 9. Enhanced 모드 폐기 및 코드 정리

**사용자 결정:**
- "A → B로 진행"
  - A: Enhanced 모드 폐기, 현재 상태 유지
  - B: UI 통합 먼저 진행

**코드 정리:**
- `ocr_service.py`: `process_image()` 함수에서 auto_enhance 로직 제거
- `image_utils.py`: Enhanced 모드 코드는 주석 없이 유지 (향후 사용 가능)
- 테스트 파일 삭제: `test_batch_ocr.py`, `test_quick_check.py`, `test_compare_modes.py`
- 저품질 이미지에 대한 경고 메시지 강화

**커밋:**
```bash
ffef80f refactor: OCR 전처리 로직 정리
```

### 10. UI 통합 확인

**확인 내용:**
1. `ImageInvoiceUpload.py` (line 123): `invoice_service.process_invoice_image()` 호출
2. `invoice_service.py` (line 82): `ocr_service.process_image()` 호출
3. `ocr_service.py`: `parse_invoice_data()` → `text_parser.parse_gsc_table()` 호출

**결과:**
- ✅ **코드 수정 불필요**
- ✅ 개선된 dual-pattern 파싱 로직 이미 통합됨
- ✅ warnings 필드 UI 연동 확인 완료

**테스트 환경:**
- Streamlit 앱 실행: http://0.0.0.0:8501
- ImageInvoiceUpload 페이지에서 IMG_1650/1651 업로드 테스트 가능

---

## 📊 변경 파일

### 수정 파일
- `app/utils/text_parser.py` (line 703-773)
  - `parse_gsc_table()`: 두 가지 패턴 자동 감지 및 파싱 로직 추가
  - 원두명 앞 숫자 자동 제거 로직 추가
- `app/utils/image_utils.py` (line 64-145)
  - `preprocess_for_easyocr()`: `mode='enhanced'` 파라미터 추가 (현재 미사용)
- `app/services/ocr_service.py` (line 445-529)
  - `process_image()`: 저품질 이미지 경고 메시지 강화

### 삭제 파일
- 어제 세션: 5개 테스트 파일 (test_pattern*.py, test_ocr_debug.py)
- 오늘 세션: 3개 테스트 파일 (test_batch_ocr.py, test_quick_check.py, test_compare_modes.py)

### 문서 업데이트
- `logs/CHANGELOG.md`: Unreleased 섹션 업데이트 (2025-11-16)
- `Documents/Progress/SESSION_SUMMARY_2025-11-16.md`: 이 파일

---

## 💡 배운 점 & 개선사항

### 1. OCR 결과의 다양성 대응

**문제:**
- 동일한 공급자 (GSC)의 명세서지만 테이블 구조가 다를 수 있음
- 수량 필드가 있는 경우 / 없는 경우

**해결:**
- 여러 패턴을 시도하는 fallback 전략
- 패턴 매칭 결과 개수로 자동 감지

### 2. 원두명 추출 시 잡음 제거

**문제:**
- 원두명 앞에 이전 항목의 금액이 붙는 현상
- 예: "235.009 Colombia Supremo..."

**해결:**
- 정규식으로 앞의 숫자 패턴 제거: `r'^[\d,\.\)\-]+\s+'`

### 3. 회귀 테스트의 중요성

**교훈:**
- 새로운 케이스를 지원하기 위해 로직을 변경할 때
- 기존 케이스가 깨지지 않는지 반드시 확인
- 이번에 IMG_1651 지원 후 IMG_1650 회귀 테스트에서 문제 발견

---

## 🎯 다음 단계

1. **HACIELO 명세서 파싱**: 두 번째 공급자 타입 지원
   - HACIELO 명세서 이미지 수집
   - 파싱 패턴 개발 및 테스트
2. **저품질 이미지 대응 개선**:
   - Enhanced 모드 재설계 (더 안정적인 전처리 파라미터)
   - 또는 사용자에게 재촬영 권장 UI 강화
3. **에러 처리 강화**: 파싱 실패 시 상세 로그 및 사용자 피드백
4. **테스트 커버리지 확대**: OCR 서비스 단위 테스트 추가

---

## 📝 커밋 내역

```bash
ab554c4 feat: OCR 파싱 로직 개선 (수량 유무 패턴 모두 지원)
# - text_parser.py: dual-pattern 감지 로직 추가
# - 테스트 파일 5개 삭제

ffef80f refactor: OCR 전처리 로직 정리
# - ocr_service.py: auto_enhance 로직 제거
# - image_utils.py: enhanced 모드 코드 유지 (미사용)
# - 테스트 파일 3개 삭제
```

---

## 🏁 세션 종료 시간
- **시작**: 2025-11-16 12:30 (추정)
- **종료**: 2025-11-16 14:40 (추정)
- **총 시간**: 약 2시간 10분

## 📌 주요 성과

1. ✅ **GSC 명세서 dual-pattern 지원 완성**
   - IMG_1650 (수량 있음) + IMG_1651 (수량 없음) 모두 100% 파싱
2. ✅ **Enhanced 전처리 모드 실험 및 의사결정**
   - 신뢰할 수 없는 결과로 폐기, 코드는 유지
3. ✅ **UI 통합 확인**
   - 기존 코드 수정 없이 개선된 로직 자동 통합 완료
4. ✅ **Claude API 통합 가이드 작성**
   - EasyOCR → Claude API 전환 완전 가이드 (1,308줄)
   - 비용 분석, 단계별 구현, 테스트, 트러블슈팅 포함
5. ✅ **문서화 완료**
   - SESSION_SUMMARY, CHANGELOG 업데이트

---

## 🎯 다음 세션 작업 계획

### 📋 다음 세션에서 진행할 작업 (우선순위순)

#### 🔴 우선순위 1: Claude API 통합 (다른 컴퓨터에서)

**문서 위치:**
- `Documents/Guides/CLAUDE_API_INTEGRATION_GUIDE.md`

**작업 요약:**
1. Anthropic API 키 발급 (https://console.anthropic.com)
2. anthropic SDK 설치: `./venv/bin/pip install anthropic python-dotenv`
3. .env 파일 생성: `ANTHROPIC_API_KEY=sk-ant-...`
4. `app/services/claude_ocr_service.py` 작성 (문서에 전체 코드 있음)
5. `app/services/invoice_service.py` 수정
6. `app/pages/ImageInvoiceUpload.py` 수정
7. 테스트: `test_claude_ocr.py` 실행

**예상 소요 시간:** 2시간
**예상 효과:** OCR 인식률 60% → 95%+

**참고:**
- 가이드 문서에 모든 코드 포함 (복사 가능)
- 단계별 체크리스트 제공
- 트러블슈팅 섹션 완비

---

#### 🟡 우선순위 2: statusline 개선 (현재 컴퓨터에서 가능)

**문서 위치:**
- `Documents/Planning/STATUSLINE_ENHANCEMENT_PLAN.md`

**작업 요약:**
1. jq 설치: `sudo apt-get install jq`
2. statusline.sh 백업: `cp statusline.sh statusline.sh.backup-$(date +%Y%m%d)`
3. 새 statusline.sh 작성 (문서 부록 C에 전체 코드 있음)
4. 실행 권한: `chmod +x statusline.sh`
5. 테스트: 문서의 테스트 JSON으로 확인

**예상 소요 시간:** 45분
**예상 효과:** statusline에 모델/프로젝트/토큰/비용 실시간 표시

**출력 형식:**
```
🤖 sonnet-4-5 | 📁 TheMoon_Project | 💰 $0.15/$0.50 | 🧠 25K (12%)
```

**참고:**
- 독립 실행 가이드 완비 (부록 C)
- 전체 코드 복사 가능 (1156-1255 라인)
- 5분 빠른 시작 가이드 있음

---

### 📌 다음 세션 시작 시 확인사항

**1단계: 어떤 작업을 먼저 할지 결정**
```
옵션 A: Claude API 통합 (다른 컴퓨터, 2시간, 높은 효과)
옵션 B: statusline 개선 (현재 컴퓨터, 45분, 편의 기능)
옵션 C: 둘 다 진행 (순서: B → A 권장)
```

**2단계: 해당 문서 읽기**
- 옵션 A: `Documents/Guides/CLAUDE_API_INTEGRATION_GUIDE.md`
- 옵션 B: `Documents/Planning/STATUSLINE_ENHANCEMENT_PLAN.md`

**3단계: 문서 내 체크리스트 따라 진행**
- 각 문서에 단계별 체크리스트 있음
- 코드 전체 포함되어 복사만 하면 됨

---

### 💡 권장 진행 순서

**시나리오 1: 현재 컴퓨터에서 바로 시작**
1. statusline 개선 (45분) ← 빠르고 간단
2. 문서화 및 커밋
3. Claude API는 다른 컴퓨터에서

**시나리오 2: 다른 컴퓨터에서 시작**
1. Claude API 통합 (2시간) ← 높은 효과
2. IMG_1650~1659 전체 테스트
3. 비용/성능 측정

**시나리오 3: 둘 다 한 번에**
1. statusline 개선 (45분)
2. 커밋 및 푸시
3. 다른 컴퓨터로 이동
4. Claude API 통합 (2시간)
5. 전체 테스트 및 문서화
