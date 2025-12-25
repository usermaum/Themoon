# 재사용 컴포넌트 사용 가이드

완성된 컴포넌트 라이브러리를 사용하여 페이지를 구현하는 방법에 대한 가이드입니다.

## 📦 컴포넌트 구조

```
app/components/
├── __init__.py           # 모든 컴포넌트 export
├── layout.py             # 레이아웃 컴포넌트 (SessionManager, PageTemplate 등)
├── ui.py                 # UI 컴포넌트 (헤더, 메트릭, 테이블 등)
├── forms.py              # 폼 컴포넌트 (입력 필드, CRUDForm 등)
├── helpers.py            # 유틸리티 함수 (포맷팅, 검증 등)
└── test_components.py    # 컴포넌트 테스트
```

## 🚀 빠른 시작

### 1. 레이아웃 컴포넌트 사용

#### SessionManager - 서비스 초기화

```python
from app.components import SessionManager

# 필요한 서비스 초기화
services = SessionManager.init_services([
    "db",
    "bean_service",
    "blend_service"
])

db = services["db"]
bean_service = services["bean_service"]
```

#### PageTemplate - 페이지 구조

```python
from app.components import PageTemplate

def render_content():
    st.write("페이지 내용")

PageTemplate(
    title="원두 관리",
    subtitle="모든 원두의 가격을 관리합니다",
    show_refresh=True,
    refresh_callback=lambda: print("Refreshing..."),
    content_func=render_content
)
```

#### TabbedLayout - 탭 기반 네비게이션

```python
from app.components import TabbedLayout

tabs = {
    "목록": lambda: st.write("List content"),
    "추가": lambda: st.write("Add content"),
    "편집": lambda: st.write("Edit content"),
}

icons = {
    "목록": "📋",
    "추가": "➕",
    "편집": "✏️",
}

TabbedLayout(tabs, icons)
```

#### ColumnLayout - 다중 열 레이아웃

```python
from app.components import ColumnLayout

content = [
    lambda: st.metric("메트릭 1", 100),
    lambda: st.metric("메트릭 2", 200),
    lambda: st.metric("메트릭 3", 300),
]

ColumnLayout(columns=3, content_funcs=content)
```

### 2. UI 컴포넌트 사용

#### PageHeader - 페이지 헤더

```python
from app.components import PageHeader

PageHeader(
    title="대시보드",
    subtitle="시스템 개요",
    show_refresh=True,
    refresh_callback=lambda: st.rerun()
)
```

#### MetricsGrid - 메트릭 그리드

```python
from app.components import MetricsGrid

metrics = [
    {"label": "총 로스팅", "value": 25, "icon": "☕", "delta": "↑ 5"},
    {"label": "평균 비용", "value": "2,500원", "icon": "💰"},
    {"label": "효율성", "value": "83.3%", "icon": "📈"},
    {"label": "수익성", "value": "15%", "icon": "💹"},
    {"label": "고객 만족도", "value": "4.5/5", "icon": "⭐"},
]

MetricsGrid(metrics, columns=5)
```

#### DataTable - 데이터 테이블

```python
from app.components import DataTable
import pandas as pd

df = pd.DataFrame({
    "원두명": ["에티오피아", "케냐", "콜롬비아"],
    "가격": [15000, 18000, 12000],
    "재고": [10, 20, 15]
})

filtered_df, selected_indices = DataTable(
    data=df,
    columns=["원두명", "가격", "재고"],
    searchable=True,
    height=400,
    key="bean_table"
)
```

#### StatCard - 통계 카드

```python
from app.components import StatCard

StatCard(
    title="총 판매량",
    value="1,234 kg",
    description="지난 달 기준",
    icon="📦",
    color="#1F4E78"
)
```

#### StatsChart - 차트 표시

```python
from app.components import StatsChart
import plotly.graph_objects as go

# 플롯리 피겨 생성
fig = go.Figure(data=[
    go.Bar(x=['A', 'B', 'C'], y=[10, 20, 30])
])

StatsChart(title="판매량 추이", figure=fig, height=400)
```

### 3. 폼 컴포넌트 사용

#### FormField - 폼 필드 정의

```python
from app.components import FormField

# 텍스트 입력 필드
name_field = FormField(
    name="bean_name",
    label="원두명",
    type="text",
    required=True,
    placeholder="예: 에티오피아 예가체프"
)

# 숫자 입력 필드
price_field = FormField(
    name="price",
    label="가격",
    type="number",
    required=True,
    min_value=0,
    max_value=100000
)

# 선택 드롭다운
category_field = FormField(
    name="category",
    label="분류",
    type="select",
    options=["에티오피아", "케냐", "콜롬비아"],
    default="에티오피아"
)

# 다중 선택
tags_field = FormField(
    name="tags",
    label="태그",
    type="multiselect",
    options=["산미", "단맛", "과일향", "초콜릿향"]
)
```

#### FormGroup - 폼 그룹

```python
from app.components import FormGroup, FormField

fields = [
    FormField("name", "원두명", type="text"),
    FormField("price", "가격", type="number"),
    FormField("category", "분류", type="select", options=["A", "B"]),
    FormField("notes", "설명", type="textarea"),
]

values = FormGroup(fields, columns=2)
# returns: {"name": "값", "price": 1000, "category": "A", "notes": "..."}
```

#### CRUDForm - CRUD 폼

```python
from app.components import CRUDForm, FormField

def on_submit(data):
    """폼 제출 콜백"""
    db_service.add_bean(data)
    st.success("추가되었습니다!")

fields = [
    FormField("bean_name", "원두명", type="text"),
    FormField("price_per_kg", "가격/kg", type="number"),
    FormField("category", "분류", type="select", options=["Ethiopia", "Kenya"]),
]

CRUDForm(
    title="새 원두 추가",
    fields=fields,
    on_submit=on_submit,
    edit_mode=False,
    columns=2
)
```

#### SearchBox - 검색 상자

```python
from app.components import SearchBox

query = SearchBox(placeholder="원두 이름으로 검색...")
if query:
    filtered_results = search_beans(query)
    st.write(filtered_results)
```

### 4. 헬퍼 함수 사용

#### 포맷팅 함수

```python
from app.components import (
    format_number,
    format_currency,
    format_percentage,
    format_date
)

# 숫자 포맷팅
format_number(1234567.89, 2)  # "1,234,567.89"

# 통화 포맷팅
format_currency(100000)  # "₩100,000"

# 퍼센트 포맷팅
format_percentage(75.5)  # "75.5%"

# 날짜 포맷팅
from datetime import date
format_date(date(2025, 10, 27))  # "2025-10-27"
```

#### 검증 함수

```python
from app.components import validate_email, validate_phone

validate_email("user@example.com")  # True
validate_phone("010-1234-5678")     # True
```

#### 데이터 처리 함수

```python
from app.components import (
    truncate_text,
    calculate_change,
    filter_dataframe,
    sort_dataframe,
    batch_list
)

# 텍스트 자르기
truncate_text("Very long text...", max_length=20)

# 변화 계산
change, direction = calculate_change(120, 100)  # (20.0, 'up')

# 데이터프레임 필터링
filtered = filter_dataframe(df, {"status": "active"})

# 데이터프레임 정렬
sorted_df = sort_dataframe(df, "price", ascending=False)

# 리스트 배치 처리
batches = batch_list([1,2,3,4,5], 2)  # [[1,2], [3,4], [5]]
```

## 📋 실제 예제

### 완전한 원두 관리 페이지 예제

```python
import streamlit as st
from app.components import (
    SessionManager,
    PageHeader,
    TabbedLayout,
    DataTable,
    CRUDForm,
    FormField,
    format_currency,
)

# 서비스 초기화
services = SessionManager.init_services([
    "db",
    "bean_service"
])

bean_service = services["bean_service"]

# 페이지 헤더
PageHeader(
    title="☕ 원두 관리",
    subtitle="모든 원두의 가격을 관리합니다"
)

# 탭 레이아웃
def render_list():
    """목록 탭"""
    beans = bean_service.get_all_beans()
    df = pd.DataFrame(beans)

    filtered_df, _ = DataTable(
        data=df,
        searchable=True,
        height=500
    )

    st.write(f"총 {len(filtered_df)}개의 원두")

def render_add():
    """추가 탭"""
    def on_submit(data):
        bean_service.add_bean(data)
        st.success("원두가 추가되었습니다!")

    fields = [
        FormField("bean_name", "원두명", type="text"),
        FormField("price_per_kg", "가격/kg", type="number", min_value=0),
        FormField("category", "분류", type="select",
                 options=["Ethiopia", "Kenya", "Colombia"]),
        FormField("description", "설명", type="textarea"),
    ]

    CRUDForm("새 원두 추가", fields, on_submit)

def render_stats():
    """통계 탭"""
    stats = bean_service.get_statistics()

    metrics = [
        {"label": "총 원두 종류", "value": stats["total"], "icon": "☕"},
        {"label": "평균 가격", "value": format_currency(stats["avg_price"]), "icon": "💰"},
        {"label": "최고 가격", "value": format_currency(stats["max_price"]), "icon": "📈"},
        {"label": "최저 가격", "value": format_currency(stats["min_price"]), "icon": "📉"},
    ]

    MetricsGrid(metrics, columns=4)

tabs = {
    "목록": render_list,
    "추가": render_add,
    "통계": render_stats,
}

icons = {
    "목록": "📋",
    "추가": "➕",
    "통계": "📊",
}

TabbedLayout(tabs, icons)
```

## 🎨 컴포넌트 커스터마이징

### 색상 커스터마이징

대부분의 컴포넌트는 색상을 커스터마이징할 수 있습니다:

```python
StatCard(
    title="매출",
    value="1,000,000원",
    color="#FF6B6B"  # 빨간색
)

MetricsCard(
    label="성장률",
    value="25%",
    icon="📈"
)
```

### 고급 커스터마이징

필요한 경우 직접 Streamlit 함수를 사용할 수 있습니다:

```python
# 컴포넌트로 부족할 경우 Streamlit 함수 직접 사용
st.metric("사용자정의 메트릭", value=123)
st.dataframe(df)  # 더 세밀한 제어가 필요할 때
```

## ✅ 모범 사례

### 1. SessionManager 사용

모든 페이지는 서비스를 초기화할 때 SessionManager를 사용하세요:

```python
# ✅ 좋음
services = SessionManager.init_services(["db", "bean_service"])

# ❌ 피해야 할 방법
# 수동으로 session_state 관리하기
```

### 2. FormField로 폼 정의

폼을 만들 때는 FormField로 정의하세요:

```python
# ✅ 좋음
fields = [
    FormField("name", "이름", type="text"),
    FormField("price", "가격", type="number"),
]
values = FormGroup(fields)

# ❌ 피해야 할 방법
# 개별 st.text_input, st.number_input 사용
```

### 3. 데이터 포맷팅

헬퍼 함수로 포맷팅하세요:

```python
# ✅ 좋음
st.write(format_currency(100000))

# ❌ 피해야 할 방법
st.write(f"₩{100000:,}")
```

### 4. 에러 처리

폼에서 검증 에러는 자동으로 처리됩니다:

```python
# FormField의 validation 파라미터 사용
field = FormField(
    "email",
    "이메일",
    type="text",
    validation=lambda x: validate_email(x) or raise ValueError("Invalid email")
)
```

## 🔧 공통 문제 해결

### 1. 컴포넌트가 import되지 않음

```python
# ❌ 틀림
from app.components.ui import page_header

# ✅ 맞음
from app.components import PageHeader
# 또는
from app.components import page_header
```

### 2. SessionManager 에러

```python
# 반드시 필요한 서비스먼저 초기화
services = SessionManager.init_services(["db"])
# 그 후에 다른 서비스 추가 가능
```

### 3. 폼 제출이 작동하지 않음

```python
# on_submit 콜백이 반드시 필요함
def on_submit(data):
    # 데이터 처리
    pass

CRUDForm("제목", fields, on_submit)  # on_submit 필수
```

## 📚 추가 리소스

- [COMPONENT_DESIGN.md](./COMPONENT_DESIGN.md) - 아키텍처 상세 설계
- [app/components/](./app/components/) - 컴포넌트 소스코드
- Streamlit 공식 문서: https://docs.streamlit.io/

## 🚀 다음 단계

1. **기존 페이지 리팩토링**: 현재 페이지들을 컴포넌트로 재구성
2. **성능 최적화**: 개별 컴포넌트 성능 측정 및 최적화
3. **추가 컴포넌트**: 필요한 새로운 컴포넌트 구현
4. **테마 시스템**: 통일된 색상/스타일 시스템 구축

---

**마지막 업데이트**: 2025-10-27
