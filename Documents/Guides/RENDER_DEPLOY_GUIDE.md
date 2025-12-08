# 🚀 Render.com 배포 가이드

> **프로젝트**: TheMoon - 커피 로스팅 원가 계산 시스템
> **버전**: 0.0.7
> **플랫폼**: Render.com (무료 티어)
> **작성일**: 2025-12-08

---

## 📋 목차

1. [개요](#개요)
2. [사전 준비](#사전-준비)
3. [수동 배포 방법](#수동-배포-방법)
4. [자동 배포 스크립트 사용](#자동-배포-스크립트-사용)
5. [배포 후 확인](#배포-후-확인)
6. [Troubleshooting](#troubleshooting)

---

## 개요

이 가이드는 TheMoon 프로젝트를 Render.com에 배포하는 전체 과정을 설명합니다.

### 배포 대상

| 서비스 | 타입 | URL | 브랜치 |
|--------|------|-----|-------|
| **Frontend** | Next.js | https://themoon-frontend-0s4m.onrender.com | `claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck` |
| **Backend** | FastAPI | https://themoon-api-gv1u.onrender.com | `claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck` |
| **Database** | PostgreSQL 18 | (내부) | - |

---

## 사전 준비

### 1. 환경 확인

```bash
# Git 상태 확인
git status

# 모든 변경사항 커밋되었는지 확인
git log --oneline -1
```

### 2. 로컬 빌드 테스트

배포 전에 로컬에서 빌드 테스트를 수행합니다.

**Backend 테스트**:
```bash
cd backend
pip install -r requirements.txt
python -m pytest  # 테스트 실행 (선택사항)
```

**Frontend 테스트**:
```bash
cd frontend
npm install
npm run build  # 프로덕션 빌드 테스트
npm start      # 빌드된 앱 실행 테스트
```

### 3. 환경 변수 확인

**render.yaml 확인**:
```yaml
# Backend 환경 변수
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: themoon-db
  - key: BACKEND_CORS_ORIGINS
    value: '["https://themoon-frontend-0s4m.onrender.com"]'

# Frontend 환경 변수
envVars:
  - key: NEXT_PUBLIC_API_URL
    value: https://themoon-api-gv1u.onrender.com
```

---

## 수동 배포 방법

### 방법 1: Git Push로 자동 배포

**1단계: 배포 브랜치로 전환**

```bash
# 배포 브랜치로 전환
git checkout claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck

# main 브랜치 최신 변경사항 병합
git merge main -m "merge: main 브랜치 변경사항 병합"
```

**2단계: 변경사항 푸시**

```bash
# 원격 저장소에 푸시
git push origin claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck
```

**3단계: Render.com 자동 배포 대기**

- Render.com이 자동으로 배포를 시작합니다 (약 5~10분 소요)
- Dashboard에서 배포 로그 실시간 확인 가능

### 방법 2: Render.com Dashboard에서 수동 배포

**1단계: Render.com 접속**

https://dashboard.render.com 접속

**2단계: 서비스 선택**

- `themoon-api` (Backend) 또는
- `themoon-frontend` (Frontend) 선택

**3단계: Manual Deploy 실행**

1. 상단의 **"Manual Deploy"** 버튼 클릭
2. 브랜치 선택: `claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck`
3. **"Deploy"** 버튼 클릭

**4단계: 배포 로그 확인**

- "Logs" 탭에서 실시간 배포 진행 상황 확인
- Health Check 성공 확인 (`GET /health → 200 OK`)

---

## 자동 배포 스크립트 사용

프로젝트 루트에 자동 배포 스크립트가 제공됩니다.

### 스크립트 파일

- **`deploy-render.sh`** - Render.com 자동 배포 스크립트

### 사용 방법

**1. 스크립트 실행 권한 부여** (최초 1회):

```bash
chmod +x deploy-render.sh
```

**2. 스크립트 실행**:

```bash
# 기본 사용 (자동 배포)
./deploy-render.sh

# 커밋 메시지 지정
./deploy-render.sh "feat: 새로운 기능 추가"

# 도움말 확인
./deploy-render.sh --help
```

### 스크립트 동작 과정

1. ✅ 현재 브랜치 확인
2. ✅ main 브랜치 최신 변경사항 병합
3. ✅ 로컬 빌드 테스트 (Backend + Frontend)
4. ✅ Git 커밋 (변경사항이 있는 경우)
5. ✅ 배포 브랜치로 푸시
6. ✅ 배포 완료 메시지 출력

### 스크립트 출력 예시

```
🚀 Render.com 배포 시작...

📌 현재 브랜치: claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck
✅ 배포 브랜치 확인 완료

🔄 main 브랜치 최신 변경사항 병합 중...
✅ 병합 완료

🧪 로컬 빌드 테스트 중...
  ├─ Backend 빌드 테스트...
  │  ✅ requirements.txt 의존성 확인 완료
  └─ Frontend 빌드 테스트...
     ✅ Next.js 빌드 완료

📦 변경사항 커밋 중...
✅ 커밋 완료: deploy: Render.com 배포 준비 완료

🚢 배포 브랜치에 푸시 중...
✅ 푸시 완료

✅ 배포 성공!

📊 배포 상태 확인:
  Frontend: https://themoon-frontend-0s4m.onrender.com
  Backend:  https://themoon-api-gv1u.onrender.com

⏳ Render.com에서 자동 배포 진행 중 (약 5~10분 소요)

📍 배포 로그 확인:
  https://dashboard.render.com
```

---

## 배포 후 확인

### 1. Health Check 확인

**Backend Health Check**:

```bash
curl https://themoon-api-gv1u.onrender.com/health
```

**예상 응답**:
```json
{
  "status": "healthy",
  "service": "themoon-api"
}
```

### 2. Frontend 접속 확인

브라우저에서 접속:

https://themoon-frontend-0s4m.onrender.com

### 3. API 연결 확인

Frontend에서 Backend API 호출이 정상적으로 작동하는지 확인:

1. 원두 목록 페이지 접속
2. 데이터 로딩 확인
3. CORS 에러 발생 여부 확인 (브라우저 콘솔)

### 4. 배포 로그 확인

**Render.com Dashboard**:

1. https://dashboard.render.com 접속
2. `themoon-api` 또는 `themoon-frontend` 선택
3. "Logs" 탭에서 로그 확인

**주요 확인 사항**:
- ✅ 빌드 성공 (`Build succeeded`)
- ✅ Health Check 통과 (`GET /health → 200 OK`)
- ✅ 서비스 시작 (`Uvicorn running on...`)
- ❌ 에러 메시지 없음

---

## Troubleshooting

### 문제 1: 빌드 실패 (Build Failed)

**증상**:
```
ERROR: Could not install packages due to an EnvironmentError
```

**해결 방법**:

1. **로컬에서 빌드 테스트**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **의존성 버전 확인**:
   ```bash
   # requirements.txt에서 충돌하는 패키지 확인
   pip check
   ```

3. **Python 버전 확인**:
   ```yaml
   # render.yaml에 Python 버전 명시
   runtime: python
   buildCommand: |
     python --version
     pip install -r requirements.txt
   ```

---

### 문제 2: Health Check 실패

**증상**:
```
Health check failed: GET /health returned 503
```

**해결 방법**:

1. **Health Check 엔드포인트 확인**:
   ```python
   # backend/app/main.py
   @app.get("/health")
   def health_check():
       return {"status": "healthy", "service": "themoon-api"}
   ```

2. **로그에서 에러 확인**:
   - Render.com Dashboard → Logs
   - 데이터베이스 연결 오류 확인

3. **타임아웃 확인**:
   - Health Check는 5초 내에 응답해야 함
   - DB 쿼리 제거하고 즉시 응답하도록 수정

---

### 문제 3: CORS 에러

**증상**:
```
Access to fetch at 'https://themoon-api-gv1u.onrender.com/api/v1/beans/'
from origin 'https://themoon-frontend-0s4m.onrender.com' has been blocked by CORS policy
```

**해결 방법**:

1. **render.yaml 확인**:
   ```yaml
   envVars:
     - key: BACKEND_CORS_ORIGINS
       value: '["https://themoon-frontend-0s4m.onrender.com"]'
   ```

2. **코드에서 CORS 설정 확인**:
   ```python
   # backend/app/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://themoon-frontend-0s4m.onrender.com"
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **환경 변수 재배포**:
   - render.yaml 수정 후 다시 푸시

---

### 문제 4: 데이터베이스 연결 실패

**증상**:
```
OperationalError: (psycopg2.OperationalError) could not connect to server
```

**해결 방법**:

1. **DATABASE_URL 환경 변수 확인**:
   ```yaml
   # render.yaml
   envVars:
     - key: DATABASE_URL
       fromDatabase:
         name: themoon-db  # ✅ 데이터베이스 이름 정확히 일치
         property: connectionString
   ```

2. **IP Allowlist 확인**:
   ```yaml
   # render.yaml
   databases:
     - name: themoon-db
       ipAllowList:
         - source: 0.0.0.0/0  # 모든 IP 허용
   ```

3. **수동으로 DATABASE_URL 확인**:
   - Render.com Dashboard → Database → Info
   - External Database URL 복사
   - Backend Service → Environment → DATABASE_URL에 직접 입력

---

### 문제 5: Cold Start 지연 (무료 티어)

**증상**:
- 15분간 요청이 없으면 서비스 자동 중지
- 다음 요청 시 30초 지연

**해결 방법**:

1. **Ping 서비스 사용** (UptimeRobot):
   - URL: https://themoon-api-gv1u.onrender.com/health
   - Interval: 5분

2. **유료 플랜 업그레이드**:
   - Starter Plan: $7/month
   - Cold Start 없음

---

## 배포 체크리스트

### 배포 전 ✅

- [ ] 로컬에서 빌드 테스트 완료
- [ ] `git status`로 변경사항 확인
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
- [ ] `render.yaml` 환경 변수 확인
- [ ] CORS 설정 확인 (Frontend URL 포함)
- [ ] Health Check 엔드포인트 동작 확인

### 배포 후 ✅

- [ ] Render.com Dashboard에서 배포 성공 확인
- [ ] Health Check 통과 확인 (`/health → 200 OK`)
- [ ] Frontend 접속 확인
- [ ] API 연결 확인 (CORS 에러 없음)
- [ ] 로그에서 에러 메시지 확인
- [ ] 데이터베이스 연결 확인

---

## 🔗 관련 문서

**← 상위**: [Documents README](../README.md) | [프로젝트 루트](../../README.md)

**아키텍처 문서**:
- [배포 아키텍처](../Architecture/DEPLOYMENT_ARCHITECTURE.md) - Render.com 상세 구조 및 CI/CD
- [시스템 개요](../Architecture/SYSTEM_OVERVIEW.md) - 전체 시스템 개요
- [API 명세](../Architecture/API_SPECIFICATION.md) - API 엔드포인트 상세

**개발 가이드**:
- [문제 해결](../Architecture/TROUBLESHOOTING.md) - 16가지 오류 & 해결법
- [개발 가이드](../Architecture/DEVELOPMENT_GUIDE.md) - 5단계 개발 프로세스

---

**문서 버전**: v1.0
**최종 업데이트**: 2025-12-08
**작성자**: Claude (TheMoon Project Team)
