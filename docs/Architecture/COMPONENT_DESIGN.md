# 재사용 컴포넌트 아키텍처 설계 문서

## 📋 목차
1. [개요](#개요)
2. [분석 결과](#분석-결과)
3. [컴포넌트 분류](#컴포넌트-분류)
4. [상세 설계](#상세-설계)
5. [구현 계획](#구현-계획)
6. [사용 예제](#사용-예제)

---

## 개요

**목표**: 현재 페이지들의 중복된 코드를 제거하고 재사용 가능한 컴포넌트 체계 구축

**현황**:
- 9개의 페이지 파일 (각 15-24KB)
- 반복되는 코드 패턴 존재
- 일관성 유지의 어려움
- 유지보수 비용 증가

**기대효과**:
- 코드 중복 제거 (30-40% 감소 예상)
- 개발 속도 향상 (신규 페이지 개발 시간 50% 단축)
- 유지보수성 개선
- UI/UX 일관성 보장

---

## 분석 결과

### 🔍 발견된 반복 패턴

#### 1. 세션 상태 초기화 (모든 페이지)
```python
# 반복 코드
if "db" not in st.session_state:
    st.session_state.db = SessionLocal()
if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)
```

#### 2. 헤더 레이아웃 (모든 페이지)
```python
# 반복 구조
st.markdown("<h1 style='color: #1F4E78;'>아이콘 제목</h1>", unsafe_allow_html=True)
st.markdown("부제목 설명")
col1, col2 = st.columns([10, 1])
# 새로고침 버튼 등
```

#### 3. 메트릭 디스플레이 (대시보드)
```python
# 반복 구조
st.metric(label="라벨", value=값, delta="단위")
# 5개 이상의 메트릭 반복
```

#### 4. 탭 구성 (CRUD 페이지)
```python
# 반복 구조
tab1, tab2, tab3, tab4 = st.tabs(["📋 목록", "➕ 추가", "✏️ 편집", "📊 통계"])
```

#### 5. 테이블 & 필터 (목록 조회)
```python
# 반복 구조
필터링 옵션 (multiselect, text_input)
↓
데이터 로드
↓
필터링 적용
↓
테이블 표시 (st.dataframe)
```

#### 6. CRUD 폼 (추가/편집)
```python
# 반복 구조
form 생성
  ├─ text_input (여러 개)
  ├─ number_input / selectbox
  ├─ submit button
  └─ validation & 데이터베이스 작업
```

---

## 컴포넌트 분류

### 📊 3대 카테고리

```
Components/
├── 1. UI Components (화면 표시)
│   ├── PageHeader          # 페이지 제목 + 새로고침
│   ├── MetricsCard         # 메트릭 카드 (단일)
│   ├── MetricsGrid         # 메트릭 그리드 (여러 개)
│   ├── DataTable           # 데이터 테이블
│   ├── StatCard            # 통계 카드
│   └── StatsChart          # 통계 그래프
│
├── 2. Form Components (입력/작업)
│   ├── TextInput            # 텍스트 입력
│   ├── NumberInput          # 숫자 입력
│   ├── SelectInput          # 선택 (단일)
│   ├── MultiSelectInput     # 선택 (다중)
│   ├── FormGroup            # 폼 그룹 (여러 입력란)
│   ├── CRUDForm             # CRUD 폼 (추가/편집)
│   └── ConfirmDialog        # 확인 대화상자
│
└── 3. Layout Components (페이지 구조)
    ├── PageTemplate         # 기본 페이지 템플릿
    ├── TabbedLayout         # 탭 레이아웃
    ├── ColumnLayout         # 컬럼 레이아웃
    ├── SectionLayout        # 섹션 레이아웃
    └── SessionManager       # 세션 상태 관리
```

---

## 상세 설계

### 1️⃣ UI Components

#### PageHeader
**목적**: 모든 페이지의 헤더 표시

```python
def page_header(
    title: str,           # "📊 대시보드"
    subtitle: str,        # "핵심 지표 및 실시간 모니터링"
    show_refresh: bool = True
) -> None:
    """페이지 헤더 렌더링"""
```

**사용 위치**:
- Dashboard.py
- BeanManagement.py
- BlendManagement.py
- 모든 페이지

**반복 코드 제거**: 40줄 → 1줄

---

#### MetricsGrid
**목적**: 여러 메트릭을 그리드로 표시

```python
def metrics_grid(
    metrics: List[Dict[str, Any]],  # [{"label": "원두 종류", "value": 5, "delta": "종류"}, ...]
    columns: int = 5                 # 한 줄에 표시할 개수
) -> None:
    """메트릭 그리드 렌더링"""
```

**데이터 구조**:
```python
metrics = [
    {"label": "☕ 원두 종류", "value": 13, "delta": "종류"},
    {"label": "🎨 블렌드", "value": 8, "delta": "개"},
    {"label": "📦 총 재고", "value": 2500.5, "delta": "kg"},
    {"label": "💰 총 비용", "value": 15000000, "delta": "₩"},
    {"label": "📊 판매량", "value": 450, "delta": "kg"}
]
```

**사용 위치**:
- Dashboard.py (7줄 → 1줄)

---

#### DataTable
**목적**: 데이터프레임을 테이블로 표시 + 선택 기능

```python
def data_table(
    data: pd.DataFrame,
    columns: List[str] = None,      # 표시할 컬럼
    searchable: bool = True,         # 검색 기능
    selectable: bool = True,         # 선택 기능 (체크박스)
    height: int = 400,
    key: str = None
) -> Tuple[pd.DataFrame, List[int]]:
    """데이터 테이블 렌더링 + 선택된 행 반환"""
```

**사용 위치**:
- BeanManagement.py (Tab 1)
- BlendManagement.py (Tab 1)
- InventoryManagement.py

---

### 2️⃣ Form Components

#### CRUDForm
**목적**: 추가/편집 폼 일관성 있게 처리

```python
def crud_form(
    title: str,                     # "원두 추가" or "원두 편집"
    fields: List[FormField],        # 폼 필드 정의
    on_submit: Callable,            # 제출 시 실행할 함수
    initial_data: Dict = None,      # 편집 시 초기값
    edit_mode: bool = False
) -> None:
    """CRUD 폼 렌더링"""
```

**FormField 구조**:
```python
@dataclass
class FormField:
    name: str                       # 필드명 (DB 컬럼명)
    label: str                      # 라벨 ("원두명")
    type: str                       # "text", "number", "select", "multiselect"
    required: bool = True
    options: List[str] = None       # select/multiselect용
    placeholder: str = None
    validation: Callable = None     # 검증 함수
```

**사용 위치**:
- BeanManagement.py (Tab 2, 3)
- BlendManagement.py (Tab 2, 3)
- InventoryManagement.py (Tab 2, 3)

**반복 코드 제거**: 각 페이지 50-80줄 → 15-20줄

---

#### ConfirmDialog
**목적**: 삭제 등의 확인 대화상자

```python
def confirm_dialog(
    title: str,                     # "원두 삭제"
    message: str,                   # "정말 삭제하시겠습니까?"
    on_confirm: Callable,
    danger: bool = True             # 위험한 작업 여부
) -> bool:
    """확인 대화상자 표시"""
```

---

### 3️⃣ Layout Components

#### PageTemplate
**목적**: 표준 페이지 구조 제공

```python
def page_template(
    page_title: str,
    page_icon: str,
    render_content: Callable,       # 페이지 본문 렌더링 함수
    services: Dict = None           # 필요한 서비스 dict
) -> None:
    """표준 페이지 템플릿"""
    # 1. set_page_config 자동 처리
    # 2. 세션 상태 초기화
    # 3. 헤더 렌더링
    # 4. 본문 렌더링
    # 5. 푸터 (선택사항)
```

**사용 방법**:
```python
# 기존 (50줄)
st.set_page_config(...)
if "db" not in st.session_state:
    st.session_state.db = SessionLocal()
st.markdown("<h1>...</h1>", unsafe_allow_html=True)
# ... 페이지 본문 ...

# 신규 (10줄)
def render_page():
    # 페이지 본문만 작성
    pass

page_template(
    page_title="원두 관리",
    page_icon="☕",
    render_content=render_page,
    services={"bean_service": BeanService}
)
```

---

#### TabbedLayout
**목적**: 탭 레이아웃 표준화

```python
def tabbed_layout(
    tabs: List[Dict]                # [{"label": "📋 목록", "render": func}, ...]
) -> None:
    """탭 레이아웃 렌더링"""
```

**사용 방법**:
```python
tabs = [
    {"label": "📋 목록", "render": render_bean_list},
    {"label": "➕ 추가", "render": render_bean_add},
    {"label": "✏️ 편집", "render": render_bean_edit},
    {"label": "📊 통계", "render": render_bean_stats}
]

tabbed_layout(tabs)
```

---

#### SessionManager
**목적**: 세션 상태 일괄 관리

```python
class SessionManager:
    @staticmethod
    def init_services(required_services: List[str]) -> Dict:
        """필요한 서비스 자동 초기화"""
        # required_services: ["bean_service", "blend_service", ...]

    @staticmethod
    def get_service(service_name: str):
        """서비스 조회"""

    @staticmethod
    def clear_service(service_name: str):
        """서비스 삭제"""
```

**사용 방법**:
```python
# 기존 (10줄)
if "db" not in st.session_state:
    st.session_state.db = SessionLocal()
if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

# 신규 (1줄)
bean_service = SessionManager.init_services(["bean_service"])["bean_service"]
```

---

## 구현 계획

### 📅 Phase 1: 기초 컴포넌트 (1주)
```
Week 1:
├─ Day 1: SessionManager, PageTemplate
├─ Day 2: PageHeader, MetricsGrid, DataTable
├─ Day 3: TextInput, SelectInput, FormField
├─ Day 4: CRUDForm, ConfirmDialog
└─ Day 5: TabbedLayout, ColumnLayout
```

### 📅 Phase 2: 리팩토링 (2주)
```
Week 2-3:
├─ Dashboard.py 리팩토링
├─ BeanManagement.py 리팩토링
├─ BlendManagement.py 리팩토링
├─ InventoryManagement.py 리팩토링
├─ Settings.py 리팩토링
└─ 나머지 페이지 리팩토링
```

### 📅 Phase 3: 문서화 및 최적화 (1주)
```
Week 4:
├─ 컴포넌트 API 문서화
├─ 사용 가이드 작성
├─ 테스트 및 버그 수정
└─ 성능 최적화
```

### 📊 목표 메트릭

| 항목 | 현황 | 목표 | 개선율 |
|------|------|------|--------|
| 페이지 평균 코드 라인 | 400줄 | 200줄 | 50% ↓ |
| 중복 코드 | ~40% | <5% | 35% ↓ |
| 신규 페이지 개발 시간 | 3시간 | 1.5시간 | 50% ↓ |
| 유지보수 난이도 | 높음 | 낮음 | - |

---

## 사용 예제

### 📌 예제 1: 기존 Dashboard.py

**Before (현황 - 400줄)**:
```python
import streamlit as st
from models import SessionLocal
from services.bean_service import BeanService

st.set_page_config(page_title="대시보드", page_icon="📊", layout="wide")

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()
if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

st.markdown("<h1 style='color: #1F4E78;'>📊 더문드립바 대시보드</h1>", unsafe_allow_html=True)
st.markdown("핵심 지표 및 실시간 모니터링")

col1, col2 = st.columns([10, 1])
with col2:
    if st.button("🔄"):
        st.rerun()

st.divider()
st.markdown("## 🎯 핵심 지표")

metrics = [...]
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="☕ 원두 종류", value=..., delta="종류")
# ... 4개 더 반복 ...
```

**After (신규 - 100줄)**:
```python
from components.layout import page_template
from components.ui import metrics_grid
from services.bean_service import BeanService

def render_dashboard(bean_service):
    # 메트릭 데이터 준비
    metrics = [
        {"label": "☕ 원두 종류", "value": 13, "delta": "종류"},
        {"label": "🎨 블렌드", "value": 8, "delta": "개"},
        # ...
    ]

    # 메트릭 표시
    metrics_grid(metrics)

    st.divider()
    st.markdown("## 📈 판매 추세")
    # ... 그래프 코드 ...

# 페이지 렌더링
page_template(
    page_title="대시보드",
    page_icon="📊",
    render_content=render_dashboard,
    services={"bean_service": BeanService}
)
```

**개선 효과**:
- 코드 라인: 400줄 → 100줄 (75% 감소)
- 가독성: 향상
- 유지보수: 간편

---

### 📌 예제 2: 기존 BeanManagement.py

**Before (현황 - 350줄)**:
```python
import streamlit as st
from models import SessionLocal
from services.bean_service import BeanService

st.set_page_config(...)

if "db" not in st.session_state:
    st.session_state.db = SessionLocal()
if "bean_service" not in st.session_state:
    st.session_state.bean_service = BeanService(st.session_state.db)

st.markdown("<h1>☕ 원두 관리</h1>", unsafe_allow_html=True)
st.markdown("13종 원두의 정보를 관리하고 CRUD 작업을 수행합니다.")

tab1, tab2, tab3, tab4 = st.tabs(["📋 목록", "➕ 추가", "✏️ 편집", "📊 통계"])

with tab1:
    st.markdown("### 📋 원두 목록")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_country = st.multiselect("국가 필터", ...)
    # ... 필터 로직 ...
    beans = bean_service.get_active_beans()
    st.dataframe(beans)

with tab2:
    st.markdown("### ➕ 원두 추가")
    with st.form("add_bean"):
        name = st.text_input("원두명")
        country = st.selectbox("생산국", ...)
        # ... 필드들 ...
        if st.form_submit_button("추가"):
            # ... 검증 및 저장 로직 ...

# ... tab3, tab4 반복 ...
```

**After (신규 - 80줄)**:
```python
from components.layout import page_template, tabbed_layout
from components.forms import crud_form, FormField
from components.ui import data_table
from services.bean_service import BeanService

def render_bean_list(bean_service):
    beans = bean_service.get_active_beans()
    selected_rows, data = data_table(
        beans,
        searchable=True,
        selectable=True
    )

def render_bean_add(bean_service):
    fields = [
        FormField(name="name", label="원두명", type="text", required=True),
        FormField(name="country", label="생산국", type="select",
                 options=["에티오피아", "케냐", "콜롬비아", ...]),
        FormField(name="roast_level", label="로스팅", type="select",
                 options=["W", "N", "Pb", "Rh", "SD", "SC"]),
    ]

    def on_submit(data):
        bean_service.create_bean(**data)
        st.success("원두가 추가되었습니다.")

    crud_form("원두 추가", fields, on_submit, edit_mode=False)

def render_content(bean_service):
    tabs = [
        {"label": "📋 목록", "render": lambda: render_bean_list(bean_service)},
        {"label": "➕ 추가", "render": lambda: render_bean_add(bean_service)},
        {"label": "✏️ 편집", "render": lambda: render_bean_edit(bean_service)},
        {"label": "📊 통계", "render": lambda: render_bean_stats(bean_service)},
    ]
    tabbed_layout(tabs)

page_template(
    page_title="원두 관리",
    page_icon="☕",
    render_content=render_content,
    services={"bean_service": BeanService}
)
```

**개선 효과**:
- 코드 라인: 350줄 → 80줄 (77% 감소)
- 로직 분리: 각 탭별 함수로 명확함
- 재사용성: FormField, data_table 다른 곳에서도 사용 가능

---

## 다음 단계

1. ✅ 이 설계 문서 검토 및 피드백
2. ⬜ Phase 1: 기초 컴포넌트 구현
3. ⬜ Phase 2: 기존 페이지 리팩토링
4. ⬜ Phase 3: 문서화 및 최적화
5. ⬜ 신규 페이지 추가 시 컴포넌트 활용

---

## 기술 스택

- **프레임워크**: Streamlit
- **UI 라이브러리**: Streamlit built-in
- **데이터 처리**: Pandas, NumPy
- **데이터베이스**: SQLAlchemy ORM
- **유형 검사**: Python type hints

---

**작성일**: 2025-10-27
**버전**: v1.0.0
**상태**: 설계 완료, 구현 대기
