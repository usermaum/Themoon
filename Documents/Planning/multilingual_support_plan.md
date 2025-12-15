# 전사적 다국어(한글/영문) 지원 및 검색 시스템 개선 계획안

## 1. 개요 (Overview)
*   **목표**: 시스템 전체(원두 관리, 재고 관리, 로스팅 등)에서 한글("에티오피아")과 영문("Ethiopia")을 명확히 구분하여 저장하고, 어떤 언어로 검색하든 원하는 결과를 얻을 수 있도록 합니다.
*   **범위**: Frontend (모든 페이지), Backend (DB Schema & API), Data Migration.

## 2. 현황 및 문제점 (Current Status)
*   **DB**: `Bean` 모델에 `name`, `origin`이 단일 컬럼으로 존재하여 한/영 혼용 불가.
*   **UI**: 화면마다 한글/영문 표시 기준이 모호함.
*   **Data**: "Ethiopia"로만 저장된 경우 "에티오피아" 검색 시 결과 없음.

## 3. 개선 방안 (Implementation Plan)

### 3.1 DB 스키마 변경 (Database Schema)
`beans` 테이블을 확장하여 한글/영문 데이터를 분리 저장합니다.

#### `Bean` 모델 변경
```python
class Bean(Base):
    # ... 기존 필드 ...
    name = Column(String(100), index=True, nullable=True) # 하위 호환성 유지 
    
    name_ko = Column(String(100), index=True, comment="품목명(한글) - 예: 예가체프")
    name_en = Column(String(200), index=True, comment="품목명(영문) - 예: Yirgacheffe")
    
    origin = Column(String(50), nullable=True) # 하위 호환성 유지
    
    origin_ko = Column(String(50), index=True, comment="원산지(한글) - 예: 에티오피아")
    origin_en = Column(String(50), index=True, comment="원산지(영문) - 예: Ethiopia")
```

### 3.2 Backend 검색 로직 강화
`BeanService.get_beans` 및 관련 검색 API를 수정하여 4개 필드 전체에 대한 검색을 지원합니다.
*   **Search Query**: `OR` 조건으로 `name_ko`, `name_en`, `origin_ko`, `origin_en` 모두 검사.

### 3.3 UI/UX 전면 개편 (All Pages)

#### 1) 공통 컴포넌트 (Common)
*   **BeanSelect (Dropdown)**: 옵션 표시 시 `[한글명] 영문명` 포맷으로 표시 (예: `[예가체프] Yirgacheffe`). 검색 시 한글/영문 모두 필터링 동작.

#### 2) 원두 관리 페이지 (`/beans`)
*   **카드 UI**:
    *   **메인 타이틀**: `name_ko` (예: 예가체프) 강조.
    *   **서브 타이틀**: `name_en` (예: Yirgacheffe) 작게 표기.
    *   **원산지 뱃지**: `origin_ko` (예: 에티오피아) 표시.

#### 3) 재고 관리 페이지 (`/inventory`)
*   **테이블 UI**:
    *   **원두명 컬럼**: `name_ko` 위주 표시, 툴팁이나 하단에 `name_en` 병기.
    *   **원산지 컬럼**: `origin_ko` 표시.
*   **입출고 로그**:
    *   로그 생성 시점의 스냅샷이 아닌, 관계형으로 가져올 경우 `Bean`의 다국어 필드 활용.

#### 4) 로스팅 페이지 (`/roasting/*`)
*   **생두 선택**: 개선된 `BeanSelect` 컴포넌트 적용.
*   **시뮬레이션 결과**: 한글/영문 명칭 병기하여 정확한 품목 확인 유도.

### 3.4 데이터 마이그레이션 (Data Migration)
`Themoon_Rostings_v2.md`의 마스터 데이터를 기준으로 기존 DB를 일괄 업데이트합니다.
*   **Mapping Rule**:
    *   `Eth` -> `origin_ko`: 에티오피아, `origin_en`: Ethiopia
    *   `G1` -> `name_ko`/`name_en` 파싱 로직 적용.

## 4. 단계별 실행 (Action Items)

### Phase 1: Backend & DB (우선 순위)
1.  **Schema Update**: `models/bean.py` 수정 및 Alembic Migration (또는 재생성).
2.  **Service Logic**: `get_beans` 검색 쿼리 개선.
3.  **Data Seed**: `Themoon_Rostings_v2.md` 파서 구현 및 DB 초기화 스크립트 실행.

### Phase 2: Frontend Integration
1.  **API Type Definition**: `lib/api/types.ts`에 `name_ko`, `name_en` 등 필드 추가.
2.  **Common UI Update**: `BeanCard`, `BeanSelect` 등 재사용 컴포넌트 수정.
3.  **Page Update**: `/beans`, `/inventory`, `/roasting` 페이지 순차 적용.

### Phase 3: Verification
1.  **Search Test**: "Ethiopia" 검색 -> 결과 나옴 / "에티오피아" 검색 -> 결과 나옴.
2.  **Display Test**: 모든 페이지에서 깨짐 없이 한/영 병기 확인.
