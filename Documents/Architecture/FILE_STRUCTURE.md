# 프로젝트 파일 구조 & 책임

> 프로젝트의 모든 파일의 위치, 책임, 그리고 상호 관계를 설명합니다.

---

## 📊 전체 구조 한눈에 보기

```
TheMoon_Project/                          # 프로젝트 루트
│
├── venv/                                 # 프로젝트 격리 Python 환경 (3.12.3)
│   └── bin/python, streamlit, pip (필수 사용)
│
├── run.py                                # 메인 런처 (엔트리포인트)
├── requirements.txt                      # 의존성 (5개 패키지)
├── README.md                             # 사용자 가이드
└── .claude/CLAUDE.md                     # 개발 규칙 (필독)

```

---

## 🎯 Core Application (app/)

### 📍 app/app.py (450줄) - **핵심 진입점**
**책임:**
- Streamlit 앱 설정 및 초기화
- 메인 대시보드 레이아웃
- 사이드바 네비게이션
- 세션 상태 관리

**관계:**
- pages/ 모든 페이지로부터 참조됨
- models/database.py로부터 DB 연결
- services/ 모든 서비스 로드

**주요 함수:**
```python
init_database()        # DB 테이블 초기화
init_session_state()   # 세션 상태 초기화
render_sidebar()       # 사이드바 렌더링
```

---

### 📄 app/pages/ (9개 페이지, 4,500줄)

모든 사용자 인터페이스 페이지들입니다. 각 페이지는 독립적이며 특정 기능에 집중합니다.

| 파일 | 줄수 | 책임 | 사용 서비스 |
|------|------|------|----------|
| **Dashboard.py** | 440 | 홈 대시보드, KPI 메트릭 | bean_service, analytics |
| **BeanManagement.py** | 293 | 원두 CRUD (Create, Read, Update, Delete) | bean_service |
| **BlendManagement.py** | 488 | 블렌드 레시피 관리 | blend_service, bean_service |
| **Analysis.py** | 594 | 상세 비용 분석, 차트 | analytics_service |
| **InventoryManagement.py** | 483 | 원두 입출고 추적 | 자동 생성됨 |
| **Report.py** | 588 | 보고서 생성, 내보내기 | report_service |
| **Settings.py** | 502 | 시스템 설정, 비용 파라미터 | - |
| **ExcelSync.py** | 349 | Excel 임포트/내보내기 | excel_service |
| **AdvancedAnalysis.py** | 566 | 머신러닝 기반 분석 | analytics_service |

**페이지 작성 규칙:**
```python
import streamlit as st
from app.services import bean_service  # 서비스 import
from app.components import PageHeader   # 컴포넌트 import

# 1. 서비스 초기화
bean_svc = bean_service.BeanService()

# 2. 페이지 렌더링
st.set_page_config(page_title="페이지명", layout="wide")
PageHeader(title="제목", subtitle="부제목")

# 3. 비즈니스 로직
beans = bean_svc.get_all_beans()

# 4. UI 렌더링
st.dataframe(beans)
```

---

### ⚙️ app/services/ (6개, 2,000줄)

비즈니스 로직 계층입니다. 데이터 처리, 계산, 변환을 담당합니다.

| 파일 | 책임 | 핵심 메서드 |
|------|------|----------|
| **bean_service.py** | 원두 관리 로직 | `add_bean()`, `get_all()`, `update()`, `delete()` |
| **blend_service.py** | 블렌드 관리 로직 | `create_blend()`, `calculate_cost()`, `get_recipes()` |
| **report_service.py** | 보고서 생성 | `export_to_excel()`, `generate_summary()` |
| **excel_service.py** | Excel 임포트/내보내기 | `import_beans()`, `export_data()` |
| **analytics_service.py** | 분석 & 예측 | `analyze_cost()`, `predict_inventory()`, `roi_analysis()` |
| **transaction_service.py** | 거래 기록 관리 | `record_transaction()`, `get_history()` |

**서비스 작성 규칙:**
```python
from app.models import database
from app.models.bean import Bean

class BeanService:
    def __init__(self):
        self.db = database.get_session()

    def add_bean(self, name, price):
        bean = Bean(name=name, price_per_kg=price)
        self.db.add(bean)
        self.db.commit()
        return bean

    def get_all_beans(self):
        return self.db.query(Bean).all()
```

---

### 🗄️ app/models/ (ORM 모델, SQLAlchemy)

데이터베이스 스키마 정의합니다. SQLAlchemy ORM을 사용합니다.

| 파일 | 책임 | 테이블 |
|------|------|--------|
| **database.py** | DB 연결, 세션 관리 | - |
| **bean.py** | 원두 모델 | `beans` 테이블 |
| **blend.py** | 블렌드 모델 | `blends` 테이블 |
| **inventory.py** | 재고 모델 | `inventory` 테이블 |
| **transaction.py** | 거래 모델 | `transactions` 테이블 |
| **cost_setting.py** | 비용 설정 모델 | `cost_settings` 테이블 |

**모델 작성 규칙:**
```python
from sqlalchemy import Column, String, Float
from app.models.database import Base

class Bean(Base):
    __tablename__ = "beans"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    price_per_kg = Column(Float)

    def __repr__(self):
        return f"<Bean {self.name}>"
```

---

### 🎨 app/components/ (15+ 컴포넌트)

재사용 가능한 UI 컴포넌트들입니다.

| 파일 | 컴포넌트 | 용도 |
|------|----------|------|
| **layout.py** | PageTemplate, TabbedLayout, ColumnLayout | 페이지 구조 |
| **ui.py** | PageHeader, MetricsGrid, DataTable, StatCard | UI 요소 |
| **forms.py** | FormField, FormGroup, CRUDForm, SearchBox | 폼 입력 |
| **helpers.py** | format_currency(), validate_email(), 등 | 유틸리티 |

**컴포넌트 사용:**
```python
from app.components import PageHeader, MetricsGrid

PageHeader(title="원두 관리", subtitle="모든 원두의 가격")

metrics = [
    {"label": "총 원두", "value": 13, "icon": "☕"}
]
MetricsGrid(metrics, columns=4)
```

---

### 🛠️ app/utils/

지연 상수 및 유틸리티입니다.

| 파일 | 내용 |
|------|------|
| **constants.py** | 13종 원두, 7개 블렌드 정의 |
| **validators.py** | 데이터 검증 함수 |

---

### 🧪 app/test_*.py

테스트 파일들입니다.

| 파일 | 목적 |
|------|------|
| **test_data.py** | 샘플 데이터 생성 (실행: `./venv/bin/python app/test_data.py`) |
| **test_integration.py** | 통합 테스트 (50개, 100% 통과) |

---

## 📊 Data Layer

### 📍 data/roasting_data.db
SQLite 데이터베이스 파일입니다. 모든 데이터를 저장합니다.

**테이블 목록:**
```
1. beans (원두 목록)
2. blends (블렌드 레시피)
3. inventory (재고)
4. transactions (거래 기록)
5. cost_settings (비용 설정)
6. roasting_logs (로스팅 기록)
```

---

## 📚 Documents/ (23개 문서)

### Architecture/
```
├── COMPONENT_DESIGN.md       # 컴포넌트 시스템 설계
├── COMPONENT_USAGE_GUIDE.md  # 컴포넌트 사용법
├── PROJECT_SETUP_GUIDE.md    # 프로젝트 설정 가이드
├── FILE_STRUCTURE.md         # 이 파일 (파일 구조)
├── DEVELOPMENT_GUIDE.md      # 개발 워크플로우
└── SYSTEM_ARCHITECTURE.md    # 시스템 아키텍처
```

### Guides/
```
├── 배포가이드.md             # Docker, Nginx 배포
├── 사용자가이드.md           # 사용자 매뉴얼
├── 성능최적화_가이드.md      # 성능 최적화
├── TROUBLESHOOTING.md        # 문제 해결 & FAQ
└── COMMON_TASKS.md           # 25가지 자주 하는 작업
```

### Progress/
```
├── 00_프로젝트_진행상황.md
├── PHASE1~4_완료_가이드.md
├── SESSION_SUMMARY_*.md      # 세션 요약
├── SESSION_START_CHECKLIST.md
└── SESSION_END_CHECKLIST.md
```

### Planning/
```
└── 웹페이지_구현_마스터플랜.*
```

### Resources/
```
├── roasting_and_abbrev.mdc   # 로스팅 용어
├── the_moon.mdc              # 사업 개요
└── (기타 데이터 파일)
```

---

## 🔄 데이터 흐름도

```
사용자 입력 (UI)
    ↓
pages/*.py (페이지 로직)
    ↓
components/ (UI 렌더링)
    ↓
services/*.py (비즈니스 로직)
    ↓
models/*.py (ORM)
    ↓
data/roasting_data.db (SQLite)
    ↓
결과 표시
```

---

## 📊 파일 통계

| 항목 | 수량 | 줄수 |
|------|------|------|
| 페이지 | 9개 | 4,500 |
| 서비스 | 6개 | 2,000 |
| 모델 | 6개 | 600 |
| 컴포넌트 | 15개 | 1,500 |
| 유틸리티 | 2개 | 300 |
| 테스트 | 2개 | 250 |
| **전체 코드** | **40개 파일** | **9,561줄** |
| 문서 | 28개 | 5,000+ |

---

## 🔗 파일 의존성 맵

```
pages/* (사용자 인터페이스)
    ↓
services/* (비즈니스 로직)
    ↓
models/* (데이터 모델)
    ↓
database.py (DB 연결)
    ↓
SQLite (데이터 저장소)

components/* (UI 요소)
    ↓ (모든 pages에서 사용)

utils/* (헬퍼 함수)
    ↓ (전체에서 사용)
```

---

## ✅ 파일 추가 규칙

### 새 페이지 추가
1. `app/pages/PageName.py` 생성
2. `app/pages/__init__.py` 업데이트 (필요시)
3. 기존 페이지 참고하여 구조 유지

### 새 서비스 추가
1. `app/services/feature_service.py` 생성
2. 해당 모델 클래스 참고
3. 페이지에서 import하여 사용

### 새 모델 추가
1. `app/models/model_name.py` 생성
2. `models/database.py`에 테이블 정보 추가
3. `app/models/__init__.py` 업데이트

---

**마지막 업데이트: 2025-10-27**
