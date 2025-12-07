# 세션 요약 - 2025-12-07

## 📅 세션 정보

- **날짜**: 2025-12-07
- **시간**: 02:30 - 03:53 (약 1시간 23분)
- **현재 버전**: 0.0.6

---

## ✅ 완료된 작업

### 1. Inventory API 버그 수정 (심각)

- **문제**: `/inventory` 페이지에서 "데이터를 불러오는데 실패했습니다" 에러
- **원인**:
  1. `inventory_logs` 라우터가 메인 API에 등록되지 않음 (404)
  2. Pydantic 스키마와 SQLAlchemy 모델의 필드명 불일치
- **수정 파일**:
  - `backend/app/api/v1/__init__.py`: inventory_logs 라우터 등록
  - `backend/app/schemas/inventory_log.py`: 필드명 통일 (transaction_type→change_type, quantity_change→change_amount, reason→notes)
  - `backend/app/services/inventory_log_service.py`: 필드명 통일
  - `backend/app/api/v1/endpoints/inventory_logs.py`: 파라미터명 수정
  - `frontend/lib/api.ts`: InventoryLog 타입 및 API 메서드 완전 구현
  - `frontend/app/inventory/page.tsx`: 새 필드명 사용
  - `frontend/app/page.tsx`: 새 필드명 사용

### 2. 사이드바 UI 수정

- **문제**: 사이드바 접힘 시 세로 줄무늬 발생
- **수정**:
  - `border-r`을 `isOpen` 상태일 때만 표시
  - `shadow`를 `isOpen` 상태일 때만 표시
  - 배경색 `bg-white/60` → `bg-white` (완전 불투명)
  - 호버 색상 `hover:bg-white/50` → `hover:bg-latte-100` (메뉴 아이템만)
- **파일**: `frontend/components/layout/Sidebar.tsx`

### 3. 메인 페이지 Hero 컴포넌트 통일

- **문제**: 메인 Hero와 PageHero 스타일 불일치
- **수정**: 메인 Hero를 PageHero와 동일한 스타일로 변경
  - `min-h-[400px]`, `flex items-center`, `shadow-md`, `hover:shadow-lg`, `mb-8` 등 추가
  - 이미지에 `hover:scale-105` 효과 추가
- **파일**: `frontend/components/home/Hero.tsx`

### 4. Beans 페이지 이미지 매핑 수정

- **문제**: 원두 카드에 잘못된/중복 이미지 표시
- **수정**: `getBeanImage` 함수를 실제 이미지 경로(`/images/raw_material/`)와 매칭
- **파일**: `frontend/app/beans/page.tsx`

### 5. 싱글 오리진 로스팅 페이지 개선

- **목표**: 생산량 기반 자동 계산 및 UI/UX 통일
- **구현**:
  - `Input` -> `Target Weight` 방식으로 변경 (역산 공식 적용)
  - 2-Column Grid Layout 적용 (좌측 설정 / 우측 시뮬레이션)
  - Shadcn UI `Select`, `Input`, `Badge` 컴포넌트 적용
  - 재고 부족 경고 및 손실률 자동 반영 로직 추가
- **파일**: `frontend/app/roasting/single-origin/page.tsx`

---

## 🐛 알려진 이슈 (미해결)

### 사이드바 호버 시 줄무늬 현상

- **상황**: 메인 페이지에서만 사이드바 토글 버튼 hover 시 세로 줄무늬가 간헐적으로 보임
- **원인 추정**: `hover:bg-white/50` 스타일이 Hero 배경과 간섭
- **시도한 해결책**:
  - 사이드바 border/shadow 조건부 적용 ✅
  - 사이드바 배경 불투명 처리 ✅
  - Hero negative margin 확장 (복구함)
- **다음 시도 필요**:
  - Hero와 사이드바 z-index 관계 재검토
  - 토글 버튼 hover 스타일을 불투명 색상으로 변경 검토

---

## 📂 수정된 주요 파일

### Backend

- `backend/app/api/v1/__init__.py`
- `backend/app/schemas/inventory_log.py`
- `backend/app/services/inventory_log_service.py`
- `backend/app/api/v1/endpoints/inventory_logs.py`
- `backend/test_api_response.py` (테스트용)

### Frontend

- `frontend/lib/api.ts`
- `frontend/app/inventory/page.tsx`
- `frontend/app/page.tsx`
- `frontend/app/beans/page.tsx`
- `frontend/app/roasting/single-origin/page.tsx`
- `frontend/components/layout/Sidebar.tsx`
- `frontend/components/home/Hero.tsx`

---

## 🚀 다음 세션 TODO

1. **사이드바 호버 줄무늬 이슈 완전 해결**
   - 토글 버튼 hover 스타일 재검토
   - z-index 및 레이어 구조 분석

2. **Sticky Footer 이슈 (이전 세션에서 미해결)**
   - 콘텐츠가 짧을 때 Footer가 바닥에 붙지 않는 문제

3. **기능 테스트 및 고도화**
   - 블렌드 로스팅 기능 구현 (백엔드 연동)
   - 재고 관리 대시보드 시각화 강화

4. **버전 업데이트 고려**
   - 이번 세션에서 주요 버그 수정됨 (PATCH 버전 업데이트 고려)

---

## 💡 참고 사항

- 백엔드: `http://localhost:8000`
- 프론트엔드: `http://localhost:3500`
- 데이터베이스: SQLite (`backend/themoon.db`)
