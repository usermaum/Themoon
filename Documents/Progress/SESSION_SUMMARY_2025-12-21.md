# 세션 요약: 2025-12-21 (Cost Analysis & Analytics)

## 📅 세션 정보
- **날짜**: 2025년 12월 21일
- **목표**: 원가 정밀 분석(FIFO) 로직 구현 및 통계 대시보드 구축
- **버전**: 0.3.0 → 0.4.0 (Minor Update)

## ✅ 주요 성과 (Key Achievements)

### 1. Backend: 정밀 원가 분석 시스템 구축
- **Virtual FIFO 로직 구현**: `CostService`
  - 기존의 단순 평균 단가가 아닌, 실제 입고된 배치(`InboundItem`) 순서대로 소진되는 가상 FIFO 모델 적용.
  - 로스팅 시점에 사용된 원두의 정확한 매입 단가를 역추적하여 계산.
- **통계 서비스 구현**: `StatsService`
  - 공급자별 매입 통계 (공급자명 정규화 포함: "ABC(주)" → "ABC")
  - 월별 매입 추이 및 품목별 단가 변동 내역 집계

### 2. Frontend: 비즈니스 분석 대시보드 (`/analytics`)
- **UI 구성**:
  - **공급자 분석**: `SupplierPieChart` (Recharts)
  - **원가 추이**: `CostTrendChart` (라인 차트)
  - **재고 가치**: `InventoryValueTable` (현재 재고 평가액)
- **통합**: `PageHero` 공통 헤더 적용 및 사이드바 메뉴 연동

### 3. 안정화 및 버그 수정
- **Router 경로 수정**: Frontend와 Backend 간 API 경로 불일치 현상 해결 (`/inbound`, `/inventory-logs`).
- **서비스 오류 수정**: `StatsService` 내 필드명 오류(`total_amount`) 및 Import 누락 해결.
- **문서 한글화**: `GEMINI.md` 규칙에 따라 모든 아티팩트(Walkthrough, Implementation Plan)를 한글로 작성.

## 📝 변경된 파일
- `backend/app/services/cost_service.py` (New)
- `backend/app/services/stats_service.py` (New)
- `backend/app/api/v1/analytics.py` (New)
- `backend/app/main.py` (Modified)
- `frontend/app/analytics/page.tsx` (New)
- `frontend/components/analytics/*` (New)
- `frontend/components/layout/Sidebar.tsx` (Modified)

## ⚠️ 이슈 및 해결
- **이슈**: `AttributeError: type object 'InboundDocument' has no attribute 'grand_total'`
- **해결**: 모델 정의를 확인하여 `total_amount`로 필드명 수정.
- **이슈**: `NameError: name 'desc' is not defined`
- **해결**: SQLAlchemy import 문에 `desc` 추가.

## 🔜 다음 계획
1. **로스팅 로그 연동**: 구현된 `calculate_fifo_cost`를 실제 로스팅 로그 저장 시점에 적용하여 `cost_per_kg` 기록.
2. **날짜 필터링**: 대시보드에 조회 기간 설정 기능 추가.

---

## 📌 세션 후반부 (2025-12-21 저녁)

### 버전 동기화 완료
- **작업**: 모든 문서의 버전을 0.4.0으로 동기화
- **변경 파일**:
  - `logs/VERSION`: 0.3.0 → 0.4.0
  - `.claude/CLAUDE.md` Line 4: 0.3.0 → 0.4.0
  - `README.md`:
    - Line 76: v0.1.0 → v0.4.0
    - Line 122: 0.3.0 → 0.4.0
    - Line 601: 커밋 해시 업데이트 (02595e2 → 2067190)
- **커밋**: 57ffaf4 "docs: 버전 동기화 0.3.0 → 0.4.0"

### 프로젝트 구조 정리
- **작업**: README에서 삭제된 `data/` 폴더 제거
- **이유**: 데이터베이스는 프로젝트 루트의 `themoon.db` 사용
- **커밋**: 14d9ae0 "docs: README에서 삭제된 data 폴더 제거"
