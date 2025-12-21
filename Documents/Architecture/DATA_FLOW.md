# 🔄 TheMoon 데이터 흐름도 (Data Flow Diagram)

> **작성일**: 2025-12-07
> **버전**: 0.0.6
> **작성자**: AI Assistant

---

## 📋 목차

1. [개요](#개요)
2. [전체 데이터 흐름](#전체-데이터-흐름)
3. [기능별 데이터 흐름](#기능별-데이터-흐름)
4. [데이터 변환 규칙](#데이터-변환-규칙)
5. [에러 처리 흐름](#에러-처리-흐름)

---

## 개요

TheMoon 시스템의 데이터는 **프론트엔드 → 백엔드 → 데이터베이스** 3계층을 거치며,
각 계층에서 검증, 변환, 영속화 과정을 거칩니다.

### 데이터 흐름 원칙

1. **단방향 흐름**: 사용자 액션 → 상태 업데이트 → UI 재렌더링
2. **서버 신뢰**: 프론트엔드는 백엔드 응답을 신뢰하고 그대로 표시
3. **낙관적 업데이트**: SWR의 Optimistic Update 활용
4. **에러 전파**: 각 계층에서 발생한 에러는 상위 계층으로 전파

---

## 전체 데이터 흐름

### 읽기 (Read) 흐름

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant FE as Frontend (Next.js)
    participant API as Backend (FastAPI)
    participant SVC as Service Layer
    participant DB as Database (PostgreSQL)

    User->>FE: 페이지 접속 / 데이터 요청
    FE->>FE: useBeans() (SWR Cache Check)
    alt Cache Miss
        FE->>API: GET /api/v1/beans
        API->>SVC: BeanService.get_beans()
        SVC->>DB: SQL Query (SELECT)
        DB-->>SVC: Result Rows
        SVC-->>API: Pydantic Service Objects
        API-->>FE: JSON Response
    else Cache Hit
        FE-->>FE: Return cached data
    end
    FE->>User: UI 업데이트
```


### 쓰기 (Write) 흐름

```mermaid
sequenceDiagram
    autonumber
    actor User as 사용자
    participant FE as Frontend (Next.js)
    participant API as Backend (FastAPI)
    participant SVC as Service Layer
    participant DB as Database (PostgreSQL)

    User->>FE: 폼 제출 (Action)
    FE->>FE: Validate Input (Client-side)
    FE->>API: POST /api/v1/beans (JSON Body)
    API->>API: Validate Schema (Pydantic)
    API->>SVC: BeanService.create_bean()
    SVC->>SVC: Business Logic (SKU Gen, etc.)
    SVC->>DB: BEGIN Transaction
    DB->>DB: INSERT INTO beans
    DB->>DB: INSERT INTO inventory_logs
    DB-->>SVC: COMMIT
    SVC-->>API: Created Object
    API-->>FE: Response (201 Created)
    FE->>FE: SWR Mutate (Cache Invalidation)
    FE->>User: UI Update (Toast/Redirect)
```


---

## 기능별 데이터 흐름

### 1. 생두 등록 (Bean Registration)

```mermaid
flowchart TD
    User[사용자] -->|1. 폼 입력| FE[BeanForm 컴포넌트]
    FE -->|2. 클라이언트 검증| Func[createBean 함수]
    Func -->|3. POST /api/v1/beans| API[FastAPI Endpoint]
    API -->|4. Pydantic 검증| SVC[BeanService]
    SVC -->|5. 비즈니스 로직| Logic{로직 처리}
    Logic -->|Bean 객체 생성| DB1[INSERT beans]
    Logic -->|InventoryLog 생성| DB2[INSERT inventory_logs]
    DB1 & DB2 -->|8. 데이터 저장| DB[(PostgreSQL)]
    DB -->|9. 생성된 Bean 반환| Response[Response]
    Response -->|10. Cache 무효화| SWR[SWR]
    SWR -->|11. 목록 자동 갱신| UI[UI]
```


### 2. Single Origin 로스팅 (Roasting)

```mermaid
sequenceDiagram
    actor User as 사용자
    participant API as Roasting API
    participant SVC as RoastingService
    participant DB as Database

    User->>API: 1. 로스팅 폼 제출
    Note right of User: green_bean_id: 1<br/>input: 20kg, output: 17kg<br/>profile: MEDIUM
    
    API->>SVC: 2. 로스팅 요청
    SVC->>SVC: 3. 손실률 & 원가 계산
    Note right of SVC: loss = 15%<br/>price = 14,118원/kg
    
    SVC->>DB: 4. 트랜잭션 시작
    DB->>DB: 5a. 생두 재고 감소 (-20kg)
    DB->>DB: 5b. 원두 생성 (17kg)
    DB->>DB: 5c. 원두 재고 증가 (+17kg)
    DB-->>SVC: 6. 커밋
    
    SVC-->>API: 결과 반환
    API-->>User: 7. Response
    Note right of API: success: true<br/>cost: 14,118
```


### 3. 블렌드 레시피 생성 (Blend Creation)

```mermaid
sequenceDiagram
    actor User as 사용자
    participant API as Blend API
    participant SVC as BlendService
    participant DB as Database

    User->>API: 1. 블렌드 폼 제출
    Note right of User: Full Moon<br/>Beans: A(40), B(40), C(10), D(10)
    
    API->>SVC: 2. 검증 요청
    SVC->>SVC: 비율 합계(1.0) 및 ID 검증
    
    SVC->>DB: 3. Blend 생성 (INSERT)
    DB-->>SVC: ID 반환
    
    SVC-->>API: 생성된 블렌드 객체
    API-->>User: 5. Response
```


### 4. 블렌드 로스팅 (Blend Roasting)

```mermaid
sequenceDiagram
    actor User as 사용자
    participant API as Roasting API
    participant SVC as RoastingService
    participant DB as Database

    User->>API: 1. 블렌드 로스팅 요청
    Note right of User: blend_id: 1<br/>output: 10kg
    
    API->>SVC: 2. 레시피 조회 요청
    SVC->>SVC: 3. 필요량 계산
    Note right of SVC: A: 4kg, B: 4kg<br/>C: 1kg, D: 1kg
    
    SVC->>DB: 4. 트랜잭션 시작
    DB->>DB: 5a. 각 원두 재고 차감 (로그 4개)
    DB->>DB: 5b. 블렌드 원두 생성
    DB->>DB: 5c. 블렌드 재고 증가 (+10kg)
    DB-->>SVC: 6. 커밋
    
    SVC->>SVC: 가중 평균 원가 계산
    
    SVC-->>API: 결과 반환
    API-->>User: 8. Response
```


### 5. 재고 조회 및 검색 (Inventory Search)

```mermaid
sequenceDiagram
    actor User as 사용자
    participant FE as Frontend
    participant API as API
    participant DB as Check Database

    User->>FE: 1. 검색어 입력 ("예가")
    FE->>FE: 2. Debounce (300ms)
    FE->>API: 3. GET /beans?search=예가
    API->>DB: 4. LIKE Query
    Note right of DB: SELECT ... LIKE '%예가%'
    DB-->>API: 5. Result
    API-->>FE: 6. Response JSON
    FE-->>User: 결과 목록 표시
```


---

## 데이터 변환 규칙

### Frontend → Backend

| Frontend (TypeScript) | HTTP Body (JSON)                       | Backend (Python)        |
| --------------------- | -------------------------------------- | ----------------------- |
| `name: string`        | `"name": "예가체프"`                   | `name: str`             |
| `type: BeanType`      | `"type": "GREEN_BEAN"`                 | `type: BeanType (Enum)` |
| `quantity_kg: number` | `"quantity_kg": 20`                    | `quantity_kg: float`    |
| `avg_price: number`   | `"avg_price": 12000`                   | `avg_price: float`      |
| `created_at: string`  | `"created_at": "2025-12-07T12:00:00Z"` | `created_at: datetime`  |

### Backend → Database

| Python (SQLAlchemy)    | PostgreSQL (Column Type)   | 예시 값                          |
| ---------------------- | -------------------------- | -------------------------------- |
| `id: int`              | `INTEGER PRIMARY KEY`      | `1`                              |
| `name: str`            | `VARCHAR(255)`             | `"예가체프"`                     |
| `type: BeanType`       | `VARCHAR(20)`              | `"GREEN_BEAN"`                   |
| `quantity_kg: float`   | `NUMERIC(10, 3)`           | `20.000`                         |
| `avg_price: float`     | `NUMERIC(10, 2)`           | `12000.00`                       |
| `created_at: datetime` | `TIMESTAMP WITH TIME ZONE` | `2025-12-07 12:00:00+00`         |
| `recipe: List[dict]`   | `JSONB`                    | `[{"bean_id": 1, "ratio": 0.4}]` |

### Database → Frontend

```python
# 1. PostgreSQL Row
Row(id=1, name='예가체프', quantity_kg=Decimal('20.000'))

# 2. SQLAlchemy Model
bean = Bean(id=1, name='예가체프', quantity_kg=20.0)

# 3. Pydantic Schema
bean_response = BeanResponse(
    id=1,
    name='예가체프',
    quantity_kg=20.0,
    created_at=datetime(2025, 12, 7, 12, 0, 0)
)

# 4. JSON Response
{
  "id": 1,
  "name": "예가체프",
  "quantity_kg": 20.0,
  "created_at": "2025-12-07T12:00:00Z"
}

# 5. TypeScript Interface
interface Bean {
  id: number
  name: string
  quantity_kg: number
  created_at: string
}
```

---

## 에러 처리 흐름

### 검증 에러 (Validation Error)

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant API as Backend

    FE->>API: 1. 폼 제출 (quantity: -10)
    API-->>FE: 2. 422 Unprocessable Entity
    Note right of API: msg: ensure this value is greater than 0
    FE-->>FE: 3. UI 에러 메시지 표시
```


### 비즈니스 로직 에러

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant SVC as Service

    FE->>SVC: 1. 로스팅 요청 (100kg)
    SVC-->>FE: 2. 400 Bad Request
    Note right of SVC: 재고 부족 (현재: 20kg)
    FE-->>FE: 3. ErrorState 표시 (Retry 버튼)
```


### 네트워크 에러

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant NET as Network

    FE->>NET: 1. API 호출
    NET-->>FE: 2. Connection Failure
    loop Exponential Backoff
        FE->>FE: 3. Auto Retry (5s, 10s...)
    end
    FE-->>FE: 4. Retry Failed -> Error UI
```


---

---

## 🔗 관련 문서

**← 상위**: [Documents README](../README.md) | [프로젝트 루트](../../README.md)

**아키텍처 문서**:
- [시스템 개요](SYSTEM_OVERVIEW.md) - 전체 시스템 개요 및 핵심 기능
- [데이터베이스 스키마](DATABASE_SCHEMA.md) - 테이블 구조 및 관계도
- [API 명세](API_SPECIFICATION.md) ⭐ - 모든 API 엔드포인트 상세 문서
- [기술 스택](TECHNOLOGY_STACK.md) ⭐ - 사용 기술 상세 설명
- [배포 아키텍처](DEPLOYMENT_ARCHITECTURE.md) ⭐ - 배포 환경 상세 구조

**개발 가이드**:
- [개발 가이드](DEVELOPMENT_GUIDE.md) - 5단계 개발 프로세스
- [문제 해결](TROUBLESHOOTING.md) - 16가지 오류 & 해결법

---

**작성**: AI Assistant
**최종 업데이트**: 2025-12-08
**버전**: 0.0.6
