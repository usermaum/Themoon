# 자주 하는 작업 가이드 (Common Tasks)

> 프로젝트에서 자주 수행하는 25가지 작업의 단계별 가이드입니다.

---

## 📋 빠른 참조 목록

| # | 작업 | 예상 시간 | 난이도 |
|---|------|---------|--------|
| 1 | [앱 실행하기](#1-앱-실행하기) | 5초 | ⭐ |
| 2 | [앱 중지하기](#2-앱-중지하기) | 5초 | ⭐ |
| 3 | [원두 추가하기](#3-원두-추가하기) | 1분 | ⭐ |
| 4 | [블렌드 레시피 만들기](#4-블렌드-레시피-만들기) | 3분 | ⭐ |
| 5 | [로스팅 로그 기록하기](#5-로스팅-로그-기록하기) | 2분 | ⭐ |
| 6 | [비용 설정 변경하기](#6-비용-설정-변경하기) | 2분 | ⭐ |
| 7 | [분석 보고서 생성하기](#7-분석-보고서-생성하기) | 5분 | ⭐⭐ |
| 8 | [Excel로 내보내기](#8-excel로-내보내기) | 2분 | ⭐ |
| 9 | [Excel에서 임포트하기](#9-excel에서-임포트하기) | 3분 | ⭐⭐ |
| 10 | [재고 현황 확인하기](#10-재고-현황-확인하기) | 1분 | ⭐ |
| 11 | [새 패키지 설치하기](#11-새-패키지-설치하기) | 2분 | ⭐⭐ |
| 12 | [의존성 업데이트하기](#12-의존성-업데이트하기) | 3분 | ⭐⭐ |
| 13 | [데이터베이스 초기화하기](#13-데이터베이스-초기화하기) | 1분 | ⭐⭐ |
| 14 | [테스트 데이터 생성하기](#14-테스트-데이터-생성하기) | 2분 | ⭐ |
| 15 | [Git 커밋하기](#15-git-커밋하기) | 3분 | ⭐⭐ |
| 16 | [버전 업데이트하기](#16-버전-업데이트하기) | 2분 | ⭐⭐ |
| 17 | [포트 충돌 해결하기](#17-포트-충돌-해결하기) | 1분 | ⭐ |
| 18 | [데이터베이스 백업하기](#18-데이터베이스-백업하기) | 1분 | ⭐ |
| 19 | [새 페이지 추가하기](#19-새-페이지-추가하기) | 10분 | ⭐⭐⭐ |
| 20 | [새 서비스 추가하기](#20-새-서비스-추가하기) | 10분 | ⭐⭐⭐ |
| 21 | [새 모델 추가하기](#21-새-모델-추가하기) | 10분 | ⭐⭐⭐ |
| 22 | [새 컴포넌트 만들기](#22-새-컴포넌트-만들기) | 5분 | ⭐⭐⭐ |
| 23 | [디버깅 모드 실행하기](#23-디버깅-모드-실행하기) | 1분 | ⭐⭐ |
| 24 | [성능 최적화하기](#24-성능-최적화하기) | 15분 | ⭐⭐⭐ |
| 25 | [문서 작성하기](#25-문서-작성하기) | 10분 | ⭐⭐ |

---

## 🚀 기본 작업 (Basic Tasks)

### 1. 앱 실행하기

**목적:** Streamlit 애플리케이션 시작하기

**단계:**
```bash
# 1단계: 프로젝트 루트에서 실행
cd /path/to/TheMoon_Project

# 2단계: 앱 실행
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true

# 또는 메인 런처 사용
./venv/bin/python run.py
```

**확인:**
- 터미널에 "You can now view your Streamlit app in your browser"가 보임
- http://localhost:8501 접속 가능
- 웹 브라우저에서 대시보드 로드됨

**팁:**
```bash
# 포트 변경하려면
./venv/bin/streamlit run app/app.py --server.port 8502

# 개발 모드 (자동 재로드)
./venv/bin/streamlit run app/app.py --logger.level=debug

# 로그를 파일에 저장
./venv/bin/streamlit run app/app.py > streamlit.log 2>&1 &
```

---

### 2. 앱 중지하기

**목적:** 실행 중인 Streamlit 앱 종료하기

**단계:**
```bash
# 방법 1: 터미널에서 Ctrl+C 누르기
# (실행한 터미널에서)
Ctrl+C

# 방법 2: 포트로 프로세스 종료
lsof -ti :8501 | xargs kill -9

# 방법 3: streamlit 프로세스 모두 종료
pkill -f streamlit
```

**확인:**
```bash
# 포트 8501이 해제되었는지 확인
lsof -i :8501  # 아무것도 나오지 않아야 함
```

---

### 3. 원두 추가하기

**목적:** 새로운 원두 등록하기

**단계:**

1. **웹 UI에서:**
   - 앱 실행 후 좌측 사이드바 > "원두 관리" 클릭
   - "원두 목록" 탭에 있는 "새 원두 추가" 섹션으로 이동
   - 원두명 입력 (예: "Ethiopia Yirgacheffe")
   - kg당 가격 입력 (예: 28000)
   - "추가" 버튼 클릭

2. **데이터베이스 확인:**
```bash
sqlite3 data/roasting_data.db "SELECT * FROM beans WHERE name = 'Ethiopia Yirgacheffe';"
```

**팁:**
- 원두명은 고유해야 함 (중복 불가)
- 가격은 양수만 가능
- 추가 후 페이지 새로고침하면 목록에 나타남

---

### 4. 블렌드 레시피 만들기

**목적:** 여러 원두를 섞어 새 블렌드 만들기

**단계:**

1. **사전 준비:**
   - 사용할 원두들이 먼저 등록되어 있어야 함
   - 각 원두의 가격이 설정되어 있어야 함

2. **웹 UI에서:**
   - "블렌드 관리" > "블렌드 생성" 탭
   - 블렌드 이름 입력 (예: "Signature Blend")
   - "원두 추가" 버튼 클릭
   - 원두 선택 & 비율(%) 입력
   - 여러 원두를 반복하여 추가 (총합 100%)
   - "블렌드 생성" 버튼 클릭

3. **확인:**
```bash
sqlite3 data/roasting_data.db "SELECT * FROM blends WHERE name = 'Signature Blend';"
```

**예시:**
```
블렌드명: Signature Blend
- Ethiopia Yirgacheffe: 40%
- Kenya AA FAQ: 35%
- Colombia Huila: 25%
(총합: 100%)
```

---

### 5. 로스팅 로그 기록하기

**목적:** 매일의 로스팅 기록 저장하기

**단계:**

1. **웹 UI에서:**
   - "대시보드" 또는 "분석" > "로스팅 로그" 탭
   - 날짜 선택
   - 원두 선택 (또는 블렌드)
   - 생두 무게(kg) 입력 (예: 1.5)
   - 로스팅 후 무게(kg) 입력 (예: 1.25)
   - 비용 정보 입력
   - "기록 저장" 버튼 클릭

2. **데이터베이스 확인:**
```bash
sqlite3 data/roasting_data.db "SELECT * FROM roasting_logs ORDER BY date DESC LIMIT 1;"
```

**팁:**
- 로스팅 손실율은 자동 계산됨 (약 16.7%)
- 모든 필드는 필수입력
- 같은 날짜에 여러 로그 기록 가능

---

### 6. 비용 설정 변경하기

**목적:** 로스팅 비용 파라미터 업데이트하기

**단계:**

1. **웹 UI에서:**
   - "설정" 페이지 이동
   - "비용 설정" 섹션 찾기
   - 각 항목 수정:
     - 로스팅 비용/kg (예: 2000)
     - 인건비/시간 (예: 15000)
     - 로스팅 시간 (예: 2시간)
     - 전기료 (예: 5000)
     - 기타 비용 (예: 3000)
   - "저장" 버튼 클릭

2. **데이터베이스 확인:**
```bash
sqlite3 data/roasting_data.db "SELECT * FROM cost_settings;"
```

**팁:**
- 설정 변경은 즉시 반영됨
- 과거 로그의 비용은 자동 재계산됨
- 기본값: 로스팅 손실 16.7%

---

## 📊 분석 & 리포트 (Analytics & Reports)

### 7. 분석 보고서 생성하기

**목적:** 종합 비용 분석 및 차트 생성하기

**단계:**

1. **웹 UI에서:**
   - "분석" 페이지 이동
   - 분석 기간 선택 (시작일 ~ 종료일)
   - "분석 유형" 선택:
     - 월별 비용 추이
     - 원두별 비용 분석
     - 블렌드별 수익성
     - 로스팅 효율 분석
   - "보고서 생성" 버튼 클릭

2. **결과 확인:**
   - 차트와 통계 표 표시
   - KPI 메트릭 표시:
     - 총 원두 무게
     - 총 로스팅 비용
     - 평균 kg당 비용
     - 총 수익

**팁:**
- 차트는 마우스로 상호작용 가능 (확대, 축소 등)
- 기간이 없으면 전체 데이터 분석

---

### 8. Excel로 내보내기

**목적:** 모든 데이터를 Excel 파일로 저장하기

**단계:**

1. **웹 UI에서:**
   - "보고서" 페이지 이동
   - "데이터 내보내기" 섹션
   - "내보내기 형식" 선택:
     - 원두 목록 (beans)
     - 블렌드 레시피 (blends)
     - 로스팅 로그 (logs)
     - 종합 보고서 (all)
   - "Excel 다운로드" 버튼 클릭

2. **파일 확인:**
   - 브라우저 다운로드 폴더에서 파일 확인
   - Excel 또는 Google Sheets에서 열기

**팁:**
```bash
# 명령어로도 가능
./venv/bin/python -c "
from app.services.report_service import ReportService
rs = ReportService()
rs.export_to_excel('output.xlsx')
"
```

---

### 9. Excel에서 임포트하기

**목적:** Excel 파일에서 데이터 가져오기

**단계:**

1. **Excel 파일 준비:**
   - 다음 형식으로 파일 준비:
     ```
     | 원두명 | 가격(원/kg) |
     |--------|-----------|
     | Ethiopia | 28000 |
     | Kenya | 26000 |
     ```

2. **웹 UI에서:**
   - "Excel 동기화" 페이지 이동
   - "파일 선택" 버튼으로 Excel 파일 선택
   - "임포트" 버튼 클릭
   - 확인 메시지 확인

3. **데이터 확인:**
   - "원두 관리"에서 새 원두 확인
   - 데이터베이스에서 확인:
     ```bash
     sqlite3 data/roasting_data.db "SELECT COUNT(*) FROM beans;"
     ```

**팁:**
- Excel 파일은 .xlsx 형식이어야 함
- 첫 행은 헤더(열 이름)여야 함
- 중복 원두는 자동 건너뜀

---

### 10. 재고 현황 확인하기

**목적:** 현재 원두 재고량 확인하기

**단계:**

1. **웹 UI에서:**
   - "재고 관리" 페이지 이동
   - "재고 현황" 탭 클릭
   - 각 원두별 현재 재고 표시

2. **상세 정보:**
   - 원두명
   - 현재 보유량 (kg)
   - 최근 입고 날짜
   - 최근 출고 날짜
   - 사용 추이 그래프

**팁:**
- 재고는 로스팅 로그에서 자동 계산
- 부족한 원두는 경고 표시됨 (옵션)

---

## ⚙️ 개발 환경 (Development)

### 11. 새 패키지 설치하기

**목적:** 프로젝트에 새 Python 패키지 추가하기

**단계:**

1. **패키지 설치:**
```bash
# venv 내에서 설치
./venv/bin/pip install package_name

# 또는 버전 지정
./venv/bin/pip install package_name==1.2.3
```

2. **의존성 저장:**
```bash
# requirements.txt 업데이트
./venv/bin/pip freeze > requirements.txt
```

3. **설치 확인:**
```bash
./venv/bin/pip show package_name
./venv/bin/pip list | grep package_name
```

4. **코드에서 사용:**
```python
import package_name

# 앱 테스트
./venv/bin/streamlit run app/app.py
```

**예시:**
```bash
# 새로운 분석 라이브러리 설치
./venv/bin/pip install scikit-learn==1.3.0
./venv/bin/pip freeze > requirements.txt
```

---

### 12. 의존성 업데이트하기

**목적:** 설치된 패키지 버전 업그레이드하기

**단계:**

1. **단일 패키지 업그레이드:**
```bash
./venv/bin/pip install --upgrade package_name
```

2. **전체 패키지 업그레이드:**
```bash
./venv/bin/pip install --upgrade -r requirements.txt
```

3. **특정 버전으로 다운그레이드:**
```bash
./venv/bin/pip install package_name==1.2.3
```

4. **의존성 저장:**
```bash
./venv/bin/pip freeze > requirements.txt
```

5. **테스트:**
```bash
./venv/bin/streamlit run app/app.py
./venv/bin/python app/test_integration.py
```

**경고:**
- 주요 버전 업그레이드 전에 항상 테스트
- requirements.txt 변경사항은 Git에 커밋하기

---

### 13. 데이터베이스 초기화하기

**목적:** 데이터베이스를 초기 상태로 리셋하기

**단계:**

1. **데이터베이스 백업 (권장):**
```bash
cp data/roasting_data.db data/roasting_data_backup_$(date +%Y%m%d).db
```

2. **데이터베이스 삭제:**
```bash
rm data/roasting_data.db
```

3. **앱 재실행 (자동 초기화):**
```bash
./venv/bin/streamlit run app/app.py
```

4. **확인:**
```bash
sqlite3 data/roasting_data.db ".tables"
# 출력: beans blends inventory transactions cost_settings roasting_logs
```

**⚠️ 주의:** 모든 데이터가 삭제됩니다!

---

### 14. 테스트 데이터 생성하기

**목적:** 개발/테스트용 샘플 데이터 만들기

**단계:**

1. **스크립트 실행:**
```bash
./venv/bin/python app/test_data.py
```

2. **생성되는 데이터:**
   - 13종 원두
   - 7개 블렌드 레시피
   - 30개 로스팅 로그
   - 비용 설정

3. **확인:**
```bash
# 웹 UI에서 "원두 관리" 페이지 확인
# 또는 데이터베이스 확인
sqlite3 data/roasting_data.db "SELECT COUNT(*) FROM roasting_logs;"
```

**팁:**
- 기존 데이터를 덮어쓰지 않음
- 매번 실행할 때마다 새 데이터 추가
- 리셋하려면 데이터베이스 초기화 (작업 13) 후 실행

---

## 🔄 버전 관리 (Version Control)

### 15. Git 커밋하기

**목적:** 변경사항을 Git에 커밋하기

**단계:**

1. **변경사항 확인:**
```bash
git status
git diff
```

2. **파일 추가:**
```bash
# 특정 파일만
git add app/services/new_service.py

# 모든 변경사항
git add .
```

3. **커밋 메시지 작성:**
```bash
git commit -m "feat: 새로운 서비스 추가

- 새 서비스의 기능 설명
- 변경사항 상세

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

4. **푸시 (선택):**
```bash
git push origin main
```

5. **확인:**
```bash
git log --oneline | head -5
```

**커밋 타입:**
- `feat:` - 새로운 기능
- `fix:` - 버그 수정
- `docs:` - 문서 업데이트
- `refactor:` - 코드 리팩토링
- `test:` - 테스트 추가
- `chore:` - 빌드, 패키지 관리

---

### 16. 버전 업데이트하기

**목적:** 프로젝트 버전 번호 업데이트하기

**단계:**

1. **현재 버전 확인:**
```bash
cat logs/VERSION
# 출력: 1.2.0
```

2. **새 버전으로 업데이트:**
```bash
# Semantic Versioning 규칙:
# MAJOR.MINOR.PATCH
# - PATCH: 버그 수정 (1.2.0 → 1.2.1)
# - MINOR: 새 기능 (1.2.0 → 1.3.0)
# - MAJOR: 호환성 깨짐 (1.2.0 → 2.0.0)

# 스크립트로 자동 업데이트
./venv/bin/python logs/update_version.py --type minor --summary "새 기능 추가"
```

3. **CHANGELOG 업데이트:**
```bash
# logs/CHANGELOG.md 편집
cat logs/CHANGELOG.md
```

4. **커밋:**
```bash
git add logs/VERSION logs/CHANGELOG.md
git commit -m "chore: v1.3.0 버전 업데이트"
```

---

### 17. 포트 충돌 해결하기

**목적:** 포트 8501이 이미 사용 중일 때 해결하기

**단계:**

1. **포트 점유 프로세스 확인:**
```bash
lsof -i :8501
```

2. **프로세스 종료:**
```bash
# 프로세스 ID 확인 후 종료
lsof -ti :8501 | xargs kill -9

# 또는 streamlit 모두 종료
pkill -f streamlit
```

3. **다른 포트로 실행:**
```bash
./venv/bin/streamlit run app/app.py --server.port 8502
```

4. **확인:**
```bash
lsof -i :8501  # 비어있어야 함
curl http://localhost:8502  # 새 포트에서 실행 확인
```

---

### 18. 데이터베이스 백업하기

**목적:** 데이터베이스 정기적으로 백업하기

**단계:**

1. **파일 복사 백업:**
```bash
# 현재 날짜를 파일명에 포함
cp data/roasting_data.db data/roasting_data_backup_$(date +%Y%m%d_%H%M%S).db
```

2. **SQL 덤프 백업 (권장):**
```bash
sqlite3 data/roasting_data.db ".dump" > data/backup.sql
```

3. **복원하기:**
```bash
# SQL 덤프에서 복원
sqlite3 data/roasting_data_restored.db < data/backup.sql

# 또는 파일 복사본 사용
cp data/roasting_data_backup_20251027.db data/roasting_data.db
```

4. **자동 백업 설정 (선택):**
```bash
# cron 작업으로 매일 백업
crontab -e
# 다음 추가:
# 0 2 * * * cp /path/to/data/roasting_data.db /path/to/data/backup_$(date +\%Y\%m\%d).db
```

---

## 🛠️ 고급 개발 (Advanced Development)

### 19. 새 페이지 추가하기

**목적:** 새로운 UI 페이지 추가하기

**단계:**

1. **페이지 파일 생성:**
```bash
touch app/pages/NewPage.py
```

2. **기본 구조 작성:**
```python
# app/pages/NewPage.py
import streamlit as st
from app.components import PageHeader, MetricsGrid
from app.services import bean_service

# 페이지 설정
st.set_page_config(page_title="새 페이지", layout="wide")

# 서비스 초기화
bean_svc = bean_service.BeanService()

# 헤더
PageHeader(title="새 페이지", subtitle="설명")

# 탭 레이아웃
tab1, tab2 = st.tabs(["목록", "추가"])

with tab1:
    st.subheader("목록")
    beans = bean_svc.get_all_beans()
    if beans:
        st.dataframe(beans)
    else:
        st.info("데이터 없음")

with tab2:
    st.subheader("추가")
    with st.form("add_form"):
        name = st.text_input("이름")
        if st.form_submit_button("추가"):
            st.success("추가됨!")
```

3. **사이드바에 등록:**
```python
# app/app.py render_sidebar() 함수에 추가
if st.sidebar.button("새 페이지", key="new_page"):
    st.switch_page("pages/NewPage.py")
```

4. **테스트:**
```bash
./venv/bin/streamlit run app/app.py
# 사이드바에서 새 페이지 클릭 확인
```

---

### 20. 새 서비스 추가하기

**목적:** 비즈니스 로직 계층에 새 서비스 추가하기

**단계:**

1. **서비스 파일 생성:**
```bash
touch app/services/new_service.py
```

2. **서비스 클래스 구현:**
```python
# app/services/new_service.py
from app.models import database
from app.models.my_model import MyModel

class MyService:
    def __init__(self):
        self.db = database.get_session()

    def add_item(self, name, value):
        """새 항목 추가"""
        item = MyModel(name=name, value=value)
        self.db.add(item)
        self.db.commit()
        return item

    def get_all(self):
        """모든 항목 조회"""
        return self.db.query(MyModel).all()

    def get_by_id(self, item_id):
        """ID로 조회"""
        return self.db.query(MyModel).filter(
            MyModel.id == item_id
        ).first()

    def update(self, item_id, **kwargs):
        """항목 수정"""
        item = self.get_by_id(item_id)
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            self.db.commit()
        return item

    def delete(self, item_id):
        """항목 삭제"""
        item = self.get_by_id(item_id)
        if item:
            self.db.delete(item)
            self.db.commit()
        return True
```

3. **모델 필요시 생성:**
```bash
touch app/models/my_model.py
```

4. **페이지에서 사용:**
```python
from app.services.new_service import MyService

my_svc = MyService()
items = my_svc.get_all()
```

---

### 21. 새 모델 추가하기

**목적:** 데이터베이스 테이블을 위한 새 모델 정의하기

**단계:**

1. **모델 파일 생성:**
```bash
touch app/models/feature.py
```

2. **SQLAlchemy 모델 정의:**
```python
# app/models/feature.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.models.database import Base
from datetime import datetime

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Feature {self.name}>"
```

3. **모델 등록 (자동 생성):**
```python
# app/app.py init_database() 함수에서
# Base.metadata.create_all() 호출 시 자동 생성됨
```

4. **데이터베이스 확인:**
```bash
# 앱 실행하면 자동으로 테이블 생성됨
./venv/bin/streamlit run app/app.py

# 확인
sqlite3 data/roasting_data.db ".schema features"
```

---

### 22. 새 컴포넌트 만들기

**목적:** 재사용 가능한 UI 컴포넌트 만들기

**단계:**

1. **컴포넌트 파일 생성:**
```bash
touch app/components/custom.py
```

2. **컴포넌트 함수 정의:**
```python
# app/components/custom.py
import streamlit as st

def CustomCard(title, content, color="blue"):
    """커스텀 카드 컴포넌트"""
    with st.container(border=True):
        st.markdown(f"### {title}")
        st.write(content)

def StatusBadge(status, color_map=None):
    """상태 배지 컴포넌트"""
    if color_map is None:
        color_map = {
            "완료": "green",
            "진행중": "orange",
            "대기": "gray"
        }
    color = color_map.get(status, "blue")
    st.markdown(
        f"<span style='background:{color};padding:5px 10px;border-radius:3px;color:white'>{status}</span>",
        unsafe_allow_html=True
    )
```

3. **__init__.py에 등록:**
```python
# app/components/__init__.py에 추가
from .custom import CustomCard, StatusBadge
```

4. **페이지에서 사용:**
```python
from app.components import CustomCard

CustomCard("제목", "내용 설명")
```

---

### 23. 디버깅 모드 실행하기

**목적:** 개발 중 디버깅 정보를 자세히 확인하기

**단계:**

1. **로그 레벨 설정:**
```bash
./venv/bin/streamlit run app/app.py --logger.level=debug
```

2. **로그를 파일에 저장:**
```bash
./venv/bin/streamlit run app/app.py 2>&1 | tee debug.log
```

3. **로그 확인:**
```bash
# 오류 메시지 찾기
grep -i "error" debug.log

# 경고 메시지 찾기
grep -i "warning" debug.log
```

4. **코드에서 디버그 정보 출력:**
```python
import streamlit as st

# 변수 확인
st.write("디버깅:", variable_name)

# 데이터프레임 확인
st.dataframe(df)

# JSON 형식으로 출력
st.json(dict_variable)
```

---

### 24. 성능 최적화하기

**목적:** 느린 부분을 찾아 성능 개선하기

**단계:**

1. **캐싱 추가:**
```python
import streamlit as st

# 데이터 캐싱
@st.cache_data
def load_data():
    return expensive_function()

# 연산 캐싱
@st.cache_resource
def initialize_model():
    return heavy_model()
```

2. **N+1 쿼리 해결:**
```python
# ❌ 느림
for bean in beans:
    price = get_bean_price(bean.id)  # 매번 쿼리

# ✅ 빠름
beans_with_prices = get_beans_with_prices()  # 한 번 조인
```

3. **불필요한 재계산 제거:**
```python
# ❌ 매번 계산
if "result" not in st.session_state:
    st.session_state.result = expensive_calc()

# ✅ 캐시 사용
@st.cache_data
def cached_calc():
    return expensive_calc()
```

4. **성능 측정:**
```bash
# 서버 상태 확인
./venv/bin/streamlit run app/app.py --logger.level=debug 2>&1 | grep "duration"
```

---

### 25. 문서 작성하기

**목적:** 새 기능에 대한 문서 작성하기

**단계:**

1. **문서 파일 생성:**
```bash
# 기능 가이드
touch Documents/Guides/새기능_가이드.md

# 또는 아키텍처 문서
touch Documents/Architecture/새기능_설계.md
```

2. **문서 작성:**
```markdown
# 새 기능 가이드

## 목적
기능의 목적 설명

## 사용 방법

### 1단계
첫 번째 단계

### 2단계
두 번째 단계

## 예시
코드나 스크린샷 예시

## FAQ
자주 묻는 질문
```

3. **문서 구조:**
```
Documents/
├── Architecture/     # 기술 설계 문서
│   ├── SYSTEM_ARCHITECTURE.md
│   └── 새기능_설계.md
├── Guides/          # 사용 가이드
│   ├── 사용자가이드.md
│   └── 새기능_사용법.md
└── Progress/        # 진행 상황
    └── SESSION_SUMMARY.md
```

4. **문서 커밋:**
```bash
git add Documents/
git commit -m "docs: 새 기능 가이드 추가

- 기능 설명
- 사용 방법
- 예시 코드"
```

---

## 📌 빠른 단축키

| 작업 | 명령어 |
|------|--------|
| 앱 시작 | `./venv/bin/streamlit run app/app.py` |
| 앱 중지 | `Ctrl+C` |
| 포트 초기화 | `lsof -ti :8501 \| xargs kill -9` |
| DB 초기화 | `rm data/roasting_data.db && ./venv/bin/streamlit run app/app.py` |
| 테스트 데이터 | `./venv/bin/python app/test_data.py` |
| Git 커밋 | `git add . && git commit -m "메시지"` |
| 버전 확인 | `cat logs/VERSION` |
| 로그 확인 | `sqlite3 data/roasting_data.db "SELECT * FROM roasting_logs;"` |
| 패키지 목록 | `./venv/bin/pip list` |

---

**마지막 업데이트: 2025-10-27**

