# TheMoon 프로젝트 기능 흐름도 (Feature Flows)

> **문서 버전**: 1.0
> **최종 업데이트**: 2025-12-22
> **프로젝트 버전**: 0.4.5

---

## 📋 목차

1. [시스템 개요](#시스템-개요)
2. [전체 아키텍처](#전체-아키텍처)
3. [핵심 기능별 흐름도](#핵심-기능별-흐름도)
   - [Beans Management (생두 관리)](#1-beans-management-생두-관리)
   - [Inbound Processing (입고 처리)](#2-inbound-processing-입고-처리)
   - [Roasting Operations (로스팅 작업)](#3-roasting-operations-로스팅-작업)
   - [Blends Management (블렌드 관리)](#4-blends-management-블렌드-관리)
   - [Inventory Tracking (재고 추적)](#5-inventory-tracking-재고-추적)
   - [Analytics Dashboard (분석 대시보드)](#6-analytics-dashboard-분석-대시보드)
   - [Cost Calculation (원가 계산)](#7-cost-calculation-원가-계산)
4. [데이터 모델 관계도](#데이터-모델-관계도)
5. [API 엔드포인트 참조](#api-엔드포인트-참조)

---

## 시스템 개요

TheMoon은 커피 로스팅 사업의 **생두 구매부터 로스팅, 원가 계산까지** 전 과정을 관리하는 시스템입니다.

### 핵심 모듈

- **Frontend**: Next.js 14 (App Router, TypeScript)
- **Backend**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **AI/ML**: Google Gemini 2.5 Flash (OCR & Document Analysis)

### 주요 기능 (7가지)

1. **Beans Management**: 생두/로스팅 원두 재고 관리
2. **Inbound Processing**: 명세서 OCR 분석 및 입고 처리
3. **Roasting Operations**: 단일 원산지 & 블렌드 로스팅
4. **Blends Management**: 블렌드 레시피 관리
5. **Inventory Tracking**: 재고 이동 로그 추적
6. **Analytics Dashboard**: 비용 분석 및 통계
7. **Cost Calculation**: FIFO 기반 원가 계산

---

## 전체 아키텍처

```mermaid
graph TB
    subgraph FE ["Frontend (Next.js)"]
        UI["User Interface"]
        Pages["Pages<br/>46개 페이지"]
        Hooks["Custom Hooks"]
        API_Client["API Client"]
    end

    subgraph BE ["Backend (FastAPI)"]
        Router["API Router"]
        Services["Business Logic<br/>9개 서비스"]
        Models["Data Models<br/>8개 모델"]
    end

    subgraph Ext ["External Services"]
        Gemini["Google Gemini<br/>OCR Service"]
        Storage["Image Storage<br/>로컬 파일시스템"]
    end

    subgraph DB ["Database"]
        PG["PostgreSQL"]
    end

    UI --> Pages
    Pages --> Hooks
    Hooks --> API_Client
    API_Client -->|HTTP/JSON| Router
    Router --> Services
    Services --> Models
    Models --> PG
    Services --> Gemini
    Services --> Storage

    style UI fill:#e1f5fe
    style Router fill:#fff3e0
    style PG fill:#e8f5e9
    style Gemini fill:#f3e5f5
```

---

## 핵심 기능별 흐름도

### 1. Beans Management (생두 관리)

**페이지**: `/beans`, `/beans/new`, `/beans/[id]`
**API**: `GET/POST/PUT/DELETE /api/v1/beans`
**서비스**: `BeanService`
**모델**: `Bean`

#### 1.1 생두 목록 조회 플로우

```mermaid
sequenceDiagram
    participant User
    participant Page as "Beans Page"
    participant Hook as "useBeans"
    participant API as "API Client"
    participant Backend as "Backend API"
    participant DB as "PostgreSQL"

    User->>Page: /beans 접속
    Page->>Hook: useBeans() 호출
    Hook->>API: GET /api/v1/beans
    API->>Backend: HTTP Request
    Backend->>DB: SELECT * FROM beans
    DB-->>Backend: Bean 목록
    Backend-->>API: JSON Response
    API-->>Hook: Bean[]
    Hook-->>Page: 상태 업데이트
    Page-->>User: 생두 카드 렌더링
```

#### 1.2 생두 등록 플로우

```mermaid
graph TD
    Start(["사용자: 생두 등록 버튼 클릭"]) --> Form["/beans/new<br/>등록 폼 렌더링"]
    Form --> Input["입력 항목:<br/>- 이름<br/>- 원산지<br/>- 수량<br/>- 단가<br/>- 타입"]
    Input --> Validate{입력 검증}
    Validate -->|실패| Error[에러 메시지 표시]
    Validate -->|성공| Submit[POST /api/v1/beans]
    Submit --> Backend[BeanService.create_bean]
    Backend --> DB[(DB INSERT)]
    DB --> Redirect[/beans로 리다이렉트]
    Redirect --> End([생두 목록에 추가됨])

    Error --> Input

    style Start fill:#e1f5fe
    style End fill:#c8e6c9
    style Error fill:#ffcdd2
```

#### 1.3 주요 기능

- **필터링**: 타입별 (GREEN_BEAN, ROASTED_BEAN, BLEND_BEAN)
- **검색**: 이름, 원산지
- **정렬**: 이름순, 재고순
- **이미지**: 16개 생두 품종 × 3종 이미지 (original/webview/thumbnail)
- **수량 조정**: PATCH `/beans/{id}/quantity`
- **배치 체크**: POST `/beans/check-batch` (매칭 확인)

---

### 2. Inbound Processing (입고 처리)

**페이지**: `/inventory/inbound`, `/inventory/inbound/list`, `/inventory/inbound/view`
**API**: `POST /api/v1/inbound/analyze`, `POST /api/v1/inbound/confirm`
**서비스**: `OCRService`, `ImageService`, `BeanService`
**모델**: `InboundDocument`, `InboundItem`, `Supplier`

#### 2.1 명세서 분석 플로우 (OCR)

```mermaid
sequenceDiagram
    participant User
    participant Upload as "Inbound Page"
    participant Gemini as "Gemini AI<br/>(OCR)"
    participant Image as "ImageService"
    participant Backend as "Backend API"
    participant Matching as "Bean Matching"
    participant DB as PostgreSQL

    User->>Upload: 이미지 업로드<br/>(파일 or URL)
    Upload->>Upload: 파일 유효성 검증
    Upload->>Backend: POST /inbound/analyze

    Backend->>Image: validate_image()
    Image-->>Backend: ✅ 검증 성공

    Backend->>Image: process_and_save()
    Image->>Image: 3종 이미지 생성<br/>(original/webview/thumb)
    Image-->>Backend: 이미지 경로

    Backend->>Gemini: analyze_image()
    Gemini->>Gemini: AI 문서 판독
    Gemini-->>Backend: OCR JSON 결과

    Backend->>Matching: 생두 매칭
    Matching->>DB: SELECT beans<br/>(이름, 원산지 매칭)
    DB-->>Matching: 후보 생두 목록
    Matching-->>Backend: 매칭 결과

    Backend-->>Upload: 분석 결과 JSON
    Upload-->>User: 미리보기 + 편집 가능
```

#### 2.2 입고 확정 플로우

```mermaid
graph TD
    Start(["OCR 분석 완료"]) --> Review["사용자: 데이터 검토/수정"]
    Review --> Items{모든 항목 생두 매칭?}
    Items -->|"일부 미매칭"| Match["생두 매칭 UI<br/>- 자동 제안<br/>- 수동 선택"]
    Match --> Items
    Items -->|"모두 매칭 완료"| Confirm["저장 버튼 클릭"]
    Confirm --> API["POST /inbound/confirm"]

    API --> Duplicate{"중복 체크<br/>계약번호"}
    Duplicate -->|"중복"| Alert["경고 메시지"]
    Alert --> Review

    Duplicate -->|"신규"| Save["트랜잭션 시작"]
    Save --> Doc["InboundDocument 저장"]
    Doc --> Supplier["Supplier 저장"]
    Supplier --> Items_Loop["InboundItem 저장<br/>반복"]
    Items_Loop --> Inventory["Inventory Log 생성<br/>(재고 입고)"]
    Inventory --> Bean_Update["Bean 수량 증가"]
    Bean_Update --> Commit["트랜잭션 커밋"]
    Commit --> Reset["폼 초기화"]
    Reset --> End(["입고 완료"])

    style Start fill:#e1f5fe
    style End fill:#c8e6c9
    style Alert fill:#ffcdd2
```

#### 2.3 OCR JSON 스키마 (Gemini 2.5 Flash)

```json
{
  "error": null,
  "debug_raw_text": "문서 전체 텍스트",
  "document_info": {
    "document_number": "문서번호",
    "contract_number": "발주번호 (중복 체크 키)",
    "issue_date": "YYYY-MM-DD",
    "invoice_date": "YYYY-MM-DD",
    "invoice_type": "GSC | HACIELO | STANDARD"
  },
  "supplier": {
    "name": "공급자명",
    "business_number": "사업자등록번호",
    "address": "주소"
  },
  "items": [
    {
      "bean_name": "Ethiopia Yirgacheffe",
      "quantity": 300,
      "unit": "kg",
      "unit_price": 15000,
      "amount": 4500000
    }
  ],
  "amounts": {
    "subtotal": 4500000,
    "tax_amount": 450000,
    "total_amount": 4950000
  }
}
```

#### 2.4 이미지 처리 파이프라인

```mermaid
graph LR
    Upload["원본 이미지<br/>업로드"] --> Validate{"보안 검증"}
    Validate -->|"실패"| Reject["거부"]
    Validate -->|"통과"| Process["이미지 처리"]

    Process --> Original["Original<br/>1600x2400<br/>JPEG 95%"]
    Process --> Webview["Webview<br/>1200x1800<br/>WEBP 85%"]
    Process --> Thumbnail["Thumbnail<br/>400x400<br/>WEBP 75%"]

    Original --> Save[파일 저장<br/>YYYY/MM 폴더]
    Webview --> Save
    Thumbnail --> Save

    Save --> DB_Update[DB 경로 저장]
    DB_Update --> Done([완료])

    style Reject fill:#ffcdd2
    style Done fill:#c8e6c9
```

---

### 3. Roasting Operations (로스팅 작업)

**페이지**: `/roasting/single-origin`, `/roasting/blend`
**API**: `POST /api/v1/roasting/roast` (예정)
**서비스**: `RoastingService`
**모델**: `Bean`, `Blend`, `InventoryLog`

#### 3.1 단일 원산지 로스팅 플로우

```mermaid
graph TD
    Start(["로스터: 작업 시작"]) --> Select["/roasting/single-origin<br/>생두 선택"]
    Select --> Input["입력 항목:<br/>- 생두 선택 (GREEN_BEAN)<br/>- 로스팅 무게<br/>- 로스팅 프로파일<br/>- 수율(%)"]
    Input --> Calc["수율 계산<br/>로스팅 무게 = 생두 × 수율"]
    Calc --> Validate{"재고 충분?"}
    Validate -->|"부족"| Error["재고 부족 경고"]
    Validate -->|"충분"| Submit["로스팅 실행"]

    Submit --> Deduct["생두 재고 차감<br/>FIFO 원가 계산"]
    Deduct --> Create["로스팅 원두 생성<br/>type: ROASTED_BEAN<br/>roast_profile: LIGHT/MEDIUM/DARK"]
    Create --> Log["Inventory Log 2건:<br/>1. 생두 출고<br/>2. 로스팅 원두 입고"]
    Log --> Cost["원가 이전<br/>생두 → 로스팅 원두"]
    Cost --> End(["로스팅 완료"])

    Error --> Input

    style Start fill:#e1f5fe
    style End fill:#c8e6c9
    style Error fill:#ffcdd2
```

#### 3.2 블렌드 로스팅 플로우

```mermaid
sequenceDiagram
    participant Roaster
    participant Page as "Blend Roasting Page"
    participant Service as "RoastingService"
    participant Blend as "BlendService"
    participant Bean as "BeanService"
    participant Cost as "CostService"
    participant DB as "PostgreSQL"

    Roaster->>Page: 블렌드 선택
    Page->>Blend: getBlendById(id)
    Blend->>DB: SELECT blend + items
    DB-->>Blend: 블렌드 레시피
    Blend-->>Page: 레시피 표시

    Roaster->>Page: 로스팅 무게 입력
    Page->>Service: calculateRequiredBeans()
    Service-->>Page: 필요 생두 수량

    Roaster->>Page: 로스팅 실행
    Page->>Service: roastBlend()

    loop 각 블렌드 재료
        Service->>Bean: checkStock(bean_id)
        Bean-->>Service: 재고 확인
    end

    Service->>Cost: calculateFIFO()
    Cost-->>Service: 원가 계산

    Service->>Bean: deductBeans()
    Service->>Bean: createRoastedBean()
    Service->>DB: INSERT inventory_logs
    Service-->>Page: 완료
    Page-->>Roaster: 성공 메시지
```

---

### 4. Blends Management (블렌드 관리)

**페이지**: `/blends`, `/blends/new`, `/blends/[id]`
**API**: `GET/POST/PUT/DELETE /api/v1/blends`
**서비스**: `BlendService`
**모델**: `Blend`, `BlendItem`

#### 4.1 블렌드 레시피 생성 플로우

```mermaid
graph TD
    Start(["로스터: 블렌드 생성"]) --> Form["/blends/new<br/>레시피 폼"]
    Form --> Basic["기본 정보:<br/>- 블렌드 이름<br/>- 설명<br/>- 타겟 무게"]
    Basic --> Items["재료 추가<br/>(생두 or 로스팅 원두)"]
    Items --> Ratio["비율 입력<br/>합계 100%"]
    Ratio --> Check{"비율 합계?"}
    Check -->|"!= 100%"| Error["에러: 합계 100% 필요"]
    Check -->|"= 100%"| Valid["비율 검증 성공"]
    Valid --> Preview["미리보기<br/>필요 수량 계산"]
    Preview --> Save["POST /api/v1/blends"]
    Save --> DB[("블렌드 저장")]
    DB --> End(["레시피 생성 완료"])

    Error --> Ratio

    style Start fill:#e1f5fe
    style End fill:#c8e6c9
    style Error fill:#ffcdd2
```

#### 4.2 블렌드 데이터 구조

```typescript
interface Blend {
  id: number
  name: string
  description: string
  is_active: boolean
  created_at: string
  blend_items: BlendItem[]
}

interface BlendItem {
  id: number
  blend_id: number
  bean_id: number
  ratio_percent: number  // 0-100
  bean: Bean
}
```

**예시**: Full Moon Blend

```json
{
  "name": "Full Moon Blend",
  "description": "밸런스 잡힌 블렌드",
  "blend_items": [
    {
      "bean_id": 1,  // Ethiopia Yirgacheffe
      "ratio_percent": 40
    },
    {
      "bean_id": 5,  // Colombia Huila
      "ratio_percent": 30
    },
    {
      "bean_id": 8,  // Brazil Santos
      "ratio_percent": 30
    }
  ]
}
```

---

### 5. Inventory Tracking (재고 추적)

**페이지**: `/inventory`
**API**: `GET /api/v1/inventory-logs`, `POST /api/v1/inventory-logs`
**서비스**: `InventoryLogService`
**모델**: `InventoryLog`

#### 5.1 재고 이동 로그 시스템

```mermaid
erDiagram
    INVENTORY_LOG {
        int id PK
        int bean_id FK
        string change_type
        float quantity_change
        float quantity_after
        string reason
        datetime created_at
        jsonb metadata
    }

    BEAN {
        int id PK
        float current_quantity
    }

    INVENTORY_LOG ||-- "BEAN" : tracks
```

#### 5.2 재고 변동 트리거

```mermaid
graph TD
    subgraph IN_Group
        Inbound["입고 확정"] --> IN_Log["InventoryLog<br/>type: IN<br/>quantity: +300"]
    end

    subgraph OUT_Group
        Roasting["로스팅 실행"] --> OUT_Log["InventoryLog<br/>type: OUT<br/>quantity: -50"]
    end

    subgraph ADJUST_Group
        Manual["수동 조정"] --> ADJUST_Log["InventoryLog<br/>type: ADJUST<br/>quantity: ±10"]
    end

    IN_Log --> Update["Bean.quantity 업데이트"]
    OUT_Log --> Update
    ADJUST_Log --> Update

    Update --> Trigger["quantity_after 계산"]
    Trigger --> Save[("로그 저장")]

    style Save fill:#c8e6c9
```

---

### 6. Analytics Dashboard (분석 대시보드)

**페이지**: `/analytics`
**API**: `GET /api/v1/dashboard`
**서비스**: `StatsService`, `CostService`
**모델**: `Bean`, `InboundDocument`, `InventoryLog`

#### 6.1 대시보드 데이터 흐름

```mermaid
sequenceDiagram
    participant User
    participant Page as "Analytics Page"
    participant API as "Dashboard API"
    participant Stats as "StatsService"
    participant Cost as "CostService"
    participant DB as "PostgreSQL"

    User->>Page: /analytics 접속
    Page->>API: GET /api/v1/dashboard

    par 병렬 데이터 조회
        API->>Stats: get_total_beans()
        Stats->>DB: SELECT COUNT(*)
        DB-->>Stats: 총 생두 수

        API->>Stats: get_total_inventory_value()
        Stats->>DB: SUM(quantity * price)
        DB-->>Stats: 총 재고 가치

        API->>Cost: get_average_cost()
        Cost->>DB: AVG(unit_price)
        DB-->>Cost: 평균 단가

        API->>Stats: get_recent_inbound()
        Stats->>DB: SELECT * ORDER BY date DESC
        DB-->>Stats: 최근 입고 내역
    end

    API-->>Page: 종합 통계 JSON
    Page->>Page: 차트 렌더링
    Page-->>User: 대시보드 표시
```

#### 6.2 분석 지표

```typescript
interface DashboardMetrics {
  // 재고 통계
  total_beans: number
  total_quantity_kg: number
  total_inventory_value: number

  // 원가 통계
  average_cost_per_kg: number
  weighted_average_cost: number

  // 활동 통계
  recent_inbound_count: number
  recent_roasting_count: number

  // 트렌드 차트 데이터
  monthly_inbound: Array<{month: string, value: number}>
  cost_trend: Array<{date: string, cost: number}>
  inventory_movement: Array<{date: string, in: number, out: number}>
}
```

---

### 7. Cost Calculation (원가 계산)

**서비스**: `CostService`
**알고리즘**: FIFO (First-In-First-Out)

#### 7.1 FIFO 원가 계산 로직

```mermaid
graph TD
    Start(["로스팅 요청<br/>50kg"]) --> Query["재고 조회<br/>입고일 오름차순"]
    Query --> Inventory["입고 배치:<br/>1. 30kg @ 15,000원<br/>2. 40kg @ 16,000원<br/>3. 50kg @ 14,000원"]

    Inventory --> Allocate1["배치 1: 30kg 사용<br/>원가: 450,000원"]
    Allocate1 --> Allocate2["배치 2: 20kg 사용<br/>원가: 320,000원"]
    Allocate2 --> Total["총 원가: 770,000원<br/>평균 단가: 15,400원/kg"]

    Total --> Update1["배치 1: 0kg 남음 ❌"]
    Total --> Update2["배치 2: 20kg 남음"]
    Total --> Update3["배치 3: 50kg 남음"]

    Update1 --> Log["InventoryLog:<br/>- 배치 1 OUT: -30kg<br/>- 배치 2 OUT: -20kg"]
    Update2 --> Log
    Update3 --> Log

    Log --> End(["로스팅 원두 원가: 770,000원"])

    style Start fill:#e1f5fe
    style End fill:#c8e6c9
```

#### 7.2 원가 계산 시나리오

**시나리오**: Colombia Huila 50kg 로스팅

**재고 현황** (입고일 순):

| 입고일     | 수량 | 단가     | 잔여 |
| ---------- | ---- | -------- | ---- |
| 2025-01-10 | 30kg | 15,000원 | 30kg |
| 2025-01-25 | 40kg | 16,000원 | 40kg |
| 2025-02-05 | 50kg | 14,000원 | 50kg |

**FIFO 적용**:

1. 배치 1 (2025-01-10): 30kg × 15,000원 = 450,000원
2. 배치 2 (2025-01-25): 20kg × 16,000원 = 320,000원
3. **총 원가**: 770,000원
4. **평균 단가**: 15,400원/kg

**재고 업데이트**:

| 입고일         | 수량     | 단가         | 잔여 (After) |
| -------------- | -------- | ------------ | ------------ |
| ~~2025-01-10~~ | ~~30kg~~ | ~~15,000원~~ | ~~0kg~~ ❌    |
| 2025-01-25     | 40kg     | 16,000원     | **20kg** ✅   |
| 2025-02-05     | 50kg     | 14,000원     | 50kg         |

---

## 데이터 모델 관계도

```mermaid
erDiagram
    BEAN {
        int id PK
        string name
        string origin
        string bean_type
        float current_quantity
        float unit_price
        string roast_profile
    }

    BLEND {
        int id PK
        string name
        string description
        boolean is_active
    }

    BLEND_ITEM {
        int id PK
        int blend_id FK
        int bean_id FK
        float ratio_percent
    }

    INBOUND_DOCUMENT {
        int id PK
        string contract_number UK
        date invoice_date
        int supplier_id FK
        string original_image_path
        string webview_image_path
        string thumbnail_image_path
    }

    INBOUND_ITEM {
        int id PK
        int inbound_document_id FK
        int matched_bean_id FK
        string bean_name
        float quantity
        float unit_price
        float amount
    }

    SUPPLIER {
        int id PK
        string name
        string business_number
        string address
    }

    INVENTORY_LOG {
        int id PK
        int bean_id FK
        string change_type
        float quantity_change
        float quantity_after
        string reason
    }

    BEAN ||--o{ BLEND_ITEM : "includes"
    BLEND ||--o{ BLEND_ITEM : "composed_of"
    SUPPLIER ||--o{ INBOUND_DOCUMENT : "supplies"
    INBOUND_DOCUMENT ||--o{ INBOUND_ITEM : "contains"
    BEAN ||--o{ INBOUND_ITEM : "matches"
    BEAN ||--o{ INVENTORY_LOG : "tracked_by"
```

---

## API 엔드포인트 참조

### Beans API (`/api/v1/beans`)

| Method | Endpoint              | 기능           | 입력                 | 출력                     |
| ------ | --------------------- | -------------- | -------------------- | ------------------------ |
| GET    | `/`                   | 생두 목록 조회 | 필터, 검색, 정렬     | `BeanListResponse`       |
| GET    | `/{bean_id}`          | 생두 상세 조회 | bean_id              | `Bean`                   |
| POST   | `/`                   | 생두 등록      | `BeanCreate`         | `Bean`                   |
| PUT    | `/{bean_id}`          | 생두 수정      | bean_id,`BeanUpdate` | `Bean`                   |
| DELETE | `/{bean_id}`          | 생두 삭제      | bean_id              | 204 No Content           |
| GET    | `/stats/count`        | 생두 개수 통계 | -                    | `{count: number}`        |
| PATCH  | `/{bean_id}/quantity` | 수량 조정      | bean_id, quantity    | `Bean`                   |
| POST   | `/check-batch`        | 배치 매칭 체크 | `{names: string[]}`  | `Array<{name, matched}>` |

### Blends API (`/api/v1/blends`)

| Method | Endpoint      | 기능             | 입력                   | 출력           |
| ------ | ------------- | ---------------- | ---------------------- | -------------- |
| GET    | `/`           | 블렌드 목록 조회 | -                      | `Blend[]`      |
| GET    | `/{blend_id}` | 블렌드 상세 조회 | blend_id               | `Blend`        |
| POST   | `/`           | 블렌드 생성      | `BlendCreate`          | `Blend`        |
| PUT    | `/{blend_id}` | 블렌드 수정      | blend_id,`BlendUpdate` | `Blend`        |
| DELETE | `/{blend_id}` | 블렌드 삭제      | blend_id               | 204 No Content |

### Inbound API (`/api/v1/inbound`)

| Method | Endpoint                             | 기능            | 입력             | 출력                       |
| ------ | ------------------------------------ | --------------- | ---------------- | -------------------------- |
| POST   | `/analyze`                           | 명세서 OCR 분석 | 파일 or URL      | `OCRResponse`              |
| POST   | `/confirm`                           | 입고 확정       | `InboundConfirm` | 201 Created                |
| GET    | `/list`                              | 입고 내역 목록  | page, limit      | `PaginatedInboundResponse` |
| GET    | `/{document_id}`                     | 입고 상세 조회  | document_id      | `InboundDocument`          |
| GET    | `/check-duplicate/{contract_number}` | 중복 체크       | contract_number  | `{exists: boolean}`        |

### Inventory Logs API (`/api/v1/inventory-logs`)

| Method | Endpoint    | 기능           | 입력                        | 출력                       |
| ------ | ----------- | -------------- | --------------------------- | -------------------------- |
| GET    | `/`         | 재고 로그 조회 | bean_id, type, page         | `InventoryLogListResponse` |
| POST   | `/`         | 재고 로그 생성 | `InventoryLogCreate`        | `InventoryLog`             |
| PUT    | `/{log_id}` | 재고 로그 수정 | log_id,`InventoryLogUpdate` | `InventoryLog`             |
| DELETE | `/{log_id}` | 재고 로그 삭제 | log_id                      | 204 No Content             |

### Dashboard API (`/api/v1/dashboard`)

| Method | Endpoint | 기능          | 입력 | 출력               |
| ------ | -------- | ------------- | ---- | ------------------ |
| GET    | `/`      | 대시보드 통계 | -    | `DashboardMetrics` |

---

## 부록

### 페이지 전체 목록 (46개)

**핵심 기능 (13개)**:

- `/` - Home
- `/beans` - 생두 목록
- `/beans/new` - 생두 등록
- `/beans/[id]` - 생두 상세
- `/blends` - 블렌드 목록
- `/blends/new` - 블렌드 생성
- `/blends/[id]` - 블렌드 상세
- `/roasting` - 로스팅 메인
- `/roasting/single-origin` - 단일 원산지 로스팅
- `/roasting/blend` - 블렌드 로스팅
- `/inventory` - 재고 현황
- `/inventory/inbound` - 입고 처리 (OCR)
- `/inventory/inbound/list` - 입고 내역
- `/inventory/inbound/view` - 입고 상세
- `/analytics` - 분석 대시보드

**개발/테스트 페이지 (31개)**:

- `/design-demo` - 디자인 데모
- `/design-showcase` - 디자인 쇼케이스
- `/design-lab` (6개) - 디자인 스타일 테스트
- `/design-sample` (15개) - 컴포넌트 샘플
- `/components-demo` - 컴포넌트 데모
- `/sidebar-concepts` - 사이드바 컨셉
- `/rostings-invoice-demo` - 인보이스 데모
- `/inbound/invoice` - 인보이스 뷰

---

**문서 작성일**: 2025-12-22
**작성자**: Claude Sonnet 4.5
**관련 문서**:

- `Documents/Architecture/MENU_STRUCTURE.md`
- `Documents/Architecture/SYSTEM_ARCHITECTURE.md`
- `Documents/Planning/IMAGE_OPTIMIZATION_PLAN.md`
