# 더문(The Moon) 시스템 기능 구현 및 수정 계획 (Implementation Plan)

본 문서는 `Themoon_Rostings.md`에 정의된 운영 시나리오와 기준 정보를 바탕으로, 실제 시스템 기능을 구현하고 수정하기 위한 기술적 실행 계획을 기술합니다.

---

## 1. 데이터베이스 설계 및 수정 (Database Schema)

운영 시나리오를 지원하기 위해 데이터 모델을 재설계하거나 수정해야 합니다.

### 1.1 주요 테이블 정의
*   **Beans (원두 마스터)**
    *   `id`: PK
    *   `name`: 원두명 (예: 예가체프, 마사이)
    *   `type`: 유형 (GREEN_BEAN: 생두, ROASTED_SINGLE: 싱글오리진, BLEND: 블렌드)
    *   `origin_code`: 국가 코드 (Eth, K, Co 등)
    *   `current_stock_kg`: 현재 재고량
    *   `avg_cost_price`: 평균 매입/생산 단가

*   **Recipes (블렌딩 레시피)**
    *   `id`: PK
    *   `blend_bean_id`: FK (Beans - 블렌드 제품)
    *   `ingredient_bean_id`: FK (Beans - 재료 원두)
    *   `ratio_percent`: 배합 비율 (%)

*   **InboundDocuments (입고 문서)**
    *   `id`: PK
    *   `file_path`: 영수증/견적서 파일 경로
    *   `upload_date`: 업로드 일시
    *   `status`: 상태 (PENDING, VERIFIED, CONFIRMED)
    *   `raw_ocr_data`: OCR 추출 원본 데이터 (JSON)

*   **Transactions (재고 수불 내역)**
    *   `id`: PK
    *   `bean_id`: FK
    *   `type`: 유형 (INBOUND: 입고, ROASTING_IN: 로스팅투입, ROASTING_OUT: 로스팅생산, BLENDING_IN: 블렌딩투입, BLENDING_OUT: 블렌딩생산, SALES: 판매, LOSS: 손실)
    *   `amount_kg`: 수량 (+/-)
    *   `cost_price`: 당시 단가
    *   `related_doc_id`: 관련 문서 ID (입고 시)
    *   `created_at`: 일시

---

## 2. 기능 구현 상세 (Feature Implementation)

### 2.1 자재 입고 기능 (Material Inbound) - **Priority: High**
> **목표**: 견적서/영수증 이미지를 통해 생두 입고를 자동화하고 재고에 반영한다.

*   **UI/UX**:
    *   파일 업로드 영역 (Drag & Drop) 및 카메라 촬영 지원.
    *   OCR 인식 결과와 원두 마스터 매핑 확인/수정 그리드(Grid).
    *   '입고 확정' 버튼.
*   **Backend Logic**:
    *   **OCR Integration**: Google Gemini 또는 Claude API를 활용하여 이미지에서 품목명, 수량, 단가 추출.
    *   **Fuzzy Matching**: 추출된 품목명과 DB의 `Beans` 테이블 이름을 유사도 기반으로 자동 매칭 추천.
    *   **Stock Update**: 확정 시 `Transactions`에 INBOUND 기록 추가 및 `Beans` 재고/평균단가 갱신.

### 2.2 로스팅 관리 기능 (Roasting Management) - **Priority: High**
> **목표**: 로스팅 수행 결과를 기록하고 손실률을 자동 계산하여 재고를 조정한다.

*   **UI/UX**:
    *   로스팅 대상 생두 선택 및 투입량(Input) 입력 폼.
    *   로스팅 후 생산량(Output) 입력 폼.
    *   실시간 손실률(%) 표시.
*   **Backend Logic**:
    *   **Validation**: 투입량이 현재 생두 재고보다 많은지 체크.
    *   **Transaction**:
        1.  생두 재고 차감 (ROASTING_IN)
        2.  원두(싱글) 재고 증가 (ROASTING_OUT)
    *   **Cost Calculation**: `(생두 총 투입 비용) / (원두 생산량)`으로 로스팅된 원두의 단가 재산정.

### 2.3 블렌딩 관리 기능 (Blending Management) - **Priority: Medium**
> **목표**: 정의된 레시피에 따라 블렌드 제품을 생산하고 재고를 처리한다.

*   **UI/UX**:
    *   블렌드 제품 선택 (풀문, 뉴문 등).
    *   목표 생산량 입력 시, 필요한 재료 원두 소요량 자동 계산 표시.
    *   '생산 완료' 버튼.
*   **Backend Logic**:
    *   **Recipe Load**: 선택된 블렌드의 레시피(`Recipes`) 조회.
    *   **Stock Check**: 필요한 재료 원두의 재고 부족 여부 확인.
    *   **Transaction**:
        1.  각 재료 원두 재고 차감 (BLENDING_IN)
        2.  블렌드 제품 재고 증가 (BLENDING_OUT)
    *   **Cost Calculation**: 각 재료 원두의 투입 원가 가중 평균으로 블렌드 단가 산정.

### 2.4 재고 및 원가 대시보드 (Dashboard) - **Priority: Low**
> **목표**: 현재 재고 현황과 가치를 한눈에 파악한다.

*   **UI/UX**:
    *   원두 유형별(생두/싱글/블렌드) 재고 리스트 카드.
    *   재고 부족 알림 (Safety Stock 미달 시 하이라이트).
# 더문(The Moon) 시스템 기능 구현 및 수정 계획 (Implementation Plan)

본 문서는 `Themoon_Rostings.md`에 정의된 운영 시나리오와 기준 정보를 바탕으로, 실제 시스템 기능을 구현하고 수정하기 위한 기술적 실행 계획을 기술합니다.

---

## 1. 데이터베이스 설계 및 수정 (Database Schema)

운영 시나리오를 지원하기 위해 데이터 모델을 재설계하거나 수정해야 합니다.

### 1.1 주요 테이블 정의
*   **Beans (원두 마스터)**
    *   `id`: PK
    *   `name`: 원두명 (예: 예가체프, 마사이)
    *   `type`: 유형 (GREEN_BEAN: 생두, ROASTED_SINGLE: 싱글오리진, BLEND: 블렌드)
    *   `origin_code`: 국가 코드 (Eth, K, Co 등)
    *   `current_stock_kg`: 현재 재고량
    *   `avg_cost_price`: 평균 매입/생산 단가

*   **Recipes (블렌딩 레시피)**
    *   `id`: PK
    *   `blend_bean_id`: FK (Beans - 블렌드 제품)
    *   `ingredient_bean_id`: FK (Beans - 재료 원두)
    *   `ratio_percent`: 배합 비율 (%)

*   **InboundDocuments (입고 문서)**
    *   `id`: PK
    *   `file_path`: 영수증/견적서 파일 경로
    *   `upload_date`: 업로드 일시
    *   `status`: 상태 (PENDING, VERIFIED, CONFIRMED)
    *   `raw_ocr_data`: OCR 추출 원본 데이터 (JSON)

*   **Transactions (재고 수불 내역)**
    *   `id`: PK
    *   `bean_id`: FK
    *   `type`: 유형 (INBOUND: 입고, ROASTING_IN: 로스팅투입, ROASTING_OUT: 로스팅생산, BLENDING_IN: 블렌딩투입, BLENDING_OUT: 블렌딩생산, SALES: 판매, LOSS: 손실)
    *   `amount_kg`: 수량 (+/-)
    *   `cost_price`: 당시 단가
    *   `related_doc_id`: 관련 문서 ID (입고 시)
    *   `created_at`: 일시

---

## 2. 기능 구현 상세 (Feature Implementation)

### 2.1 자재 입고 기능 (Material Inbound) - **Priority: High**
> **목표**: 견적서/영수증 이미지를 통해 생두 입고를 자동화하고 재고에 반영한다.

*   **UI/UX**:
    *   파일 업로드 영역 (Drag & Drop) 및 카메라 촬영 지원.
    *   OCR 인식 결과와 원두 마스터 매핑 확인/수정 그리드(Grid).
    *   '입고 확정' 버튼.
*   **Backend Logic**:
    *   **OCR Integration**: Google Gemini 또는 Claude API를 활용하여 이미지에서 품목명, 수량, 단가 추출.
    *   **Fuzzy Matching**: 추출된 품목명과 DB의 `Beans` 테이블 이름을 유사도 기반으로 자동 매칭 추천.
    *   **Stock Update**: 확정 시 `Transactions`에 INBOUND 기록 추가 및 `Beans` 재고/평균단가 갱신.

### 2.2 로스팅 관리 기능 (Roasting Management) - **Priority: High**
> **목표**: 로스팅 수행 결과를 기록하고 손실률을 자동 계산하여 재고를 조정한다.

*   **UI/UX**:
    *   로스팅 대상 생두 선택 및 투입량(Input) 입력 폼.
    *   로스팅 후 생산량(Output) 입력 폼.
    *   실시간 손실률(%) 표시.
*   **Backend Logic**:
    *   **Validation**: 투입량이 현재 생두 재고보다 많은지 체크.
    *   **Transaction**:
        1.  생두 재고 차감 (ROASTING_IN)
        2.  원두(싱글) 재고 증가 (ROASTING_OUT)
    *   **Cost Calculation**: `(생두 총 투입 비용) / (원두 생산량)`으로 로스팅된 원두의 단가 재산정.

### 2.3 블렌딩 관리 기능 (Blending Management) - **Priority: Medium**
> **목표**: 정의된 레시피에 따라 블렌드 제품을 생산하고 재고를 처리한다.

*   **UI/UX**:
    *   블렌드 제품 선택 (풀문, 뉴문 등).
    *   목표 생산량 입력 시, 필요한 재료 원두 소요량 자동 계산 표시.
    *   '생산 완료' 버튼.
*   **Backend Logic**:
    *   **Recipe Load**: 선택된 블렌드의 레시피(`Recipes`) 조회.
    *   **Stock Check**: 필요한 재료 원두의 재고 부족 여부 확인.
    *   **Transaction**:
        1.  각 재료 원두 재고 차감 (BLENDING_IN)
        2.  블렌드 제품 재고 증가 (BLENDING_OUT)
    *   **Cost Calculation**: 각 재료 원두의 투입 원가 가중 평균으로 블렌드 단가 산정.

### 2.4 재고 및 원가 대시보드 (Dashboard) - **Priority: Low**
> **목표**: 현재 재고 현황과 가치를 한눈에 파악한다.

*   **UI/UX**:
    *   원두 유형별(생두/싱글/블렌드) 재고 리스트 카드.
    *   재고 부족 알림 (Safety Stock 미달 시 하이라이트).
    *   총 재고 자산 가치 표시.

---

## 3. 개발 단계별 진행 계획 (Phased Plan)

### Phase 1: 기반 구축 및 입고 자동화 (Foundation)
- [x] 1. DB 스키마 설계 및 마이그레이션.
- [x] 2. 원두 마스터 데이터(`Beans`, `Recipes`) 초기 적재.
- [x] 3. OCR 연동 모듈 개발 및 입고 등록 페이지 구현.
    - [x] OCR 연동 및 이미지 업로드
    - [x] 입고 등록 UI
    - [x] 중복 방지 (Invoice Number)
    - [x] 원두 매칭 (Fuzzy Matching) 기능 구현

### Phase 2: 데이터 모델 고도화 및 생산 (Refinement & Production)
> **Goal**: `Themoon_Rostings_v2.md` 기준의 SKU 체계(생두 vs 원두) 확립.

- [x] 1. 데이터 모델 개선 (Data Model Refinement)
    - [x] **Beans 테이블 확장**: `type` (GREEN/ROASTED), `roast_profile` (LIGHT/MEDIUM/DARK), `cost_price` 추가.
    - [x] **API 스키마 업데이트**: Pydantic 모델에 신규 필드 반영.
    - [x] **DB 마이그레이션**: 기존 테이블 구조 변경 적용.
- [x] 2. 로스팅 관리 기능 (Roasting Management)
    - [x] UI: 생두/원두 탭 분리 (Inventory Page).
    - [x] UI: 로스팅 입력 폼 (New Page Needed).
    - [x] Backend: 투입량/생산량 기반 재고 처리 및 원가 계산 로직.
- [x] 3. 블렌딩 관리 기능 (Blending Management)
    - [x] UI: 블렌드 레시피 선택 및 생산.
    - [x] Backend: 블렌드 생산 로직 적용 (Standard Post-roast).

### Phase 3: 대시보드 및 안정화 (Analytics)
1.  [x] 재고 현황 대시보드 개발 (안전재고 알림).
2.  [ ] 전체 시나리오(입고->로스팅->블렌딩) 통합 테스트.
3.  [ ] UI 폴리싱 및 사용자 피드백 반영.
