# TheMoon Roasting Cost Calculator

> **v0.50.2** | 커피 로스팅 비용 계산 및 재고 관리 시스템

[![Python](https://img.shields.io/badge/Python-3.12.3-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.0-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 목차 (Table of Contents)

- [프로젝트 개요](#-프로젝트-개요)
- [아키텍처](#-아키텍처)
- [마이그레이션 진행 상황](#-마이그레이션-진행-상황)
- [빠른 시작](#-빠른-시작)
- [기능 목록](#-기능-목록)
- [프로젝트 구조](#-프로젝트-구조)
- [기술 스택](#-기술-스택)
- [개발 가이드](#-개발-가이드)
- [API 문서](#-api-문서)
- [테스트](#-테스트)
- [배포](#-배포)
- [기여하기](#-기여하기)
- [라이선스](#-라이선스)

---

## 🎯 프로젝트 개요

**TheMoon Roasting Cost Calculator**는 커피 로스팅 업체를 위한 **비용 계산 및 재고 관리 시스템**입니다.

### 핵심 기능

- ☕ **원두 관리** - 생두 정보, 가격, 로스팅 레벨 관리
- 🧪 **블렌드 관리** - 블렌드 레시피 및 원가 계산
- 📦 **재고 관리** - 실시간 재고 추적 및 입출고 관리
- 📊 **로스팅 기록** - 로스팅 로그 및 손실률 분석
- 💰 **비용 계산** - 정확한 원가 계산 및 가격 제안
- 📈 **분석 및 리포트** - 손실률, 비용 추이, 재고 분석
- 🖼️ **OCR 송장 처리** - AI 기반 송장 자동 인식 (Gemini/Claude)

### 프로젝트 현황

현재 프로젝트는 **Streamlit**에서 **Next.js + FastAPI** 아키텍처로의 마이그레이션이 진행 중입니다.

- ✅ **기존 시스템** (Production): Streamlit 기반 - 완전 동작
- 🚧 **신규 시스템** (Development): Next.js + FastAPI - Phase 1 진행 중

---

## 🏗️ 아키텍처

### 현재 아키텍처 (Streamlit)

```
┌─────────────────────────────────────────┐
│         Streamlit Application           │
│  ┌───────────────────────────────────┐  │
│  │  UI Pages (14 pages)              │  │
│  │  - Dashboard, BeanManagement,     │  │
│  │  - BlendManagement, CostCalc,     │  │
│  │  - InventoryManagement, etc.      │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │  Services (12 services)           │  │
│  │  - BeanService, BlendService,     │  │
│  │  - InventoryService, etc.         │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │  SQLAlchemy Models                │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                  ↓
         ┌─────────────────┐
         │  SQLite Database │
         └─────────────────┘
```

### 목표 아키텍처 (Next.js + FastAPI)

```
┌────────────────────────────────────────────────────┐
│              Next.js Frontend (Port 3000)          │
│  ┌──────────────────────────────────────────────┐  │
│  │  Pages: Dashboard, Beans, Blends, etc.      │  │
│  │  Components: UI Components (shadcn/ui)      │  │
│  │  Hooks: useWebSocket, API hooks             │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
                       ↓ (REST API + WebSocket)
┌────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)           │
│  ┌──────────────────────────────────────────────┐  │
│  │  API v1 Endpoints                            │  │
│  │  - /auth, /beans, /blends, /inventory        │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Business Logic Services                     │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  SQLAlchemy Models + Pydantic Schemas        │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
         ↓                              ↓
┌─────────────────┐         ┌─────────────────────┐
│   PostgreSQL    │         │  Redis + Celery     │
│   (Port 5432)   │         │  (Async Tasks)      │
└─────────────────┘         └─────────────────────┘
```

---

## 🚧 마이그레이션 진행 상황

### Phase 1: 기반 구축 및 백엔드 API화 (진행 중 - 70%)

#### ✅ 완료된 작업

- [x] **인프라 구성**
  - Docker Compose 설정 (PostgreSQL, Redis)
  - FastAPI 프로젝트 구조 생성

- [x] **데이터베이스**
  - SQLAlchemy 모델 정의 (8개 모델)
    - Bean, BeanPriceHistory
    - Blend, BlendRecipe, BlendRecipesHistory
    - Inventory
    - Transaction, RoastingLog, LossRateWarning
    - User, UserPermission, AuditLog
    - Invoice, InvoiceItem, InvoiceLearning
    - CostSetting
  - Alembic 마이그레이션 설정
  - DB 마이그레이션 스크립트 (`scripts/migrate_db.py`)

- [x] **API 개발**
  - 인증/인가 (JWT 기반 로그인) - `/api/v1/login/access-token`
  - 원두(Beans) CRUD API - `/api/v1/beans/`
  - 블렌드(Blends) CRUD API - `/api/v1/blends/`
  - 재고(Inventory) API - `/api/v1/inventory/`
  - WebSocket 엔드포인트 - `/api/v1/ws`

- [x] **프론트엔드 초기 구축**
  - Next.js 14 + TypeScript 프로젝트 생성
  - Tailwind CSS + shadcn/ui 설정
  - 기본 페이지 구조 (Home, Dashboard, Beans, Blends)
  - API 클라이언트 모듈 (`lib/api.ts`)
  - WebSocket 훅 (`lib/hooks/useWebSocket.ts`)

- [x] **실행 스크립트**
  - `run_backend.sh` - 백엔드 자동 실행 스크립트
  - `run_frontend.sh` - 프론트엔드 자동 실행 스크립트

#### 🚧 진행 중인 작업

- [ ] Pydantic 스키마 완성
- [ ] 비즈니스 로직 서비스 이식
- [ ] 단위 테스트 작성 (Pytest)
- [ ] API 문서화 (Swagger UI 보강)

#### 📝 남은 작업

- [ ] Celery + Redis 비동기 작업 큐 설정
- [ ] OCR 처리 로직 API화
- [ ] 데이터 이관 스크립트 완성 및 실행

### Phase 2: 프론트엔드 전환 (대기 중)

- [ ] 주요 페이지 완성 (Dashboard, Beans, Blends, Inventory)
- [ ] API 연동 완료
- [ ] 하이브리드 운영 (Streamlit + Next.js 병행)

### Phase 3: 고도화 (계획 중)

- [ ] 실시간 알림 (WebSocket)
- [ ] PWA 적용 (모바일 최적화)
- [ ] 성능 최적화

### Phase 4: 완료 (계획 중)

- [ ] 레거시 Streamlit 제거
- [ ] 프로덕션 배포

---

## 🚀 빠른 시작

### 시스템 요구사항

- **Python**: 3.12.3 이상
- **Node.js**: 18.0 이상
- **Docker**: 20.0 이상 (선택사항)
- **PostgreSQL**: 15.0 이상 (Docker로 제공 가능)
- **Redis**: 7.0 이상 (Docker로 제공 가능)

### 옵션 1: Streamlit 앱 실행 (기존 시스템)

```bash
# 1. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. Streamlit 앱 실행
streamlit run app/app.py --server.port 8501 --server.headless true
```

**접속**:

http://localhost:8501

### 옵션 2: Next.js + FastAPI 실행 (신규 시스템)

#### 백엔드 (FastAPI)

```bash
# 1. 인프라 시작 (PostgreSQL + Redis)
cd infrastructure
docker-compose up -d

# 2. 백엔드 실행 (자동화 스크립트)
cd ..
./run_backend.sh
```

**접속**:
- API:

http://localhost:8000

- Swagger UI:

http://localhost:8000/docs

#### 프론트엔드 (Next.js)

```bash
# 터미널을 새로 열고 실행
./run_frontend.sh
```

**접속**:

http://localhost:3000

---

## ✨ 기능 목록

### 기존 시스템 (Streamlit) - 14개 페이지

| 페이지 | 기능 | 상태 |
|--------|------|------|
| **Dashboard** | 일일 로스팅 통계, 재고 현황, 손실률 추이 | ✅ 완료 |
| **BeanManagement** | 원두 등록/수정/삭제, 가격 이력 관리 | ✅ 완료 |
| **BlendManagement** | 블렌드 레시피 생성/관리, 원가 계산 | ✅ 완료 |
| **InventoryManagement** | 재고 현황 조회, 입출고 관리 | ✅ 완료 |
| **CostCalculation** | 정확한 원가 계산, 가격 제안 | ✅ 완료 |
| **RoastingRecord** | 로스팅 기록 등록, 로스팅 로그 관리 | ✅ 완료 |
| **RoastingReceipt** | 로스팅 영수증 출력 | ✅ 완료 |
| **Analysis** | 기본 분석 (손실률, 비용 추이) | ✅ 완료 |
| **AdvancedAnalysis** | 고급 분석 (재고 회전율, ABC 분석) | ✅ 완료 |
| **AnalysisReport** | 종합 분석 리포트 | ✅ 완료 |
| **Report** | 맞춤형 리포트 생성 | ✅ 완료 |
| **ImageInvoiceUpload** | OCR 기반 송장 자동 입력 | ✅ 완료 |
| **ExcelSync** | Excel 데이터 동기화 | ✅ 완료 |
| **Settings** | 시스템 설정, 비용 설정 | ✅ 완료 |

### 신규 시스템 (Next.js) - API 엔드포인트

| 엔드포인트 | 메서드 | 기능 | 상태 |
|-----------|--------|------|------|
| `/api/v1/login/access-token` | POST | JWT 로그인 | ✅ 완료 |
| `/api/v1/beans/` | GET, POST | 원두 조회/생성 | ✅ 완료 |
| `/api/v1/beans/{id}` | GET, PUT, DELETE | 원두 상세/수정/삭제 | ✅ 완료 |
| `/api/v1/blends/` | GET, POST | 블렌드 조회/생성 | ✅ 완료 |
| `/api/v1/inventory/` | GET, POST | 재고 조회/생성 | ✅ 완료 |
| `/api/v1/ws` | WebSocket | 실시간 알림 | 🚧 진행 중 |

---

## 📁 프로젝트 구조

```
TheMoon/
├── app/                          # Streamlit 애플리케이션 (기존 시스템)
│   ├── pages/                    # 14개 페이지 모듈
│   │   ├── Dashboard.py
│   │   ├── BeanManagement.py
│   │   ├── BlendManagement.py
│   │   ├── InventoryManagement.py
│   │   ├── CostCalculation.py
│   │   ├── RoastingRecord.py
│   │   ├── RoastingReceipt.py
│   │   ├── Analysis.py
│   │   ├── AdvancedAnalysis.py
│   │   ├── AnalysisReport.py
│   │   ├── Report.py
│   │   ├── ImageInvoiceUpload.py
│   │   ├── ExcelSync.py
│   │   └── Settings.py
│   ├── services/                 # 12개 비즈니스 로직 서비스
│   │   ├── bean_service.py
│   │   ├── blend_service.py
│   │   ├── inventory_service.py
│   │   ├── roasting_service.py
│   │   ├── cost_calculator_service.py
│   │   ├── analytics_service.py
│   │   ├── report_service.py
│   │   ├── invoice_service.py
│   │   ├── gemini_ocr_service.py
│   │   ├── claude_ocr_service.py
│   │   └── ...
│   ├── models/                   # SQLAlchemy 모델
│   │   ├── bean.py
│   │   ├── blend.py
│   │   ├── inventory.py
│   │   ├── transaction.py
│   │   ├── user.py
│   │   └── invoice.py
│   ├── components/               # UI 컴포넌트
│   ├── utils/                    # 유틸리티
│   ├── tests/                    # 테스트 (20개 파일)
│   └── app.py                    # 메인 진입점
│
├── backend/                      # FastAPI 백엔드 (신규 시스템)
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/    # API 엔드포인트
│   │   │       │   ├── auth.py
│   │   │       │   ├── beans.py
│   │   │       │   ├── blends.py
│   │   │       │   ├── inventory.py
│   │   │       │   └── websockets.py
│   │   │       └── api.py
│   │   ├── core/                 # 핵심 설정
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── celery_app.py
│   │   ├── models/               # SQLAlchemy 모델 (8개)
│   │   │   ├── bean.py
│   │   │   ├── blend.py
│   │   │   ├── inventory.py
│   │   │   ├── transaction.py
│   │   │   ├── user.py
│   │   │   ├── invoice.py
│   │   │   └── cost_setting.py
│   │   ├── schemas/              # Pydantic 스키마
│   │   │   ├── bean.py
│   │   │   ├── blend.py
│   │   │   ├── inventory.py
│   │   │   ├── user.py
│   │   │   └── token.py
│   │   ├── database.py           # DB 연결
│   │   └── main.py               # FastAPI 앱
│   ├── alembic/                  # DB 마이그레이션
│   ├── tests/                    # API 테스트
│   └── requirements.txt
│
├── frontend/                     # Next.js 프론트엔드 (신규 시스템)
│   ├── app/                      # Next.js App Router
│   │   ├── page.tsx              # 홈 페이지
│   │   ├── layout.tsx            # 레이아웃
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── beans/
│   │   │   └── page.tsx
│   │   └── blends/
│   │       └── page.tsx
│   ├── components/               # React 컴포넌트
│   │   └── ui/                   # shadcn/ui 컴포넌트
│   ├── lib/                      # 라이브러리
│   │   ├── api.ts                # API 클라이언트
│   │   ├── hooks/
│   │   │   └── useWebSocket.ts
│   │   └── utils.ts
│   ├── public/
│   └── package.json
│
├── infrastructure/               # 인프라 설정
│   └── docker-compose.yml        # PostgreSQL + Redis
│
├── scripts/                      # 유틸리티 스크립트
│   ├── migrate_db.py             # DB 마이그레이션
│   └── generate_icons.py         # 아이콘 생성
│
├── data/                         # 데이터베이스 파일
│   └── roasting_data.db          # SQLite (기존)
│
├── Documents/                    # 프로젝트 문서
│   ├── Architecture/             # 아키텍처 문서
│   ├── Guides/                   # 가이드
│   ├── Progress/                 # 진행 상황
│   └── Planning/                 # 계획 문서
│
├── logs/                         # 로그 및 버전 관리
│   ├── VERSION                   # 현재 버전
│   ├── CHANGELOG.md              # 변경 로그
│   └── VERSION_MANAGEMENT.md     # 버전 관리 규칙
│
├── run_backend.sh                # 백엔드 실행 스크립트
├── run_frontend.sh               # 프론트엔드 실행 스크립트
├── implementation_plan.md        # 마이그레이션 실행 계획
├── README.md                     # 이 파일
└── requirements.txt              # Python 의존성 (Streamlit용)
```

---

## 🛠️ 기술 스택

### 기존 시스템 (Streamlit)

| 분류 | 기술 |
|------|------|
| **프레임워크** | Streamlit 1.28+ |
| **언어** | Python 3.12.3 |
| **데이터베이스** | SQLite 3 |
| **ORM** | SQLAlchemy 2.0 |
| **AI/ML** | Google Gemini API, Anthropic Claude API |
| **테스트** | pytest, pytest-cov |
| **기타** | pandas, Pillow, python-dotenv |

### 신규 시스템 (Next.js + FastAPI)

#### Backend

| 분류 | 기술 |
|------|------|
| **프레임워크** | FastAPI 0.100+ |
| **언어** | Python 3.12.3 |
| **데이터베이스** | PostgreSQL 15 |
| **ORM** | SQLAlchemy 2.0 |
| **마이그레이션** | Alembic 1.10+ |
| **스키마** | Pydantic 2.0 |
| **인증** | JWT (python-jose, passlib) |
| **캐시/큐** | Redis 7, Celery 5.3 |
| **서버** | Uvicorn (ASGI) |
| **테스트** | pytest |

#### Frontend

| 분류 | 기술 |
|------|------|
| **프레임워크** | Next.js 14.0 |
| **언어** | TypeScript 5 |
| **UI 라이브러리** | React 18 |
| **스타일링** | Tailwind CSS 3.3 |
| **UI 컴포넌트** | shadcn/ui (Radix UI) |
| **아이콘** | lucide-react |
| **HTTP 클라이언트** | Axios 1.6 |
| **빌드 도구** | Next.js (Turbopack) |

#### Infrastructure

| 분류 | 기술 |
|------|------|
| **컨테이너** | Docker, Docker Compose |
| **데이터베이스** | PostgreSQL 15 (Docker) |
| **캐시** | Redis 7 (Docker) |

---

## 💻 개발 가이드

### 개발 환경 설정

#### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd TheMoon
```

#### 2. 환경 변수 설정

```bash
# 루트 디렉토리에 .env 파일 생성
cp .env.example .env

# .env 파일 편집
nano .env
```

**.env 예시:**

```env
# Database
DATABASE_URL=postgresql://themoon:themoon_password@localhost:5432/themoon_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=480

# AI API Keys
GEMINI_API_KEY=your-gemini-api-key
ANTHROPIC_API_KEY=your-claude-api-key
```

#### 3. Streamlit 앱 개발

```bash
# 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app/app.py --server.port 8501 --server.headless true
```

#### 4. FastAPI 백엔드 개발

```bash
# 인프라 시작
cd infrastructure
docker-compose up -d
cd ..

# 가상환경 생성 (루트에 venv 사용)
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r backend/requirements.txt

# 데이터베이스 마이그레이션
cd backend
alembic upgrade head

# 개발 서버 실행
uvicorn app.main:app --reload --port 8000
```

**API 테스트:**
- Swagger UI:

http://localhost:8000/docs

- ReDoc:

http://localhost:8000/redoc

#### 5. Next.js 프론트엔드 개발

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

**접속**:

http://localhost:3000

### 코드 스타일

#### Python (PEP 8)

```bash
# 코드 포맷팅 (black)
pip install black
black app/ backend/

# 린트 (flake8)
pip install flake8
flake8 app/ backend/
```

#### TypeScript (ESLint + Prettier)

```bash
# 린트
cd frontend
npm run lint

# 포맷팅
npm run format  # package.json에 스크립트 추가 필요
```

### 브랜치 전략

```
main            # 프로덕션 브랜치
├── develop     # 개발 브랜치
│   ├── feature/bean-management
│   ├── feature/blend-calculation
│   └── feature/ocr-integration
└── hotfix/     # 긴급 수정
```

---

## 📚 API 문서

### Base URL

- **개발**:

http://localhost:8000

- **프로덕션**: TBD

### 인증

모든 API 요청은 JWT 토큰이 필요합니다 (로그인 제외).

```bash
# 1. 로그인
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 응답
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

# 2. API 호출 (토큰 사용)
curl -X GET "http://localhost:8000/api/v1/beans/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 주요 엔드포인트

#### 원두 (Beans)

```bash
# 원두 목록 조회
GET /api/v1/beans/?skip=0&limit=100

# 원두 생성
POST /api/v1/beans/
{
  "no": 1,
  "name": "Ethiopia Yirgacheffe",
  "country_name": "Ethiopia",
  "roast_level": "MEDIUM",
  "price_per_kg": 25000,
  "status": "active"
}

# 원두 상세 조회
GET /api/v1/beans/{bean_id}

# 원두 수정
PUT /api/v1/beans/{bean_id}

# 원두 삭제
DELETE /api/v1/beans/{bean_id}
```

#### 블렌드 (Blends)

```bash
# 블렌드 목록 조회
GET /api/v1/blends/?skip=0&limit=100

# 블렌드 생성
POST /api/v1/blends/
{
  "name": "House Blend",
  "blend_type": "CUSTOM",
  "total_portion": 10,
  "suggested_price": 18000,
  "recipes": [
    {
      "bean_id": 1,
      "portion_count": 6,
      "ratio": 60.0
    },
    {
      "bean_id": 2,
      "portion_count": 4,
      "ratio": 40.0
    }
  ]
}
```

#### 재고 (Inventory)

```bash
# 재고 조회
GET /api/v1/inventory/?skip=0&limit=100

# 재고 생성/업데이트
POST /api/v1/inventory/
{
  "bean_id": 1,
  "inventory_type": "RAW_BEAN",
  "quantity_kg": 50.0,
  "min_quantity_kg": 10.0,
  "max_quantity_kg": 100.0
}
```

**상세 API 문서**:

http://localhost:8000/docs

---

## 🧪 테스트

### Streamlit 앱 테스트

```bash
# 가상환경 활성화
source venv/bin/activate

# 전체 테스트 실행
pytest app/tests/ -v

# 커버리지 포함 테스트
pytest app/tests/ --cov=app --cov-report=html

# 특정 서비스 테스트
pytest app/tests/test_bean_service.py -v
pytest app/tests/test_blend_service.py -v
pytest app/tests/test_inventory_service.py -v
```

**커버리지 리포트**: `htmlcov/index.html`

### FastAPI 백엔드 테스트

```bash
cd backend

# 테스트 실행
pytest tests/ -v

# 커버리지 포함
pytest tests/ --cov=app --cov-report=html
```

### Next.js 프론트엔드 테스트

```bash
cd frontend

# Jest 테스트 (설정 필요)
npm run test

# E2E 테스트 (Playwright 설정 필요)
npm run test:e2e
```

---

## 🚀 배포

### Docker Compose로 전체 스택 배포

```bash
# 프로덕션 docker-compose.yml 작성 필요
docker-compose -f docker-compose.prod.yml up -d
```

### 개별 배포

#### Streamlit 앱 (Streamlit Cloud)

```bash
# Streamlit Cloud에 배포
# 1. GitHub 레포지토리 연결
# 2. app/app.py를 메인 파일로 지정
# 3. requirements.txt 사용
```

#### FastAPI (Render / Railway / AWS)

```bash
# Dockerfile 작성
cd backend

# Docker 이미지 빌드
docker build -t themoon-backend .

# 실행
docker run -p 8000:8000 themoon-backend
```

#### Next.js (Vercel / Netlify)

```bash
cd frontend

# 빌드
npm run build

# 프로덕션 실행
npm run start
```

---

## 🤝 기여하기

프로젝트에 기여하고 싶으신가요? 환영합니다!

### 기여 방법

1. 이 저장소를 포크합니다
2. 새 브랜치를 생성합니다 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋합니다 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/AmazingFeature`)
5. Pull Request를 생성합니다

### 커밋 메시지 규칙

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
refactor: 코드 리팩토링
test: 테스트 코드 추가/수정
chore: 빌드 스크립트, 패키지 업데이트
```

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 📞 문의

프로젝트에 대한 질문이나 제안이 있으시면 이슈를 생성해주세요.

---

## 📝 변경 로그

전체 변경 로그는 [CHANGELOG.md](logs/CHANGELOG.md)를 참조하세요.

### 최근 업데이트 (v0.50.2)

- 🚧 Next.js + FastAPI 마이그레이션 Phase 1 진행 중
- ✅ FastAPI 백엔드 기본 구조 완성
- ✅ Next.js 프론트엔드 초기 설정 완료
- ✅ Docker Compose 인프라 구성
- ✅ SQLAlchemy 모델 8개 정의 완료
- ✅ API 엔드포인트 5개 구현 완료
- 🐛 FastAPI import 오류 수정 (crud 모듈 제거)

---

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 라이브러리들을 사용하여 만들어졌습니다:

- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)

모든 기여자분들께 감사드립니다! 🎉

---

**Made with ☕ by TheMoon Team**

**Last Updated**: 2024-11-23
