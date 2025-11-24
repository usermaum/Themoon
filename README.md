# TheMoon - 커피 로스팅 원가 계산 시스템 (Modern Stack)

> **v0.0.2** | Next.js + FastAPI로 완전히 재작성

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.1-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)

---

## 📌 원본 프로젝트 참조

이 프로젝트는 Streamlit 기반의 원본 프로젝트를 **완전히 재작성**한 버전입니다.

**원본 프로젝트 위치:**
```
/mnt/d/Ai/WslProject/TheMoon_Project/
```

**원본 프로젝트 참조 방법:**
- **모델:** `/mnt/d/Ai/WslProject/TheMoon_Project/app/models/`
- **서비스 로직:** `/mnt/d/Ai/WslProject/TheMoon_Project/app/services/`
- **UI 참조:** `/mnt/d/Ai/WslProject/TheMoon_Project/app/pages/`

---

## 🎯 프로젝트 개요

**커피 로스팅 원가 계산 및 재고 관리 시스템**을 Next.js + FastAPI 아키텍처로 구현한 모던 웹 애플리케이션입니다.

### 핵심 기능

- ☕ **원두 관리** - 생두 정보, 가격, 로스팅 레벨 관리
- 🧪 **블렌드 관리** - 블렌드 레시피 및 원가 계산
- 📦 **재고 관리** - 실시간 재고 추적 및 입출고 관리
- 📊 **로스팅 기록** - 로스팅 로그 및 손실률 분석
- 💰 **비용 계산** - 정확한 원가 계산 및 가격 제안
- 📈 **분석 및 리포트** - 손실률, 비용 추이, 재고 분석

---

## 🏗️ 아키텍처

### 시스템 구조

```
┌──────────────────────────────────────┐
│    Next.js Frontend (Port 3000)      │
│  ┌────────────────────────────────┐  │
│  │  React 18 + TypeScript         │  │
│  │  Tailwind CSS + shadcn/ui      │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
              ↓ (REST API)
┌──────────────────────────────────────┐
│    FastAPI Backend (Port 8000)       │
│  ┌────────────────────────────────┐  │
│  │  API v1 (RESTful)              │  │
│  │  SQLAlchemy + Pydantic         │  │
│  │  JWT Authentication            │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│      PostgreSQL (Port 5432)          │
└──────────────────────────────────────┘
```

---

## 📁 프로젝트 구조

### 현재 구조 (v0.0.2)

```
Themoon/                       # 신규 프로젝트 (Clean Slate)
├── .claude/                   # Claude Code 설정
│   ├── CLAUDE.md              # 프로젝트 가이드
│   ├── instructions.md        # 상세 지침
│   └── settings.local.json
│
├── backend/                   # FastAPI 백엔드 (8개 파일, 20KB)
│   ├── app/
│   │   ├── __init__.py        # 버전 정보
│   │   ├── main.py            # FastAPI 앱 (50줄, 간결)
│   │   ├── config.py          # 설정 관리
│   │   └── database.py        # DB 연결
│   ├── tests/                 # 테스트 (추후 추가)
│   ├── requirements.txt       # 필수 의존성만
│   └── README.md              # 개발 가이드
│
├── frontend/                  # Next.js 프론트엔드 (9개 파일, 16KB)
│   ├── app/
│   │   ├── page.tsx           # 메인 페이지
│   │   ├── layout.tsx         # 레이아웃
│   │   └── globals.css        # 글로벌 스타일
│   ├── components/            # UI 컴포넌트 (추후 추가)
│   │   └── ui/
│   ├── lib/
│   │   └── api.ts             # API 클라이언트
│   ├── public/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── README.md
│
├── Documents/                 # 프로젝트 문서 (80+ 파일)
│   ├── Architecture/          # 아키텍처 문서 (8개)
│   ├── Guides/                # 가이드 (4개)
│   ├── Implementation/        # 구현 문서 (2개)
│   ├── Planning/              # 계획 문서 (15개)
│   ├── Progress/              # 진행 상황 (40+ 세션)
│   └── Resources/             # 자료 (엑셀, 문서 등)
│
├── logs/                      # 버전 관리
│   ├── VERSION                # 현재: 0.0.1
│   └── CHANGELOG.md           # 변경 로그
│
├── data/                      # 데이터베이스 (원본 참조용)
├── venv/                      # Python 가상환경 (원본 참조용)
├── scripts/                   # 유틸리티 스크립트
├── .env                       # 환경 변수
├── .gitignore
└── README.md                  # 이 파일
```

### 계획된 구조 (개발 예정)

아래는 Week 1-2에 추가될 예정인 구조입니다:

```
backend/app/
├── api/                       # (추가 예정)
│   └── v1/
│       ├── endpoints/         # Bean, Blend, Inventory API
│       └── deps.py
├── core/                      # (추가 예정)
│   ├── security.py            # JWT, 인증
│   └── config.py
├── models/                    # (추가 예정) SQLAlchemy 모델
├── schemas/                   # (추가 예정) Pydantic 스키마
└── services/                  # (추가 예정) 비즈니스 로직

frontend/
├── beans/                     # (추가 예정) 원두 관리 페이지
├── blends/                    # (추가 예정) 블렌드 관리 페이지
└── components/                # (추가 예정) 재사용 컴포넌트
```

---

## 🚀 빠른 시작

### 시스템 요구사항

- **Python**: 3.12 이상
- **Node.js**: 18.0 이상
- **PostgreSQL**: 15.0 이상
- **Redis**: 7.0 이상 (선택사항)

### 1. Backend (FastAPI) 실행

```bash
cd backend

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집 (DATABASE_URL, SECRET_KEY 등)

# 개발 서버 실행
uvicorn app.main:app --reload --port 8000
```

**접속:**

http://localhost:8000

**API 문서:**

http://localhost:8000/docs

### 2. Frontend (Next.js) 실행

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 개발 서버 실행
npm run dev
```

**접속:**

http://localhost:3000

---

## 🛠️ 기술 스택

### Backend

| 분류 | 기술 | 버전 |
|------|------|------|
| **프레임워크** | FastAPI | 0.109+ |
| **언어** | Python | 3.12+ |
| **데이터베이스** | PostgreSQL | 15+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **스키마** | Pydantic | 2.5+ |
| **인증** | JWT (python-jose) | 3.3+ |
| **서버** | Uvicorn | 0.27+ |

### Frontend

| 분류 | 기술 | 버전 |
|------|------|------|
| **프레임워크** | Next.js | 14.1+ |
| **언어** | TypeScript | 5.3+ |
| **UI 라이브러리** | React | 18.2+ |
| **스타일링** | Tailwind CSS | 3.4+ |
| **UI 컴포넌트** | shadcn/ui | - |
| **HTTP 클라이언트** | Axios | 1.6+ |

---

## 📚 개발 가이드

### Backend 개발

원본 프로젝트의 비즈니스 로직을 참조하여 FastAPI로 재작성합니다.

```bash
# 원본 모델 참조
/mnt/d/Ai/WslProject/TheMoon_Project/app/models/bean.py
→ backend/app/models/bean.py (새로 작성)

# 원본 서비스 참조
/mnt/d/Ai/WslProject/TheMoon_Project/app/services/bean_service.py
→ backend/app/services/bean_service.py (새로 작성)
```

**개발 순서:**
1. **모델 정의** (`app/models/`) - 원본 참조
2. **스키마 정의** (`app/schemas/`) - Pydantic으로 작성
3. **서비스 로직** (`app/services/`) - 원본 로직 이식
4. **API 엔드포인트** (`app/api/v1/endpoints/`) - RESTful API 작성
5. **테스트 작성** (`tests/`) - pytest

### Frontend 개발

원본 프로젝트의 UI/UX를 참조하여 Next.js로 재작성합니다.

```bash
# 원본 페이지 참조
/mnt/d/Ai/WslProject/TheMoon_Project/app/pages/Dashboard.py
→ frontend/app/page.tsx (새로 작성)

/mnt/d/Ai/WslProject/TheMoon_Project/app/pages/BeanManagement.py
→ frontend/app/beans/page.tsx (새로 작성)
```

**개발 순서:**
1. **페이지 작성** (`app/*/page.tsx`) - 원본 UI 참조
2. **컴포넌트 작성** (`components/`) - 재사용 가능하게 설계
3. **API 통신** (`lib/api.ts`) - Axios 사용
4. **상태 관리** - React Hooks (useState, useEffect)

---

## 🧪 테스트

### Backend 테스트

```bash
cd backend

# 전체 테스트
pytest tests/ -v

# 커버리지 포함
pytest tests/ --cov=app --cov-report=html
```

### Frontend 테스트

```bash
cd frontend

# Jest 테스트 (설정 필요)
npm run test

# E2E 테스트 (Playwright 설정 필요)
npm run test:e2e
```

---

## 🔧 환경 변수

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://themoon:password@localhost:5432/themoon_db

# Redis (Optional)
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI APIs (Optional)
GEMINI_API_KEY=your-gemini-api-key
ANTHROPIC_API_KEY=your-claude-api-key
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📝 원본 프로젝트 대응표

| 원본 (Streamlit) | 신규 (Next.js + FastAPI) | 설명 |
|------------------|--------------------------|------|
| `app/models/` | `backend/app/models/` | SQLAlchemy 모델 (재작성) |
| `app/services/` | `backend/app/services/` | 비즈니스 로직 (재작성) |
| `app/pages/Dashboard.py` | `frontend/app/page.tsx` | 메인 대시보드 |
| `app/pages/BeanManagement.py` | `frontend/app/beans/page.tsx` | 원두 관리 |
| `app/pages/BlendManagement.py` | `frontend/app/blends/page.tsx` | 블렌드 관리 |
| `app/components/` | `frontend/components/` | UI 컴포넌트 |

---

## 📖 문서

- **Backend README:** [backend/README.md](backend/README.md)
- **Frontend README:** [frontend/README.md](frontend/README.md)
- **원본 프로젝트:** `/mnt/d/Ai/WslProject/TheMoon_Project/`
- **마이그레이션 계획:** [Documents/Planning/MIGRATION_TO_MODERN_STACK_GEMINI.md](Documents/Planning/MIGRATION_TO_MODERN_STACK_GEMINI.md)

---

## 🎯 개발 원칙

### 1. **완전 재작성 (Clean Slate)**
- 원본 코드를 **참조용으로만** 사용
- 모든 코드를 **최신 Best Practice**로 새로 작성
- 기술 부채 없이 깨끗하게 시작

### 2. **원본 로직 보존**
- 비즈니스 로직은 원본과 **동일하게** 작동
- 계산 로직, 데이터 모델 구조 유지
- 기능 동등성 (Feature Parity) 보장

### 3. **모던 아키텍처**
- Frontend/Backend **완전 분리**
- RESTful API 기반
- TypeScript 타입 안정성
- 테스트 우선 개발

---

## 🚀 배포

### Backend

```bash
# Docker 이미지 빌드
cd backend
docker build -t themoon-backend .

# 실행
docker run -p 8000:8000 themoon-backend
```

### Frontend

```bash
# Vercel 배포
cd frontend
npm run build
vercel deploy
```

---

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 라이선스

MIT License - 자유롭게 사용 가능

---

## 👥 팀

**원본 프로젝트:** TheMoon_Project (Streamlit)
**재작성 버전:** Themoon (Next.js + FastAPI)

---

## 📞 문의

프로젝트에 대한 질문이나 제안이 있으시면 이슈를 생성해주세요.

---

**버전:** 1.0.0 (Clean Slate)
**최종 업데이트:** 2024-11-23
**원본 프로젝트 참조:** `/mnt/d/Ai/WslProject/TheMoon_Project/`
