# MAS (Multi-Agent System) 플로우 다이어그램

> **작성일**: 2025-12-27
> **목적**: MAS 협업 프로세스 시각화
> **도구**: Mermaid v8.8.0

---

## 1. 전체 시스템 개요

```mermaid
graph TB
    User["👤 사용자"]

    subgraph "MAS Team"
        A1["🧑‍💼 Agent 1<br/>Project Architect"]
        A2["🎨 Agent 2<br/>Frontend"]
        A3["⚙️ Agent 3<br/>Backend"]
        A4["🛠️ Agent 4<br/>Maintainer"]
    end

    subgraph "결과물"
        Doc["📚 문서"]
        FE["🖥️ Frontend"]
        BE["💾 Backend"]
        QA["✅ 품질 보증"]
    end

    User -->|요청| A1
    User -->|"@Agent2"| A2
    User -->|"@Agent3"| A3
    User -->|"@Agent4"| A4

    A1 --> Doc
    A2 --> FE
    A3 --> BE
    A4 --> QA

    A2 -.협업.-> A3
    A3 -.협업.-> A2
    A4 -.검증.-> A2
    A4 -.검증.-> A3
    A1 -.조율.-> A2
    A1 -.조율.-> A3
    A1 -.조율.-> A4
```

---

## 2. 역할 전환 프로세스

```mermaid
flowchart TD
    Start["🎯 사용자 요청"]

    Analyze{"키워드 분석"}

    Design["디자인, UI, 컴포넌트?"]
    API["API, DB, 스키마?"]
    Error["에러, 버그, 빌드?"]
    Doc["문서, 계획, 세션?"]

    A2["🎨 Agent 2<br/>Frontend"]
    A3["⚙️ Agent 3<br/>Backend"]
    A4["🛠️ Agent 4<br/>Maintainer"]
    A1["🧑‍💼 Agent 1<br/>Architect"]

    Execute["작업 수행"]

    Start --> Analyze
    Analyze --> Design
    Analyze --> API
    Analyze --> Error
    Analyze --> Doc

    Design -->|자동 전환| A2
    API -->|자동 전환| A3
    Error -->|자동 전환| A4
    Doc -->|자동 전환| A1

    A2 --> Execute
    A3 --> Execute
    A4 --> Execute
    A1 --> Execute
```

---

## 3. 협업 플로우 - 기능 추가

```mermaid
sequenceDiagram
    actor User as 👤 사용자
    participant A1 as 🧑‍💼 Agent 1
    participant A2 as 🎨 Agent 2
    participant A3 as ⚙️ Agent 3
    participant A4 as 🛠️ Agent 4

    User->>A1: "필터 기능 추가"

    Note over A1: 요구사항 분석
    A1->>A1: TodoWrite: 작업 분해

    A1->>A2: "@Agent2: 필터 UI 구현"
    activate A2
    A2->>A2: frontend-design 스킬
    A2-->>A2: 컴포넌트 생성

    A2->>A3: "@Agent3: API 필터 파라미터 추가"
    deactivate A2
    activate A3
    A3->>A3: Repository 수정
    A3->>A3: 타입 힌팅 추가
    A3-->>A2: "파라미터 추가 완료"
    deactivate A3

    activate A2
    A2->>A2: API 연동
    A2-->>A4: "구현 완료"
    deactivate A2

    activate A4
    A4->>A4: pr-review-toolkit
    A4->>A4: 코드 품질 검증
    A4->>A4: 보안 검사
    A4-->>A1: "✅ 승인"
    deactivate A4

    A1->>User: "기능 추가 완료"
```

---

## 4. 협업 플로우 - 버그 수정

```mermaid
flowchart TD
    User["👤 사용자<br/>에러 발생!"]

    A4Start["🛠️ Agent 4<br/>디버깅 시작"]

    LogCheck{"로그 확인"}
    FEError["Frontend 에러"]
    BEError["Backend 에러"]
    SysError["System 에러"]

    A2Fix["🎨 Agent 2<br/>Frontend 수정"]
    A3Fix["⚙️ Agent 3<br/>Backend 수정"]
    A4Fix["🛠️ Agent 4<br/>직접 수정"]

    Verify["🛠️ Agent 4<br/>재검증"]

    Done["✅ 버그 해결"]

    User -->|"@Agent4"| A4Start
    A4Start --> LogCheck

    LogCheck -->|"TypeError"| FEError
    LogCheck -->|"500 Error"| BEError
    LogCheck -->|"Build Error"| SysError

    FEError -->|"@Agent2"| A2Fix
    BEError -->|"@Agent3"| A3Fix
    SysError --> A4Fix

    A2Fix --> Verify
    A3Fix --> Verify
    A4Fix --> Verify

    Verify --> Done
```

---

## 5. 스킬 호출 플로우

```mermaid
stateDiagram-v2
    [*] --> SkillRequest: 사용자 요청

    SkillRequest --> ClaudeCode: Claude Code 환경?
    SkillRequest --> GeminiPro: Gemini 3 Pro 환경?

    ClaudeCode --> DirectExecution: 직접 실행
    DirectExecution --> SkillResult: /frontend-design

    GeminiPro --> Simulation: 시뮬레이션
    Simulation --> ToolCombination: 도구 조합
    ToolCombination --> SkillResult: read_file + write_file

    SkillResult --> Verification: Agent 4 검증
    Verification --> [*]: 완료
```

---

## 6. Clean Architecture 레이어별 담당

```mermaid
graph LR
    subgraph "Presentation Layer"
        UI["UI Components"]
        A2_1["🎨 Agent 2"]
    end

    subgraph "Application Layer"
        API["API Endpoints"]
        A3_1["⚙️ Agent 3"]
    end

    subgraph "Domain Layer"
        Service["Services"]
        Repo["Repositories"]
        A3_2["⚙️ Agent 3"]
    end

    subgraph "Infrastructure Layer"
        DB["Database"]
        A3_3["⚙️ Agent 3"]
    end

    subgraph "Cross-Cutting"
        Test["Testing"]
        Review["Code Review"]
        A4_1["🛠️ Agent 4"]
    end

    UI --> A2_1
    API --> A3_1
    Service --> A3_2
    Repo --> A3_2
    DB --> A3_3
    Test --> A4_1
    Review --> A4_1
```

---

## 7. 작업 우선순위 결정 플로우

```mermaid
flowchart TD
    Start["📋 새로운 작업"]

    Type{"작업 유형"}

    Bug["🔴 버그"]
    Feature["🟢 기능"]
    Refactor["🔵 리팩토링"]
    Docs["📚 문서"]

    Urgent{"긴급도"}

    HighBug["우선순위: 최고<br/>Agent 4 즉시"]
    MediumFeature["우선순위: 중<br/>Agent 2/3"]
    LowRefactor["우선순위: 하<br/>Agent 3"]
    DocsTask["우선순위: 중하<br/>Agent 1"]

    Start --> Type

    Type -->|"에러, 장애"| Bug
    Type -->|"신규 기능"| Feature
    Type -->|"코드 개선"| Refactor
    Type -->|"문서 작성"| Docs

    Bug --> Urgent
    Urgent -->|"프로덕션 영향"| HighBug
    Urgent -->|"개발 환경만"| MediumFeature

    Feature --> MediumFeature
    Refactor --> LowRefactor
    Docs --> DocsTask
```

---

## 8. Git 워크플로우와 MAS

```mermaid
gitGraph
    commit id: "feat: Init"

    branch agent2-frontend
    checkout agent2-frontend
    commit id: "Agent 2: UI Component"
    commit id: "Agent 2: Tailwind"

    checkout main
    branch agent3-backend
    checkout agent3-backend
    commit id: "Agent 3: Repository"
    commit id: "Agent 3: API Endpoint"

    checkout main
    merge agent2-frontend tag: "Frontend 완료"
    merge agent3-backend tag: "Backend 완료"

    commit id: "Agent 4: PR Review" type: HIGHLIGHT
    commit id: "Agent 1: Docs" type: NORMAL
```

---

## 9. 에러 에스컬레이션 플로우

```mermaid
flowchart TD
    Error["⚠️ 에러 발생"]

    Agent["작업 중인 에이전트"]

    CanFix{"자체 해결<br/>가능?"}

    SelfFix["자체 수정"]

    Escalate["🛠️ Agent 4<br/>에스컬레이션"]

    A4Analyze["Agent 4<br/>원인 분석"]

    CrossCutting{"Cross-Cutting<br/>이슈?"}

    A4DirectFix["Agent 4<br/>직접 수정"]

    Delegate["전문 에이전트<br/>위임"]

    Resolved["✅ 해결"]

    Error --> Agent
    Agent --> CanFix

    CanFix -->|"Yes"| SelfFix
    CanFix -->|"No"| Escalate

    SelfFix --> Resolved

    Escalate --> A4Analyze
    A4Analyze --> CrossCutting

    CrossCutting -->|"Yes"| A4DirectFix
    CrossCutting -->|"No"| Delegate

    A4DirectFix --> Resolved
    Delegate --> Resolved
```

---

## 10. 세션 관리 플로우

```mermaid
stateDiagram-v2
    [*] --> SessionStart: 세션 시작

    SessionStart --> LoadContext: AGENTS.md 읽기
    LoadContext --> AgentReady: Agent 1 활성화

    AgentReady --> Working: 작업 수행

    state Working {
        [*] --> Task
        Task --> Agent2: Frontend 작업
        Task --> Agent3: Backend 작업
        Task --> Agent4: 디버깅 작업
        Agent2 --> Collaboration
        Agent3 --> Collaboration
        Agent4 --> Done
        Collaboration --> Done
        Done --> [*]
    }

    Working --> SessionEnd: "세션 종료"

    SessionEnd --> SaveContext: Context Handover
    SaveContext --> UpdateDocs: 문서 업데이트
    UpdateDocs --> GitCommit: Git Commit
    GitCommit --> [*]: 완료
```

---

## 📊 다이어그램 범례

### 에이전트 표기
- 🧑‍💼 Agent 1: Project Architect (PM)
- 🎨 Agent 2: Frontend Specialist
- ⚙️ Agent 3: Backend Engineer
- 🛠️ Agent 4: System Maintainer

### 화살표 종류
- `-->` : 직접 작업 흐름
- `-.->` : 협업/통신
- `==>` : 강조된 흐름

### 노드 색상 (Mermaid 기본)
- 사각형: 프로세스
- 마름모: 의사결정
- 원: 시작/종료

---

**작성자**: Agent 1 (Project Architect)
**Mermaid 버전**: v8.8.0 호환
**최종 업데이트**: 2025-12-27
