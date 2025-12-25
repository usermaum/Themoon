# Project Menu Hierarchy & Optimization

## 1. 개요 (Overview)

현재 The Moon 프로젝트의 메뉴 구조를 분석하고, 사용자 워크플로우(Workflow)와 정보의 성격에 맞춰 최적의 메뉴 계층과 순서를 도출합니다.

## 2. 현재 메뉴 구조 (Current State)

The Moon 프로젝트의 실제 구현된 페이지(`frontend/app/**/page.tsx`)를 전수 조사하여, 누락 없는 메뉴 구조를 파악하고 최적화된 사용자 경험(UX)을 위한 메뉴 계층 및 순서를 정의합니다.

---

## 2. 구현된 페이지 목록 (Implemented Pages)

실제 라우팅(Routing) 기준 페이지 목록입니다. (데모/디자인 랩 제외)

| Level 1       | Level 2 | Level 3   | 경로 (Route)              | 설명                   | 비고                  |
| :------------ | :------ | :-------- | :------------------------ | :--------------------- | :-------------------- |
| **Home**      | -       | -         | `/`                       | 대시보드 메인          |                       |
| **Beans**     | 목록    | -         | `/beans`                  | 생두 재고/품목 관리    |                       |
|               | 등록    | -         | `/beans/new`              | 신규 생두 등록         |                       |
|               | 상세    | -         | `/beans/[id]`             | 생두 상세 정보         |                       |
| **Roasting**  | 목록    | -         | `/roasting`               | 로스팅 프로파일 목록   |                       |
|               | Single  | -         | `/roasting/single-origin` | 싱글 오리진 로스팅     |                       |
|               | Blend   | -         | `/roasting/blend`         | 블렌드 로스팅          |                       |
| **Blends**    | 목록    | -         | `/blends`                 | 블렌드 레시피 목록     |                       |
|               | 등록    | -         | `/blends/new`             | 신규 블렌드 생성       |                       |
|               | 상세    | -         | `/blends/[id]`            | 블렌드 상세/수정       |                       |
| **Inventory** | 현황    | -         | `/inventory`              | 통합 재고 현황         |                       |
|               | Inbound | 입고 등록 | `/inventory/inbound`      | 신규 입고(명세서) 등록 | 현: `/inbound` 믹스됨 |
|               |         | 입고 목록 | `/inventory/inbound/list` | 명세서(Invoice) 이력   | **(New Phase 4)**     |
|               |         | 상세 (구) | `/inbound/invoice`        | *Legacy?*              | 확인 필요             |
|               |         | 뷰어      | `/inventory/inbound/view` | *Legacy/Dev?*          | 확인 필요             |
| **Analytics** | -       | -         | `/analytics`              | 분석 대시보드          |                       |

---

## 3. 메뉴 구조도 (Menu Structure Diagram)

현재 구현된 페이지들의 계층 구조를 시각화합니다.

```mermaid
graph TD
    %% Nodes
    Home["🏠 Dashboard"]
    
    subgraph "재고 및 입고 (Inbound/Inventory)"
        Inv["📦 Inventory"]
        InvList["현황 조회"]
        Inbound["📥 Inbound"]
        InboundNew["입고 등록"]
        InboundList["명세서 목록"]
    end

    subgraph "기준 정보 (Master Data)"
        Beans["🫘 Beans"]
        BeansList["생두 목록"]
        BeansNew["신규 등록"]
        BeansDetail["상세 정보"]
    end

    subgraph "생산 (Production)"
        Roast["🔥 Roasting"]
        RoastList["프로파일 목록"]
        RoastSingle["싱글 로스팅"]
        RoastBlend["블렌드 로스팅"]
        
        Blends["⚖️ Blends"]
        BlendsList["레시피 목록"]
        BlendsNew["레시피 등록"]
        BlendsDetail["상세 레시피"]
    end
    
    Analytics["📊 Analytics"]

    %% Edges
    Home --> Inv
    Home --> Beans
    Home --> Roast
    Home --> Blends
    Home --> Analytics

    Inv --> InvList
    Inv --> Inbound
    Inbound --> InboundNew
    Inbound --> InboundList

    Beans --> BeansList
    BeansList --> BeansNew
    BeansList --> BeansDetail

    Roast --> RoastList
    RoastList --> RoastSingle
    RoastList --> RoastBlend

    Blends --> BlendsList
    BlendsList --> BlendsNew
    BlendsList --> BlendsDetail
```

---

## 4. 사용자 워크플로우 (User Flowchart)

실제 사용자가 데이터를 입력하고 가공하여 분석에 이르는 흐름입니다.

```mermaid
graph LR
    %% Styles
    classDef input fill:#e1f5fe,stroke:#01579b,color:black
    classDef process fill:#fff3e0,stroke:#e65100,color:black
    classDef output fill:#e8f5e9,stroke:#1b5e20,color:black

    %% Nodes
    subgraph "1. 입고 단계"
        A["Inbound Register<br/>(명세서 스캔/등록)"]:::input
        B["Inventory<br/>(생두 재고 증가)"]:::process
    end

    subgraph "2. 기준 정보"
        C["Bean Registration<br/>(생두 프로필 등록)"]:::input
    end

    subgraph "3. 가공 단계"
        D{"Roasting Type"}
        E["Single Origin Roast"]:::process
        F["Blend Roast"]:::process
        G["Blend Recipe"]:::input
    end

    subgraph "4. 결과 및 분석"
        H["Roasted Bean Stock"]:::output
        I["Analytics<br/>(생산량/재고/손익)"]:::output
    end

    %% Connections
    A --> B
    B --> D
    D -- Single --> E
    D -- Blend --> F
    C -.-> E
    C -.-> F
    G -.-> F
    E --> H
    F --> H
    H --> I
```

---

## 5. 최적화 제안 (Recommendations)

### 🚨 구조적 개선사항

1.  **Inbound 경로 통일**:
    *   현재 `/inventory/inbound` (등록)와 `/inventory/inbound/list` (목록)이 잘 정리되어 있으나, `/inbound/invoice` 등 레거시로 보이는 경로가 발견됨.
    *   **Action**: 모든 입고 관련 기능은 `/inventory/inbound/*` 하위로 엄격하게 통합 권장.

2.  **Roasting 하위 메뉴 접근성**:
    *   로스팅은 'Single'과 'Blend'의 행위가 구분되어 있음. 메뉴에서 바로 접근 가능하도록 서브 메뉴(Submenu) UI 도입 고려.

3.  **메뉴 순서 재배치 (최종안)**:
    *   **Home**
    *   **Inventory** (재고/입고) - *재료가 있어야 생산이 가능하므로 상단 이동*
    *   **Beans** (생두 관리)
    *   **Roasting** (로스팅)
    *   **Blends** (블렌딩)
    *   **Analytics** (분석)

### 📐 최적화된 메뉴 구조도 (Proposed Diagram)

```mermaid
graph TD
    classDef main fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef sub fill:#fff3e0,stroke:#ef6c00,stroke-width:1px;

    %% Top Level
    Home["🏠 1. Dashboard<br/>(Home)"]:::main
    Inv["📦 2. Inventory<br/>(Inbound + Stock)"]:::main
    Beans["🫘 3. Beans<br/>(Master Data)"]:::main
    Roast["🔥 4. Roasting<br/>(Production)"]:::main
    Blends["⚖️ 5. Blends<br/>(Recipe)"]:::main
    Analytics["📊 6. Analytics<br/>(Report)"]:::main

    %% Connections
    Home --> Inv
    Inv --> Beans
    Beans --> Roast
    Roast --> Blends
    Blends --> Analytics

    %% Sub Items (Optimization Highlight)
    subgraph "통합된 재고 관리"
        Inv --> InvList["Current Stock"]:::sub
        Inv --> InvInbound["Inbound Management<br/>(List & New)"]:::sub
    end

    subgraph "명확한 생산 관리"
        Roast --> RoastSingle["Single Roast"]:::sub
        Roast --> RoastBlend["Blend Roast"]:::sub
    end
```
