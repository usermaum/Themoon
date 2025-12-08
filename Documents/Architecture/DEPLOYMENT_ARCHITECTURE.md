# 🚀 배포 아키텍처 명세서 (Deployment Architecture)

> **프로젝트**: TheMoon - 커피 로스팅 원가 계산 시스템
> **버전**: 0.0.6
> **플랫폼**: Render.com (무료 티어)
> **작성일**: 2025-12-08

---

## 📋 목차

1. [배포 개요](#배포-개요)
2. [Render.com 배포 구조](#rendercom-배포-구조)
3. [환경 변수 관리](#환경-변수-관리)
4. [CI/CD 파이프라인](#cicd-파이프라인)
5. [Health Check & Monitoring](#health-check--monitoring)
6. [Troubleshooting](#troubleshooting)
7. [보안 및 최적화](#보안-및-최적화)

---

## 배포 개요

### 배포 전략

TheMoon 프로젝트는 **Render.com 무료 티어**를 활용하여 프로덕션 환경에 배포됩니다.

```
┌─────────────────────────────────────────────────────────┐
│                     Render.com Cloud                     │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Frontend Service (themoon-frontend)              │  │
│  │  - Next.js 14 (Node.js 18)                       │  │
│  │  - Region: Oregon (us-west-2)                    │  │
│  │  - URL: themoon-frontend-0s4m.onrender.com       │  │
│  └───────────────────┬──────────────────────────────┘  │
│                      │ HTTPS                            │
│                      ↓                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Backend API Service (themoon-api)                │  │
│  │  - FastAPI (Python 3.10+)                        │  │
│  │  - Region: Oregon (us-west-2)                    │  │
│  │  - URL: themoon-api-gv1u.onrender.com            │  │
│  └───────────────────┬──────────────────────────────┘  │
│                      │ PostgreSQL Protocol              │
│                      ↓                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database (themoon-db)                 │  │
│  │  - PostgreSQL 18                                 │  │
│  │  - Database: themoon_p922                        │  │
│  │  - User: themoon                                 │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 배포 환경

| 구분 | 서비스 이름 | 타입 | 리전 | URL |
|------|-----------|------|------|-----|
| **Frontend** | themoon-frontend | Web Service (Node.js) | Oregon | https://themoon-frontend-0s4m.onrender.com |
| **Backend** | themoon-api | Web Service (Python) | Oregon | https://themoon-api-gv1u.onrender.com |
| **Database** | themoon-db | PostgreSQL 18 | Oregon | (내부 연결) |

---

## Render.com 배포 구조

### render.yaml 설정

배포 설정은 `render.yaml` 파일에 정의되어 있습니다.

**파일 위치**: `/mnt/d/Ai/WslProject/Themoon/render.yaml`

#### 1️⃣ Backend API Service

```yaml
services:
  - type: web
    name: themoon-api
    runtime: python
    repo: https://github.com/usermaum/Themoon
    branch: claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck
    plan: free
    region: oregon
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: themoon-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "false"
      - key: BACKEND_CORS_ORIGINS
        value: '["https://themoon-frontend-0s4m.onrender.com"]'
    autoDeployTrigger: commit
```

**설정 설명**:

| 설정 항목 | 값 | 설명 |
|----------|---|------|
| `type` | web | 웹 서비스 타입 (HTTP/HTTPS 지원) |
| `runtime` | python | Python 런타임 (자동으로 최신 Python 3 사용) |
| `rootDir` | backend | 프로젝트 루트가 아닌 backend 폴더를 루트로 설정 |
| `buildCommand` | pip install -r requirements.txt | 빌드 시 의존성 설치 |
| `startCommand` | uvicorn app.main:app --host 0.0.0.0 --port $PORT | FastAPI 앱 실행 (포트는 Render가 자동 할당) |
| `healthCheckPath` | /health | Health Check 엔드포인트 (서비스 상태 모니터링) |
| `autoDeployTrigger` | commit | Git 커밋 시 자동 배포 |

---

#### 2️⃣ Frontend Service

```yaml
  - type: web
    name: themoon-frontend
    runtime: node
    repo: https://github.com/usermaum/Themoon
    branch: claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck
    plan: free
    region: oregon
    rootDir: frontend
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: NEXT_PUBLIC_API_URL
        value: https://themoon-api-gv1u.onrender.com
      - key: NODE_ENV
        value: production
    autoDeployTrigger: commit
```

**설정 설명**:

| 설정 항목 | 값 | 설명 |
|----------|---|------|
| `runtime` | node | Node.js 런타임 (자동으로 최신 Node 18 사용) |
| `rootDir` | frontend | frontend 폴더를 루트로 설정 |
| `buildCommand` | npm install && npm run build | Next.js 프로덕션 빌드 |
| `startCommand` | npm start | 빌드된 Next.js 앱 실행 (포트 3000) |
| `NEXT_PUBLIC_API_URL` | https://themoon-api-gv1u.onrender.com | Backend API URL (클라이언트에서 접근) |
| `NODE_ENV` | production | 프로덕션 모드 활성화 |

---

#### 3️⃣ PostgreSQL Database

```yaml
databases:
  - name: themoon-db
    databaseName: themoon_p922
    user: themoon
    plan: free
    region: oregon
    postgresMajorVersion: "18"
    ipAllowList:
      - source: 0.0.0.0/0
        description: Allow all (for development)
```

**설정 설명**:

| 설정 항목 | 값 | 설명 |
|----------|---|------|
| `databaseName` | themoon_p922 | 데이터베이스 이름 |
| `user` | themoon | 데이터베이스 사용자 |
| `plan` | free | 무료 티어 (90일 후 자동 중지, 수동 재시작 가능) |
| `postgresMajorVersion` | "18" | PostgreSQL 18 (최신 버전) |
| `ipAllowList` | 0.0.0.0/0 | 모든 IP 허용 (개발 단계, 프로덕션에서는 제한 필요) |

**무료 티어 제약사항**:
- **90일 후 자동 중지**: 수동으로 재시작 필요 (Render.com 대시보드)
- **스토리지 제한**: 1GB
- **동시 연결 제한**: 97개

---

## 환경 변수 관리

### Backend 환경 변수

| 환경 변수 | 소스 | 설명 |
|----------|------|------|
| `DATABASE_URL` | 자동 (fromDatabase) | PostgreSQL 연결 문자열<br>예: `postgresql://themoon:password@dpg-xxx.oregon-postgres.render.com/themoon_p922` |
| `SECRET_KEY` | 자동 생성 (generateValue) | JWT 토큰 서명용 비밀 키 (Render가 자동 생성) |
| `DEBUG` | "false" | 프로덕션 모드 (디버그 로그 비활성화) |
| `BACKEND_CORS_ORIGINS` | JSON 배열 | CORS 허용 Origin<br>`["https://themoon-frontend-0s4m.onrender.com"]` |

**로컬 개발 환경 (.env 파일)**:

```env
# .env (backend/.env)
DATABASE_URL=sqlite:///./themoon.db  # 로컬은 SQLite 사용
DEBUG=true
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
SECRET_KEY=your-local-secret-key
```

---

### Frontend 환경 변수

| 환경 변수 | 값 | 설명 |
|----------|---|------|
| `NEXT_PUBLIC_API_URL` | https://themoon-api-gv1u.onrender.com | Backend API URL (브라우저에서 접근) |
| `NODE_ENV` | production | 프로덕션 모드 (최적화 활성화) |

**로컬 개발 환경 (.env.local 파일)**:

```env
# .env.local (frontend/.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**중요**: `NEXT_PUBLIC_` 접두사가 붙은 환경 변수만 브라우저에서 접근 가능 (Next.js 보안 정책)

---

## CI/CD 파이프라인

### 현재 배포 프로세스

Render.com은 **Git 기반 자동 배포**를 제공합니다.

```
┌─────────────────────────────────────────────────────────┐
│                   Git Workflow                          │
└─────────────────────────────────────────────────────────┘
                        │
                        │ git push origin <branch>
                        ↓
┌─────────────────────────────────────────────────────────┐
│              GitHub Repository (Themoon)                │
│  Branch: claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck  │
└─────────────────────────────────────────────────────────┘
                        │
                        │ Webhook Trigger
                        ↓
┌─────────────────────────────────────────────────────────┐
│                 Render.com Auto-Deploy                  │
│  1. Git Clone                                           │
│  2. Install Dependencies                                │
│  3. Build (npm run build / pip install)                 │
│  4. Health Check (/health)                              │
│  5. Zero-Downtime Deploy                                │
└─────────────────────────────────────────────────────────┘
                        │
                        │ Success ✅
                        ↓
┌─────────────────────────────────────────────────────────┐
│              Production Environment                     │
│  - Frontend: https://themoon-frontend-0s4m...           │
│  - Backend: https://themoon-api-gv1u...                 │
└─────────────────────────────────────────────────────────┘
```

### 배포 단계

#### 1️⃣ Git Push

```bash
git add .
git commit -m "feat: 새 기능 추가"
git push origin claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck
```

#### 2️⃣ Render.com 자동 빌드

**Backend (Python)**:
```bash
# Render.com 실행 명령
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Frontend (Node.js)**:
```bash
# Render.com 실행 명령
cd frontend
npm install
npm run build
npm start
```

#### 3️⃣ Health Check

Render.com은 `/health` 엔드포인트를 주기적으로 호출하여 서비스 상태를 확인합니다.

**Health Check 엔드포인트** (backend/app/main.py:74):

```python
@app.get("/health")
def health_check():
    """Health check endpoint for Render.com"""
    return {"status": "healthy", "service": "themoon-api"}
```

**응답 예시**:
```json
{
  "status": "healthy",
  "service": "themoon-api"
}
```

#### 4️⃣ Zero-Downtime Deploy

Render.com은 **Blue-Green Deployment** 전략을 사용합니다:
1. 새 버전 빌드 (Green)
2. Health Check 성공 확인
3. 트래픽을 Green으로 전환
4. 기존 버전 종료 (Blue)

---

### 수동 배포 (Render.com Dashboard)

GitHub Push 없이 수동으로 배포할 수 있습니다:

1. Render.com 대시보드 접속
2. 서비스 선택 (themoon-api 또는 themoon-frontend)
3. **"Manual Deploy"** 버튼 클릭
4. 브랜치 선택 후 배포

---

## Health Check & Monitoring

### Health Check 설정

**엔드포인트**: `GET /health`

**응답 형식**:
```json
{
  "status": "healthy",
  "service": "themoon-api"
}
```

**Render.com 동작**:
- **주기**: 30초마다 Health Check 실행
- **Timeout**: 5초 (5초 내 응답 없으면 실패)
- **Restart Policy**: 3회 연속 실패 시 서비스 자동 재시작

---

### 로그 모니터링

Render.com은 실시간 로그 스트리밍을 제공합니다.

**로그 확인 방법**:

1. **Render.com Dashboard**:
   - 서비스 선택 → **"Logs"** 탭
   - 실시간 로그 스트리밍 (stdout/stderr)

2. **CLI (Render CLI)**:
   ```bash
   # Render CLI 설치
   npm install -g @render-com/cli

   # 로그 스트리밍
   render logs themoon-api
   ```

**로그 예시**:
```
2025-12-08T10:00:00Z INFO:     Uvicorn running on http://0.0.0.0:10000
2025-12-08T10:00:05Z INFO:     Application startup complete.
2025-12-08T10:01:00Z INFO:     GET /health → 200 OK (0.02s)
```

---

### 모니터링 메트릭

Render.com은 기본적으로 다음 메트릭을 제공합니다:

| 메트릭 | 설명 | 확인 방법 |
|--------|------|----------|
| **CPU Usage** | CPU 사용률 (%) | Dashboard → Metrics |
| **Memory Usage** | 메모리 사용량 (MB) | Dashboard → Metrics |
| **HTTP Status** | 응답 상태 코드 (200, 404, 500 등) | Dashboard → Logs |
| **Response Time** | API 응답 시간 (ms) | Dashboard → Logs |

---

## Troubleshooting

### 일반적인 배포 오류

#### 1️⃣ 빌드 실패 (Build Failed)

**증상**: 배포 중 빌드 단계에서 실패

**원인**:
- 의존성 설치 실패 (requirements.txt, package.json 오류)
- Python/Node.js 버전 불일치

**해결 방법**:
```bash
# 로컬에서 빌드 테스트
cd backend
pip install -r requirements.txt  # Python 의존성 확인

cd frontend
npm install  # Node.js 의존성 확인
npm run build  # Next.js 빌드 테스트
```

---

#### 2️⃣ Health Check 실패

**증상**: 빌드 성공했으나 Health Check 실패로 배포 중단

**원인**:
- `/health` 엔드포인트 응답 지연 (5초 초과)
- 데이터베이스 연결 실패

**해결 방법**:
```python
# backend/app/main.py
@app.get("/health")
def health_check():
    # ❌ 나쁜 예: DB 쿼리 (지연 가능)
    # db.query(Bean).count()

    # ✅ 좋은 예: 즉시 응답
    return {"status": "healthy", "service": "themoon-api"}
```

---

#### 3️⃣ CORS 에러

**증상**: 프론트엔드에서 API 호출 시 CORS 에러

**원인**:
- `BACKEND_CORS_ORIGINS` 환경 변수에 프론트엔드 URL 누락

**해결 방법**:
```yaml
# render.yaml (Backend envVars)
- key: BACKEND_CORS_ORIGINS
  value: '["https://themoon-frontend-0s4m.onrender.com"]'
```

**또는 코드에서 직접 설정**:
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://themoon-frontend-0s4m.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

#### 4️⃣ 데이터베이스 연결 실패

**증상**: `OperationalError: could not connect to server`

**원인**:
- `DATABASE_URL` 환경 변수 오류
- IP Allowlist 설정 누락

**해결 방법**:

1. **render.yaml 확인**:
   ```yaml
   envVars:
     - key: DATABASE_URL
       fromDatabase:
         name: themoon-db  # ✅ 데이터베이스 이름 일치 확인
         property: connectionString
   ```

2. **IP Allowlist 확인**:
   ```yaml
   databases:
     - name: themoon-db
       ipAllowList:
         - source: 0.0.0.0/0  # ✅ 모든 IP 허용 (개발)
   ```

---

#### 5️⃣ 무료 티어 제한 (90일 후 중지)

**증상**: 90일 후 데이터베이스 자동 중지

**원인**: Render.com 무료 티어 정책

**해결 방법**:

1. **Render.com Dashboard**:
   - Database 선택 → **"Resume"** 버튼 클릭

2. **유료 플랜 업그레이드** (선택사항):
   - Starter Plan: $7/month (자동 중지 없음)

---

## 보안 및 최적화

### 보안 설정

#### 1️⃣ 환경 변수 암호화

Render.com은 모든 환경 변수를 **암호화하여 저장**합니다.

**중요**: `.env` 파일을 Git에 커밋하지 마세요!

```bash
# .gitignore
.env
.env.local
.env.production
```

---

#### 2️⃣ HTTPS 강제

Render.com은 모든 서비스에 **자동으로 HTTPS를 적용**합니다.

- **SSL 인증서**: Let's Encrypt (자동 갱신)
- **HTTP → HTTPS 리다이렉트**: 자동

---

#### 3️⃣ IP Allowlist (프로덕션)

**개발 단계**:
```yaml
ipAllowList:
  - source: 0.0.0.0/0  # 모든 IP 허용
```

**프로덕션 단계 (권장)**:
```yaml
ipAllowList:
  - source: <Backend Service IP>  # Render.com Backend IP만 허용
    description: Backend API only
```

**Backend Service IP 확인 방법**:
- Render.com Dashboard → Backend Service → Settings → Outbound IPs

---

### 성능 최적화

#### 1️⃣ 무료 티어 제약사항

| 제약사항 | 값 | 영향 |
|---------|---|------|
| **Cold Start** | 최대 30초 | 15분간 요청 없으면 서비스 중지 → 다음 요청 시 재시작 (30초 지연) |
| **CPU** | 0.1 vCPU (공유) | 느린 빌드 (5~10분) |
| **Memory** | 512MB | OOM 위험 (큰 의존성 설치 시) |

**해결 방법**:
- **Ping 서비스 사용**: 15분마다 Health Check 호출 (Cold Start 방지)
  - 예: UptimeRobot (https://uptimerobot.com/)

```bash
# UptimeRobot 설정
Monitor URL: https://themoon-api-gv1u.onrender.com/health
Interval: 5 minutes
```

---

#### 2️⃣ Next.js 최적화

**프로덕션 빌드 최적화**:

```javascript
// next.config.js
module.exports = {
  reactStrictMode: true,
  swcMinify: true,  // ✅ SWC 미니파이어 활성화 (Terser 대비 7배 빠름)
  compress: true,   // ✅ Gzip 압축
  images: {
    domains: ['themoon-api-gv1u.onrender.com'],  // 이미지 최적화
  },
}
```

---

#### 3️⃣ 데이터베이스 연결 풀링

**SQLAlchemy 연결 풀 설정**:

```python
# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,        # ✅ 최대 5개 연결 (무료 티어 제한: 97개)
    max_overflow=10,    # ✅ 임시 추가 연결 10개
    pool_timeout=30,    # ✅ 30초 대기
    pool_recycle=1800,  # ✅ 30분마다 연결 재생성 (PostgreSQL timeout 대비)
)
```

---

## 배포 체크리스트

### 배포 전 확인사항

- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
- [ ] `render.yaml` 파일의 환경 변수가 올바른지 확인
- [ ] 로컬에서 빌드 테스트 완료 (`npm run build`, `pip install -r requirements.txt`)
- [ ] Health Check 엔드포인트 동작 확인 (`GET /health`)
- [ ] CORS 설정 확인 (Frontend URL이 `BACKEND_CORS_ORIGINS`에 포함)
- [ ] 데이터베이스 마이그레이션 완료 (Alembic)
- [ ] Git 커밋 메시지 명확히 작성 (Semantic Versioning)

---

### 배포 후 확인사항

- [ ] Render.com Dashboard에서 배포 성공 확인
- [ ] Health Check 통과 확인 (`GET /health` → 200 OK)
- [ ] Frontend에서 API 호출 테스트 (CORS 에러 없는지 확인)
- [ ] 로그에서 에러 메시지 확인 (Render.com Logs)
- [ ] 데이터베이스 연결 확인 (API에서 데이터 조회 테스트)
- [ ] 성능 테스트 (Cold Start 지연 확인)

---

## 향후 계획

### CI/CD 개선 (Roadmap)

- [ ] **GitHub Actions 통합**
  - 자동 테스트 (pytest, Jest)
  - 코드 품질 검사 (ESLint, Black)
  - 자동 배포 (Render.com Deploy Hook)

- [ ] **Monitoring 강화**
  - Sentry (에러 트래킹)
  - Google Analytics (사용자 분석)

- [ ] **프로덕션 보안 강화**
  - IP Allowlist 제한 (Backend Service IP만 허용)
  - Rate Limiting (DDoS 방지)
  - JWT 인증 활성화

---

## 🔗 관련 문서

**← 상위**: [Documents README](../README.md) | [프로젝트 루트](../../README.md)

**아키텍처 문서**:
- [시스템 개요](SYSTEM_OVERVIEW.md) - 전체 시스템 개요 및 핵심 기능
- [데이터 흐름도](DATA_FLOW.md) - 시스템 내 데이터 흐름 상세 분석
- [데이터베이스 스키마](DATABASE_SCHEMA.md) - 테이블 구조 및 관계도
- [API 명세](API_SPECIFICATION.md) ⭐ - 모든 API 엔드포인트 상세 문서
- [기술 스택](TECHNOLOGY_STACK.md) ⭐ - 사용 기술 상세 설명

**개발 가이드**:
- [개발 가이드](DEVELOPMENT_GUIDE.md) - 5단계 개발 프로세스
- [문제 해결](TROUBLESHOOTING.md) - 16가지 오류 & 해결법

---

**문서 버전**: v1.0
**최종 업데이트**: 2025-12-08
**작성자**: Claude (TheMoon Project Team)
