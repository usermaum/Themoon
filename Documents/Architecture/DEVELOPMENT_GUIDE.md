# 개발 워크플로우 가이드

> 새로운 기능을 추가하거나 버그를 수정할 때 따라할 수 있는 단계별 가이드입니다.

---

## 🚀 5단계 개발 프로세스

### 1️⃣ 요구사항 정의 & 설계

**할 일:**
- 추가할 기능이 뭔가 명확히 하기
- 어떤 데이터가 필요한가?
- 어떤 서비스가 필요한가?
- 어떤 UI가 필요한가?

**예시:**
```
기능: "월별 비용 분석 대시보드 추가"

필요한 것:
  - 데이터: 월별 집계된 비용 데이터
  - 서비스: analytics_service.py 함수 추가
  - UI: Analysis.py 페이지에 차트 추가
  - 모델: 기존 모델 재활용
```

---

### 2️⃣ 데이터 모델 (필요시)

**새 모델이 필요한 경우만:**

```python
# app/models/my_model.py
from sqlalchemy import Column, String, Float, Integer, DateTime
from app.models.database import Base
from datetime import datetime

class MyModel(Base):
    __tablename__ = "my_models"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<MyModel {self.name}>"
```

**체크리스트:**
- [ ] 모델 파일 생성
- [ ] `__tablename__` 정의
- [ ] 필드 정의 (id, name, ... )
- [ ] `__repr__` 메서드 구현

**DB에 반영:**
```bash
# app.py의 init_database()에서 자동으로 테이블 생성됨
./venv/bin/streamlit run app/app.py
```

---

### 3️⃣ 비즈니스 로직 (Service Layer)

**기본 패턴:**

```python
# app/services/my_service.py
from app.models import database
from app.models.my_model import MyModel

class MyService:
    def __init__(self):
        self.db = database.get_session()

    # Create
    def add_item(self, name, value):
        """새 항목 추가"""
        item = MyModel(name=name, value=value)
        self.db.add(item)
        self.db.commit()
        return item

    # Read
    def get_all(self):
        """모든 항목 조회"""
        return self.db.query(MyModel).all()

    def get_by_name(self, name):
        """이름으로 조회"""
        return self.db.query(MyModel).filter(
            MyModel.name == name
        ).first()

    # Update
    def update(self, id, **kwargs):
        """항목 수정"""
        item = self.db.query(MyModel).filter(MyModel.id == id).first()
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            self.db.commit()
        return item

    # Delete
    def delete(self, id):
        """항목 삭제"""
        item = self.db.query(MyModel).filter(MyModel.id == id).first()
        if item:
            self.db.delete(item)
            self.db.commit()
        return True
```

**테스트:**
```bash
# 간단한 테스트
./venv/bin/python -c "
from app.services.my_service import MyService
svc = MyService()
item = svc.add_item('test', 100.0)
print(f'추가됨: {item}')
"
```

---

### 4️⃣ 사용자 인터페이스 (Page)

**기본 페이지 구조:**

```python
# app/pages/MyPage.py
import streamlit as st
from app.services.my_service import MyService
from app.components import PageHeader, DataTable

# 1. 페이지 설정
st.set_page_config(page_title="내 페이지", layout="wide")

# 2. 서비스 초기화
my_svc = MyService()

# 3. 페이지 헤더
PageHeader(title="내 페이지", subtitle="설명")

# 4. 탭 레이아웃 (선택)
tab1, tab2, tab3 = st.tabs(["목록", "추가", "분석"])

with tab1:
    st.subheader("목록")
    items = my_svc.get_all()
    if items:
        df = pd.DataFrame(items)
        st.dataframe(df)
    else:
        st.info("데이터가 없습니다")

with tab2:
    st.subheader("새 항목 추가")
    with st.form("add_form"):
        name = st.text_input("이름")
        value = st.number_input("값", min_value=0.0)

        if st.form_submit_button("추가"):
            my_svc.add_item(name, value)
            st.success("추가되었습니다!")

with tab3:
    st.subheader("분석")
    items = my_svc.get_all()
    if items:
        # 분석 로직
        st.bar_chart([item.value for item in items])
```

**체크리스트:**
- [ ] 페이지 파일 생성 (app/pages/PageName.py)
- [ ] 서비스 임포트
- [ ] PageHeader 추가
- [ ] 탭 레이아웃 (필요시)
- [ ] 각 탭에서 기능 구현
- [ ] 컴포넌트 사용

---

### 5️⃣ 테스트 & 배포

**로컬 테스트:**
```bash
# 앱 실행
./venv/bin/streamlit run app/app.py --server.port 8501

# 브라우저에서 확인
http://localhost:8501
```

**체크리스트:**
- [ ] 페이지 로드됨
- [ ] 데이터 입력 작동
- [ ] 데이터 저장 확인
- [ ] 데이터 조회 작동
- [ ] 오류 없음

**Git 커밋:**
```bash
# 1. 변경사항 확인
git status

# 2. 커밋
git add .
git commit -m "feat: 새 기능 설명

- 기능 1 추가
- 기능 2 추가
- 테스트 완료"

# 3. 버전 업데이트 (선택)
./venv/bin/python logs/update_version.py \
  --type minor \
  --summary "새 기능 추가"

# 4. 최종 커밋 (선택)
git status
```

---

## 🔧 일반적인 작업 패턴

### 패턴 1: CRUD 기능 추가

```
1. 모델 생성 (app/models/)
2. 서비스 구현 (app/services/)
3. 페이지 작성 (app/pages/)
4. 테스트
5. 커밋
```

### 패턴 2: 분석 기능 추가

```
1. 분석 함수 추가 (analytics_service.py)
2. 기존 페이지에 차트 추가
3. 테스트
4. 커밋
```

### 패턴 3: 컴포넌트 추가

```
1. 컴포넌트 파일 생성 (app/components/)
2. 여러 페이지에서 재사용
3. 테스트
4. 커밋
```

---

## 📊 의존성 순서 (중요!)

```
모델 (models/)
  ↓
서비스 (services/)
  ↓
페이지 (pages/)
```

**규칙:**
- ✅ 페이지는 서비스 사용 가능
- ✅ 서비스는 모델 사용 가능
- ❌ 모델은 서비스/페이지 사용 불가
- ❌ 서비스는 페이지 사용 불가
- ❌ 페이지는 다른 페이지 사용 불가

---

## ⚡ 빠른 개발 팁

### 1. 기존 코드 복사
새 기능은 기존 기능과 유사한 경우가 많습니다. 기존 파일을 복사하여 수정하세요.

```bash
# BeanManagement.py를 참고하여 OriginManagement.py 생성
cp app/pages/BeanManagement.py app/pages/OriginManagement.py

# 내용 수정
nano app/pages/OriginManagement.py
```

### 2. 컴포넌트 사용
공통 UI는 컴포넌트로 만들어져 있습니다. 복사/붙여넣기보다는 컴포넌트를 사용하세요.

```python
# ❌ 나쁜 예
st.text_input("이름")
st.number_input("값")

# ✅ 좋은 예
from app.components import FormField, FormGroup
fields = [
    FormField("name", "이름", type="text"),
    FormField("value", "값", type="number"),
]
values = FormGroup(fields)
```

### 3. 자동 생성되는 것들
다음은 자동으로 생성/관리됩니다:
- 데이터베이스 테이블 (models 정의 후 자동)
- 컴포넌트 export (components/__init__.py 자동 관리)

---

## 🐛 문제 발생시

**모듈을 못 찾음:**
```python
# ❌ 틀림
from services.bean_service import BeanService

# ✅ 맞음
from app.services.bean_service import BeanService
```

**데이터베이스 오류:**
```bash
# DB 재초기화
rm data/roasting_data.db
./venv/bin/streamlit run app/app.py
```

**포트 사용 중:**
```bash
# 포트 8501 강제 종료
lsof -ti :8501 | xargs kill -9
```

자세한 문제 해결은 → `TROUBLESHOOTING.md` 참고

---

**마지막 업데이트: 2025-10-27**
