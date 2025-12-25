# TheMoon - 커피 로스팅 원가 계산 시스템 (Modern Stack)

> **v0.4.8** | Next.js + FastAPI로 고도화된 시스템 기능

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

#### 기본 기능
- ☕ **원두 관리** - 생두 정보, 가격, 로스팅 레벨 관리, WebP 이미지 최적화
- 🧪 **블렌드 관리** - 블렌드 레시피 및 원가 계산
- 📦 **재고 관리** - 실시간 재고 추적 및 입출고 관리
- 📊 **로스팅 기록** - 로스팅 로그 및 손실률 분석
- 💰 **비용 계산** - 정확한 원가 계산 및 가격 제안

#### 고급 기능 (v0.4.x~)
- 📄 **명세서 OCR** - Gemini AI 기반 명세서 자동 인식 및 데이터 추출
- 🖼️ **이미지 최적화** - 3종 이미지 생성 (Original/WebView/Thumbnail), WebP 변환
- 📋 **명세서 관리** - 목록 조회, 상세 보기, Paper Invoice UI, 썸네일 미리보기
- 💹 **FIFO 재고 시스템** - 선입선출 기반 원가 계산 및 로스팅 로그 자동 연동
- 📈 **Analytics 대시보드** - 공급업체별 재고 분포, Top 3 가치 품목, Smart Analysis Briefing
- 🛡️ **엔터프라이즈급 보안** - EXIF 제거, Magic Bytes 검증, 원자적 저장, 경로 검증
- ⏳ **실시간 분석** - SSE 기반 OCR 분석 상태 스트리밍 (v0.4.6)
- 🖥️ **시스템 대시보드** - CPU, 메모리, 디스크 실시간 사용량 모니터링 및 메모 통합 (v0.5.0)
- 🐱 **프리미엄 UX** - 냥이 테마 재재시작 오버레이 및 리얼 물방울 효과 (v0.5.2)

---

## 🏗️ 아키텍처

### 시스템 구조

```
┌──────────────────────────────────────┐
│    Next.js Frontend (Port 3500)      │
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

### 현재 구조 (v0.4.6)

```
Themoon/                       # 신규 프로젝트 (Clean Slate)
├── .claude/                   # Claude Code 설정
│   ├── CLAUDE.md              # 프로젝트 가이드 (Claude용)
│   ├── instructions.md        # 상세 지침
│   └── settings.local.json
├── .gemini/                   # Gemini 설정
│   └── GEMINI.md              # 프로젝트 가이드 (Gemini용)
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
├── docs/                  # 프로젝트 문서 (80+ 파일)
│   ├── Architecture/          # 아키텍처 문서 (8개)
│   ├── Guides/                # 가이드 (4개)
│   ├── Implementation/        # 구현 문서 (2개)
│   ├── Planning/              # 계획 문서 (15개)
│   ├── Progress/              # 진행 상황 (40+ 세션)
│   └── Resources/             # 자료 (엑셀, 문서 등)

### 프로젝트 문서 (docs/)

모든 기술 문서는 `docs/` 폴더에 체계적으로 정리되어 있습니다.

- **📚 문서 인덱스**: [docs/README.md](docs/README.md) - 모든 문서 네비게이션

#### 핵심 아키텍처 문서 ✅

| 문서              | 설명                                  | 경로                                                                         |
| ----------------- | ------------------------------------- | ---------------------------------------------------------------------------- |
| **시스템 개요**   | 전체 시스템 개요 및 핵심 기능         | [SYSTEM_OVERVIEW.md](docs/Architecture/SYSTEM_OVERVIEW.md)                   |
| **데이터 흐름**   | 데이터 흐름도 및 프로세스 간 상호작용 | [DATA_FLOW.md](docs/Architecture/DATA_FLOW.md)                               |
| **DB 스키마**     | PostgreSQL 데이터베이스 스키마 (ERD)  | [DATABASE_SCHEMA.md](docs/Architecture/DATABASE_SCHEMA.md)                   |
| **API 명세**      | RESTful API 엔드포인트 상세 명세      | [API_SPECIFICATION.md](docs/Architecture/API_SPECIFICATION.md) ⭐             |
| **기술 스택**     | 기술 선정 이유 및 버전 정보           | [TECHNOLOGY_STACK.md](docs/Architecture/TECHNOLOGY_STACK.md) ⭐               |
| **배포 아키텍처** | Render.com 배포 구조 및 CI/CD         | [DEPLOYMENT_ARCHITECTURE.md](docs/Architecture/DEPLOYMENT_ARCHITECTURE.md) ⭐ |

#### 개발 가이드

- **Backend README:** [backend/README.md](backend/README.md)
- **Frontend README:** [frontend/README.md](frontend/README.md)
- **개발 가이드**: [docs/Architecture/DEVELOPMENT_GUIDE.md](docs/Architecture/DEVELOPMENT_GUIDE.md)
- **문제 해결**: [docs/Architecture/TROUBLESHOOTING.md](docs/Architecture/TROUBLESHOOTING.md)

#### 원본 프로젝트 참조

- **원본 프로젝트 위치**: `/mnt/d/Ai/WslProject/TheMoon_Project/`
- **마이그레이션 계획**: [docs/Planning/MIGRATION_TO_MODERN_STACK_GEMINI.md](docs/Planning/MIGRATION_TO_MODERN_STACK_GEMINI.md)

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

**버전:** 0.5.2
**최종 업데이트:** 2025-12-25
**최종 커밋:** Premium Water Drops UI and System Monitoring Integration
**원본 프로젝트 참조:** `/mnt/d/Ai/WslProject/TheMoon_Project/`
