# 🌙 더문(TheMoon) 프로젝트 구성 가이드

**The Moon Drip BAR - Roasting Cost Calculator**

이 문서는 처음부터 TheMoon 프로젝트를 완전히 동일하게 재구성하는 방법을 설명합니다.

---

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [사전 요구사항](#사전-요구사항)
3. [전체 구성 절차](#전체-구성-절차)
4. [디렉토리 구조](#디렉토리-구조)
5. [파일 설정 상세](#파일-설정-상세)
6. [Git 설정](#git-설정)
7. [검증 절차](#검증-절차)
8. [문제 해결](#문제-해결)

---

## 프로젝트 개요

| 항목 | 값 |
|------|-----|
| 프로젝트명 | The Moon Drip BAR - Roasting Cost Calculator |
| 버전 | 1.0.0 |
| 타입 | Streamlit 웹 애플리케이션 |
| Python | 3.12.3 |
| 주요 프레임워크 | Streamlit, SQLite, Pandas, NumPy, Plotly |
| 저장소 | git@github.com:usermaum/Project.git |
| 마지막 업데이트 | 2025-10-24 |

---

## 사전 요구사항

### 시스템 요구사항
- **OS**: Windows, macOS, Linux (WSL 포함)
- **Python**: 3.12.3 이상
- **Git**: 2.0 이상
- **디스크 공간**: 최소 500MB

### 필수 설치 소프트웨어
```bash
# Python 버전 확인
python3 --version  # 3.12.3 이상

# Git 버전 확인
git --version      # 2.0 이상
```

### GitHub SSH 설정 (선택사항)
SSH로 저장소를 클론하려면 GitHub에 SSH 키를 등록해야 합니다.

```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your.email@example.com"

# SSH 키 확인
cat ~/.ssh/id_ed25519.pub
# GitHub Settings > SSH and GPG keys 에 등록
```

---

## 전체 구성 절차

### 1단계: 프로젝트 디렉토리 생성 및 클론

```bash
# 프로젝트 디렉토리 생성
mkdir -p ~/projects
cd ~/projects

# GitHub 저장소에서 클론 (SSH 사용)
git clone git@github.com:usermaum/Project.git TheMoon_Project

# 또는 HTTPS 사용
git clone https://github.com/usermaum/Project.git TheMoon_Project

# 프로젝트 디렉토리로 이동
cd TheMoon_Project
```

### 2단계: Python 가상환경 설정

```bash
# 프로젝트 격리 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (Linux/macOS/WSL)
source venv/bin/activate

# 가상환경 활성화 (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 가상환경 활성화 (Windows CMD)
venv\Scripts\activate.bat
```

### 3단계: Python 패키지 설치

```bash
# pip 최신 버전으로 업그레이드
python -m pip install --upgrade pip setuptools wheel

# requirements.txt에서 패키지 설치
pip install -r requirements.txt

# 설치 확인
pip list
```

**설치되어야 할 패키지:**
- streamlit==1.38.0
- pandas==2.2.3
- numpy==2.1.3
- plotly==5.24.1
- openpyxl==3.1.5

### 4단계: SQLite 데이터베이스 초기화

```bash
# Python 스크립트로 데이터베이스 자동 생성
# (app.py 실행 시 자동으로 생성되지만, 수동으로 생성할 수도 있음)

python << 'EOF'
import sqlite3
import os

db_path = 'Data/roasting_data.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# roasting_logs 테이블
cursor.execute('''
    CREATE TABLE IF NOT EXISTS roasting_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        bean_name TEXT NOT NULL,
        bean_code TEXT,
        green_weight_kg REAL NOT NULL,
        roasted_weight_kg REAL NOT NULL,
        roasting_loss_rate REAL DEFAULT 16.7,
        bean_cost_per_kg REAL NOT NULL,
        roasting_cost_per_kg REAL DEFAULT 2000,
        labor_cost REAL DEFAULT 15000,
        electricity_cost REAL DEFAULT 5000,
        misc_cost REAL DEFAULT 3000,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# bean_prices 테이블
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bean_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bean_name TEXT UNIQUE NOT NULL,
        price_per_kg REAL NOT NULL,
        updated_date TEXT DEFAULT CURRENT_DATE
    )
''')

# cost_settings 테이블
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cost_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parameter_name TEXT UNIQUE NOT NULL,
        value REAL NOT NULL,
        description TEXT
    )
''')

# 기본값 설정 삽입
default_settings = [
    ('roasting_loss_rate', 16.7, '로스팅 손실률 (%)'),
    ('roasting_cost_per_kg', 2000, '킬로그램당 로스팅 비용 (₩)'),
    ('labor_cost_per_hour', 15000, '시간당 인건비 (₩)'),
    ('roasting_time_hours', 2, '로스팅 시간 (시간)'),
    ('electricity_cost', 5000, '전기료 (₩)'),
    ('misc_cost', 3000, '기타 비용 (₩)'),
]

for param_name, value, description in default_settings:
    cursor.execute('''
        INSERT OR IGNORE INTO cost_settings (parameter_name, value, description)
        VALUES (?, ?, ?)
    ''', (param_name, value, description))

conn.commit()
conn.close()
print('✅ Database initialized successfully')
EOF
```

### 5단계: 애플리케이션 실행 및 테스트

```bash
# Streamlit 애플리케이션 실행
streamlit run app/app.py --server.port 8501

# 또는 메인 런처 사용
python run.py
```

**예상 출력:**
```
  You can now view your Streamlit app in your browser.

  URL: http://localhost:8501
```

---

## 디렉토리 구조

최종 프로젝트의 완전한 디렉토리 구조:

```
TheMoon_Project/
│
├── venv/                              # ✅ Python 가상환경
│   ├── bin/                           # 실행 파일 (Linux/macOS)
│   │   ├── python
│   │   ├── pip
│   │   └── streamlit
│   ├── lib/
│   │   └── python3.12/
│   │       └── site-packages/         # 설치된 패키지
│   └── pyvenv.cfg
│
├── app/                               # ✅ Streamlit 애플리케이션
│   ├── app.py                         # 메인 UI (약 340줄)
│   │   ├── init_database()            # DB 초기화
│   │   ├── get_db_connection()        # DB 연결
│   │   └── [Multi-tab Streamlit UI]   # 5개 탭
│   ├── run_app.py                     # 대체 런처
│   ├── test_data.py                   # 테스트 데이터 생성
│   └── data/                          # 선택적 추가 데이터
│
├── Data/                              # ✅ 데이터 저장소
│   └── roasting_data.db               # SQLite DB (28KB)
│       ├── roasting_logs              # 로스팅 기록
│       ├── bean_prices                # 원두 가격
│       └── cost_settings              # 비용 설정 (6개 기본값)
│
├── Documents/                         # ✅ 프로젝트 문서
│   ├── roasting_and_abbrev.mdc        # 로스팅 용어 정리
│   └── the_moon.mdc                   # 사업 개요
│
├── .claude/                           # ✅ Claude Code 설정
│   ├── CLAUDE.md                      # 개발 가이드 (310줄)
│   ├── ARCHITECTURE.md
│   ├── TECHNICAL_ANALYSIS_REPORT.md
│   ├── instructions.md
│   ├── components.mdc
│   ├── mcpServers.json
│   ├── settings.local.json
│   ├── theme.JSON
│   └── 문서.mdc
│
├── .git/                              # ✅ Git 저장소
│   ├── config                         # 로컬 git 설정
│   ├── HEAD
│   ├── objects/
│   ├── refs/
│   └── [Git metadata]
│
├── .gitignore                         # Git 무시 파일
├── run.py                             # 메인 런처 (30줄)
├── requirements.txt                   # 패키지 의존성 (5줄)
├── README.md                          # 프로젝트 문서 (313줄)
└── PROJECT_SETUP_GUIDE.md             # 이 파일
```

---

## 파일 설정 상세

### 1. requirements.txt

**위치**: `/TheMoon_Project/requirements.txt`

```
# The Moon Drip BAR - Roasting Cost Calculator
# 더문 드립바 로스팅 원가 계산기 의존성

# Core
streamlit==1.38.0
pandas==2.2.3
numpy==2.1.3

# Visualization
plotly==5.24.1

# Utilities
openpyxl==3.1.5
```

**확인 방법:**
```bash
pip list | grep -E 'streamlit|pandas|numpy|plotly|openpyxl'
```

### 2. app/app.py

**위치**: `/TheMoon_Project/app/app.py`

**핵심 함수:**
- `init_database()`: SQLite 테이블 생성 및 초기화
- `get_db_connection()`: DB 연결 풀
- Main Streamlit UI: 5개 탭 인터페이스
  - 홈 (Home)
  - 로스팅 기록 (Roasting Log)
  - 원가 설정 (Cost Setup)
  - 분석 (Analysis)
  - 통계 (Statistics)

**크기**: 약 340줄

### 3. app/test_data.py

**위치**: `/TheMoon_Project/app/test_data.py`

**기능**: 샘플 로스팅 데이터 생성
- 5종류의 원두 가격 설정
- 6주간의 샘플 로스팅 기록 생성

**사용:**
```bash
python app/test_data.py
```

### 4. app/run_app.py

**위치**: `/TheMoon_Project/app/run_app.py`

**기능**: Streamlit 애플리케이션 실행

### 5. run.py

**위치**: `/TheMoon_Project/run.py`

**기능**: 메인 런처 스크립트
- 환경 초기화
- Streamlit 애플리케이션 실행

**사용:**
```bash
python run.py
# 또는
./venv/bin/python run.py
```

### 6. .claude/CLAUDE.md

**위치**: `/TheMoon_Project/.claude/CLAUDE.md`

**내용**:
- 프로젝트 아키텍처
- 개발 규칙
- 명령어 가이드
- 데이터베이스 스키마
- 비용 계산 공식

**크기**: 약 310줄

### 7. README.md

**위치**: `/TheMoon_Project/README.md`

**내용**:
- 프로젝트 개요
- 기술 스택
- 설치 및 실행 방법
- 데이터베이스 스키마
- 기여 가이드

**크기**: 약 313줄

---

## Git 설정

### 초기 Git 설정 (로컬)

```bash
# 프로젝트 디렉토리에서 로컬 git 설정
cd TheMoon_Project

# 사용자 정보 설정 (로컬)
git config user.name "your-name"
git config user.email "your.email@example.com"

# 설정 확인
git config --local user.name
git config --local user.email

# 원격 저장소 추가 (이미 clone했으면 자동 설정됨)
git remote add origin git@github.com:usermaum/Project.git
```

### Git 기본 워크플로우

```bash
# 변경사항 확인
git status

# 변경사항 스테이징
git add <filename>    # 특정 파일
git add .             # 모든 파일

# 커밋
git commit -m "commit message"

# 원격 저장소에 푸시
git push origin main

# 최신 코드 가져오기
git pull origin main
```

### 첫 번째 커밋 예시

```bash
# 모든 파일 스테이징
git add .

# 초기 커밋
git commit -m "Initial commit: TheMoon Drip BAR - Roasting Cost Calculator v1.0.0"

# 원격 저장소에 푸시
git push -u origin main
```

---

## 검증 절차

### 1. 환경 확인

```bash
# Python 버전 확인
python --version
# 출력: Python 3.12.3 (또는 그 이상)

# 가상환경 활성화 확인
which python  # Linux/macOS
# 출력: /path/to/TheMoon_Project/venv/bin/python
```

### 2. 패키지 설치 확인

```bash
# 필수 패키지 확인
pip list | grep -E 'streamlit|pandas|numpy|plotly|openpyxl'

# 출력 예시:
# numpy                    2.1.3
# openpyxl                 3.1.5
# pandas                   2.2.3
# plotly                   5.24.1
# streamlit                1.38.0
```

### 3. 데이터베이스 확인

```bash
# SQLite 데이터베이스 테이블 확인
python << 'EOF'
import sqlite3
conn = sqlite3.connect('Data/roasting_data.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables:", [t[0] for t in tables])

# cost_settings 확인
cursor.execute("SELECT parameter_name, value FROM cost_settings")
settings = cursor.fetchall()
print("\nDefault Settings:")
for param, value in settings:
    print(f"  - {param}: {value}")
conn.close()
EOF

# 출력 예시:
# Tables: ['roasting_logs', 'sqlite_sequence', 'bean_prices', 'cost_settings']
# Default Settings:
#   - roasting_loss_rate: 16.7
#   - roasting_cost_per_kg: 2000.0
#   - labor_cost_per_hour: 15000.0
#   - roasting_time_hours: 2.0
#   - electricity_cost: 5000.0
#   - misc_cost: 3000.0
```

### 4. 애플리케이션 실행 확인

```bash
# Streamlit 애플리케이션 실행
streamlit run app/app.py

# 또는
python run.py

# 출력 예시:
# You can now view your Streamlit app in your browser.
# URL: http://localhost:8501
```

**브라우저에서 확인:**
- URL: `http://localhost:8501` 접속
- 홈 페이지 표시 확인
- 네비게이션 메뉴 (홈, 로스팅 기록, 원가 설정, 분석, 통계) 표시 확인

---

## 문제 해결

### 문제: 가상환경 활성화 안 됨

**증상:**
```
command not found: venv
```

**해결:**
```bash
# WSL/Linux/macOS
source venv/bin/activate

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

### 문제: 패키지 설치 실패

**증상:**
```
ERROR: Could not find a version that satisfies the requirement
```

**해결:**
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 캐시 초기화
pip install --no-cache-dir -r requirements.txt
```

### 문제: SQLite 데이터베이스 파일 없음

**증상:**
```
FileNotFoundError: Data/roasting_data.db
```

**해결:**
```bash
# 데이터베이스 디렉토리 생성
mkdir -p Data

# 데이터베이스 초기화 (위의 4단계 참조)
python << 'EOF'
import sqlite3
import os
os.makedirs('Data', exist_ok=True)
conn = sqlite3.connect('Data/roasting_data.db')
# ... (테이블 생성 코드)
EOF
```

### 문제: Streamlit 포트 충돌

**증상:**
```
Address already in use
```

**해결:**
```bash
# 다른 포트 사용
streamlit run app/app.py --server.port 8502

# 또는 기존 프로세스 종료
lsof -ti :8501 | xargs kill -9  # Linux/macOS
netstat -ano | findstr :8501     # Windows
```

### 문제: Git SSH 연결 실패

**증상:**
```
Permission denied (publickey)
```

**해결:**
```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your.email@example.com"

# SSH 키 확인
cat ~/.ssh/id_ed25519.pub

# GitHub에 키 등록
# https://github.com/settings/ssh/new
```

---

## 다른 개발자를 위한 빠른 시작

```bash
# 1. 저장소 클론
git clone git@github.com:usermaum/Project.git TheMoon_Project
cd TheMoon_Project

# 2. 가상환경 설정
python3 -m venv venv
source venv/bin/activate  # Linux/macOS/WSL
# .\venv\Scripts\Activate.ps1  # Windows

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 애플리케이션 실행
streamlit run app/app.py

# 5. 브라우저에서 http://localhost:8501 접속
```

---

## 환경 정보 스냅샷

이 가이드 작성 기준의 환경:

| 항목 | 버전 |
|------|------|
| Python | 3.12.3 |
| Streamlit | 1.38.0 |
| Pandas | 2.2.3 |
| NumPy | 2.1.3 |
| Plotly | 5.24.1 |
| OpenPyXL | 3.1.5 |
| SQLite | 3.x |
| Git | 2.0+ |
| OS | Linux/macOS/Windows (WSL) |

---

## 참고 자료

- **Streamlit 문서**: https://docs.streamlit.io
- **Pandas 문서**: https://pandas.pydata.org/docs
- **SQLite 문서**: https://www.sqlite.org/docs.html
- **Python venv**: https://docs.python.org/3/library/venv.html
- **Git 가이드**: https://git-scm.com/book

---

## 최종 검사 리스트

프로젝트 구성이 완료되었는지 확인하세요:

- [ ] Python 3.12.3 이상 설치됨
- [ ] Git 2.0 이상 설치됨
- [ ] 저장소 클론됨
- [ ] 가상환경 생성됨
- [ ] 가상환경 활성화됨
- [ ] requirements.txt에서 패키지 설치됨
- [ ] Data/roasting_data.db 파일 존재함
- [ ] app/app.py 파일 존재함
- [ ] Streamlit 실행 시 http://localhost:8501 접근 가능함
- [ ] Git 로컬 설정 완료됨
- [ ] .claude/CLAUDE.md 파일 존재함

모든 항목이 확인되었다면 프로젝트 구성이 완료된 것입니다! ✅

---

**Last Updated**: 2025-10-24
**Created by**: Claude Code
**Version**: 1.0.0
