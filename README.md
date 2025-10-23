# ☕ 더문 로스팅 원가 계산기

**The Moon Drip BAR - Roasting Cost Calculator**

프리미엄 스페셜티 커피 로스팅 사업을 위한 원가 분석 및 수익성 계산 시스템

---

## 🎯 주요 기능

### 📊 원가 관리
- **로스팅 기록 관리**: 일일 로스팅 데이터 저장 및 추적
- **원두 비용 관리**: 원두 종류별 원가 설정 및 관리
- **비용 설정 커스터마이징**: 로스팅, 인건비, 전기료 등 상세 설정

### 💰 원가 계산
- **실시간 원가 계산**: 자동 비용 계산 및 분석
- **손실율 반영**: 로스팅 손실(약 16.7%) 자동 계산
- **마진 분석**: 수익성 분석 및 비교

### 📈 데이터 분석
- **Plotly 기반 시각화**: 인터랙티브 차트 및 그래프
- **로스팅량 추적**: 원두별 로스팅 통계
- **비용 추이 분석**: 시간대별 비용 변화 추적

---

## 🏗️ 기술 스택

| 항목 | 기술 |
|------|------|
| **Frontend** | Streamlit 1.38.0 |
| **Database** | SQLite 3.x |
| **Data Processing** | Pandas 2.2.3, NumPy 2.1.3 |
| **Visualization** | Plotly 5.24.1 |
| **Excel Support** | OpenPyXL 3.1.5 |
| **Runtime** | Python 3.12.3 |

---

## 📁 프로젝트 구조

```
TheMoon_Project/
├── venv/                          # 프로젝트 격리 Python 환경 (3.12.3)
│
├── app/                           # Streamlit 애플리케이션
│   ├── app.py                     # 메인 애플리케이션 (Streamlit UI)
│   ├── run_app.py                 # 대체 런처
│   ├── test_data.py               # 테스트 데이터 생성 유틸
│   └── data/                      # 옵션: 추가 데이터
│
├── Data/                          # 데이터 저장소
│   └── roasting_data.db           # SQLite 데이터베이스
│       ├── roasting_logs 테이블   # 로스팅 기록
│       ├── bean_prices 테이블     # 원두 가격
│       └── cost_settings 테이블   # 비용 설정
│
├── Documents/                     # 프로젝트 문서
│   ├── roasting_and_abbrev.mdc    # 로스팅 용어 정리
│   └── the_moon.mdc               # 사업 개요
│
├── run.py                         # 메인 런처 스크립트
├── requirements.txt               # Python 패키지 의존성
├── README.md                      # 이 파일
└── .claude/                       # Claude Code 가이드
    └── CLAUDE.md                  # 개발 규칙 및 아키텍처
```

---

## 🚀 설치 및 실행

### 1단계: 프로젝트 클론
```bash
git clone git@github.com:usermaum/Project.git TheMoon_Project
cd TheMoon_Project
```

### 2단계: 가상환경 설정
```bash
# 이미 설정된 venv가 있다면 그대로 사용
# 없다면 생성:
python3 -m venv venv
```

### 3단계: 의존성 설치
```bash
# 프로젝트 격리 Python 사용
./venv/bin/pip install -r requirements.txt

# 또는 시스템 Python 사용
pip install -r requirements.txt
```

### 4단계: 애플리케이션 실행

**방법 1: 메인 런처 (권장)**
```bash
./venv/bin/python run.py
```

**방법 2: Streamlit 직접 실행**
```bash
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true
```

### 5단계: 브라우저 접속
```
http://localhost:8501
```

---

## 📖 사용 가이드

### 테스트 데이터 생성
```bash
# 샘플 로스팅 데이터 생성
./venv/bin/python app/test_data.py
```

### 패키지 관리
```bash
# 새 패키지 설치
./venv/bin/pip install package_name

# 설치된 패키지 목록 확인
./venv/bin/pip list

# requirements.txt 업데이트
./venv/bin/pip freeze > requirements.txt
```

### 데이터베이스 확인
```bash
# SQLite 데이터베이스 직접 확인
./venv/bin/python -c "
import sqlite3
conn = sqlite3.connect('Data/roasting_data.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
print(cursor.fetchall())
conn.close()
"
```

---

## 🗄️ 데이터베이스 스키마

### roasting_logs 테이블
로스팅 기록을 저장합니다.

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | 고유 ID (자동증가) |
| date | TEXT | 로스팅 날짜 |
| bean_name | TEXT | 원두 이름 |
| green_weight_kg | REAL | 생두 무게 (kg) |
| roasted_weight_kg | REAL | 로스팅 후 무게 (kg) |
| bean_cost_per_kg | REAL | 원두 비용 (₩/kg) |
| roasting_cost_per_kg | REAL | 로스팅 비용 (₩/kg) |
| labor_cost | REAL | 인건비 (₩) |
| electricity_cost | REAL | 전기료 (₩) |
| misc_cost | REAL | 기타 비용 (₩) |
| notes | TEXT | 메모 |

### bean_prices 테이블
원두 종류별 가격을 관리합니다.

| 컬럼 | 설명 |
|------|------|
| id | 고유 ID |
| bean_name | 원두 이름 (유일) |
| price_per_kg | 킬로그램당 가격 (₩) |
| updated_date | 업데이트 날짜 |

### cost_settings 테이블
전역 비용 설정을 관리합니다.

| 파라미터 | 기본값 | 설명 |
|---------|-------|------|
| roasting_loss_rate | 16.7% | 로스팅 손실률 |
| roasting_cost_per_kg | 2,000₩ | 킬로그램당 로스팅 비용 |
| labor_cost_per_hour | 15,000₩ | 시간당 인건비 |
| roasting_time_hours | 2시간 | 로스팅 소요 시간 |
| electricity_cost | 5,000₩ | 전기료 |
| misc_cost | 3,000₩ | 기타 비용 |

---

## 💡 원가 계산 공식

```
총 비용 = 원두 비용 + 로스팅 비용 + 인건비 + 전기료 + 기타 비용

원두 비용 = 생두 무게(kg) × 원두 비용(₩/kg)
로스팅 비용 = 로스팅 후 무게(kg) × 킬로그램당 로스팅 비용(₩)
인건비 = 시간당 인건비 × 로스팅 소요 시간

킬로그램당 원가 = 총 비용 ÷ 로스팅 후 무게(kg)
수익률(%) = (판매가 - 원가) / 판매가 × 100
```

---

## 🎯 주요 페이지 설명

### 홈 (Home)
- 프로젝트 소개
- 주요 통계 (총 로스팅 건수, 평균 원가, 총 로스팅량)

### 로스팅 기록 (Roasting Log)
- 새로운 로스팅 기록 추가
- 원두 이름, 무게, 비용 입력
- 자동 비용 계산

### 원가 설정 (Cost Setup)
- 비용 파라미터 커스터마이징
- 로스팅 비용, 인건비 등 조정

### 분석 (Analysis)
- 로스팅 데이터 분석 (추후 추가)
- 비용 비교 분석
- Plotly 시각화

### 통계 (Statistics)
- 종합 통계 보고서 (추후 추가)
- 시계열 데이터 분석
- 원두별 비용 비교

---

## 🌙 더문의 원두 상품군

### 아프리카 (Africa)
- 에티오피아: Yirgacheffe, Momora, Gokehuni, Uraga
- 케냐: AA FAQ, Kirinyaga

### 남미 (Americas)
- 콜롬비아: Huila
- 과테말라: Antigua
- 브라질: Fazenda Carmo

### 특별 상품
- Decaf: SDM, SM
- Flavored: Swiss Water

---

## 🔧 개발 가이드

### 새 기능 추가
1. `.claude/CLAUDE.md` 참조하여 프로젝트 규칙 확인
2. `./venv/bin/python` 또는 `./venv/bin/streamlit` 사용
3. 로컬에서 `./venv/bin/streamlit run app/app.py` 테스트
4. 패키지 추가 후 `./venv/bin/pip freeze > requirements.txt` 실행

### 데이터베이스 수정
- 스키마 변경: `app/app.py`의 `init_database()` 함수 수정
- 마이그레이션: 현재 SQLite `CREATE TABLE IF NOT EXISTS` 패턴 사용
- 백업: `Data/roasting_data.db`

### Git 워크플로우
```bash
# 변경사항 커밋
git add .
git commit -m "설명: 기능설명"

# 원격 저장소에 푸시
git push origin main
```

---

## 📚 참고 문서

- **CLAUDE.md**: 개발 가이드 및 아키텍처 (.claude/CLAUDE.md)
- **Documents/the_moon.mdc**: 사업 개요
- **Documents/roasting_and_abbrev.mdc**: 로스팅 용어 정리

---

## 📊 프로젝트 정보

- **프로젝트명**: The Moon Drip BAR - Roasting Cost Calculator
- **버전**: 1.0.0
- **마지막 업데이트**: 2025-10-24
- **라이선스**: MIT
- **저장소**: git@github.com:usermaum/Project.git

---

## 🤝 기여 가이드

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📧 문의

- **개발자**: usermaum
- **이메일**: usermaum@gmail.com
- **GitHub**: https://github.com/usermaum

---

**☕ The Moon Drip BAR | Made with Streamlit & SQLite**
