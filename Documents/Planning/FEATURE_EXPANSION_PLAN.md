# 기능 확장 계획: 원가 분석 및 통계 (Feature Expansion Plan)

> **목표**: 100% 저장된 OCR 입고 데이터를 활용하여 정밀한 원가 분석 및 경영 통계 기능을 구현합니다.

---

## 1. 정밀 원가 분석 시스템 (Cost Analysis)

### 🎯 목표
기존의 '평균 단가(avg_price)' 방식에서 벗어나, **실제 입고된 명세서(Inbound Item)**의 단가를 기반으로 정확한 원가를 산출합니다.

### ⚙️ 구현 로직 (Logic)

#### A. 현재 방식 (AS-IS)
- `Bean.avg_price`: 사용자가 수동 입력하거나 단순 평균값 사용
- 정확도 낮음, 환율/세금 변동 반영 어려움

#### B. 개선 방식 (TO-BE)
- **FIFO (선입선출) 기반 원가 추적**
  1. 로스팅 시 사용된 생두량(kg) 파악
  2. `inventory_logs`를 역추적하여 해당 생두가 **어떤 입고(Inbound Item)**에서 왔는지 식별
  3. `inbound_items`의 `supply_amount` + `tax_amount` (실제 매입가) 적용
  4. 부대비용(배송비 등)을 `inbound_document_details`에서 가져와 N분의 1 배분

### 📋 데이터 소스
- `inbound_items.unit_price`: 공급 단가
- `inbound_items.tax_amount`: 세액
- `inbound_document_details.grand_total`: 총 합계 (검증용)

---

## 2. 경영 통계 대시보드 (Business Statistics)

### 🎯 목표
공급자별, 품목별 매입 현황을 시각화하여 구매 전략 수립을 지원합니다.

### 📊 주요 기능

#### A. 공급자 분석 (Supplier Analysis)
- **기간별 매입액**: 월별/분기별 총 매입 금액 추이 (Bar/Line Chart)
- **공급자 점유율**: 전체 매입 중 각 공급자가 차지하는 비중 (Pie Chart)
- **미수금 현황**: `payment_due_date` 기반 결제 예정 금액 및 기한 경과 알림

#### B. 품목 분석 (Item Analysis)
- **단가 변동 추이**: 특정 생두의 입고 단가 변화 그래프 (Line Chart)
- **최다 매입 품목**: 수량/금액 기준 Top 5 품목 리스트

---

## 3. 구현 단계 (Milestones)

### Phase 1: 데이터 연결 및 API (Backend)
- [ ] `CostService` 구현: FIFO 원가 계산 로직 작성
- [ ] `StatsService` 구현: 통계 쿼리 최적화 (Aggregation)
- [ ] API Endpoints 추가: `/api/v1/analytics/cost`, `/api/v1/analytics/stats/*`

### Phase 2: UI 구현 (Frontend)
- [ ] **Roasting Log Detail**: 로스팅 기록 상세 페이지에 '실제 원가' 표시
- [ ] **Stats Dashboard**: `/analytics` 페이지 신설 및 차트(Recharts/Chart.js) 구현

---

## 4. 기대 효과
- **정확한 마진율 계산**: 실제 투입 원가 기반으로 순수익 파악 가능
- **데이터 기반 구매**: 단가 추이 비교를 통한 최적 구매 시점 파악
