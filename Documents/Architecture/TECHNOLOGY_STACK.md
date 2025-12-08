# 🛠️ 기술 스택 명세서 (Technology Stack)

> **프로젝트**: TheMoon - 커피 로스팅 원가 계산 시스템
> **버전**: 0.0.6
> **아키텍처**: Modern Full-Stack (Next.js + FastAPI + PostgreSQL)
> **작성일**: 2025-12-08

---

## 📋 목차

1. [기술 스택 개요](#기술-스택-개요)
2. [Frontend 기술 스택](#frontend-기술-스택)
3. [Backend 기술 스택](#backend-기술-스택)
4. [Database & Infrastructure](#database--infrastructure)
5. [DevOps & Deployment](#devops--deployment)
6. [개발 도구 & 환경](#개발-도구--환경)
7. [기술 선정 이유 (Decision Making)](#기술-선정-이유-decision-making)

---

## 기술 스택 개요

### 전체 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend Layer                      │
│   Next.js 14 + TypeScript + Shadcn UI + Tailwind CSS   │
└───────────────────────┬─────────────────────────────────┘
                        │ REST API (axios)
┌───────────────────────▼─────────────────────────────────┐
│                      Backend Layer                       │
│        FastAPI + Pydantic + SQLAlchemy + Uvicorn        │
└───────────────────────┬─────────────────────────────────┘
                        │ SQL
┌───────────────────────▼─────────────────────────────────┐
│                     Database Layer                       │
│          PostgreSQL (Production) / SQLite (Dev)         │
└─────────────────────────────────────────────────────────┘
```

### 핵심 철학

- **타입 안정성**: TypeScript (Frontend) + Pydantic (Backend) → 종단 간 타입 검증
- **개발 생산성**: Hot Reload (Next.js, Uvicorn), 자동 문서화 (FastAPI Swagger)
- **확장 가능성**: Modular Architecture (Services, Schemas, Models 분리)
- **사용자 경험**: Shadcn UI (접근성), Tailwind CSS (반응형 디자인)

---

## Frontend 기술 스택

### Core Framework

| 기술 | 버전 | 역할 | 선정 이유 |
|------|------|------|-----------|
| **Next.js** | 14.2.33 | React 메타 프레임워크 | • SSR/SSG 지원으로 SEO 최적화<br>• App Router (최신 라우팅 시스템)<br>• API Routes (BFF 패턴 구현 가능)<br>• 이미지 최적화 (next/image) |
| **React** | 18.3.1 | UI 라이브러리 | • 컴포넌트 기반 개발<br>• React Hooks (상태 관리)<br>• Virtual DOM (렌더링 최적화) |
| **TypeScript** | 5.9.3 | 정적 타입 시스템 | • 컴파일 타임 에러 검출<br>• IntelliSense 지원<br>• 코드 가독성 및 유지보수성 향상 |

### UI & Styling

| 기술 | 버전 | 역할 | 선정 이유 |
|------|------|------|-----------|
| **Shadcn UI** | - | UI 컴포넌트 시스템 | • Radix UI 기반 (접근성 표준 준수)<br>• Copy-paste 방식 (번들 크기 최소화)<br>• Tailwind CSS 통합<br>• 커스터마이징 용이 |
| **Tailwind CSS** | 3.4.18 | 유틸리티 CSS 프레임워크 | • 빠른 스타일링<br>• 일관된 디자인 시스템<br>• PurgeCSS (미사용 CSS 제거)<br>• 반응형 디자인 간편화 |
| **Radix UI** | 1.x | 접근성 프리미티브 | • WAI-ARIA 준수<br>• 키보드 내비게이션 지원<br>• 스크린 리더 호환 |
| **Framer Motion** | 12.23.25 | 애니메이션 라이브러리 | • 선언적 애니메이션<br>• Spring Physics 기반 자연스러운 효과<br>• Gesture 지원 (드래그, 스와이프) |
| **Lucide React** | 0.556.0 | 아이콘 라이브러리 | • Tree-shakable (번들 최적화)<br>• 1400+ 아이콘<br>• MIT 라이선스 |

### Data Fetching & State Management

| 기술 | 버전 | 역할 | 선정 이유 |
|------|------|------|-----------|
| **SWR** | 2.3.7 | 데이터 페칭 라이브러리 | • Stale-While-Revalidate 전략<br>• 자동 캐싱 및 갱신<br>• 낙관적 UI 업데이트<br>• 네트워크 상태 관리 |
| **Axios** | 1.6.5 | HTTP 클라이언트 | • 요청/응답 인터셉터<br>• 자동 JSON 파싱<br>• 타임아웃 설정<br>• CSRF 보호 |

### Utilities

| 기술 | 버전 | 역할 | 선정 이유 |
|------|------|------|-----------|
| **clsx** | 2.1.1 | 조건부 className 생성 | • 작은 번들 크기 (228B)<br>• 타입 안전성<br>• Tailwind CSS와 호환 |
| **tailwind-merge** | 3.4.0 | Tailwind 클래스 병합 | • 중복 클래스 제거<br>• 우선순위 관리 |
| **date-fns** | 4.1.0 | 날짜 유틸리티 | • Tree-shakable<br>• Immutable (함수형 프로그래밍)<br>• TypeScript 지원 |

### Visualization

| 기술 | 버전 | 역할 | 선정 이유 |
|------|------|------|-----------|
| **Recharts** | 3.5.1 | 차트 라이브러리 | • React 컴포넌트 기반<br>• 반응형 차트<br>• 다양한 차트 타입 지원<br>• D3.js 기반 (유연한 커스터마이징) |

---

## Backend 기술 스택

### Core Framework

| 기술 | 버전 | 역할 | 선정 이유 |
|------|------|------|-----------|
| **FastAPI** | 0.109.0 | 웹 프레임워크 | • **자동 문서화** (Swagger UI, ReDoc)<br>• **타입 검증** (Pydantic)<br>• **비동기 지원** (async/await)<br>• **빠른 성능** (Starlette + Uvicorn)<br>• **Django/Flask 대비 40% 빠른 응답 속도** |
| **Uvicorn** | 0.27.0 | ASGI 서버 | • 비동기 I/O 지원<br>• Hot Reload (개발 편의성)<br>• HTTP/2 지원 |
| **Pydantic** | 2.5.0 | 데이터 검증 라이브러리 | • 런타임 타입 검증<br>• JSON 스키마 자동 생성<br>• 에러 메시지 자동 생성<br>• FastAPI와 완벽한 통합 |

### Database & ORM

| 기술 | 버전 | 역할 | 선정 이유 |
|------|------|------|-----------|
| **SQLAlchemy** | 2.0.25 | ORM (Object-Relational Mapping) | • **업계 표준** Python ORM<br>• **타입 안전성** (2.0+ 버전)<br>• **Migration 지원** (Alembic 통합)<br>• **Raw SQL 지원** (복잡한 쿼리)<br>• **Lazy Loading** (성능 최적화) |
| **Alembic** | 1.13.0 | 데이터베이스 마이그레이션 도구 | • 버전 관리 (스키마 변경 추적)<br>• 롤백 기능<br>• 자동 마이그레이션 생성 |
| **psycopg2-binary** | 2.9.9 | PostgreSQL 어댑터 | • PostgreSQL과 Python 연결<br>• 빠른 성능 (C 확장)<br>• SQLAlchemy 호환 |

### Authentication & Security

| 기술 | 버전 | 역할 | 선정 이유 |
|------|------|------|-----------|
| **python-jose** | 3.3.0 | JWT 인증 라이브러리 | • JWT 토큰 생성/검증<br>• 암호화 알고리즘 지원 (RS256, HS256) |
| **passlib** | 1.7.4 | 비밀번호 해싱 라이브러리 | • bcrypt 해싱 (보안 강화)<br>• 솔트 자동 생성 |

### Configuration & Environment

| 기술 | 버전 | 역할 | 선정 이유 |
|------|------|------|-----------|
| **pydantic-settings** | 2.1.0 | 환경 변수 관리 | • .env 파일 자동 로드<br>• 타입 검증<br>• 환경별 설정 분리 (dev/prod) |
| **python-dotenv** | 1.0.0 | .env 파일 로더 | • 환경 변수 관리 간편화<br>• 12-Factor App 준수 |

---

## Database & Infrastructure

### Database

| 기술 | 버전 | 역할 | 환경 | 선정 이유 |
|------|------|------|------|-----------|
| **PostgreSQL** | 15+ | 관계형 데이터베이스 | 프로덕션 | • **ACID 준수** (트랜잭션 안정성)<br>• **JSON 지원** (유연한 스키마)<br>• **확장성** (수평/수직 확장 가능)<br>• **무료 & 오픈소스**<br>• **Render.com 무료 티어 지원** |
| **SQLite** | 3.x | 파일 기반 DB | 개발 | • 설정 불필요 (파일 하나로 관리)<br>• 빠른 로컬 개발<br>• 테스트 용이 |

### Why PostgreSQL?

**원본 프로젝트 비교**:

| 항목 | 원본 (SQLite) | 신규 (PostgreSQL) | 개선 효과 |
|------|--------------|------------------|----------|
| **동시성** | 단일 Writer 제한 | 다중 Writer 지원 | 🚀 **동시 접속 처리 가능** |
| **트랜잭션** | 기본 지원 | ACID 완전 준수 | 🔒 **데이터 무결성 보장** |
| **확장성** | 로컬 파일 제한 | 수평 확장 가능 | 📈 **대규모 서비스 대응** |
| **배포** | 파일 배포 필요 | 원격 DB 서비스 | 🌐 **Render.com 무료 호스팅** |

---

## DevOps & Deployment

### Deployment Platform

| 플랫폼 | 역할 | 선정 이유 |
|--------|------|-----------|
| **Render.com** | 클라우드 호스팅 | • **무료 티어** (PostgreSQL + 웹 서비스)<br>• **자동 배포** (GitHub 연동)<br>• **HTTPS 자동 설정**<br>• **환경 변수 관리**<br>• **Health Check 지원**<br>• **Heroku 대비 저렴한 가격** |

### CI/CD

| 기술 | 역할 | 현황 |
|------|------|------|
| **GitHub Actions** | CI/CD 파이프라인 | 🔜 예정 (자동 테스트 + 배포) |
| **Git Hooks** | 커밋 전 검증 | 🔜 예정 (Lint, Format 검사) |

---

## 개발 도구 & 환경

### Development Tools

| 도구 | 역할 | 선정 이유 |
|------|------|-----------|
| **WSL2 (Ubuntu)** | 개발 환경 | • Linux 네이티브 환경<br>• Docker 호환성<br>• 패키지 관리 용이 |
| **Python 3.10+** | Backend 런타임 | • FastAPI 호환<br>• 타입 힌트 강화 (3.10+)<br>• 안정성 (LTS) |
| **Node.js 18+** | Frontend 런타임 | • Next.js 14 지원<br>• npm/pnpm 패키지 관리 |

### Code Quality

| 도구 | 역할 | 현황 |
|------|------|------|
| **ESLint** | JavaScript/TypeScript 린터 | ✅ 설정 완료 (Next.js 기본) |
| **Prettier** | 코드 포매터 | 🔜 예정 |
| **Black** | Python 코드 포매터 | 🔜 예정 |
| **mypy** | Python 타입 체커 | 🔜 예정 |

---

## 기술 선정 이유 (Decision Making)

### 1️⃣ **원본 프로젝트 대비 개선점**

| 항목 | 원본 (TheMoon_Project) | 신규 (Themoon) | 개선 이유 |
|------|----------------------|---------------|----------|
| **Frontend** | Streamlit | Next.js + Shadcn UI | • **완전한 UI 제어권**<br>• **반응형 디자인**<br>• **확장 가능성** |
| **Backend** | Streamlit (단일 앱) | FastAPI (API 서버) | • **프론트엔드 분리** (MSA 대비)<br>• **자동 문서화**<br>• **타입 안정성** |
| **Database** | SQLite | PostgreSQL | • **프로덕션 레디**<br>• **동시성 지원**<br>• **클라우드 배포** |
| **Architecture** | Monolithic | 3-Layer (Frontend/Backend/DB) | • **유지보수성**<br>• **확장성**<br>• **팀 협업 용이** |

---

### 2️⃣ **FastAPI vs Django/Flask**

| 비교 항목 | FastAPI | Django | Flask |
|----------|---------|--------|-------|
| **성능** | ⚡ **매우 빠름** (Starlette) | 느림 (동기) | 보통 |
| **타입 검증** | ✅ **자동** (Pydantic) | ❌ 수동 | ❌ 수동 |
| **문서화** | ✅ **자동** (Swagger) | ❌ 수동 | ❌ 수동 |
| **비동기 지원** | ✅ **네이티브** | 부분 지원 | 확장 필요 |
| **학습 곡선** | 낮음 | 높음 (ORM, Admin) | 낮음 |
| **사용 사례** | **API 서버** | 풀스택 웹앱 | 간단한 API |

**결론**: API 전용 서버로 FastAPI가 최적 (성능 + 개발 생산성)

---

### 3️⃣ **Next.js vs CRA/Vite**

| 비교 항목 | Next.js | Create React App | Vite |
|----------|---------|------------------|------|
| **SSR/SSG** | ✅ 기본 지원 | ❌ | ❌ (플러그인) |
| **라우팅** | ✅ **파일 기반** | ❌ (React Router) | ❌ |
| **이미지 최적화** | ✅ next/image | ❌ | ❌ |
| **API Routes** | ✅ BFF 패턴 | ❌ | ❌ |
| **빌드 속도** | 보통 | 느림 | ⚡ **빠름** |
| **SEO** | ✅ **우수** | ❌ (CSR) | ❌ |

**결론**: 관리 대시보드는 SEO가 중요하지 않지만, Next.js의 통합 개발 경험 (라우팅, 이미지 최적화, API Routes)이 생산성 향상에 기여

---

### 4️⃣ **Shadcn UI vs MUI/Ant Design**

| 비교 항목 | Shadcn UI | Material UI | Ant Design |
|----------|-----------|-------------|------------|
| **번들 크기** | ✅ **작음** (Copy-paste) | 큼 (전체 번들) | 큼 |
| **커스터마이징** | ✅ **완전 제어** | 제한적 (테마) | 제한적 |
| **접근성** | ✅ **A+ (Radix UI)** | 보통 | 보통 |
| **디자인 시스템** | Tailwind 통합 | CSS-in-JS | Less |
| **학습 곡선** | 낮음 | 보통 | 보통 |

**결론**: Shadcn UI는 **소스 코드 완전 소유** + **번들 최적화** + **Tailwind 통합**으로 장기적인 유지보수에 유리

---

### 5️⃣ **PostgreSQL vs MySQL/MongoDB**

| 비교 항목 | PostgreSQL | MySQL | MongoDB |
|----------|-----------|-------|---------|
| **트랜잭션** | ✅ **ACID 완전 준수** | 부분 지원 | ❌ (최종 일관성) |
| **JSON 지원** | ✅ **네이티브** | 보통 | ✅ 네이티브 |
| **확장성** | ✅ 수평/수직 | 수직 | ✅ 수평 |
| **무료 호스팅** | ✅ **Render.com** | 제한적 | MongoDB Atlas |
| **SQL 표준** | ✅ 완전 준수 | 부분 준수 | ❌ NoSQL |

**결론**:
- **관계형 데이터 모델** (원두-로스팅-재고)은 SQL이 적합
- **PostgreSQL**은 JSON 지원으로 유연성도 확보
- **Render.com 무료 티어**로 비용 절감

---

## 📊 버전 관리 정책

### 의존성 버전 고정 전략

```python
# ✅ 좋은 예 (Semantic Versioning 범위 지정)
fastapi>=0.109.0,<0.110.0  # MINOR 버전 고정, PATCH 업데이트 허용

# ❌ 나쁜 예 (버전 완전 고정)
fastapi==0.109.0  # PATCH 업데이트도 차단 (보안 패치 누락 위험)

# ❌ 나쁜 예 (버전 제한 없음)
fastapi  # MAJOR 버전 업데이트로 호환성 깨질 위험
```

**이유**:
- **보안 패치 자동 적용**: PATCH 버전 업데이트 허용
- **호환성 보장**: MINOR 버전 고정으로 Breaking Changes 차단

---

## 🔗 관련 문서

**← 상위**: [Documents README](../README.md) | [프로젝트 루트](../../README.md)

**아키텍처 문서**:
- [시스템 개요](SYSTEM_OVERVIEW.md) - 전체 시스템 개요 및 핵심 기능
- [데이터 흐름도](DATA_FLOW.md) - 시스템 내 데이터 흐름 상세 분석
- [데이터베이스 스키마](DATABASE_SCHEMA.md) - 테이블 구조 및 관계도
- [API 명세](API_SPECIFICATION.md) ⭐ - 모든 API 엔드포인트 상세 문서
- [배포 아키텍처](DEPLOYMENT_ARCHITECTURE.md) ⭐ - 배포 환경 상세 구조

**개발 가이드**:
- [개발 가이드](DEVELOPMENT_GUIDE.md) - 5단계 개발 프로세스
- [문제 해결](TROUBLESHOOTING.md) - 16가지 오류 & 해결법

---

**문서 버전**: v1.0
**최종 업데이트**: 2025-12-08
**작성자**: Claude (TheMoon Project Team)
