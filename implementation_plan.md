# TheMoon 프로젝트 마이그레이션 실행 계획 (Implementation Plan)

> **기반 문서**: `Documents/Planning/MIGRATION_TO_MODERN_STACK_GEMINI.md`
> **목표**: Streamlit 앱을 Next.js + FastAPI 아키텍처로 전환

---

## 1. 개요 (Overview)

이 문서는 `MIGRATION_TO_MODERN_STACK_GEMINI.md`에서 수립된 전략을 실제 실행 가능한 단위 작업(Task)으로 세분화한 계획입니다. 전체 마이그레이션은 4단계(Phase)로 진행되며, 본 문서는 **Phase 1: 기반 구축 및 백엔드 API화**에 집중하여 상세 계획을 수립합니다.

---

## 2. 단계별 실행 계획 (Phased Execution Plan)

### Phase 1: 기반 구축 및 백엔드 API화 (Backend Foundation)

**목표**: 데이터 레이어 분리 (SQLite → PostgreSQL) 및 핵심 비즈니스 로직의 API 서버(FastAPI) 구축

#### 1.1 개발 환경 및 인프라 구성

- [ ] **PostgreSQL & Redis 설정**
  - Docker Compose를 사용하여 로컬 개발용 PostgreSQL 및 Redis 컨테이너 구성
  - `infrastructure/docker-compose.yml` 작성
- [ ] **FastAPI 프로젝트 초기화**
  - `backend/` 디렉토리 구조 생성
  - Poetry 또는 pip를 이용한 의존성 관리 (`pyproject.toml` / `requirements.txt`)
  - FastAPI 기본 앱 (`main.py`) 및 Health Check 엔드포인트 구현

#### 1.2 데이터베이스 마이그레이션

- [ ] **SQLAlchemy 모델 정의**
  - 기존 Streamlit 앱의 데이터 구조를 분석하여 SQLAlchemy 모델로 변환 (`backend/app/models/`)
- [ ] **Alembic 설정**
  - DB 마이그레이션 도구 Alembic 초기화 및 설정
  - 초기 마이그레이션 스크립트 생성 및 적용
- [ ] **데이터 이관 스크립트 개발**
  - SQLite(`data/roasting_data.db`) 데이터를 PostgreSQL로 이관하는 Python 스크립트 작성 (`scripts/migrate_db.py`)
  - 데이터 무결성 검증 (Row count, 주요 필드 비교)

#### 1.3 핵심 API 개발

- [ ] **인증/인가 (Authentication)**
  - JWT 기반 로그인/회원가입 API 구현 (`/api/v1/auth`)
  - 보안 유틸리티 (Password Hashing, Token 생성) 구현
- [ ] **원두(Beans) 도메인 API**
  - CRUD 엔드포인트 구현 (`GET`, `POST`, `PUT`, `DELETE` `/api/v1/beans`)
  - Pydantic 스키마 정의 (Request/Response DTO)
- [ ] **블렌드(Blends) 도메인 API**
  - 블렌드 생성 및 조회 API
  - 블렌드 원가 계산 로직 이식
- [ ] **재고(Inventory) 도메인 API**
  - 재고 현황 조회 및 입출고 트랜잭션 API

#### 1.4 테스트 및 문서화

- [ ] **단위 테스트 (Unit Tests)**
  - Pytest 설정
  - 각 API 엔드포인트 및 서비스 로직에 대한 테스트 코드 작성
- [ ] **API 문서화**
  - Swagger UI (`/docs`) 확인 및 설명 보강

---

### Phase 2: 프론트엔드 전환 (Frontend Transition)

**목표**: Next.js 기반의 모던 UI 구축 및 하이브리드 운영 시작

- [ ] **Next.js 프로젝트 셋업** (`frontend/`)
  - TypeScript, TailwindCSS, shadcn/ui 설정
- [ ] **API 클라이언트 모듈 구현**
  - Axios 또는 Fetch 기반의 API 통신 모듈 (Interceptors 포함)
- [ ] **핵심 페이지 구현**
  - 로그인 페이지
  - 대시보드 (Dashboard)
  - 원두 관리 리스트 및 상세 페이지
- [ ] **Streamlit 연동 (하이브리드)**
  - 기존 앱에서 신규 페이지로의 링크 연결

---

### Phase 3: 고도화 (Optimization)

**목표**: 실시간 기능, 모바일 최적화, 성능 개선

- [ ] **Celery 비동기 작업 큐 구축**
  - OCR 처리 로직을 Celery Worker로 분리
- [ ] **실시간 알림 (WebSocket)**
  - OCR 처리 완료 알림 구현
- [ ] **PWA 적용**
  - `manifest.json` 및 Service Worker 설정

---

### Phase 4: 완료 (Completion)

**목표**: 레거시 제거 및 완전 전환

- [ ] **나머지 기능 이관**
- [ ] **프로덕션 배포**
- [ ] **Streamlit 코드 제거 및 아카이빙**

---

## 3. 사용자 리뷰 요청 사항 (User Review Required)

> [!IMPORTANT]
> **Phase 1 우선순위 승인**: 현재 계획은 백엔드(DB+API) 구축을 최우선으로 합니다. UI 변경은 Phase 2부터 시작됩니다. 이 순서에 동의하시나요?

> [!NOTE]
> **데이터베이스 변경**: 기존 SQLite 파일(`roasting_data.db`)은 PostgreSQL로 마이그레이션된 후에는 **읽기 전용 백업**으로만 남게 됩니다.

## 4. 검증 계획 (Verification Plan)

### 자동화 테스트

- `pytest`: 백엔드 API 기능 검증 (커버리지 목표 80% 이상)
- `npm run test`: 프론트엔드 컴포넌트 테스트 (Phase 2)

### 수동 검증

- Swagger UI를 통한 API 호출 테스트
- 데이터 이관 후 기존 앱 데이터와 DB 데이터 일치 여부 확인
