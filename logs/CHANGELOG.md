# 변경 로그 (Changelog)

모든 주목할 만한 프로젝트 변경사항은 이 파일에 문서화됩니다.

## 버전 관리 규칙 (Semantic Versioning)

- **MAJOR.MINOR.PATCH** 형식 사용
  - MAJOR: 대규모 기능 추가 또는 호환성 깨지는 변경
  - MINOR: 새로운 기능 추가 (하위 호환성 유지)
  - PATCH: 버그 수정 (하위 호환성 유지)

---

## [1.1.0] - 2025-10-27

### ✨ 마이너 업데이트 (Minor Update): Implement comprehensive reusable component system with 15+ components

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [1.0.0] - 2025-10-27

### 🚀 주요 버전 (Major Release): docs: Add comprehensive reusable component architecture design

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.1.3] - 2025-10-27

### 🐛 패치 (Bug Fix): docs: Add comprehensive version management documentation to CLAUDE.md

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.1.2] - 2025-10-27

### 🐛 패치 (Bug Fix): Remove unsupported Streamlit config options

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.1.1] - 2025-10-27

### 🐛 패치 (Bug Fix): feat: Implement comprehensive version management and fix multiple bugs

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.1.0] - 2025-10-27

### 🎯 주요 작업: 데이터베이스 모델 개선 및 UI 오류 수정

#### ✨ 추가 (Added)
- `.streamlit/config.toml` 설정 파일 추가
  - 사이드바 네비게이션 강제 활성화
  - 다크 테마 설정
- `Transaction` 모델에 `bean_id` 필드 추가
  - 원두별 거래 추적 기능 개선
- `Transaction` 모델에 `description` 필드 추가
  - 거래 상세 정보 기록 가능

#### 🐛 수정 (Fixed)
1. **FormMixin.form_submit_button() 오류 해결**
   - 파일: `app/pages/InventoryManagement.py:286`
   - 문제: `key` 파라미터는 form_submit_button()이 지원하지 않음
   - 해결: `key="btn_outflow"` 파라미터 제거

2. **Excel 내보내기 오류 해결**
   - 파일: `app/services/report_service.py`
   - 문제: "At least one sheet must be visible" 오류
   - 해결: 데이터가 없을 때도 빈 시트를 생성하도록 예외 처리 추가
   - 변경사항:
     - `export_to_excel()` 함수: 시트 생성 추적 및 빈 시트 생성 로직
     - `_create_summary_sheet()`: try-except 블록 추가
     - `_create_cost_sheet()`: 데이터 존재 여부 확인 로직
     - `_create_bean_usage_sheet()`: 데이터 존재 여부 확인 로직
     - `_create_blend_sheet()`: 데이터 존재 여부 확인 로직

3. **st.number_input() 타입 불일치 오류 해결**
   - 파일: `app/pages/Settings.py:184, 114`
   - 문제: min_value(float), value(int), step(float) 타입 불일치
   - 해결: 모든 파라미터를 float으로 통일
   ```python
   # 수정 전
   current_time = float(roasting_time.value) if roasting_time else 2
   current_roasting = float(roasting_cost.value) if roasting_cost else 2000

   # 수정 후
   current_time = float(roasting_time.value) if roasting_time else 2.0
   current_roasting = float(roasting_cost.value) if roasting_cost else 2000.0
   ```

4. **데이터베이스 스키마 오류 해결**
   - 문제: 변경된 Transaction 모델이 기존 DB와 불일치
   - 해결: 데이터베이스 재초기화 및 테이블 재생성
   - 결과: 모든 테이블 정상 생성 (6개 테이블)

#### 🔧 개선 (Improved)
1. **페이지 파일명 국제화**
   - 한글 파일명 → 영문으로 변경
   - Streamlit 호환성 및 크로스 플랫폼 호환성 개선
   - 파일명 변경 목록:
     - `1_대시보드.py` → `Dashboard.py`
     - `2_원두관리.py` → `BeanManagement.py`
     - `3_블렌딩관리.py` → `BlendManagement.py`
     - `4_분석.py` → `Analysis.py`
     - `5_재고관리.py` → `InventoryManagement.py`
     - `6_보고서.py` → `Report.py`
     - `7_설정.py` → `Settings.py`
     - `8_Excel동기화.py` → `ExcelSync.py`
     - `9_고급분석.py` → `AdvancedAnalysis.py`

2. **파일명 구조 단순화**
   - 숫자 접두사 제거 (1_, 2_ 등)
   - 이유: 더 깔끔한 파일명 구조 및 직관적인 네비게이션
   - 영향: 9개 페이지 파일명, st.switch_page() 참조 12개 업데이트

3. **코드 참조 업데이트**
   - 파일: `app/app.py`, `app/pages/Dashboard.py`
   - 변경: 모든 `st.switch_page()` 호출을 새로운 파일명으로 업데이트

#### 📝 문서화 (Documentation)
- VERSION 파일 추가 (현재 버전: 0.1.0)
- CHANGELOG.md 파일 생성

#### 🔍 테스트 (Testing)
- ✅ Streamlit 웹서버 정상 작동 확인
- ✅ 데이터베이스 연결 및 쿼리 정상 작동 확인
- ✅ 사이드바 네비게이션 정상 표시 확인
- ✅ 모든 페이지 링크 정상 작동 확인

### 📊 통계
- 수정된 파일: 5개
- 추가된 파일: 2개
- 생성된 버그 수정: 4개
- 구현된 개선사항: 3개

---

## 버전 관리 가이드

### 새로운 작업 추가 방법

1. 작업 완료 후 이 파일에 변경사항 기록
2. 버전 번호 결정:
   - 버그 수정 → PATCH 증가 (0.1.0 → 0.1.1)
   - 새 기능 → MINOR 증가 (0.1.0 → 0.2.0)
   - 대규모 변경 → MAJOR 증가 (0.1.0 → 1.0.0)
3. VERSION 파일 업데이트
4. 변경사항을 아래 섹션 중 하나에 추가:
   - **✨ Added** - 새로운 기능
   - **🐛 Fixed** - 버그 수정
   - **🔧 Improved** - 기존 기능 개선
   - **🗑️ Removed** - 제거된 기능
   - **⚠️ Deprecated** - 곧 제거될 기능
   - **📝 Documentation** - 문서 업데이트
   - **🔍 Testing** - 테스트 추가

### 버전 번호 선택 기준

| 변경 유형 | 버전 증가 | 예시 |
|---------|---------|------|
| 버그 수정 | PATCH | 0.1.0 → 0.1.1 |
| 새 기능 추가 | MINOR | 0.1.0 → 0.2.0 |
| 호환성 깨지는 변경 | MAJOR | 0.1.0 → 1.0.0 |
| 여러 작업 묶음 | MINOR | 0.1.0 → 0.2.0 |

---

## 향후 계획

### v0.2.0 예정 기능
- [ ] 사용자 인증 시스템
- [ ] 실시간 데이터 동기화
- [ ] 고급 분석 기능 강화

### v1.0.0 목표
- [ ] 안정적인 프로덕션 배포
- [ ] 완전한 테스트 커버리지
- [ ] 완전한 사용자 문서

