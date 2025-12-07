# 완전 무료 배포 가이드 (Vercel + Render)

## 🎯 배포 아키텍처

- **Frontend**: Vercel (Next.js) - 100% 무료
- **Backend**: Render (FastAPI) - 무료 티어
- **Database**: Render PostgreSQL - 무료 티어

---

## 📦 사전 준비

### 1. GitHub 레포지토리 생성

```bash
cd /mnt/d/Ai/WslProject/TheMoon

# Git 초기화 (아직 안했다면)
git init
git add .
git commit -m "Initial commit: The Moon Drip Bar"

# GitHub에 레포지토리 생성 후
git remote add origin https://github.com/YOUR_USERNAME/TheMoon.git
git branch -M main
git push -u origin main
```

### 2. 계정 준비

- [Vercel](https://vercel.com) - GitHub 계정으로 가입
- [Render](https://render.com) - GitHub 계정으로 가입

---

## 🗄️ 1단계: Database 배포 (Render PostgreSQL)

### 1-1. PostgreSQL 인스턴스 생성

1. Render 대시보드 → "New +" → "PostgreSQL"
2. 설정:
   - **Name**: `themoon-db`
   - **Database**: `themoon`
   - **User**: 자동 생성
   - **Region**: Singapore (가장 가까운 지역)
   - **Plan**: **Free** 선택
3. "Create Database" 클릭

### 1-2. 연결 정보 복사

생성 완료 후 **Internal Database URL** 복사 (나중에 사용):
```
postgresql://themoon_db_user:xxxxx@dpg-xxxxx-a.singapore-postgres.render.com/themoon_db
```

---

## 🐍 2단계: Backend 배포 (Render Web Service)

### 2-1. Web Service 생성

1. Render 대시보드 → "New +" → "Web Service"
2. GitHub 레포지토리 연결 (TheMoon)
3. 설정:
   - **Name**: `themoon-api`
   - **Region**: Singapore
   - **Branch**: main
   - **Root Directory**: `backend`
   - **Runtime**: Python 3.12
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: **Free** 선택

### 2-2. 환경 변수 설정

"Environment" 탭에서 추가:

```bash
# 데이터베이스 (1단계에서 복사한 URL)
DATABASE_URL=postgresql://themoon_db_user:xxxxx@dpg-xxxxx-a.singapore-postgres.render.com/themoon_db

# CORS (Vercel 배포 후 업데이트)
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# 기타
DEBUG=False
SECRET_KEY=your-random-secret-key-change-this-12345
```

### 2-3. 배포

"Create Web Service" 클릭 → 자동 배포 시작 (5-10분 소요)

배포 완료 후 URL 확인:
```
https://themoon-api.onrender.com
```

테스트: `https://themoon-api.onrender.com/docs` 접속

---

## 🌐 3단계: Frontend 배포 (Vercel)

### 3-1. Vercel 프로젝트 생성

1. [Vercel Dashboard](https://vercel.com/dashboard) → "Add New" → "Project"
2. GitHub 레포지토리 선택 (TheMoon)
3. 설정:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (자동 감지)
   - **Output Directory**: `.next` (자동 감지)

### 3-2. 환경 변수 설정

"Environment Variables" 섹션에서 추가:

```bash
NEXT_PUBLIC_API_URL=https://themoon-api.onrender.com
```

**중요**: Render Backend URL을 정확히 입력!

### 3-3. 배포

"Deploy" 클릭 → 자동 빌드 및 배포 (3-5분)

배포 완료 후 URL 확인:
```
https://themoon-xxxxx.vercel.app
```

---

## 🔗 4단계: CORS 업데이트

Frontend 배포 완료 후 Vercel URL을 Backend CORS에 추가:

### Render Backend 환경 변수 업데이트

```bash
BACKEND_CORS_ORIGINS=["https://themoon-xxxxx.vercel.app","http://localhost:3000"]
```

변경 후 자동 재배포됨.

---

## ✅ 배포 확인

### 체크리스트

1. [ ] Render PostgreSQL 생성 완료
2. [ ] Render Backend 배포 완료
   - [ ] `/docs` 접속 성공
   - [ ] API 문서 표시됨
3. [ ] Vercel Frontend 배포 완료
   - [ ] 메인 페이지 로드 성공
4. [ ] CORS 설정 완료
5. [ ] 원두 등록 테스트 성공
6. [ ] 모든 기능 동작 확인

### 테스트

1. Frontend URL 접속
2. 원두 관리 → 새 원두 등록
3. 블렌드 레시피 → 새 블렌드 생성
4. 재고 관리 → 입출고 처리
5. 대시보드에서 통계 확인

---

## ⚠️ 무료 티어 제약사항

### Render 무료 티어

**슬립 모드**
- 15분 미사용 시 자동 슬립
- 첫 요청 시 10-30초 소요 (콜드 스타트)
- 해결: 정기적인 핑 서비스 사용 (UptimeRobot 등)

**PostgreSQL 90일 제한**
- 90일 후 비활성화됨 (데이터는 유지)
- 재활성화 가능 (무료)
- 해결: 90일마다 재활성화 또는 유료 전환 ($7/월)

**성능 제한**
- 512MB RAM
- 0.1 CPU
- 100GB 대역폭/월

### Vercel 무료 티어

- 100GB 대역폭/월 (충분함)
- 100GB-hours 실행 시간
- 상업용 프로젝트 제한 (개인 프로젝트는 OK)

---

## 🔧 트러블슈팅

### Backend가 슬립에서 깨어나지 않음

**원인**: 무료 티어 슬립 모드
**해결**: 1분 정도 기다리거나, UptimeRobot으로 정기적 핑

### CORS 에러

**확인사항**:
1. Render 환경 변수의 `BACKEND_CORS_ORIGINS`에 Vercel URL 포함 확인
2. Frontend `NEXT_PUBLIC_API_URL`이 Render URL과 일치하는지 확인
3. 브라우저 개발자 도구에서 실제 요청 URL 확인

### 데이터베이스 연결 실패

**확인사항**:
1. Render PostgreSQL이 "Available" 상태인지 확인
2. `DATABASE_URL` 형식이 올바른지 확인
3. Render Backend 로그에서 에러 메시지 확인

### 빌드 실패

**Frontend (Vercel)**:
- Root Directory가 `frontend`로 설정되었는지 확인
- `package.json`에 모든 의존성이 포함되어 있는지 확인

**Backend (Render)**:
- Root Directory가 `backend`로 설정되었는지 확인
- `requirements.txt`가 최신인지 확인

---

## 💡 비용 절감 팁

### 1. UptimeRobot으로 슬립 방지 (무료)

[UptimeRobot](https://uptimerobot.com)에서:
- 5분마다 Backend URL 핑
- 슬립 모드 방지
- 무료 플랜으로 충분

### 2. 데이터베이스 백업

90일 제한 대비 정기 백업:
```bash
# Railway CLI로 백업 (선택사항)
pg_dump $DATABASE_URL > backup.sql
```

### 3. 유료 전환 고려 (필요 시)

프로젝트가 성장하면:
- Render PostgreSQL: $7/월
- Render Web Service: $7/월
- **총 $14/월로 슬립 모드 없이 사용 가능**

---

## 🎉 완료!

모든 단계가 완료되면:
- Frontend: `https://themoon-xxxxx.vercel.app`
- Backend API: `https://themoon-api.onrender.com`
- Database: Render PostgreSQL

**100% 무료로 운영 가능!**

처음 사용자는 10-30초 대기 후 정상 작동합니다.

---

## 📚 참고 링크

- [Vercel 문서](https://vercel.com/docs)
- [Render 문서](https://render.com/docs)
- [Render Free Tier 가이드](https://render.com/docs/free)
