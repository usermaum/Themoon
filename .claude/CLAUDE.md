# CLAUDE.md

Claude Code 프로젝트 지시사항 (한글 기본 설정)

> **버전**: 1.0.0 · **날짜**: 2025-10-24
> **시스템**: The Moon Drip BAR - 로스팅 비용 계산기
> **스택**: Streamlit + SQLite + Plotly + Pandas + NumPy
> **환경**: 프로젝트 격리 Python venv (./venv/)

---

## 🌐 언어 설정 (MANDATORY)

**모든 대화, 설명, 피드백은 한글로 진행합니다.**
- Claude의 모든 응답은 한글로 작성
- 코드 주석과 변수명은 영문 유지
- 오류 메시지와 로그는 원본 유지 (영문)
- 사용자 대면 메시지와 문서는 한글로 작성

---

### 체계적인 접근 방법 순서도
1. Constitution (원칙) - 프로젝트 기본 원칙 설정
2. Specify (명세) - 무엇을 만들지 상세하게 정의 
3. Clarify (명확화) - 불분명한 부분을 질문으로 해소
4. Plan (계획) - 기술 스택과 아키텍처 결정
5. Tasks (작업 분해) - 실행 가능한 단위로 쪼개기 
6. Implement (구현) - 자동으로 코드 생성
7. Analyze (검증) - 명세와 코드 일치 확인

---

## 🎯 Critical Rules

### 1. **Project-Isolated Virtual Environment** (MANDATORY)
```bash
# ✅ ALWAYS use project venv at ./venv/
./venv/bin/python script.py
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true
./venv/bin/pip install package

# ✅ Installation & Verification
./venv/bin/pip list                    # Show installed packages
./venv/bin/pip freeze > requirements.txt  # Export dependencies

# ❌ NEVER use system Python
python script.py          # FORBIDDEN
python3 script.py         # FORBIDDEN
```

### 2. **Environment Setup**
If `./venv/` doesn't exist, initialize it:
```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

---

## 📁 Project Architecture

### High-Level Structure
```
TheMoon_Project/
├── venv/                    # Project-isolated Python environment
│   ├── bin/
│   │   ├── python           # Python 3.12.3
│   │   ├── pip
│   │   └── streamlit
│   └── lib/
│
├── app/                     # Streamlit application core
│   ├── app.py              # Main Streamlit UI (entry point)
│   ├── run_app.py          # Alternative launcher
│   ├── test_data.py        # Test data generation utility
│   └── data/               # Supporting data (optional)
│
├── Data/
│   └── roasting_data.db    # SQLite database (roasting logs & prices)
│
├── Documents/              # Project documentation & references
│   ├── roasting_and_abbrev.mdc    # Roasting terminology
│   └── the_moon.mdc               # Business overview
│
├── run.py                  # Main launcher (entry point)
├── requirements.txt        # Python dependencies (5 core packages)
├── README.md               # User-facing documentation
└── .claude/                # Claude Code instructions
    └── CLAUDE.md           # This file
```

### Core Application Flow
1. **Entry Point**:
   - `./venv/bin/python run.py` - Main launcher
   - `./venv/bin/streamlit run app/app.py` - Direct Streamlit run
2. **Database**: SQLite at `Data/roasting_data.db`
   - Roasting logs (green bean weight, roasted bean weight, costs)
   - Bean prices (cost per kg)
   - Cost settings (roasting cost, labor, electricity, etc.)
3. **Frontend**: Streamlit UI with:
   - Plotly interactive visualizations
   - Multi-tab interface (Home, Roasting Log, Cost Setup, Analysis, Statistics)
4. **Data Processing**: Pandas + NumPy for cost calculations

### Key Modules in app.py
- `init_database()` - Initialize SQLite schema and tables
- Cost calculation formulas for roasting business margins
- Multi-tab Streamlit interface
- Database CRUD operations

---

## 🚀 Common Commands

### Running the Application
```bash
# Method 1: Using main launcher (recommended)
./venv/bin/python run.py

# Method 2: Direct Streamlit
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true

# Access: http://localhost:8501
```

### Creating Test Data
```bash
./venv/bin/python app/test_data.py
```

### Package Management
```bash
# Install new package
./venv/bin/pip install package_name

# Update requirements.txt after installing new packages
./venv/bin/pip freeze > requirements.txt

# List all installed packages
./venv/bin/pip list

# Check specific package
./venv/bin/pip show streamlit
```

### Debugging & Verification
```bash
# Verify environment
./venv/bin/python --version  # Should be 3.12.3
./venv/bin/streamlit --version  # Should be 1.38.0

# Test database connection
./venv/bin/python -c "import sqlite3; conn = sqlite3.connect('Data/roasting_data.db'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"'); print(cursor.fetchall())"

# Run with debug logging
./venv/bin/streamlit run app/app.py --logger.level=debug
```

---

## 🗄️ Database Schema

SQLite database (`Data/roasting_data.db`) contains:

### Tables

#### roasting_logs
- Purpose: Daily roasting records
- Key Columns: id, date, bean_name, bean_code, green_weight_kg, roasted_weight_kg, roasting_loss_rate, bean_cost_per_kg, roasting_cost_per_kg, labor_cost, electricity_cost, misc_cost, notes
- Access: Read/write for daily operations

#### bean_prices
- Purpose: Cost per kg for each bean type
- Key Columns: id, bean_name, price_per_kg, updated_date
- Access: Updated via Streamlit UI

#### cost_settings
- Purpose: Global roasting cost parameters
- Key Columns: id, parameter_name, value, description
- Default Values:
  - roasting_loss_rate: 16.7%
  - roasting_cost_per_kg: 2,000₩
  - labor_cost_per_hour: 15,000₩
  - roasting_time_hours: 2
  - electricity_cost: 5,000₩
  - misc_cost: 3,000₩

### Access Pattern
- All queries use relative path from app.py: `../Data/roasting_data.db`
- Database initialized on startup via `init_database()` if tables don't exist
- Supports concurrent reads, single-threaded writes (Streamlit limitation)

---

## 📊 Data Flow & Cost Calculation

### User Workflow
```
Login/Access → Roasting Log Entry → Price Setup → Cost Calculation → Analysis/Charts
```

### Cost Calculation Formula
```
Total Cost = Green Bean Cost + Roasting Cost + Labor + Electricity + Misc

Green Bean Cost = Weight(kg) × Price per kg
Roasting Cost = Roasted Weight(kg) × Cost per kg
Labor Cost = Hourly Rate × Roasting Hours
Cost per kg = Total Cost ÷ Roasted Weight(kg)

Efficiency = Roasted Weight ÷ Green Weight (accounting for roasting loss ~16.7%)
```

### Data Pipeline
```
User Input (Streamlit Form)
    ↓
Validation (Python)
    ↓
Database Storage (SQLite)
    ↓
Pandas DataFrames
    ↓
NumPy Calculations
    ↓
Plotly Visualization
    ↓
Streamlit Display
```

---

## ⚙️ Dependencies

### Core Packages (from requirements.txt)
| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.38.0 | Web UI framework |
| pandas | 2.2.3 | Data manipulation & analysis |
| numpy | 2.1.3 | Numerical computing |
| plotly | 5.24.1 | Interactive charts & graphs |
| openpyxl | 3.1.5 | Excel file support |

All dependencies are locked in `requirements.txt` and installed in `./venv/`.

---

## 🔧 Development Guidelines

### Adding New Features
1. Always use `./venv/bin/python` or `./venv/bin/streamlit` exclusively
2. Test locally with `./venv/bin/streamlit run app/app.py`
3. For database schema changes: Edit `init_database()` in `app/app.py`
4. After installing new packages: Run `./venv/bin/pip freeze > requirements.txt`
5. Test with sample data: `./venv/bin/python app/test_data.py`

### Database Modifications
- **Schema Changes**: Edit `init_database()` function in `app/app.py`
- **Migrations**: Currently use SQLite `CREATE TABLE IF NOT EXISTS` pattern
- **Backup Location**: `Data/roasting_data.db`
- **Recovery**: Database auto-initializes with empty tables if corrupted

### Streamlit UI Modifications
- Custom CSS is embedded at top of `app.py`
- Page configuration at `app.py` beginning
- Tab structure defines main navigation
- All session state management via Streamlit's built-in `st.session_state`

### Testing Data
```bash
./venv/bin/python app/test_data.py  # Populates with sample roasting records
```

---

## 📈 Key Business Logic

### Bean Categories Managed
- Ethiopia: Yirgacheffe, Momora, Gokehuni, Uraga
- Kenya: AA FAQ, Kirinyaga
- Colombia: Huila
- Guatemala: Antigua
- Brazil: Fazenda Carmo
- Decaf: SDM, SM
- Flavored: Swiss Water

### Cost Calculation Features
- Per-bean cost tracking
- Loss accounting (roasting reduces weight ~16.7%)
- Multi-factor cost aggregation
- Real-time margin analysis
- Historical trend analysis via charts

---

## ✅ Current Status (2025-10-24)

### Environment Setup
- ✅ Project-isolated venv at ./venv/ with Python 3.12.3
- ✅ 5 core packages installed (Streamlit, Pandas, NumPy, Plotly, OpenPyXL)
- ✅ Database schema initialized and verified
- ✅ Documentation complete

### Project Files
- ✅ app/app.py - Main Streamlit application
- ✅ app/test_data.py - Test data generation utility
- ✅ app/run_app.py - Alternative launcher
- ✅ run.py - Main launcher script
- ✅ Data/roasting_data.db - SQLite database
- ✅ Documents/ - Project documentation
- ✅ requirements.txt - Dependency list

---

## 📦 버전 관리 시스템 (Version Management)

### 개요
프로젝트의 모든 변경사항을 자동으로 추적하고 버전을 관리합니다.
**Semantic Versioning (SemVer)** 규칙: `MAJOR.MINOR.PATCH`

### 파일 구조
```
logs/                          # 버전 관리 폴더
├── VERSION                    # 현재 버전 (예: 0.1.2)
├── CHANGELOG.md              # 변경 이력 (자동 생성)
├── update_version.py         # 버전 관리 스크립트
├── VERSION_MANAGEMENT.md     # 상세 가이드
└── QUICK_START.md            # 빠른 시작 가이드

.git/hooks/
└── post-commit               # Git 훅 (자동 실행)
```

### 🚀 자동 버전 관리 (권장)

Git 커밋 메시지 규칙에 따라 자동으로 버전이 업데이트됩니다:

#### 1️⃣ 버그 수정 (PATCH: 0.1.0 → 0.1.1)
```bash
git commit -m "fix: 버그 설명"
git commit -m "🐛 버그 설명"
```
**자동 실행:** `logs/VERSION` 업데이트, `logs/CHANGELOG.md` 추가

#### 2️⃣ 새 기능 (MINOR: 0.1.0 → 0.2.0)
```bash
git commit -m "feat: 기능 설명"
git commit -m "✨ 기능 설명"
```
**자동 실행:** `logs/VERSION` 업데이트, `logs/CHANGELOG.md` 추가

#### 3️⃣ 호환성 변경 (MAJOR: 0.1.0 → 1.0.0)
```bash
git commit -m "🚀 설명"
git commit -m "BREAKING CHANGE: 설명"
```
**자동 실행:** `logs/VERSION` 업데이트, `logs/CHANGELOG.md` 추가

### 🔧 수동 버전 관리

자동화가 필요 없을 때 또는 테스트 목적:
```bash
# 현재 버전 확인
python3 logs/update_version.py --show

# 패치 버전 업데이트
python3 logs/update_version.py --type patch --summary "버그 설명"

# 마이너 버전 업데이트
python3 logs/update_version.py --type minor --summary "기능 설명"

# 메이저 버전 업데이트
python3 logs/update_version.py --type major --summary "주요 변경"

# 상세 변경사항 포함
python3 logs/update_version.py \
  --type patch \
  --summary "설명" \
  --changes "
- 변경사항 1
- 변경사항 2
- 변경사항 3
  "
```

### 📋 파일 설명

#### `logs/VERSION`
- 현재 프로젝트 버전을 저장하는 텍스트 파일
- 형식: `MAJOR.MINOR.PATCH` (예: 0.1.2)
- 자동으로 업데이트됨

#### `logs/CHANGELOG.md`
- 모든 버전의 변경사항을 기록
- 마크다운 형식으로 자동 생성
- 버전별로 추가/수정/개선사항 분류

#### `logs/update_version.py`
- Python 스크립트로 버전 자동 관리
- 버전 파싱, 증가, 파일 업데이트 기능
- 자동 실행 (post-commit 훅 사용) 또는 수동 실행 가능

#### `logs/VERSION_MANAGEMENT.md`
- 버전 관리 시스템의 상세 가이드
- 사용 방법, 예제, 베스트 프랙티스 포함

#### `logs/QUICK_START.md`
- 빠른 시작을 위한 간단한 가이드
- Git 커밋 메시지 규칙과 예제

#### `.git/hooks/post-commit`
- Git 커밋 후 자동으로 실행되는 훅
- 커밋 메시지 분석 후 버전 자동 업데이트
- 수정 불필요 (이미 설정됨)

### 📊 버전 관리 방식

| 변경 유형 | 버전 증가 | 키워드 | 예시 |
|---------|---------|--------|------|
| 버그 수정 | PATCH | `fix:`, `🐛` | 0.1.0 → 0.1.1 |
| 새 기능 | MINOR | `feat:`, `✨` | 0.1.0 → 0.2.0 |
| 호환성 변경 | MAJOR | `🚀`, `BREAKING` | 0.1.0 → 1.0.0 |

### 💡 팁

1. **매 커밋마다 자동으로 관리됨** - 수동 작업 불필요
2. **커밋 메시지 규칙 준수** - 규칙이 맞아야 자동 감지됨
3. **CHANGELOG 자동 생성** - 변경사항이 자동으로 기록됨
4. **언제든 현재 버전 확인** - `python3 logs/update_version.py --show`
5. **다른 프로젝트에 복사 가능** - logs 폴더와 .git/hooks/post-commit 만 복사하면 됨

---

## ⚠️ Important Notes

### Path References
- Database path uses relative `../Data/` reference from `app/app.py`
- Ensure scripts run from project root or adjust paths accordingly
- Use absolute paths for robustness if needed

### Version Constraints
- Python 3.12.3 required (in venv)
- Streamlit 1.38.0 pinned for stability
- Do not upgrade without testing

### Development Workflow
- Never use system Python directly
- Always activate project venv: `./venv/bin/`
- Update requirements.txt after adding packages
- Test with sample data before production use
