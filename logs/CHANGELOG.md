# 변경 로그 (Changelog)

모든 주목할 만한 프로젝트 변경사항은 이 파일에 문서화됩니다.

## 버전 관리 규칙 (Semantic Versioning)

- **MAJOR.MINOR.PATCH** 형식 사용
  - MAJOR: 대규모 기능 추가 또는 호환성 깨지는 변경
  - MINOR: 새로운 기능 추가 (하위 호환성 유지)
  - PATCH: 버그 수정 (하위 호환성 유지)

---

## [0.35.0] - 2025-11-13

### ✨ 마이너 업데이트 (Minor Update): Phase 5 완료 - 학습 기능 구현

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.34.0] - 2025-11-13

### ✨ 마이너 업데이트 (Minor Update): Phase 4 완료 - ImageInvoiceUpload.py UI 구현

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.33.0] - 2025-11-13

### ✨ 마이너 업데이트 (Minor Update): Phase 3 완료 - 서비스 계층 구현

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.32.0] - 2025-11-13

### ✨ 마이너 업데이트 (Minor Update): Phase 2 완료 - 이미지 처리 유틸리티 구현

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.31.0] - 2025-11-12

### ✨ 마이너 업데이트 (Minor Update): Phase 1 완료 - Invoice 데이터베이스 모델 구현

#### 📝 변경사항

**신규 파일: app/models/invoice.py (91 lines)**
- `Invoice` 클래스: 거래 명세서 메타데이터
  - 이미지 경로, 공급업체, 거래일자, 총액
  - 상태(PENDING/COMPLETED/FAILED), 신뢰도, OCR 원본 텍스트
- `InvoiceItem` 클래스: 명세서 항목 (다중 원두 지원)
  - OCR 추출 원두명 (bean_name_raw), 매칭된 원두 (bean_id)
  - 수량, 단가, 금액, 원산지, 비고
  - 항목별 신뢰도
- `InvoiceLearning` 클래스: 학습 데이터 (사용자 수정 내역)
  - OCR 인식 텍스트, 사용자 수정 값, 필드명
  - 향후 동일 오류 발생 시 자동 제안

**신규 파일: migrations/add_invoice_tables.py (172 lines)**
- 3개 테이블 생성 마이그레이션
  - `invoices`: 거래 명세서 메타데이터
  - `invoice_items`: 명세서 항목 (다중 원두)
  - `invoice_learning`: 학습 데이터
- DB 자동 백업 기능
- `transactions` 테이블에 `invoice_item_id` 컬럼 추가
- 테이블 존재 여부 검증 로직

**수정 파일: app/models/database.py**
- Invoice 모델 import 추가
- Circular import 방지를 위한 상대 경로 사용

**데이터 모델 관계:**
- Invoice 1:N InvoiceItem
- InvoiceItem 1:N InvoiceLearning
- InvoiceItem N:1 Bean

**마이그레이션 실행 결과:**
- ✅ invoices 테이블 생성 완료
- ✅ invoice_items 테이블 생성 완료
- ✅ invoice_learning 테이블 생성 완료
- ✅ transactions.invoice_item_id 컬럼 추가 완료

## [Unreleased] - 거래 명세서 이미지 자동 입고 기능 (v0.31.0+)

### 🚧 진행 중 (Work In Progress)

**Phase 0: 환경 설정 ✅ (2025-11-12) - v0.31.0에 포함**
- ✅ Unity Hub 패키지 문제 해결 (tesseract-ocr-kor 설치 차단 해제)
- ✅ Tesseract OCR 한글 언어팩 설치 (`kor` 지원 확인)
- ✅ 시스템 패키지 확인 (tesseract-ocr, poppler-utils)
- ✅ Python 패키지 설치 (6개):
  - pytesseract==0.3.10 (Tesseract OCR Python wrapper)
  - opencv-python==4.8.1.78 (이미지 전처리: 회전, 대비, 노이즈)
  - pdf2image==1.16.3 (PDF → 이미지 변환)
  - python-Levenshtein==0.25.0 (원두명 유사도 매칭)
  - dateparser==1.2.0 (날짜 파싱)
  - Pillow>=8.0.0 (이미지 처리)
- ✅ 디렉토리 생성 (data/invoices/, data/invoices/temp/)
- ✅ requirements.txt 업데이트

**Phase 1: 데이터베이스 모델 ✅ (2025-11-12) - v0.31.0에 포함**
- ✅ Invoice 모델 (거래 명세서)
- ✅ InvoiceItem 모델 (명세서 항목 - 다중 원두)
- ✅ InvoiceLearning 모델 (학습 데이터)
- ✅ 마이그레이션 스크립트 작성 및 실행

**Phase 2: 이미지 처리 유틸리티 (진행 예정)**
- image_utils.py: 전처리, 회전, 대비 향상, 노이즈 제거
- text_parser.py: 텍스트 파싱, 원두명/수량/가격/날짜 추출

**Phase 3~6: (예정)**
- Phase 2: 이미지 처리 유틸리티 (image_utils, text_parser)
- Phase 3: 서비스 계층 (ocr_service, invoice_service, learning_service)
- Phase 4: UI 구현 (ImageInvoiceUpload.py)
- Phase 5: 학습 기능 (사용자 피드백 기반 정확도 향상)
- Phase 6: 테스트 & 문서화

**관련 문서:**
- 플랜: `Documents/Planning/IMAGE_INVOICE_UPLOAD_PLAN.md` (1,662 lines)
- 세션 요약: `Documents/Progress/SESSION_SUMMARY_2025-11-12.md`

---

## [0.30.3] - 2025-11-11

### 🐛 패치 (Bug Fix): 원가 계산 페이지 margin_percent None 처리 오류 수정

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.30.2] - 2025-11-11

### 🐛 패치 (Bug Fix): 사이드바에서 세션 상태 자동 초기화 추가

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.30.1] - 2025-11-11

### 🐛 패치 (Bug Fix): 순환 import 해결 및 원두 국가 코드 표준화

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.30.0] - 2025-11-11

### ✨ 마이너 업데이트 (Minor Update): 버전 정보 중앙 관리 시스템 구축 (SSOT 원칙)

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.29.0] - 2025-11-11

### ✨ 마이너 업데이트 (Minor Update): Phase 5 완료 - 보고서 및 분석 시스템

#### 📝 변경사항

**신규 페이지: 분석 보고서 (AnalysisReport.py)**
- 3개 탭으로 구성된 종합 분석 페이지
- Tab 1: 📈 월별 리포트 (최근 12개월 선택 가능)
- Tab 2: 💰 수익성 분석 (원두별 수익률 계산)
- Tab 3: 📥 데이터 다운로드 (Excel/CSV 내보내기)

**Tab 1 - 월별 리포트 기능:**
- 월별 요약 통계 4개 메트릭 (입고량, 출고량, 로스팅 횟수, 재고 증감)
- Plotly 인터랙티브 라인 차트 (일별 추이: 입고/출고/로스팅)
- Plotly 파이 차트 (거래 유형별 분포)
- 월별 종합 리포트 Excel 다운로드 (4개 시트)

**Tab 2 - 수익성 분석 기능:**
- 기간 선택 (시작일 ~ 종료일)
- 요약 메트릭 3개 (평균 손실률, 최고/최저 수익률 원두)
- 원두별 상세 테이블 (손실률, 투입량, 산출량, 수익률)
- 정렬 옵션 (수익률순/손실률순/투입량순)
- Plotly 바 차트 (상위/하위 5개 원두 수익률 비교)
- 수익성 분석 결과 CSV 다운로드

**Tab 3 - 데이터 다운로드 기능:**
- 로스팅 기록 (기간별 필터링, Excel/CSV)
- 재고 현황 (현재 시점, Excel/CSV)
- 거래 내역 (기간별 필터링, Excel/CSV)
- 월별 종합 리포트 (4개 시트 Excel)

**신규 유틸리티: export_utils.py (266 lines)**
- `dataframe_to_excel()`: DataFrame을 Excel로 변환 (단일 시트)
- `dataframe_to_csv()`: DataFrame을 CSV로 변환
- `create_multi_sheet_excel()`: 여러 시트를 가진 Excel 생성
- `create_monthly_report_excel()`: 월별 종합 리포트 Excel 생성
- 자동 헤더 스타일링 (파란색 배경, 흰색 글자, 굵게)
- 자동 컬럼 너비 조정
- 숫자 포맷 적용 (#,##0.00)

**ReportService 확장 (7개 메서드 추가):**
- `get_monthly_transactions_report()`: 월별 거래 리포트 데이터 생성
- `get_profitability_by_bean()`: 원두별 수익성 분석
- `get_roasting_logs_dataframe()`: 로스팅 기록 DataFrame 조회
- `get_inventory_dataframe()`: 재고 현황 DataFrame 조회
- `get_transactions_dataframe()`: 거래 내역 DataFrame 조회
- `generate_monthly_excel()`: 월별 종합 리포트 Excel 생성
- `export_profitability_csv()`: 수익성 분석 CSV 생성

**기술 스택 추가:**
- xlsxwriter==3.2.0 (Excel 고급 기능 지원)
- Plotly 차트 (Line, Pie, Bar)

#### 🎯 주요 개선사항
- **종합 분석**: 월별 로스팅 현황을 한눈에 파악
- **수익성 평가**: 원두별 손실률 및 수익률 비교 분석
- **데이터 추출**: 모든 핵심 데이터 Excel/CSV 내보내기 지원
- **시각화 강화**: Plotly 인터랙티브 차트로 직관적 데이터 이해
- **경영 의사결정**: 데이터 기반 원두 구매 및 재고 전략 수립

## [0.28.0] - 2025-11-10

### ✨ 마이너 업데이트 (Minor Update): Phase 4 핵심 기능 완료 - 대시보드 고급 기능

#### 📝 변경사항

**대시보드 재고 가치 계산 및 표시:**
- 생두 + 원두 재고의 총 가치 계산 기능 추가
- 손실률을 고려한 원두 가치 환산 로직 구현
- 재고 가치 메트릭 표시 (총 재고 가치)

**저재고 알림 시스템:**
- 최소 재고량 미만 원두 목록 자동 표시
- 권장 주문량 자동 계산 기능
- 재입고 예상 비용 계산 및 표시
- 저재고 원두별 알림 카드 UI

**재고 소진 예측 로직 (InventoryService):**
- 최근 30일 소비 패턴 분석 기능 추가
- 일평균 소비량 자동 계산
- 재고 소진 예상 날짜 예측 알고리즘
- 소비 추이 분석 (증가/안정/감소 판정)
- `predict_stockout_date()` 메서드 구현

#### 🎯 주요 개선사항
- **재고 가치 관리**: 생두/원두 재고의 실시간 가치 파악 가능
- **선제적 재고 관리**: 저재고 알림으로 품절 방지
- **데이터 기반 의사결정**: 소비 패턴 분석으로 최적 발주 시점 예측
- **비용 최적화**: 권장 주문량 및 예상 비용 자동 계산

## [0.27.0] - 2025-11-10

### ✨ 마이너 업데이트 (Minor Update): Phase 3 완료 - 원두 관리 고도화

#### 📝 변경사항

**Tab 1: 원두 목록 테이블 확장:**
- 브랜드 컬럼 추가 (원두 브랜드 정보 표시)
- 평균 손실률(%) 컬럼 추가 (소수점 2자리)
- 로스팅 횟수 컬럼 추가 (총 로스팅 횟수 표시)
- 마지막 로스팅 날짜 컬럼 추가
- 브랜드별 필터링 기능 추가 (전체/특정 브랜드 선택)

**Tab 2: 원두 추가 폼 개선:**
- 브랜드 입력 필드 추가 (예: "스타벅스", "블루보틀" 등)
- BeanService.create_bean()에 brand 파라미터 추가
- 브랜드 정보 자동 저장

**Tab 4: 원두별 상세 통계 섹션 신규 추가:**
- 로스팅 이력이 있는 원두만 선택 가능 (selectbox)
- 통계 카드 4개:
  - 평균 손실률 (%)
  - 표준편차 (±%)
  - 로스팅 횟수
  - 마지막 로스팅 날짜
- 최근 10건 로스팅 이력 테이블 (날짜, 손실률, 생두 무게, 원두 무게)
- 손실률 추이 그래프 (Plotly Line Chart)
  - X축: 로스팅 날짜
  - Y축: 손실률(%)
  - 평균선 표시

#### 🎯 주요 개선사항
- **원두 브랜드 관리**: 브랜드별 원두 구분 및 필터링 가능
- **손실률 통계**: 원두별 로스팅 성과 추적
- **데이터 시각화**: 손실률 추이를 그래프로 직관적 확인
- **이력 관리**: 최근 로스팅 이력을 한눈에 파악

## [0.26.0] - 2025-11-10

### ✨ 마이너 업데이트 (Minor Update): 재고 관리 UI 개선 - 생두/원두 구분 표시

#### 📝 변경사항

**재고 조회 로직 개선:**
- `inventory_service.get_all_inventory()` 사용으로 변경
- 생두(RAW_BEAN)/원두(ROASTED_BEAN) 재고 별도 조회
- 원두별 재고 타입별 구분 관리

**재고 통계 메트릭 개선 (5개):**
- ☕ 원두 종류 (총 몇 종류의 원두)
- 🌾 총 생두 (로스팅 전 재고 합계, kg)
- ☕ 총 원두 (로스팅 후 재고 합계, kg)
- 📦 전체 재고 (생두 + 원두 총 합계, kg)
- 🔴 저재고 (생두 또는 원두 중 하나라도 저재고인 원두 개수)

**재고 목록 테이블 개선:**
- "생두 (Raw)" 컬럼 추가 (kg, 소수점 2자리)
- "원두 (Roasted)" 컬럼 추가 (kg, 소수점 2자리)
- "합계" 컬럼 추가 (생두 + 원두 합계, kg)
- 상태 컬럼 개선: 🔴생두, 🔴원두, 🟢정상 아이콘으로 저재고 상태 표시
- 생두/원두 각각 최소 재고량 체크

**재고 시각화 개선:**
- 스택 바 차트 (Stacked Bar Chart) 추가
- 생두: 갈색 (#8B4513)
- 원두: 진한 갈색 (#654321)
- 각 원두별 생두/원두 재고량 시각적 비교 가능
- X축: 재고량(kg), Y축: 원두명

#### 🎯 주요 개선사항
- **명확한 구분**: 생두와 원두를 컬럼으로 명확히 구분
- **한눈에 파악**: 로스팅 전후 재고를 테이블 한 줄에서 확인
- **저재고 관리 개선**: 생두/원두 각각 저재고 체크로 정확성 향상
- **시각화 강화**: 스택 바 차트로 재고 구성 직관적 파악

## [0.25.0] - 2025-11-10

### ✨ 마이너 업데이트 (Minor Update): 투입량 계산기 UI 구현

#### 📝 변경사항

**새로운 탭 추가: 📐 투입량 계산기**
- CostCalculation.py에 투입량 계산기 탭 추가 (총 5개 탭)
  1. 📐 투입량 계산기 (신규)
  2. 🧮 원가 계산
  3. 📊 일괄 비교
  4. 💰 원두 가격 관리
  5. ⚙️ 비용 설정

**투입량 계산기 주요 기능:**
- 원두 선택 (특정 원두 or 전체 평균 손실률)
- 안전 여유율 설정 (0~10%, 기본값 2%)
- 목표 산출량 입력 (kg 단위)

**계산 결과 표시:**
- 원두 손실률 통계:
  - 평균 손실률 (%)
  - 표준편차 (±%)
  - 로스팅 횟수
- 투입량 계산:
  - 기본 투입량 (손실률만 고려)
  - ⭐ 권장 투입량 (여유율 포함) - 강조 표시
  - 예상 산출량 범위 (최소/평균/최대)
- 계산 공식: `투입량 = 산출량 ÷ (1 - 손실률)`

**UI 특징:**
- 깔끔한 카드 스타일 결과 표시
- st.metric을 활용한 시각적 메트릭
- 도움말 expander (계산 공식 및 해석 가이드)
- 모바일 반응형 레이아웃

**계산 예시:**
- 목표: 10kg 원두 필요
- 평균 손실률: 18.36%
- 기본 투입량: 12.21kg
- 권장 투입량: 12.45kg (여유 2% 포함)
- 예상 결과: 9.8kg ~ 10.2kg

#### 🎯 주요 개선사항
- **역계산 기능**: 산출량 목표에서 필요 투입량 자동 계산
- **안전 여유율**: 손실률 변동성을 고려한 안전 재고
- **범위 예측**: 최소/평균/최대 산출량 제공으로 리스크 관리
- **사용자 친화적**: 직관적인 UI로 누구나 쉽게 사용

## [0.24.0] - 2025-11-10

### ✨ 마이너 업데이트 (Minor Update): 원가계산기 고도화 Phase 1-2 - 재고 관리 및 투입량 계산 서비스 구현

#### 📝 변경사항

**1. inventory_service.py (재고 관리 서비스) 신규 추가:**
- `get_inventory()`: 특정 원두의 재고 조회 (생두/원두별)
- `get_all_inventory()`: 전체 재고 조회 (모든 원두)
- `get_low_stock_items()`: 저재고 항목 조회 (최소 재고량 미만)
- `add_stock()`: 재고 추가 (입고, 생산)
- `reduce_stock()`: 재고 차감 (출고, 사용)
- `process_roasting_transaction()`: 로스팅 시 재고 자동 연동
  - 생두 재고 자동 차감
  - 원두 재고 자동 증가
  - Transaction 기록 자동 생성
- `adjust_inventory()`: 재고 실사 및 조정 (재고 실사 시)
- `get_transactions()`: 거래 기록 조회 (입출고 이력)

**2. cost_calculator_service.py (투입량 계산기 서비스) 신규 추가:**
- `get_bean_statistics()`: 원두별 손실률 통계 조회
- `calculate_required_input()`: 목표 산출량 → 투입량 역산
  - 공식: `투입량 = 산출량 ÷ (1 - 손실률)`
  - 안전 여유율 2% 포함
  - 예상 범위 계산 (표준편차 고려)
- `predict_output()`: 투입량 → 산출량 예측 (정방향)
- `update_bean_statistics()`: 원두 통계 재계산 (로스팅 후 자동 업데이트)
- `calculate_cost()`: 원가 계산 (손실률 고려)

**3. roasting_service.py 수정:**
- `create_roasting_log()`에 재고 자동 연동 기능 추가
- `auto_inventory` 파라미터 추가 (기본값: True)
- 로스팅 기록 생성 후 자동 실행:
  1. 생두 재고 차감 (raw_weight_kg만큼)
  2. 원두 재고 증가 (roasted_weight_kg만큼)
  3. Transaction 기록 생성 (ROASTING 타입)
  4. Bean 통계 업데이트 (평균 손실률, 표준편차, 로스팅 횟수)

#### 🎯 주요 개선사항
- **자동화**: 로스팅 기록 시 재고 자동 연동으로 수작업 최소화
- **정확성**: 손실률 통계 자동 업데이트로 데이터 정확성 향상
- **역계산**: 목표 산출량에서 필요 투입량 자동 계산
- **거래 이력**: 모든 입출고 거래 추적 가능
- **생두/원두 분리**: 로스팅 전후 재고를 별도 관리

## [0.23.0] - 2025-11-10

### ✨ 마이너 업데이트 (Minor Update): 원가계산기 고도화 Phase 1 - 데이터베이스 모델 확장

#### 📝 변경사항

**Bean 모델에 로스팅 통계 필드 추가:**
- `brand` (브랜드): VARCHAR(100), 원두 브랜드명
- `avg_loss_rate` (평균 손실률): FLOAT, 평균 손실률 %
- `std_loss_rate` (표준편차): FLOAT, 손실률 표준편차 %
- `total_roasted_count` (총 로스팅 횟수): INTEGER, 로스팅 횟수 누적
- `last_roasted_date` (마지막 로스팅 날짜): DATE, 최근 로스팅 날짜

**Inventory 모델에 재고 유형 필드 추가:**
- `inventory_type` (재고 타입): VARCHAR(20), RAW_BEAN/ROASTED_BEAN
- UNIQUE 제약 조건: (bean_id, inventory_type) 조합 유일성 보장
- 원두별 생두/원두 재고 별도 관리 가능
- 하나의 원두당 2개의 재고 레코드 (생두 1개, 원두 1개)

**Transaction 모델 확장:**
- `inventory_type` (재고 타입): 어떤 재고에 영향을 주는지 (RAW_BEAN/ROASTED_BEAN)
- `roasting_log_id` (로스팅 기록 ID): 로스팅과 연결 (Foreign Key)

**마이그레이션 스크립트 (migrate_database_v0_23_0.py):**
- 기존 데이터 자동 백업 (data/roasting_data_backup_YYYYMMDD_HHMMSS.db)
- 테이블 재생성 (SQLite ALTER TABLE 제약 극복)
- 기존 데이터 마이그레이션
- 원두별 손실률 통계 자동 계산:
  - 모든 로스팅 기록에서 평균 손실률 계산
  - 표준편차 계산
  - 로스팅 횟수 집계
  - 마지막 로스팅 날짜 추출
- 17개 원두 × 2가지 재고 = 총 34개 재고 항목 자동 생성
  - 각 원두마다 RAW_BEAN, ROASTED_BEAN 재고 생성
  - 초기 재고량: 0kg (실제 재고는 수동 입력 필요)

#### 🎯 주요 개선사항
- **모델 확장**: 원두별 손실률 통계 자동 추적
- **재고 타입 분리**: 생두/원두 재고를 명확히 구분하여 관리
- **거래 추적**: 로스팅과 재고 거래를 연결하여 추적성 향상
- **자동 마이그레이션**: 기존 데이터 보존하며 스키마 변경 안전하게 적용
- **통계 자동화**: 로스팅 이력에서 손실률 통계 자동 계산

## [0.22.0] - 2025-11-09

### ✨ 마이너 업데이트 (Minor Update): T2-1 손실률 분석 시스템 강화 완료

#### 📝 변경사항
- **개선**: 로스팅 후 무게 입력 시 포커스 아웃으로도 손실률 자동 계산 지원
  - 기록 추가 탭: `st.form` 제거, `session_state`로 실시간 업데이트
  - 기록 편집 탭: `st.form` 제거, `session_state`로 실시간 업데이트
  - `number_input`에서 엔터 또는 포커스 아웃 시 손실률 자동 계산
  - 입력 필드 헬프 텍스트 추가로 사용법 안내

- **신규**: 로스팅 기록 목록에 수동 페이징 기능 추가
  - 페이지당 표시 개수 선택 (10, 25, 50, 100개)
  - 페이징 버튼 추가 (⏮️ 처음, ◀️ 이전, 다음 ▶️, 마지막 ⏭️)
  - 현재 페이지 / 총 페이지 정보 표시 (예: 3 / 10 페이지, 전체 100건)
  - Session State 기반 페이지 상태 관리
  - 날짜 필터 및 정렬 기능 유지
  - 전체 데이터 접근 가능 (페이징으로 모든 데이터 탐색)

- **테스트**: 로스팅 기록 테스트 데이터 100건 추가
  - 기간: 2024-01-01 ~ 2025-11-08 (675일)
  - 계절별 손실률 패턴 적용 (겨울 -1.5%, 여름 +3.5%)
  - 17종 원두 골고루 분포
  - 정규분포 기반 랜덤 무게 생성

- **수정**: 손실률 상태 판정 로직 개선

- **신규**: 로스팅 기록에 원두 선택 기능 추가
  - 기록 추가 시 원두 선택 가능 (17종 원두 목록)
  - 기록 편집 시 원두 변경 가능
  - 목록 조회에 "원두" 컬럼 추가
  - 원두 미지정 옵션 포함 ("선택 안함")
  - roasting_service에 bean_id 파라미터 지원

- **개선**: 조회 기간 메뉴를 목록 방식으로 변경
  - 7가지 옵션 제공 (전체, 날짜조회, 오늘, 1개월, 3개월, 6개월, 1년)
  - date_input을 selectbox로 대체하여 모바일 접근성 향상
  - 날짜조회 선택 시에만 date_input 표시
  - 자동 날짜 필터링 로직 구현

- **개선**: 페이징 버튼 모바일 최적화
  - 5버튼 레이아웃 → 3컬럼 레이아웃 변경
  - 페이지 번호 직접 입력 기능 추가 (number_input)
  - 터치 친화적 UI로 개선

- **문서**: 원가계산기 고도화 기획 문서 작성 (1002 lines)
  - 역계산 기능 설계 (산출량 → 투입량 계산)
  - 원두별 재고 관리 시스템 설계
  - 입출고 관리 시스템 설계 (7가지 거래 유형)
  - 3주 구현 계획 수립 (4단계)
  - ERD, UI 목업, 성공 지표 포함
  - 파일: `Documents/Planning/COST_CALCULATOR_ENHANCEMENT_PLAN.md`

#### 🎯 주요 개선사항
- **UX 개선**: 엔터 입력 없이도 포커스 이동만으로 손실률 자동 계산
- **실시간 피드백**: 입력 즉시 손실률 상태 표시 (🟢우수/정상, 🟡주의, 🔴위험)
- **사용성 향상**: form 제거로 더 직관적인 입력 경험 제공
- **페이징 시스템**: 수동 페이징 버튼으로 직관적인 데이터 탐색 제공
  - 사용자가 원하는 개수만큼 표시 가능
  - 명확한 페이지 정보 제공
  - 전체 데이터 접근 보장
- **원두 선택 기능**: 로스팅 기록에 원두 정보 연결
  - 어떤 원두를 로스팅했는지 추적 가능
  - 17종 원두 중 선택 또는 미지정 가능
  - 목록 조회에서 원두명 확인 가능
- **모바일 최적화**: 페이징 및 조회 기간 메뉴 개선
  - 터치 친화적 UI로 모바일 사용성 향상
  - 페이지 번호 직접 입력 기능 추가
  - 조회 기간 목록 선택으로 빠른 필터링
- **테스트 환경**: 현실적인 테스트 데이터로 기능 검증 가능
- **시스템 계획**: 원가계산기 고도화 기획 문서 완성 (1002줄)
  - 역계산, 재고관리, 입출고 시스템 상세 설계
  - 3주 구현 로드맵 및 리스크 관리 계획

## [0.21.0] - 2025-11-07

### ✨ 마이너 업데이트 (Minor Update): 전체 17종 원두 정보 검증 및 완성

#### 📝 변경사항
- **추가**: 디카페 3종 가격 설정 (SDM ₩7,500, SM ₩8,000, 스위스워터 ₩7,000)
- **추가**: 14종 원두 상세 설명 추가 (특징, 향미, 용도)
- **검증**: 모든 원두 정보 완벽 검증 완료 (17/17 ✅)
- **추가**: Phase 2 계획 문서 작성 (`MASTER_PLAN_v2_Phase2.md`)

#### 🎯 주요 개선사항
- **원두 정보 완성도**: 100% (17/17 완벽)
- **디카페 3종**: 가격 0원 → 정상 설정
- **Phase 2 계획**: 5개 작업 정의 (T2-1 ~ T2-5)
- **로드맵 확보**: v0.22.0 ~ v0.30.0 방향성 명확

#### 원두 목록
- 에티오피아 5종, 케냐 3종, 콜롬비아 2종
- 과테말라 1종, 코스타리카 1종, 브라질 2종
- 디카페 3종

## [0.20.0] - 2025-11-07

### ✨ 마이너 업데이트 (Minor Update): 뉴문 블렌딩 판매가 조정

#### 📝 변경사항
- **추가**: `app/update_newmoon_price.py` - 판매가 업데이트 스크립트 (146 lines)
- **수정**: 뉴문 블렌딩 판매가 ₩4,000 → ₩15,000 (+275%)
- **개선**: 마진 -56.3% → 58.3% (수익 구조 정상화)

#### 🎯 주요 개선사항
- **마진 개선**: -56.3% → +58.3% (손실 제거)
- **마진액**: ₩8,747/kg
- **사용자 수정 가능**: BlendManagement 페이지에서 자유 수정

## [Unreleased]

### 🚀 Phase 2 T2-1 손실률 분석 시스템 강화 (완료 ✅)

#### 📝 변경사항 (2025-11-08)
- **추가**: `app/scripts/generate_test_roasting_data.py` - 계절성 패턴 테스트 데이터 생성 스크립트 (268 lines)
- **추가**: `app/services/loss_analytics_service.py` - 손실률 예측 및 계절성 분석 서비스 (81 lines)
- **추가**: `app/components/loss_widgets.py` - Dashboard 손실률 분석 위젯 4개 (339 lines)
- **추가**: `LossRateAnalyzer.get_loss_rate_by_bean()` - 원두별 손실률 분석 기능 (91 lines)
- **수정**: `app/pages/Dashboard.py` - 손실률 분석 섹션 추가 (4개 탭)
- **추가**: 계절성 패턴이 반영된 100개 테스트 로스팅 데이터 (2024-01-01 ~ 2025-11-08)
- **추가**: 테스트 코드 11개 (loss_rate_analyzer 3개 + loss_analytics_service 8개)

#### 🎯 주요 기능

**1. 원두별 손실률 분석**
- 17종 원두에 대한 통계 분석 (평균, 표준편차, min/max, 글로벌 대비 편차)
- 상태 자동 판단: NORMAL/ATTENTION/CRITICAL
- SQLite 호환: Python statistics 모듈 사용

**2. 계절성 예측 모델**
- 월별 계절 지수 계산 (여름 +15%, 겨울 -15% 등)
- 이동평균 + 계절성 예측 모델
- 95% 신뢰구간 제공
- 24시간 캐시 기능

**3. Dashboard 위젯**
- 📈 손실률 트렌드 차트 (±3σ 범위 표시)
- 🌾 원두별 손실률 비교 (막대 그래프)
- ⚠️ 경고 알림 카드 (미해결 경고 관리)
- 🔮 계절성 예측 (향후 3개월)

#### ✅ 완료된 작업 (T2-1)
- [x] Phase 1: 테스트 데이터 생성 (30분)
- [x] Task 2.1: get_loss_rate_by_bean() 구현 (1시간)
- [x] Task 2.2: 테스트 코드 작성 (20분)
- [x] Phase 3: 계절성 예측 모델 (1.5시간)
- [x] Task 3.1: LossAnalyticsService 클래스 생성
- [x] Task 3.2: 테스트 코드 8개 작성
- [x] Phase 4: Dashboard 위젯 (1시간)
- [x] Task 4.1: loss_widgets.py 4개 위젯 작성
- [x] Task 4.2: Dashboard.py 통합

#### 📊 통계
- **추가 코드**: ~1,400 lines
- **테스트**: 11개 추가 (모두 통과)
- **커버리지**: LossAnalyticsService 90%
- **커밋**: 6개

---

### 🧪 테스트 커버리지 개선 (96% → 97%)

#### 📝 변경사항
- **추가**: `test_analytics_service.py` - 12월 처리 분기 테스트 (+1)
- **추가**: `test_excel_service.py` - openpyxl ImportError 처리 테스트 (+1)
- **추가**: `test_cost_service.py` - 일괄 계산 예외 처리 테스트 (+1)
- **추가**: `test_auth_service.py` - 비활성화/존재하지 않는 사용자 테스트 (+3)

#### 🎯 주요 개선사항
- **전체 커버리지**: 96% → 97% (목표 달성!)
- **100% 달성 서비스**: 6개
  - analytics_service.py: 99% → 100%
  - auth_service.py: 96% → 100%
  - cost_service.py: 96% → 100%
  - excel_service.py: 97% → 100%
  - loss_rate_analyzer.py: 100% (유지)
  - roasting_service.py: 100% (유지)
- **전체 테스트**: 220개 → 226개 (6개 추가)

## [0.19.0] - 2025-11-07

### ✨ 마이너 업데이트 (Minor Update): 마스터플랜 v2 Phase 1 T1-3 완료

#### 📝 변경사항
- **추가**: `app/update_blend_recipes.py` - 블렌드 레시피 업데이트 스크립트 (229 lines)
- **수정**: 풀문 블렌드 레시피 업데이트 (마사이 40% + 안티구아 40% + 모모라 10% + g4 10%)
- **수정**: 뉴문 블렌딩 레시피 업데이트 (브라질 60% + 콜롬비아 30% + g4 10%)

#### 🎯 주요 기능
- **블렌드 원가 계산**: 손실률 17% 반영 공식 적용
  - 풀문: ₩6,566/kg → ₩22,000 판매 (마진 70.2%)
  - 뉴문: ₩6,253/kg → ₩4,000 판매 (마진 -56.3%, 가격 조정 필요)
- **레시피 검증**: 비율 합계 100% 자동 검증

## [0.18.0] - 2025-11-07

### ✨ 마이너 업데이트 (Minor Update): 마스터플랜 v2 Phase 1 T1-2 완료

#### 📝 변경사항
- **추가**: `app/update_bean_master_data.py` - 원두 마스터 데이터 업데이트 스크립트 (174 lines)
- **수정**: 4개 원두 정보 업데이트 (마사이, g4, 브라질, 콜롬비아)
- **검증**: 6개 필수 원두 확인 (마사이, 안티구아, 모모라, g4, 브라질, 콜롬비아)

#### 🎯 주요 기능
- **원두 정보**: 국가명, 로스팅 레벨, 가격/kg, 설명 자동 설정
- **가격 책정**: 에티오피아 ₩5,000, 케냐 ₩6,000, 브라질 ₩4,700, 콜롬비아 ₩5,900

## [0.17.0] - 2025-11-07

### ✨ 마이너 업데이트 (Minor Update): 마스터플랜 v2 Phase 1 T1-1 완료

#### 📝 변경사항
- **추가**: `app/migrate_roasting_data.py` - 로스팅 데이터 마이그레이션 스크립트 (327 lines)
- **수정**: `app/models/database.py` - RoastingLog 모델에 bean_id 추가
- **수정**: `app/models/__init__.py` - RoastingLog export 추가

#### 🎯 주요 기능
- **데이터 마이그레이션**: 2개월(2025-09, 2025-10) 테스트 데이터 생성
  - 14개 로스팅 기록
  - 생두량: 33,975.88kg
  - 로스팅량: 28,200kg
  - 손실률: 17% (목표 일치)
- **원두 자동 생성**: 마사이, 안티구아, 모모라, g4, 브라질, 콜롬비아 (6종)
- **데이터 검증**: 손실률, 날짜, 무게 자동 검증

## [0.16.0] - 2025-11-06

### 🧪 테스트 개선 (Test Coverage: 94% → 96%)

#### 📝 변경사항
- **추가**: `app/tests/test_cost_service.py` - CostService 테스트 8개 추가 (+185)
- **추가**: `app/tests/test_excel_service.py` - ExcelService 중복 날짜 테스트 추가 (+31)

#### 🎯 주요 개선사항

**테스트 커버리지 향상**
- **전체 커버리지**: 94% → 96% (목표 초과 달성!)
- **cost_service.py**: 82% → 96% (14% 향상)
- **excel_service.py**: 93% → 97% (4% 향상)
- **전체 테스트**: 211개 → 220개 (9개 추가)
- **Missing lines**: 65 → 46 (19 lines 커버)

**CostService 테스트 추가**
1. `test_get_bean_price_history` - 가격 변경 이력 조회 (26 lines 커버)
2. `test_get_bean_price_history_invalid_bean` - 없는 원두 예외 처리
3. `test_get_bean_price_history_no_changes` - 이력 없을 때 빈 리스트 반환
4. `test_update_bean_price_no_change` - 가격 동일 시 이력 미기록
5. `test_update_cost_setting_new_parameter` - 신규 설정 추가 (insert)
6. `test_get_blend_cost_with_selling_price` - 판매가 있을 때 마진 계산
7. `test_get_blend_cost_missing_bean_in_recipe` - 원두 누락 시 건너뛰기
8. `test_batch_calculate_with_error` - 일괄 계산 중 에러 처리

**ExcelService 테스트 추가**
1. `test_validate_phase1_migration_duplicate_dates` - 중복 날짜 감지 (3 lines 커버)

#### 🔧 기술 구현
- **BeanPriceHistory 모델 테스트**: 가격 변경 이력 CRUD 전체 커버
- **예외 처리 테스트**: ValueError, 데이터 누락, 중복 검증
- **엣지 케이스 커버**: 가격 변경 없음, 빈 블렌드, 잘못된 참조

---

### ✨ 마이너 업데이트 (Minor Update): CostCalculation Tab 4 - CostSetting 모델 완전 연동

#### 📝 변경사항
- **수정**: `app/pages/CostCalculation.py` - Tab 4 UI 활성화 및 CostSetting 연동 (+100, -26)

#### 🎯 주요 기능

**Tab 4: 비용 설정 - 완전 활성화**
- **현재 설정 표시 개선**
  - 4개 Metric 카드: 손실률, 로스팅 비용, 인건비, 전기료
  - CostSetting 테이블에서 실시간 데이터 불러오기
  - 설정값 없을 경우 기본값 사용 (fallback 로직)

- **비용 파라미터 설정 폼**
  - 손실률 슬라이더 (0~50%, 기본 17%)
  - 로스팅 비용 (원/kg, 기본 500원)
  - 인건비 (원/batch, 기본 10,000원)
  - 전기료 (원/batch, 기본 3,000원)
  - 기타 비용 (원/kg, 기본 200원)
  - 모든 컨트롤 활성화 (disabled 제거)

- **설정 저장/복원 기능**
  - 💾 설정 저장: CostService.update_cost_setting() 호출
  - ↺ 기본값 복원: 모든 설정을 기본값으로 초기화
  - 저장 후 st.rerun()으로 UI 자동 갱신
  - 성공/실패 메시지 표시

- **설정 정보 Expander**
  - 각 비용 파라미터에 대한 상세 설명
  - 손실률, 로스팅 비용, 인건비, 전기료, 기타 비용 안내

#### 🔧 기술 구현
- **CostService 연동**
  - `get_cost_setting(db, parameter_name)`: 설정값 조회
  - `update_cost_setting(db, parameter_name, value, description)`: 설정값 저장
- **Streamlit Form**: 일괄 입력 및 제출
- **st.metric()**: 현재 설정 시각화
- **예외 처리**: try-except로 안전한 에러 핸들링

#### 🧪 검증
- ✅ Streamlit 앱 정상 실행 확인
- ✅ 설정 불러오기 정상 작동
- ✅ 설정 저장 정상 작동 (예상)

## [0.15.0] - 2025-11-06

### ✨ 마이너 업데이트 (Minor Update): 원두 가격 변경 이력 추적 시스템 구현 (Tab 3)

#### 📝 변경사항
- **신규 모델**: `app/models/database.py` - BeanPriceHistory 모델 추가
- **마이그레이션**: `migrations/add_bean_price_history.py` - bean_price_history 테이블 생성
- **수정**: `app/services/cost_service.py` - update_bean_price, get_bean_price_history 메서드 추가 (+54줄)
- **수정**: `app/pages/CostCalculation.py` - Tab 3 UI 업데이트 (+100줄)

#### 🎯 주요 기능

**1. 데이터베이스 (BeanPriceHistory 모델)**
- bean_id: 원두 ID (FK)
- old_price: 이전 가격
- new_price: 새 가격
- change_reason: 변경 사유 (선택사항)
- created_at: 변경 일시
- Bean 모델에 price_history relationship 추가

**2. 비즈니스 로직 (CostService)**
- **update_bean_price 개선**
  - change_reason 파라미터 추가 (선택사항)
  - 가격 변경 시 자동으로 BeanPriceHistory에 이력 기록
  - 가격이 동일하면 이력 기록 안 함 (중복 방지)

- **get_bean_price_history 신규**
  - 원두별 가격 변경 이력 조회 (최신순)
  - limit 파라미터로 조회 개수 제어 (기본 10개, 최대 100개)
  - 변동액, 변동률 자동 계산
  - 반환값: 이력 리스트 (id, bean_name, old/new_price, change, created_at)

**3. UI 개선 (CostCalculation Tab 3)**
- **가격 변경 폼 개선**
  - 변경 사유 입력 필드 추가 (선택사항)
  - Placeholder: "예: 생두 가격 인상, 환율 변동, 품질 향상 등"

- **가격 변경 이력 표시**
  - 원두 선택 + 조회 개수 설정 (5~100개, 기본 10개)
  - 이력 테이블: 변경일시, 이전/새 가격, 변동액, 변동률, 변경 사유
  - Plotly 타임라인 차트: 가격 변동 추이 시각화
  - 📈 상승, 📉 하락, ➡️ 동일 아이콘 표시
  - hover 템플릿으로 상세 정보 표시

#### 🔧 기술 구현
- **SQLAlchemy ORM**: BeanPriceHistory 모델
- **마이그레이션**: bean_price_history 테이블 생성 (checkfirst=True)
- **Plotly Scatter Chart**: mode='lines+markers', 타임라인 시각화
- **변동률 계산**: (new_price - old_price) / old_price * 100
- **시간순 정렬**: order_by(desc(created_at)).limit(n)

#### 🧪 검증
- ✅ 마이그레이션 성공 (bean_price_history 테이블 생성)
- ✅ Streamlit 앱 정상 실행 확인
- ✅ import 오류 없음

## [0.14.1] - 2025-11-06

### 🐛 패치 (Bug Fix): ExcelSync 페이지 세션 상태 초기화 순서 버그 수정

#### 📝 변경사항
- **수정**: `app/pages/ExcelSync.py` - 세션 상태 초기화 순서 변경
- **수정**: `app/pages/RoastingReceipt.py` - 날짜 타입 변환 버그 수정
- **수정**: `app/services/excel_service.py` - import 경로 수정
- **업데이트**: `logs/VERSION` - 0.14.0 → 0.14.1

#### 🐛 버그 수정 상세

**1. ExcelSync 페이지 세션 상태 초기화 순서 버그**
- **문제**: `render_sidebar()` 호출 시 `st.session_state.db`가 초기화되지 않아 `AttributeError` 발생
- **원인**: 세션 상태 초기화가 `render_sidebar()` 호출 이후에 실행됨
- **해결**: 세션 상태 초기화 블록을 `render_sidebar()` 호출 전으로 이동
- **영향**: ExcelSync 페이지 새로고침 시 정상 작동

**2. ExcelService → ExcelSyncService 이름 변경**
- ExcelSync 페이지에서 사용하는 서비스 이름을 명확히 함
- Static 메서드만 사용하므로 인스턴스화 불필요

**3. Import 경로 일관성 개선**
- `app.models.database` → `models.database` (프로젝트 표준에 맞춤)

**4. RoastingReceipt 날짜 타입 변환 버그 수정**
- **문제**: 세션 상태 직렬화 시 날짜가 문자열로 변환됨
- **해결**: `st.data_editor` 호출 전 날짜 컬럼을 `date` 타입으로 보장
- **영향**: 날짜 입력 필드가 항상 올바른 타입으로 표시됨

#### 🧪 검증
- ✅ Streamlit 앱 정상 실행 확인
- ✅ ExcelSync 페이지 접근 가능
- ✅ 세션 상태 초기화 오류 해결

## [0.14.0] - 2025-11-05

### ✨ 마이너 업데이트 (Minor Update): 원가계산(CostCalculation) 페이지 구현

#### 📝 변경사항
- **신규 페이지**: `app/pages/CostCalculation.py` (547줄)
- **수정**: `app/components/sidebar.py` (+9줄, "🧮 원가계산" 메뉴 추가)

#### 🎯 주요 기능 (4개 탭)

**Tab 1: 블렌드별 원가 계산**
- 블렌드 선택 및 계산 단위 선택 (kg/cup)
- 실시간 원가 계산 (혼합원가, 최종원가, 제안판매가, 마진율)
- 구성 원두 상세 테이블 (최종 기여도 포함)
- 계산 공식 설명 (Expander)

**Tab 2: 전체 블렌드 일괄 비교**
- 모든 활성 블렌드 원가 일괄 계산
- 정렬 가능한 비교 테이블
- Plotly 차트 2개:
  - 손실 전/후 원가 비교 (막대 그래프)
  - 블렌드별 마진율 비교 (색상 코딩)

**Tab 3: 원두 가격 관리**
- 활성 원두 목록 및 현재 가격 표시
- 원두 가격 업데이트 폼
- 가격 변경 기록 (향후 추가 예정)

**Tab 4: 원가 설정**
- 현재 설정값 표시 (손실률, 비용 구조)
- 고급 설정 UI (향후 CostSetting 모델 연동 예정)
- 모든 컨트롤 disabled 상태 (미래 확장 대비)

#### 🔧 기술 구현
- **7단계 방법론** 적용: Constitution → Specify → Clarify → Plan → Tasks → Implement → Analyze
- **CostService** 연동: `get_blend_cost()`, `batch_calculate_all_blends()`, `update_bean_price()`
- **Plotly Express** 시각화: 비용 비교 및 마진 분석 차트
- **Streamlit 폼** 검증: 안전한 입력 처리

#### 📊 프로젝트 통계 업데이트
- 페이지: 9개 → 10개
- 총 코드: 9,500+줄 → 10,100+줄 (+600줄)
- 시각화: 35+ → 37+ 차트 (+2개)

## [Unreleased] - 2025-11-05

### ✅ 테스트 개선: ReportService 예외 처리 테스트 추가

#### 📝 변경사항
- **파일**: `app/tests/test_report_service.py`
- **목표**: 전체 커버리지 95% 달성

#### 🎯 주요 성과
- ✅ ReportService 커버리지: 88% → 93% (+5%p)
- ✅ 전체 커버리지: 94% → 95% (+1%p, 목표 달성!)
- ✅ 테스트 개수: 208개 → 211개 (+3개)
- ✅ 통과율: 100% 유지

#### 추가된 테스트 (3개)
1. **test_export_excel_exception_in_summary_sheet**
   - _create_summary_sheet에서 예외 발생 시 오류 시트 생성 테스트
   - bean_service.get_beans_summary() 예외 처리 경로 커버

2. **test_export_excel_exception_in_cost_sheet**
   - _create_cost_sheet에서 예외 발생 시 오류 시트 생성 테스트
   - DataFrame.to_excel() 예외 처리 경로 커버

3. **test_export_excel_all_sheets_empty_creates_default_sheet**
   - sheets_created == 0일 때 기본 "정보" 시트 생성 테스트
   - 모든 데이터가 비어있을 때 안전한 Excel 생성 확인

#### 최종 서비스별 커버리지
| 서비스 | 커버리지 | 상태 |
|--------|----------|------|
| LossRateAnalyzer | 100% | ✅ |
| RoastingService | 100% | ✅ |
| AnalyticsService | 99% | ✅ |
| AuthService | 96% | ✅ |
| **ReportService** | **93%** | ✅ **+5%p** |
| ExcelService | 93% | ✅ |
| BlendService | 92% | ✅ |
| BeanService | 91% | ✅ |
| CostService | 90% | ✅ |

#### 기술적 세부사항
- **Mock 전략**: unittest.mock.patch를 사용한 예외 주입
- **테스트 격리**: 각 테스트는 독립적으로 실행
- **예외 처리 검증**: 예외 발생 시에도 Excel 파일 생성 확인
- **데이터 검증**: 오류 메시지가 Excel 시트에 포함되는지 확인

---

## [0.13.7] - 2025-11-04

### 🐛 패치 (Bug Fix): 날짜 형식 변환 오류 수정

#### 📝 변경사항
- **파일**: `app/pages/RoastingReceipt.py` - calculate_results() 함수
- **문제**: `AttributeError: 'str' object has no attribute 'strftime'`
- **원인**: st.data_editor가 날짜를 str 또는 datetime 객체로 반환 (컨텍스트에 따라 다름)
- **해결**: 타입 체크 추가
  ```python
  # OLD:
  "날짜": row["날짜"].strftime("%Y-%m-%d") if not pd.isna(row["날짜"]) else ""

  # NEW:
  if pd.isna(row["날짜"]):
      date_str = ""
  elif isinstance(row["날짜"], str):
      date_str = row["날짜"]
  else:
      date_str = row["날짜"].strftime("%Y-%m-%d")
  ```

## [0.13.6] - 2025-11-04

### 🐛 패치 (Bug Fix): 상태 판정 로직 수정 및 예상 손실률 자동 계산 기능 추가

#### 📝 변경사항
- **파일**: `app/pages/RoastingReceipt.py`

**1️⃣ 상태 판정 로직 수정** (calculate_results 함수):
- **문제**: `abs(variance)` 사용으로 방향 무시 → -12% (예상보다 손실률 낮음 = 좋음)가 "🔴 위험"으로 표시됨
- **해결**: variance 방향을 고려한 로직으로 수정
  - `variance ≤ 0`: 예상보다 손실률 낮음 = 🟢 정상
  - `0 < variance ≤ 3%`: 🟢 정상
  - `3% < variance ≤ 5%`: 🟡 주의
  - `variance > 5%`: 🔴 위험

**2️⃣ 예상 손실률 자동 계산 기능 추가**:
- "🔢 예상 손실률 자동 계산" 버튼 추가 (데이터 입력 테이블 하단)
- 입력된 생두 무게와 로스팅 후 무게를 기반으로 실제 손실률 계산
- 계산된 값을 "예상손실률(%)" 컬럼에 자동으로 채워넣음
- 사용자가 수동으로 손실률을 계산할 필요 없이 버튼 클릭만으로 처리 가능

## [0.13.5] - 2025-11-04

### 🐛 패치 (Bug Fix): number_input max_value를 100.0에서 10000.0으로 확대

#### 📝 변경사항
- **파일**: `app/pages/RoastingRecord.py` (Tab 2, Tab 3), `app/pages/RoastingReceipt.py` (column_config)
- **문제**: `StreamlitAPIException: default_value 481.93 must be less than or equal to max_value 100.0`
- **원인**: 데이터베이스에 481.93kg 같은 대량 로스팅 기록 존재, 기존 max_value=100.0으로는 표시 불가
- **해결**:
  - 생두 무게(kg) 필드: max_value를 100.0 → 10000.0 (10톤)으로 확대
  - 로스팅 후 무게(kg) 필드: max_value를 100.0 → 10000.0 (10톤)으로 확대
  - 다양한 규모의 로스팅 작업 지원 가능

## [0.13.4] - 2025-11-04

### 🐛 패치 (Bug Fix): get_db() generator 대신 SessionLocal() 직접 사용

#### 📝 변경사항
- **파일**: `app/pages/RoastingRecord.py`, `app/pages/RoastingReceipt.py`
- **문제**: `AttributeError: 'generator' object has no attribute 'query'`
- **원인**:
  - `get_db()`는 FastAPI 의존성 주입용 generator (yield 사용)
  - Streamlit에서는 generator가 아닌 직접 인스턴스화된 세션 필요
- **해결**:
  ```python
  # OLD:
  if 'db' not in st.session_state:
      st.session_state.db = get_db()  # Generator 반환 (❌)

  # NEW:
  if 'db' not in st.session_state:
      st.session_state.db = SessionLocal()  # Session 직접 생성 (✅)
  ```

## [0.13.3] - 2025-11-04

### 🐛 패치 (Bug Fix): bean_service 및 blend_service 초기화 추가

#### 📝 변경사항
- **파일**: `app/pages/RoastingRecord.py`, `app/pages/RoastingReceipt.py`
- **문제**: `AttributeError: st.session_state has no attribute 'bean_service'`
- **원인**: sidebar.py의 통계 섹션 (line 196-197)이 bean_service와 blend_service를 요구
- **해결**: Session state에 BeanService 및 BlendService 초기화 추가
  ```python
  if 'bean_service' not in st.session_state:
      st.session_state.bean_service = BeanService(st.session_state.db)
  if 'blend_service' not in st.session_state:
      st.session_state.blend_service = BlendService(st.session_state.db)
  ```

## [0.13.2] - 2025-11-04

### 🐛 패치 (Bug Fix): language_manager 초기화 추가

#### 📝 변경사항
- **파일**: `app/pages/RoastingRecord.py`, `app/pages/RoastingReceipt.py`
- **문제**: `AttributeError: st.session_state has no attribute 'language_manager'`
- **원인**: sidebar.py가 language_manager를 요구하지만 로스팅 페이지에 초기화 코드 누락
- **해결**: BeanManagement.py 패턴을 따라 Translator 및 LanguageManager 초기화 추가
  ```python
  if "translator" not in st.session_state:
      st.session_state.translator = Translator(default_language="ko")
  if "language_manager" not in st.session_state:
      st.session_state.language_manager = LanguageManager(st.session_state.translator)
  ```

## [0.13.1] - 2025-11-04

### 🐛 패치 (Bug Fix): database import 경로 수정 (app.utils → app.models)

#### 📝 변경사항
- **파일**: `app/pages/RoastingRecord.py`, `app/pages/RoastingReceipt.py`
- **문제**: `ModuleNotFoundError: No module named 'app.utils.database'`
- **원인**: database.py가 app/models/에 위치하는데 app/utils/database에서 import 시도
- **해결**:
  ```python
  # OLD:
  from app.utils.database import get_db

  # NEW:
  from app.models import SessionLocal
  ```

## [0.13.0] - 2025-11-03

### ✨ 마이너 업데이트 (Minor Update): 로스팅 일괄 입력 페이지 구현 (RoastingReceipt.py)

#### 📝 변경사항

**새로운 페이지 추가 - RoastingReceipt.py** (335줄):
- `st.data_editor`를 활용한 Excel 스타일 그리드 입력 인터페이스
- 템플릿 생성 기능: 기본 10개 행, 사용자 지정 가능 (1~100)
- 동적 행 추가/삭제 (`num_rows="dynamic"`)
- 5개 입력 컬럼 with 타입 검증:
  - 날짜: `DateColumn` (미래 날짜 차단, 기본값 오늘)
  - 생두(kg): `NumberColumn` (0.0~100.0, 0.1 단위)
  - 로스팅후(kg): `NumberColumn` (0.0~100.0, 0.1 단위)
  - 예상손실률(%): `NumberColumn` (0.0~50.0, 0.1 단위, 기본값 17.0)
  - 메모: `TextColumn` (최대 500자)

**실시간 계산 및 검증**:
- `calculate_results()`: 실제손실률, 차이(%), 상태 표시
- 상태 판정 로직: 🟢 정상(±3%), 🟡 주의(±5%), 🔴 위험(±5% 초과)
- 별도 테이블로 계산 결과 실시간 표시
- `validate_all_rows()`: All or Nothing 검증 방식
  - 6가지 검증 규칙 적용
  - 빈 행 자동 건너뛰기
  - 오류 발생 시 전체 배치 거부

**배치 저장 기능**:
- 기존 `RoastingService.create_roasting_log()` 재사용
- 행별 개별 처리 with 실패 추적
- 성공/실패 상세 리포트 제공
- 저장 성공 시 템플릿 초기화 및 축하 애니메이션

**사이드바 메뉴 통합**:
- `sidebar.py`: "📝 로스팅 일괄입력" 버튼 추가
- "📦 운영 관리" 섹션 내 배치
- 페이지 활성 상태 표시 지원

#### 🧪 테스트
- Python 문법 검증 통과
- Streamlit 앱 실행 확인 (포트 8501)
- 메뉴 네비게이션 검증 완료

#### 📊 통계
- **파일**: 2개 수정 (1개 신규, 1개 업데이트)
  - `app/pages/RoastingReceipt.py` ← 신규 (335줄)
  - `app/components/sidebar.py` ← 메뉴 항목 추가
- **코드**: +335줄 추가

## [0.12.0] - 2025-11-03

### ✨ 마이너 업데이트 (Minor Update): RoastingRecord 페이지를 사이드바 메뉴에 추가

#### 📝 변경사항

**사이드바 메뉴 통합**:
- sidebar.py: "📦 운영 관리" 섹션에 "📊 로스팅 기록" 버튼 추가
- RoastingRecord.py: sidebar 렌더링 및 current_page 설정 추가
- 페이지 활성 상태 표시 기능 추가

**접근성 개선**:
- 사용자가 사이드바에서 직접 로스팅 기록 관리 페이지로 이동 가능
- "운영 관리" 메뉴 구성: 로스팅 기록 → 재고관리 → 보고서 → Excel동기화

**커밋**:
- `1b1dda36` - feat: RoastingRecord 페이지를 사이드바 메뉴에 추가

## [0.11.0] - 2025-11-03

### ✨ 마이너 업데이트 (Minor Update): 로스팅 기록 관리 페이지 구현 (RoastingRecord.py)

#### 📝 변경사항

**신규 페이지 추가**:
- 📊 **RoastingRecord.py** (598줄) - 로스팅 기록 관리 페이지
  - Tab 1: 📋 목록 조회 (필터링, 정렬, 통계 카드)
  - Tab 2: ➕ 기록 추가 (실시간 계산, 검증 로직)
  - Tab 3: ✏️ 기록 편집 (수정/삭제 기능)
  - Tab 4: 📊 통계 분석 (월별 통계, 추이 그래프)

**주요 기능**:
- ✅ 전체 CRUD 기능 (생성, 조회, 수정, 삭제)
- ✅ 실시간 손실률 계산 및 상태 표시 (🟢🟡🔴)
- ✅ 사용자 정의 필터링 (날짜, 개수, 정렬)
- ✅ 월별 통계 및 추이 그래프
- ✅ RoastingService 7개 메서드 완전 활용
- ✅ 입력 검증 (4가지 규칙)

**개발 방법론**:
- 7단계 체계적 개발 방법론 적용 (Constitution → Analyze)
- 명세 대비 100% 구현 달성

**커밋**:
- `df130207` - feat: 로스팅 기록 관리 페이지 구현

## [0.10.0] - 2025-11-03

### ✨ 테스트: ExcelService + ReportService 테스트 완성 (전체 94% 커버리지 달성)

#### 📝 변경사항

**1. ExcelService 테스트 완성 (0% → 93%)**:
- 총 14개 테스트 작성 (9개 기본 + 5개 검증)
- Bean 모델 필수 필드 추가 (no, roast_level)
- 빈 데이터 처리 테스트 수정 (None 반환 예상)
- validate_phase1_migration() 검증 테스트 추가
- get_migration_summary() 요약 테스트 추가

**2. ReportService 테스트 확장 (78% → 88%)**:
- 6개 추가 테스트 작성 (15→21, +6개)
  - test_export_to_excel_cost, blend, bean_usage
  - test_export_to_excel_no_sheets (빈 시트 생성)
  - test_export_to_csv_cost, bean_usage
- sample_transactions 픽스처 추가 (conftest.py)

**전체 테스트 통계**:
- 총 테스트: 188개 → 208개 (+20개)
- 전체 커버리지: 84% → 94% (+10%p)
- ExcelService: 0% → 93% (85/91 lines)
- ReportService: 78% → 88% (145/164 lines)
- 통과율: 100% (208/208)

**서비스별 커버리지** (9개 서비스, 평균 94%):
- RoastingService: 100% ✅
- LossRateAnalyzer: 100% ✅
- AnalyticsService: 99% ✅
- AuthService: 96% ✅
- ExcelService: 93% ✅ (NEW! 0%→93%)
- BlendService: 92% ✅
- BeanService: 91% ✅
- CostService: 90% ✅
- ReportService: 88% ✅ (NEW! 78%→88%)

**수정된 버그**:
1. Bean 모델 필수 필드 누락 (no, roast_level)
2. 빈 데이터 처리 assertion 불일치

**생성/수정된 파일**:
- app/tests/test_excel_service.py (14개 테스트)
- app/tests/test_report_service.py (15→21개, +6개)
- app/tests/conftest.py (sample_transactions 픽스처 추가)

**문서 업데이트**:
- README.md: v0.10.0 동기화, 208개 테스트, 94% 커버리지
- .claude/CLAUDE.md: v0.10.0 동기화
- SESSION_SUMMARY_2025-11-03.md: 신규 생성 및 업데이트
- CHANGELOG.md: [0.10.0] 종합 업데이트

**이전 세션 (2025-11-02)**:
- 데이터 검증 스크립트 및 리포트 생성
- ExcelService 기본 테스트 작성 (54% 커버리지)

## [0.9.1] - 2025-11-02

### 🐛 패치 (Bug Fix): test_analysis_workflow 테스트 수정 - 월초 날짜 문제 해결

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.9.0] - 2025-11-01

### ✨ 테스트: Phase 1 서비스 테스트 추가 - 103개 테스트 작성

#### 📝 변경사항

**전체 테스트 통계**
- 총 103개 테스트 작성 (100% 통과율)
- Phase 1 서비스 평균 커버리지: 90% (목표 88% 초과 달성)
- 테스트 실행 시간: ~11초

**Phase 1 서비스별 테스트 현황**

1. **BeanService 테스트** (35개 테스트, 커버리지 91%)
   - CRUD 작업 (생성, 조회, 수정, 삭제)
   - 조회 메서드 (ID, No, Name, Country, RoastLevel 등)
   - 비즈니스 로직 (재고 자동 생성, 소프트/하드 삭제)
   - 분석 기능 (요약 통계, 자주 사용되는 원두)
   - 초기화 및 내보내기

2. **BlendService 테스트** (39개 테스트, 커버리지 92%)
   - CRUD 작업 (블렌드 생성, 조회, 수정, 삭제)
   - 레시피 관리 (원두 추가/제거, 비율 재계산)
   - 원가 계산 (블렌드 원가, 제안 가격)
   - 분석 기능 (요약 통계)
   - 초기화 및 내보내기

3. **AnalyticsService 테스트** (14개 테스트, 커버리지 99%)
   - 트렌드 분석 (월별 거래 추이)
   - 재고 예측 및 사용량 예측
   - ROI 분석
   - 성능 지표
   - 원두별 효율성 분석
   - 블렌드 간 비교 분석

4. **ReportService 테스트** (15개 테스트, 커버리지 78%)
   - 월별 요약 데이터
   - 비용 분석
   - 원두 사용량 분석
   - 블렌드 성과 분석
   - Excel/CSV 내보내기

**수정된 버그 및 개선사항**

1. **blend_service.py 수정**
   - `add_recipe_to_blend()` 메서드의 `total_portion` 계산 로직 수정

2. **conftest.py 픽스처 개선**
   - `sample_blend`에 `total_portion` 명시적 설정 추가

3. **test_analytics_service.py 수정**
   - `Inventory` 픽스처에서 존재하지 않는 `location` 필드 제거

**생성된 파일**
- `app/tests/test_bean_service.py` (35개 테스트)
- `app/tests/test_blend_service.py` (39개 테스트)
- `app/tests/test_analytics_service.py` (14개 테스트)
- `app/tests/test_report_service.py` (15개 테스트)

**전체 프로젝트 테스트 현황**
- Phase 2 서비스: 85개 테스트 (커버리지 96.5%)
- Phase 1 서비스: 103개 테스트 (커버리지 90%)
- **총 188개 테스트** (100% 통과율)

### 📝 문서: 문서 업데이트 누락 방지 시스템 구축

#### 문제 발견
- 코드 작성 후 문서 업데이트를 반복적으로 누락하는 현상 발견
- 사용자가 두 번 지적한 후에야 업데이트 수행
- CHANGELOG, SESSION_SUMMARY, README 등 주요 문서 동기화 실패

#### 해결책 구현
- **.claude/CLAUDE.md**에 "3-단계 작업 완료 프로토콜" 추가
- 코드 작성 → 커밋 → 문서 4종 세트 업데이트 강제화
- 문서 4종 세트: CHANGELOG, SESSION_SUMMARY, README, CLAUDE.md

#### 기대 효과
- 문서 동기화 누락 방지
- 프로젝트 문서 일관성 유지
- 세션 간 연속성 보장

**수정된 파일:**
- `.claude/CLAUDE.md` - "🚨 작업 완료 = 3단계 필수" 규칙 추가

**커밋:** fc4660a

### 📝 문서: 7단계 체계적 개발 방법론 추가

#### 추가 배경
- 사용자 요청: 프로그래밍/플랜 작성 시 체계적 접근 방법 필요
- 기존: DEVELOPMENT_GUIDE의 5단계 (구현 중심)
- 신규: 상위 레벨 7단계 방법론 (프로젝트 전체)

#### 7단계 구조
1. **Constitution (원칙)** - 프로젝트 기본 원칙 수립
2. **Specify (명세)** - 요구사항 상세 정의
3. **Clarify (명확화)** - 불분명한 부분 질문으로 해소
4. **Plan (계획)** - 기술 스택과 아키텍처 결정
5. **Tasks (작업 분해)** - 실행 가능한 단위로 분해
6. **Implement (구현)** - 코드 작성 및 테스트
7. **Analyze (검증)** - 명세와 코드 일치 확인

#### 적용 범위
- 모든 프로그래밍 작업 시 필수 준수
- 플랜 작성 시 필수 준수
- TodoWrite와 AskUserQuestion 활용 강조

**수정된 파일:**
- `.claude/CLAUDE.md` - "🎯 7단계 체계적 개발 방법론" 섹션 추가 (52줄)

**커밋:** fd30ee2

---

## [0.9.0] - 2025-10-31

### ✨ 마이너 업데이트 (Minor Update): T2-8 Unit Tests 완료 - Phase 2 서비스 전체 테스트 구축

#### 📝 변경사항

**전체 테스트 통계**
- 총 85개 테스트 작성 (100% 통과율)
- Phase 2 서비스 평균 커버리지: 96.5% (목표 90% 초과 달성)
- 테스트 실행 시간: ~20초

**Phase 2 서비스별 테스트 현황**

1. **CostService 테스트** (15개 테스트, 커버리지 90%)
   - 블렌드 원가 계산 (기본, 컵 단위)
   - 원두 가격 업데이트 및 유효성 검증
   - 비용 설정 CRUD 작업
   - 일괄 계산 및 상세 분석
   - 경계값 테스트 (0 비율, 음수 가격)

2. **RoastingService 테스트** (21개 테스트, 커버리지 100%)
   - 로스팅 기록 CRUD 작업
   - 손실률 자동 계산 및 편차 검증
   - 월별 통계 및 조회
   - 이상치 탐지 (WARNING, CRITICAL, 연속 발생)
   - 통합 워크플로우 테스트

3. **AuthService 테스트** (25개 테스트, 커버리지 96%)
   - 사용자 생성 및 비밀번호 해싱 (passlib + bcrypt)
   - 인증 성공/실패 시나리오
   - 권한 부여/취소/확인 워크플로우
   - Admin 역할 특별 권한 검증
   - 비밀번호 변경 및 사용자 비활성화
   - 기본 권한 자동 할당

4. **LossRateAnalyzer 테스트** (16개 테스트, 커버리지 100%)
   - 손실률 트렌드 분석 (정상/주의/심각 상태)
   - 경고 생성/조회/해결 워크플로우
   - 월별 요약 통계
   - 연속 이상 탐지
   - 심각도별 분포 분석

5. **통합 테스트** (8개 테스트)
   - 완전한 로스팅 워크플로우 (기록 생성 → 이상 탐지 → 경고 해결)
   - 사용자 인증 및 권한 생명주기
   - 원가 계산 및 가격 업데이트 전파
   - 다중 사용자 동시 작업 시나리오

**수정된 버그 및 개선사항**

1. **conftest.py 픽스처 수정**
   - `BlendRecipe`에 `portion_count` 추가 (NOT NULL 제약 위반 해결)
   - `CostSetting` 픽스처를 단일 객체에서 리스트로 재구조화

2. **cost_service.py 개선**
   - `update_bean_price()`에 음수 가격 유효성 검증 추가

3. **roasting_service.py 수정**
   - 존재하지 않는 파라미터 제거 (`blend_recipe_version_id`, `operator_id`)

4. **bcrypt 버전 호환성 해결**
   - bcrypt 5.0.0 → 4.3.0 다운그레이드 (passlib 호환성)

**테스트 패턴 및 방법론**

- pytest 8.4.2 + pytest-cov 기반 테스트 프레임워크
- 인메모리 SQLite 데이터베이스를 사용한 격리된 테스트 환경
- Fixture 기반 테스트 데이터 관리
- 단위 테스트 + 통합 테스트 혼합 전략
- 경계값 테스트 및 예외 처리 검증
- @pytest.mark.integration 마커를 통한 테스트 분류

**다음 단계 (Phase 2 완료)**

- T2-8 Unit Tests 완료로 Phase 2 개발 완료
- Phase 2 진행률: 100% (T2-1 ~ T2-8 모두 완료)
- Phase 3 계획 수립 예정

## [0.8.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): T2-7 ExcelSyncService 개발 (Excel 동기화 및 마이그레이션)

#### 📝 변경사항

**ExcelSyncService 리팩토링**
- 정적 메서드 기반 설계로 전환
- 의존성 주입 패턴 적용
- 코드 라인 수: 526줄 → 204줄 (322줄 감소, 61% 최적화)

**주요 기능**

1. **export_roasting_logs_to_excel()**: 월별 로스팅 기록 Excel 내보내기
   - openpyxl을 사용한 프로페셔널 포맷팅
   - 헤더 스타일링 (굵게, 배경색, 정렬)
   - 컬럼 너비 자동 조정
   - 자동 파일 경로 생성

2. **validate_phase1_migration()**: Phase 1 마이그레이션 검증
   - 무게 유효성 확인 (양수값, NULL 체크)
   - 손실률 범위 검증 (0-50%)
   - 날짜 검증 (유효한 날짜)
   - 중복 데이터 탐지
   - 상세한 오류 리포팅 시스템

3. **get_migration_summary()**: 마이그레이션 요약 통계
   - 전체 데이터 통계
   - 총 무게 및 평균 손실률 계산
   - 마이그레이션 상태 보고

**특징**
- 로깅을 통한 상세한 추적
- 견고한 에러 핸들링
- 통계 계산 기능
- 유연한 파일 경로 관리

**파일**
- `app/services/excel_service.py`: 204 삽입(+), 322 삭제(-)

## [0.7.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): T2-6 LossRateAnalyzer 개발 (손실률 이상 탐지)

#### 📝 변경사항

**모델 개선**
- `RoastingLog`에 `warnings` 관계 추가
- `LossRateWarning`에 `roasting_log` 관계 추가
- 경고에서 로스팅 정보 직접 접근 가능

**LossRateAnalyzer 서비스 (310줄 신규 추가)**

1. **손실률 트렌드 분석**
   - `analyze_loss_rate_trend()`: 기간별 통계 분석
   - 평균, 중앙값, 표준편차 계산
   - 이상치 개수 및 비율 산출

2. **경고 관리**
   - `get_recent_warnings()`: 미해결 경고 조회
   - `resolve_warning()`: 경고 해결 처리
   - `detect_continuous_anomalies()`: 연속 이상 탐지

3. **추가 분석 기능**
   - `get_monthly_summary()`: 월별 요약
   - `get_severity_distribution()`: 심각도별 분포

**특징**
- 3% 경고 임계값 (ATTENTION)
- 5% 심각 임계값 (CRITICAL)
- NORMAL/ATTENTION/CRITICAL 상태 자동 판단
- 통계적 이상치 탐지
- 상세 로깅 시스템

**파일**
- `app/models/database.py`: 6 삽입(+)
- `app/services/loss_rate_analyzer.py`: 310 삽입(+) (신규)

## [0.6.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): T2-5 AuthService 개발 (인증 및 권한 관리)

#### 📝 변경사항

**AuthService 구현 (398줄 신규 추가)**

1. **사용자 인증 및 관리**
   - `create_user()`: 새 사용자 생성 + 기본 권한 자동 설정
   - `authenticate()`: 사용자 인증 (bcrypt 해시 검증)
   - `change_password()`: 비밀번호 변경 (보안 검증)
   - `deactivate_user()`: 사용자 비활성화

2. **권한 관리**
   - `grant_permission()`: 사용자에게 권한 부여
   - `revoke_permission()`: 사용자 권한 취소
   - `has_permission()`: 사용자 권한 확인
   - `get_user_permissions()`: 사용자의 모든 권한 조회

3. **사용자 조회**
   - `get_user_by_username()`: 사용자명으로 조회
   - `get_user_by_id()`: ID로 조회
   - `list_all_users()`: 모든 사용자 조회

**특징**
- bcrypt 해시 기반 보안 시스템
- Admin/Editor/Viewer 역할 기반 접근 제어 (RBAC)
- 마지막 로그인 자동 추적
- 기본 권한 자동 설정
- 상세한 감사 로그

**의존성 추가**
- `passlib==1.7.4`: 비밀번호 해싱
- `bcrypt==4.1.2`: 암호화

**파일**
- `app/services/auth_service.py`: 398 삽입(+) (신규)
- `requirements.txt`: 6 삽입(+), 1 삭제(-)

## [0.5.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): T2-4 CostService 개발 (핵심 비즈니스 로직)

#### 📝 변경사항

**CostService 구현 (277줄 신규 추가)**

1. **블렌드 원가 계산**
   - `get_blend_cost()`: 최종 원가 계산 (손실률 17% 반영)
   - 공식: `Final Cost = (Σ(Bean Cost × Ratio%)) / (1 - Loss Rate)`
   - 실제 비즈니스 로직 구현

2. **가격 관리**
   - `update_bean_price()`: 원두 가격 업데이트
   - 가격 이력 자동 저장 (BeanPriceHistory)
   - 타임스탬프 기반 가격 추적

3. **일괄 계산**
   - `batch_calculate_all_blends()`: 모든 블렌드 일괄 계산
   - 대량 처리 최적화
   - 계산 결과 요약 제공

4. **비용 설정 관리**
   - `get_cost_setting()`: 비용 설정값 조회
   - `update_cost_setting()`: 비용 설정값 업데이트
   - 손실률, 마진율 등 설정 관리

5. **상세 분석**
   - `calculate_blend_cost_with_components()`: 상세 원가 분석
   - 원두별 기여도 계산
   - 단위별 원가 (kg, cup)
   - 마진율 자동 계산

**특징**
- 17% 표준 손실률 적용
- 정확한 원가 계산 로직
- 상세 로깅 시스템
- 에러 핸들링

**파일**
- `app/services/cost_service.py`: 277 삽입(+) (신규)

## [0.4.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): Phase 2 T2-1, T2-2 완료 - DB 스키마 확장 및 모델 정의

#### 📝 변경사항

**T2-1: DB 스키마 설계 및 생성 ✅**

5개 새 테이블 생성 (직접 SQL 실행):
- `blend_recipes_history` (13 컬럼) - 레시피 버전 관리
- `users` (11 컬럼) - 사용자 관리
- `user_permissions` (6 컬럼) - 권한 관리
- `audit_logs` (10 컬럼) - 감사 로그
- `loss_rate_warnings` (10 컬럼) - 손실률 이상 경고

**DB 확장**: 8개 테이블 → 13개 테이블

**T2-2: SQLAlchemy 모델 추가 ✅**

6개 새 SQLAlchemy 모델 클래스 추가:
- `RoastingLog` (11 컬럼): 로스팅 기록
- `BlendRecipesHistory` (13 컬럼): 레시피 버전 이력
- `User` (11 컬럼): 사용자
- `UserPermission` (6 컬럼): 사용자 권한
- `AuditLog` (10 컬럼): 감사 로그
- `LossRateWarning` (10 컬럼): 손실률 경고

**모델 확장**: 6개 → 11개

**추가 수정**
- Boolean import 추가 (SQLAlchemy 타입 오류 해결)
- 관계(relationship) 설정
- 백업 생성: `backups/roasting_data_before_migration.db`

**진행율**
- Phase 2: 22% 완료 (2/9 태스크)
- 전체 프로젝트: 48% 완료

**파일**
- `data/roasting_data.db`: 90KB → 139KB (54% 증가)
- `app/models/database.py`: 107 삽입(+)
- `Documents/Progress/Phase2진행상황_2025-10-29.md`: 339 삽입(+) (신규)
- `backups/`: 백업 파일 및 로스팅 메모 이미지 추가

## [0.3.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): Phase 1 완료 - 데이터 기초 구축 (v1.6.0)

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.2.1] - 2025-10-29

### 🐛 패치 (Bug Fix): test_data.py 현재 데이터베이스 스키마에 맞게 수정

#### 📝 변경사항
1. **app/test_data.py** - 데이터베이스 스키마 업데이트
   - 이전 sqlite3 직접 사용 → SQLAlchemy ORM 사용으로 변경
   - bean_prices 테이블 참조 제거 (Bean 모델의 price_per_kg 사용)
   - roasting_logs 테이블 → transactions 테이블로 변경
   - 모델 import 경로 수정 (models.models → models)
   - Bean 상태값 "활성" → "active"로 수정

#### 📊 결과
- ✅ 60개의 테스트 거래 데이터 생성 완료
  - 입고 거래: 30개
  - 출고 거래: 30개
  - 마지막 30일 거래 기록 생성

## [0.2.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): 3가지 기능 개선 적용

#### 📝 변경사항
1. **BlendManagement.py** - 레시피 편집 UI 추가
   - 기존 블렌드의 레시피 선택 및 수정 기능 추가 (Lines 455-520)
   - 원두와 포션 개수 수정 가능
   - 저장 및 삭제 버튼으로 레시피 관리 개선

2. **InventoryManagement.py** - 재고 범위 설정 커스터마이징
   - 최소/최대 재고량을 원두별로 설정 가능 (Lines 250-270)
   - 기본값 유지 (최소: 5.0kg, 최대: 50.0kg)
   - 입고 시 사용자 정의 범위 적용 (Lines 285-286)

3. **Settings.py** - 데이터 초기화 확인 로직 개선
   - 두 단계 확인 프로세스로 실수 방지 (Lines 467-507)
   - st.session_state를 통한 상태 관리
   - 명확한 경고 메시지와 취소 버튼 제공

## [0.1.0] - 2025-10-29

### 🎯 초기 버전

#### 📝 변경사항
- 프로젝트 시작: 버전 리셋 및 새로운 버전 관리 시스템 도입
- 효율적인 버전관리 전략 수립 (logs/VERSION_STRATEGY.md)
- 세션 관리 시스템 완성 (SESSION_START_CHECKLIST, SESSION_END_CHECKLIST)
- 작업 완료 후 처리 프로세스 명시

#### 🔄 버전 관리 개선
- PATCH/MINOR/MAJOR 누적 기준 명확화
- 모든 문서(README.md, CLAUDE.md) 버전 동기화 규칙 추가
- 버전 올리는 기준: PATCH(버그 3개+), MINOR(기능 3~4개+), MAJOR(호환성 변경)

#### 📚 문서화 완성
- logs/VERSION_STRATEGY.md 생성
- Documents/Progress/SESSION_SUMMARY_2025-10-29.md 생성
- CLAUDE.md에 "⚡ 빠른 버전 관리 참고" 섹션 추가
- SESSION_END_CHECKLIST.md 상세화

---

## 🎯 향후 버전 계획

```
현재: 0.1.0 (초기 버전)
  ↓
2주 후: 0.1.1 (버그 수정 3개)
4주 후: 0.1.2 (문서 개선 5개)
6주 후: 0.2.0 (새 기능 3~4개) ← MINOR
8주 후: 0.2.1 (버그 수정 2개)
12주 후: 1.0.0 (프로덕션 배포) ← MAJOR
```

---

**마지막 업데이트**: 2025-10-29
