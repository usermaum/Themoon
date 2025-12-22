# inbound/viewinbound/view시스템 아키텍처 & 데이터 흐름

> 프로젝트의 기술 스택, 시스템 구조, 데이터 흐름을 설명하는 문서입니다.

---

## 🏗️ 시스템 아키텍처 (Current Tech Stack)

### 3계층 아키텍처

```mermaid
graph TD
    subgraph Presentation ["Presentation Layer (Frontend)"]
        Next[Next.js (App Router)]
        React[React / TypeScript]
        UI[Shadcn UI / Tailwind CSS]
        PortFE[Port: 3500]
      
        Next --- React
        React --- UI
    end

    subgraph Application ["Application Layer (Backend)"]
        Fast[Python / FastAPI]
        Pydantic[Pydantic Models]
        SQLAlchemy[SQLAlchemy ORM]
        PortBE[Port: 8000]
      
        Fast --- Pydantic
        Fast --- SQLAlchemy
    end

    subgraph Data ["Data Layer (Database)"]
        SQLite[("SQLite (themoon.db)")]
        SSOT[Single Source of Truth]
    end

    Next -->|HTTP / JSON| Fast
    Fast -->|SQL| SQLite
```

---

## 🔄 데이터 흐름 (Data Flow)

### 1️⃣ OCR 데이터 처리 및 저장 프로세스 (Inbound)

```mermaid
sequenceDiagram
    participant User
    participant Frontend (Next.js)
    participant Backend (FastAPI)
    participant OCR_Service
    participant DB

    User->>Frontend: 거래명세서 이미지 업로드
    Frontend->>Backend: POST /api/v1/inbound/ocr
    Backend->>OCR_Service: 이미지 분석 요청 (Google Gemini)
    OCR_Service-->>Backend: 구조화된 JSON 데이터 반환
    Backend-->>Frontend: OCRData 반환 (SessionStorage 저장)
  
    User->>Frontend: 데이터 확인 및 확정
    Frontend->>Backend: POST /api/v1/inbound/confirm
    Backend->>DB: Transaction (Atomic)
    Note over DB: 1. inbound_documents 생성
    Note over DB: 2. inbound_document_details 생성
    Note over DB: 3. inbound_receivers 생성
    Note over DB: 4. inbound_items 생성
    Note over DB: 5. inventory_logs (입고) 생성
    Backend-->>Frontend: 저장 완료 응답
```

### 2️⃣ 원두 재고 관리 흐름

```
1. 입고 (Inbound): 
   - OCR 확정 시 `inbound_items` 테이블에 기록됨
   - 동시에 `inventory_logs`에 `INBOUND` 타입으로 수량 증가 기록

2. 출고 (Outbound / Roasting):
   - 로스팅 실행 시 `inventory_logs`에 `USED_FOR_ROASTING`으로 생두 감소
   - 동시에 `inventory_logs`에 `ROASTED_BATCH`로 원두(볶은콩) 증가
```

---

## 💾 데이터베이스 스키마 구조

### 핵심 테이블 그룹

1. **Master Data**

   - `beans`: 원두 마스터 (품종, 원산지 등)
   - `suppliers`: 공급자 정보
   - `blends`: 블렌딩 레시피
2. **Inbound & OCR Data** (OCR 데이터 100% 저장)

   - `inbound_documents`: 헤더 정보 (계약번호, 이미지 등)
   - `inbound_document_details`: 상세 정보 (세금, 결제조건 등 25개 필드)
   - `inbound_receivers`: 공급받는자 정보
   - `inbound_items`: 품목 리스트
3. **Inventory**

   - `inventory_logs`: 모든 수량 변화 기록

---

## 🚧 향후 확장 계획

1. **PostgreSQL 마이그레이션**: 배포 환경을 위한 DB 전환
2. **원가 분석 기능**: `inbound_items`의 단가 정보를 활용한 정밀 원가 계산
3. **통계 대시보드**: 공급자별, 품목별 매입 현황 시각화

---

**Last Updated**: 2025-12-21

> 시스템이 어떻게 동작하는지, 데이터가 어떻게 흐르는지 이해하기 위한 가이드입니다.

---

## 🏗️ 시스템 아키텍처

### 3계층 아키텍처

```mermaid
graph TD
    subgraph UI ["Presentation Layer (UI)"]
        Streamlit[Streamlit Pages]
        Comps[UI Components]
        Forms[Forms & Charts]
    end

    subgraph Logic ["Business Logic Layer (Services)"]
        BeanSvc[BeanService]
        BlendSvc[BlendService]
        AnalSvc[AnalyticsService]
        ReportSvc[ReportService]
        ExcelSvc[ExcelService]
    end

    subgraph Models ["Data Access Layer (Models/ORM)"]
        SQLA[SQLAlchemy Models]
        Entities[Bean, Blend, Inventory, etc.]
    end

    subgraph DB ["Database Layer"]
        SQLite[("SQLite roasting_data.db")]
    end

    UI --> Logic
    Logic --> Models
    Models --> DB
```

---

## 🔄 데이터 흐름

### 1️⃣ 사용자 입력부터 저장까지

```mermaid
flowchart TD
    User[1. 사용자가 UI에서 입력] --> Streamlit[2. Streamlit 페이지가 입력 받음]
    Streamlit --> Service[3. 서비스 메서드 호출]
    Service --> Model[4. 모델 생성/수정]
    Model --> ORM[5. SQLAlchemy가 SQL 생성]
    ORM --> DB[(6. SQLite 데이터베이스에 저장)]
    DB --> Success[7. 확인 메시지 표시]
```

**예시: 새 원두 추가**

```python
# pages/BeanManagement.py
with st.form("add_bean_form"):
    name = st.text_input("원두명")
    price = st.number_input("가격")

    if st.form_submit_button("추가"):
        # 1. 서비스 호출
        bean_service.add_bean(name, price)
        # 2. DB에 저장됨 (서비스 내부)
        st.success("추가되었습니다!")
```

```python
# services/bean_service.py
def add_bean(self, name, price):
    # 1. 모델 인스턴스 생성
    bean = Bean(name=name, price_per_kg=price)

    # 2. 세션에 추가
    self.db.add(bean)

    # 3. DB에 커밋 (저장)
    self.db.commit()

    return bean
```

```python
# models/bean.py
class Bean(Base):
    __tablename__ = "beans"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price_per_kg = Column(Float)
    # SQLite에 CREATE TABLE 명령 생성
```

---

### 2️⃣ 데이터 조회부터 화면 표시까지

```mermaid
flowchart TD
    User[1. 사용자가 페이지 방문] --> Page[2. 페이지가 서비스 메서드 호출]
    Page --> Service[3. 서비스가 데이터베이스 쿼리]
    Service --> ORM[4. SQLAlchemy가 SQL SELECT 실행]
    ORM --> Data[5. 데이터 반환]
    Data --> Render[6. 페이지가 Streamlit으로 렌더링]
    Render --> Browser[7. 브라우저에 표시]
```

**예시: 원두 목록 표시**

```python
# pages/BeanManagement.py
import streamlit as st
from app.services import bean_service

# 1. 서비스 호출
beans = bean_service.get_all_beans()

# 2. DataFrame으로 변환
df = pd.DataFrame([
    {"이름": b.name, "가격": b.price_per_kg}
    for b in beans
])

# 3. 화면에 표시
st.dataframe(df)
```

---

## 📊 주요 데이터 흐름

### 로스팅 비용 계산 흐름

```mermaid
flowchart TD
    Input[사용자 입력]
    Input --> Weight[원두 무게 kg]
    Input --> OutWeight[로스팅 후 무게 kg]
    Input --> Price[원두 가격 원/kg]
    Input --> Other[기타 비용]
  
    Input --> Calc[analytics_service.calculate_cost]
  
    Calc --> CostCalc[비용 계산]
    CostCalc --> BeanCost[원두 비용 = 무게 × 가격]
    CostCalc --> RoastCost[로스팅 비용 = 무게 × 로스팅비]
    CostCalc --> Labor[인건비 = 시간 × 시급]
    CostCalc --> Elec[전기료 = 고정값]
    CostCalc --> Total[총 비용 = 합계]
  
    Total --> UnitCost[kg당 비용 계산]
    UnitCost --> Margin[마진율 계산]
    Margin --> Display[화면에 표시]
```

---

### 블렌드 레시피 흐름

```mermaid
flowchart TD
    User[사용자가 블렌드 생성] --> Service[blend_service.create_blend]
    Service --> SaveName[1. 블렌드 이름 저장]
    Service --> SaveCombi[2. 원두 조합 저장]
    Service --> PriceCheck[3. 각 원두의 비용 조회]
  
    PriceCheck --> BeanSvc[bean_service.get_bean]
    BeanSvc --> CostCalc[총 원가 계산]
    CostCalc --> SellPrice[판매가 = 원가 × 마진율 2.5배]
    SellPrice --> DB[(데이터베이스 저장)]
```

---

### 재고 추적 흐름

```mermaid
flowchart TD
    Sell[블렌드 판매] --> Trans[1. transaction_service.record_transaction]
    Trans --> Record[2. 판매량 기록]
    Record --> InvSvc[3. inventory_service.update_inventory]
    InvSvc --> CalcUsed[4. 사용된 원두 계산]
  
    CalcUsed --> Decrease[각 원두의 재고 감소]
    Decrease --> Example[예: 블렌드가 에티오피아 200g 사용 -> 에티오피아 재고에서 200g 차감]
    Example --> Display[현재 재고량 표시]
```

---

## 🔗 서비스 간 관계도

```mermaid
graph TD
    subgraph Pages [페이지들]
        Dash[Dashboard.py]
        Bean[BeanMgmt.py]
        Blend[BlendMgmt.py]
        Etc[etc...]
    end

    subgraph Services [Services 비즈니스 로직]
        BeanSvc[BeanService]
        BlendSvc[BlendService]
        TranSvc[TransService]
        InvSvc[InventoryService]
        AnalSvc[AnalyticsService]
        RepSvc[ReportService]
        ExcelSvc[ExcelService]
    end

    subgraph Models [Models 데이터]
        Entities[Bean, Blend, Inventory<br/>Transaction, CostSetting]
    end
  
    subgraph DB [SQLite DB]
        SQLite[(roasting_data.db)]
    end

    Pages -->|호출| Services
  
    BeanSvc --> AnalSvc
    BlendSvc --> RepSvc
    TranSvc --> ExcelSvc
  
    Services -->|사용| Models
    Models -->|쿼리| DB
```

---

## 🔄 세션 상태 관리

Streamlit은 상태를 유지하기 위해 `st.session_state`를 사용합니다.

```python
# 데이터 캐싱 (페이지 재로드 시에도 유지)
if "beans" not in st.session_state:
    st.session_state.beans = bean_service.get_all_beans()

# 사용자 선택 저장
selected_bean = st.selectbox(
    "원두 선택",
    [b.name for b in st.session_state.beans]
)
```

---

## 📡 API 없이 직접 데이터 접근

주의: 이 프로젝트는 API 서버가 없습니다.
Streamlit이 직접 데이터베이스에 접근합니다.

```mermaid
graph TD
    UI[Streamlit UI]
    DB[("SQLite DB")]
    UI -->|직접 접근| DB
```

이 구조의 장점:

- ✅ 간단함 (서버 설정 불필요)
- ✅ 빠름 (네트워크 지연 없음)

단점:

- ❌ 확장성 낮음 (다중 사용자 동시 접근 어려움)
- ❌ 모바일 접근 불가능

---

## 🔐 데이터 일관성

### 트랜잭션 (Transaction)

모든 데이터 변경은 트랜잭션으로 관리됩니다:

```python
# 성공 케이스
self.db.add(bean)
self.db.commit()  # 데이터 저장

# 실패 케이스 (롤백)
try:
    self.db.add(bean)
    self.db.commit()
except Exception as e:
    self.db.rollback()  # 변경사항 취소
    raise e
```

---

## 📈 성능 최적화

### 쿼리 최적화

```python
# ❌ 느린 방법 (N+1 쿼리)
blends = self.db.query(Blend).all()
for blend in blends:
    bean = self.db.query(Bean).filter(
        Bean.id == blend.bean_id
    ).first()  # 매번 쿼리

# ✅ 빠른 방법 (조인)
blends = self.db.query(Blend).join(Bean).all()
```

### 데이터 캐싱

```python
# 반복되는 데이터는 변수에 저장
beans = bean_service.get_all_beans()

# 여러 번 사용
for use_case in use_cases:
    process(beans)
```

---

## 🔍 디버깅 흐름

오류 발생 시 추적 순서:

```mermaid
flowchart TD
    Err[오류 발생] --> UI[1. Streamlit UI 브라우저 콘솔]
    UI -->|오류 메시지 확인| Page[2. Pages Python 파일]
    Page -->|서비스 호출 부분 확인| Svc[3. Services 비즈니스 로직]
    Svc -->|데이터 처리 로직 확인| Model[4. Models ORM]
    Model -->|데이터 유형 확인| DB[5. Database SQLite]
    DB -->|데이터 존재 여부 확인| End[원인 파악]
```

**디버깅 명령어:**

```bash
# 에러 로그 확인
./venv/bin/streamlit run app/app.py 2>&1 | grep -i error

# 데이터베이스 확인
sqlite3 data/roasting_data.db ".tables"
sqlite3 data/roasting_data.db "SELECT * FROM beans LIMIT 5;"
```

---

## 🔗 확장 포인트

### 1. API 서버 추가 (향후)

```
추가될 예정:
FastAPI 서버 추가
  └─ 모바일 앱 지원
  └─ 다중 사용자 지원
```

### 2. 실시간 동기화 (향후)

```
WebSocket 추가
  └─ 여러 사용자 실시간 협업
```

### 3. 클라우드 마이그레이션 (향후)

```
PostgreSQL 또는 MySQL로 변경
  └─ 클라우드 배포
  └─ 자동 백업
```

---

**마지막 업데이트: 2025-10-27**
