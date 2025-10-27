# 문제 해결 가이드 (Troubleshooting Guide)

> 프로젝트 실행 중 발생하는 일반적인 문제들과 해결 방법을 정리한 가이드입니다.

---

## 🚀 시작 문제

### 1️⃣ "No such file or directory: venv"

**오류 메시지:**
```
./venv/bin/python: No such file or directory
./venv/bin/streamlit: command not found
```

**원인:**
- 프로젝트 격리 Python 환경이 초기화되지 않음

**해결 방법:**
```bash
# 1. 프로젝트 루트에서 venv 생성
python3 -m venv venv

# 2. 패키지 설치
./venv/bin/pip install -r requirements.txt

# 3. 설치 확인
./venv/bin/python --version  # Python 3.12.3이어야 함
./venv/bin/streamlit --version

# 4. 앱 실행
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true
```

---

### 2️⃣ "ModuleNotFoundError: No module named 'streamlit'"

**오류 메시지:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**원인:**
- 시스템 Python을 사용하거나 패키지가 미설치됨

**해결 방법:**
```bash
# ❌ 절대 금지
python script.py
python3 script.py

# ✅ 항상 사용
./venv/bin/python script.py
./venv/bin/streamlit run app/app.py

# 패키지 확인
./venv/bin/pip list | grep streamlit

# 패키지 재설치
./venv/bin/pip install streamlit==1.38.0
./venv/bin/pip freeze > requirements.txt
```

---

### 3️⃣ "Port 8501 already in use"

**오류 메시지:**
```
Error: Address already in use :::8501
```

**원인:**
- 이전 Streamlit 프로세스가 포트를 점유하고 있음

**해결 방법:**
```bash
# 1. 포트 8501 사용하는 프로세스 종료
lsof -ti :8501 | xargs kill -9

# 또는 포트 변경
./venv/bin/streamlit run app/app.py --server.port 8502 --server.headless true

# 2. 확인
lsof -i :8501  # 아무것도 나오지 않아야 함
```

---

## 🗄️ 데이터베이스 문제

### 4️⃣ "Database table does not exist"

**오류 메시지:**
```
sqlite3.OperationalError: no such table: beans
```

**원인:**
- 데이터베이스 테이블이 생성되지 않음
- 데이터베이스 파일이 손상됨

**해결 방법:**
```bash
# 1. 데이터베이스 재초기화 (데이터 삭제됨!)
rm Data/roasting_data.db

# 2. 앱 재실행 (자동으로 테이블 생성)
./venv/bin/streamlit run app/app.py

# 3. 샘플 데이터 생성 (선택사항)
./venv/bin/python app/test_data.py

# 4. 데이터베이스 확인
sqlite3 Data/roasting_data.db ".tables"
sqlite3 Data/roasting_data.db "SELECT COUNT(*) FROM beans;"
```

**⚠️ 주의:** 데이터베이스 삭제 시 모든 데이터가 사라집니다. 백업을 먼저 하세요!

```bash
# 백업 생성
cp Data/roasting_data.db Data/roasting_data_backup_$(date +%Y%m%d_%H%M%S).db
```

---

### 5️⃣ "Database is locked"

**오류 메시지:**
```
sqlite3.OperationalError: database is locked
```

**원인:**
- 다른 프로세스가 데이터베이스를 사용 중
- SQLite WAL (Write-Ahead Logging) 파일 문제

**해결 방법:**
```bash
# 1. Streamlit 프로세스 종료
lsof -ti :8501 | xargs kill -9
pkill -f streamlit

# 2. WAL 파일 정리 (선택사항)
rm -f Data/roasting_data.db-wal
rm -f Data/roasting_data.db-shm

# 3. 앱 재실행
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true

# 4. 데이터베이스 통합성 확인
sqlite3 Data/roasting_data.db "PRAGMA integrity_check;"
```

---

### 6️⃣ "Bad database path"

**오류 메시지:**
```
FileNotFoundError: [Errno 2] No such file or directory: '../Data/roasting_data.db'
```

**원인:**
- 상대 경로 문제
- 스크립트가 잘못된 위치에서 실행됨

**해결 방법:**
```bash
# ❌ 잘못된 방법 (디렉토리에서 실행)
cd app
./venv/bin/streamlit run app.py  # 상대 경로 오류!

# ✅ 올바른 방법 (프로젝트 루트에서)
./venv/bin/streamlit run app/app.py

# 또는 절대 경로 사용 (권장)
# app/app.py 수정
db_path = os.path.join(os.path.dirname(__file__), '../Data/roasting_data.db')
# 대신
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Data/roasting_data.db'))
```

---

## 📦 패키지/의존성 문제

### 7️⃣ "ImportError: cannot import name 'xxx'"

**오류 메시지:**
```
ImportError: cannot import name 'BeanService' from 'app.services'
```

**원인:**
- 모듈 경로 오류
- 잘못된 import 문법
- 순환 참조

**해결 방법:**

```bash
# 1. 현재 설치된 패키지 확인
./venv/bin/pip list

# 2. 모듈 경로 확인
./venv/bin/python -c "import app.services.bean_service; print(app.services.bean_service.__file__)"

# 3. 파이썬 경로 확인
./venv/bin/python -c "import sys; print(sys.path)"
```

**일반적인 import 오류 수정:**

```python
# ❌ 틀린 경로
from services.bean_service import BeanService
from service import bean_service

# ✅ 올바른 경로
from app.services.bean_service import BeanService
from app.services import bean_service

# ✅ 또는 상대 import (같은 패키지 내)
from .bean_service import BeanService
```

---

### 8️⃣ "openpyxl version conflict"

**오류 메시지:**
```
ImportError: cannot import openpyxl.utils.cell
```

**원인:**
- openpyxl 버전 불일치
- 설치된 패키지와 코드 호환성 문제

**해결 방법:**
```bash
# 1. openpyxl 재설치
./venv/bin/pip uninstall openpyxl -y
./venv/bin/pip install openpyxl==3.1.5

# 2. 전체 의존성 재설치
./venv/bin/pip install -r requirements.txt --force-reinstall

# 3. 설치 확인
./venv/bin/pip show openpyxl
```

---

## 🖥️ 페이지/UI 문제

### 9️⃣ "st.form_submit_button() got unexpected keyword argument"

**오류 메시지:**
```
TypeError: form_submit_button() got an unexpected keyword argument 'key'
```

**원인:**
- Streamlit API 변경 또는 잘못된 파라미터 사용

**해결 방법:**
```python
# ❌ 틀린 방법
if st.form_submit_button("추가", key="btn_add"):
    pass

# ✅ 올바른 방법 (key 파라미터 제거)
if st.form_submit_button("추가"):
    pass

# ✅ 또는 with st.form 내부에서 사용
with st.form("my_form"):
    name = st.text_input("이름")
    if st.form_submit_button("추가"):
        # 동작 구현
        pass
```

---

### 🔟 "Session state is not persisting"

**오류 메시지:**
```
# 페이지 새로고침 후 입력값이 사라짐
```

**원인:**
- `st.session_state` 초기화 누락
- 상태 변수가 재설정됨

**해결 방법:**
```python
# ✅ 올바른 패턴
if "beans" not in st.session_state:
    st.session_state.beans = bean_service.get_all_beans()

# 이후 st.session_state.beans 사용
beans = st.session_state.beans

# ✅ 또는 session_state 콜백 사용
def update_bean_name():
    st.session_state.selected_bean = st.session_state._bean_selector

st.selectbox(
    "원두 선택",
    [b.name for b in beans],
    key="_bean_selector",
    on_change=update_bean_name
)
```

---

### 1️⃣1️⃣ "Streamlit script needs st.set_page_config() at the top"

**오류 메시지:**
```
PageConfigError: set_page_config() can only be called once per app
```

**원인:**
- `st.set_page_config()`가 여러 번 호출됨
- 페이지 파일의 시작이 아닌 곳에 위치함

**해결 방법:**
```python
# ✅ 올바른 구조
import streamlit as st

# 파일 시작에 반드시 위치
st.set_page_config(page_title="페이지명", layout="wide")

# 그 다음 다른 imports
from app.services import bean_service
from app.components import PageHeader

# 나머지 코드...
```

---

## 🔍 성능 문제

### 1️⃣2️⃣ "Page loads very slowly"

**증상:**
```
페이지 로드에 10초 이상 소요
```

**원인:**
- N+1 쿼리 문제
- 캐싱 미사용
- 불필요한 재계산

**해결 방법:**

```python
# ❌ 느린 방법 (N+1 쿼리)
blends = db.query(Blend).all()
for blend in blends:
    bean = db.query(Bean).filter(Bean.id == blend.bean_id).first()
    # 매번 쿼리 실행 (blend 수만큼 쿼리)

# ✅ 빠른 방법 (조인 사용)
blends = db.query(Blend).join(Bean).all()

# ✅ 또는 캐싱 사용
@st.cache_data
def get_all_blends():
    return db.query(Blend).all()

blends = get_all_blends()
```

---

### 1️⃣3️⃣ "Memory usage keeps increasing"

**증상:**
```
앱 사용 중 메모리 사용량 계속 증가
메모리 누수 의심
```

**원인:**
- 캐시가 계속 쌓임
- 세션 상태에 큰 객체 저장
- 데이터베이스 연결 미종료

**해결 방법:**
```bash
# 1. Streamlit 캐시 초기화
rm -rf ~/.streamlit/
./venv/bin/streamlit cache clear

# 2. 프로세스 재시작
lsof -ti :8501 | xargs kill -9
./venv/bin/streamlit run app/app.py

# 3. 코드 최적화
# ❌ 메모리 낭비
st.session_state.large_dataframe = pd.read_csv('large_file.csv')

# ✅ 캐싱 사용
@st.cache_data
def load_data():
    return pd.read_csv('large_file.csv')

df = load_data()
```

---

## 🔐 보안/권한 문제

### 1️⃣4️⃣ "Permission denied" when accessing database

**오류 메시지:**
```
PermissionError: [Errno 13] Permission denied: 'Data/roasting_data.db'
```

**원인:**
- 파일/디렉토리 권한 부족
- WSL 파일 시스템 권한 문제

**해결 방법:**
```bash
# 1. 권한 확인
ls -la Data/roasting_data.db

# 2. 권한 수정
chmod 644 Data/roasting_data.db
chmod 755 Data/

# 3. 소유권 확인
chown $USER:$USER Data/roasting_data.db

# 4. WSL 특정 문제 (필요시)
# .wslconfig 수정
[interop]
appendWindowsPath = false
```

---

## 📝 일반 워크플로우 오류

### 1️⃣5️⃣ "Changes not appearing in database"

**증상:**
```
UI에서 데이터를 추가했는데 데이터베이스에 저장되지 않음
```

**원인:**
- `db.commit()` 누락
- 트랜잭션 롤백됨
- 예외 처리로 변경사항 취소됨

**해결 방법:**

```python
# ❌ 커밋 누락
def add_bean(self, name, price):
    bean = Bean(name=name, price_per_kg=price)
    self.db.add(bean)
    # db.commit() 없음!
    return bean

# ✅ 올바른 방법
def add_bean(self, name, price):
    try:
        bean = Bean(name=name, price_per_kg=price)
        self.db.add(bean)
        self.db.commit()  # 반드시 필요!
        return bean
    except Exception as e:
        self.db.rollback()  # 오류 시 취소
        raise e
```

---

### 1️⃣6️⃣ "Excel export creates empty file"

**증상:**
```
Excel 파일이 생성되지만 내용이 비어있음
```

**원인:**
- 데이터가 없음
- 시트가 생성되지 않음
- 예외 처리 오류

**해결 방법:**

```python
# ✅ 안전한 Excel 내보내기 패턴
def export_to_excel(self):
    try:
        wb = Workbook()
        sheets_created = 0

        # 데이터가 있을 때만 시트 추가
        beans = self.get_all_beans()
        if beans:
            ws = wb.active
            ws.title = "원두"
            # 데이터 추가
            sheets_created += 1

        # 최소 1개 시트 확인
        if sheets_created == 0:
            # 빈 시트라도 생성
            wb.active.title = "데이터 없음"

        wb.save('output.xlsx')
        return True
    except Exception as e:
        st.error(f"내보내기 실패: {e}")
        return False
```

---

## 🛠️ 디버깅 기법

### 로그 확인

```bash
# 1. Streamlit 로그 레벨 지정
./venv/bin/streamlit run app/app.py --logger.level=debug

# 2. 파일로 저장
./venv/bin/streamlit run app/app.py 2>&1 | tee streamlit.log

# 3. 특정 문자열 검색
grep -i "error" streamlit.log
grep -i "warning" streamlit.log
```

### 데이터베이스 검사

```bash
# 1. 테이블 목록 확인
sqlite3 Data/roasting_data.db ".tables"

# 2. 테이블 스키마 확인
sqlite3 Data/roasting_data.db ".schema beans"

# 3. 데이터 확인
sqlite3 Data/roasting_data.db "SELECT * FROM beans LIMIT 5;"

# 4. 데이터 개수 확인
sqlite3 Data/roasting_data.db "SELECT COUNT(*) as cnt FROM beans;"

# 5. 인덱스 확인
sqlite3 Data/roasting_data.db ".indices"

# 6. 통합성 확인
sqlite3 Data/roasting_data.db "PRAGMA integrity_check;"
```

### Python 디버깅

```python
# 1. 현재 디렉토리 확인
import os
print(os.getcwd())

# 2. 경로 확인
print(os.path.abspath('Data/roasting_data.db'))

# 3. 파일 존재 확인
print(os.path.exists('Data/roasting_data.db'))

# 4. 모듈 위치 확인
import app.models
print(app.models.__file__)

# 5. 버전 확인
import streamlit as st
print(f"Streamlit: {st.__version__}")
import pandas as pd
print(f"Pandas: {pd.__version__}")
```

---

## ✅ 체크리스트

**앱 시작 전 확인:**
- [ ] venv가 ./venv/ 에 존재하는가?
- [ ] `./venv/bin/python --version`이 3.12.3인가?
- [ ] `./venv/bin/pip list | grep streamlit`에 결과가 있는가?
- [ ] 포트 8501이 사용 중이 아닌가?
- [ ] Data/roasting_data.db 파일이 쓰기 권한이 있는가?

**오류 발생 시 해결 순서:**
1. 오류 메시지 전체 읽기
2. 이 가이드에서 관련 섹션 찾기
3. 제안된 해결 방법 순서대로 시도
4. 각 단계마다 앱 실행 확인
5. 위 단계로도 해결 안 되면 로그 생성 후 검토

---

## 📞 추가 도움말

### 자주 묻는 질문 (FAQ)

**Q: 기존 데이터 유지하면서 스키마 변경하려면?**
```bash
# 1. 백업 생성
cp Data/roasting_data.db Data/roasting_data_backup.db

# 2. SQLite 백업 유틸리티 사용
sqlite3 Data/roasting_data.db ".dump" > backup.sql

# 3. 스키마 변경 후
sqlite3 Data/roasting_data_restored.db < backup.sql
```

**Q: 여러 사용자가 동시에 접근하면?**
```
현재: SQLite는 단일 파일 DB로 동시 쓰기 미지원
해결책:
- PostgreSQL로 마이그레이션 검토
- 또는 Flask/FastAPI 서버 추가
```

**Q: 앱 버전은 어디서 확인?**
```bash
cat logs/VERSION
cat logs/CHANGELOG.md
```

---

**마지막 업데이트: 2025-10-27**

