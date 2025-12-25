# The Moon Drip Bar - 배포 가이드

## 🚀 배포 아키텍처

- **Frontend**: Cloudflare Pages (Next.js)
- **Backend**: Railway (FastAPI + PostgreSQL)
- **Database**: Railway PostgreSQL

---

## 📦 Backend 배포 (Railway)

### 1. Railway 프로젝트 설정

1. [Railway](https://railway.app)에 가입/로그인
2. "New Project" → "Deploy from GitHub repo" 선택
3. `TheMoon` 레포지토리 선택
4. "Add PostgreSQL" 클릭하여 데이터베이스 추가

### 2. 환경 변수 설정

Railway 프로젝트 설정에서 다음 환경 변수를 추가:

```bash
# 자동 생성됨 (PostgreSQL 추가 시)
DATABASE_URL=postgresql://...

# 직접 추가
DEBUG=False
CORS_ORIGINS=https://your-app.pages.dev,http://localhost:3500
SECRET_KEY=your-super-secret-key-change-this
```

### 3. 배포 설정

Railway는 `Procfile`과 `requirements.txt`를 자동 감지합니다.

**Root 디렉토리 설정**: `backend`로 변경
- Railway 설정 → Settings → Root Directory: `backend`

### 4. 배포 확인

- Railway가 자동으로 빌드 및 배포
- 배포 완료 후 제공된 URL 확인 (예: `https://your-app.railway.app`)
- `/docs`로 접속하여 API 문서 확인

---

## 🌐 Frontend 배포 (Cloudflare Pages)

### 1. Cloudflare Pages 프로젝트 생성

1. [Cloudflare Dashboard](https://dash.cloudflare.com) 로그인
2. "Pages" → "Create a project" → "Connect to Git"
3. GitHub 레포지토리 연결

### 2. 빌드 설정

```yaml
Build command: npm run build
Build output directory: .next
Root directory: frontend
Framework preset: Next.js
```

### 3. 환경 변수 설정

```bash
NEXT_PUBLIC_API_URL=https://your-app.railway.app
```

**중요**: Railway 백엔드 URL을 여기에 입력!

### 4. 배포

- "Save and Deploy" 클릭
- 빌드 완료 후 제공된 URL로 접속 (예: `https://your-app.pages.dev`)

---

## 🔄 데이터베이스 마이그레이션 (SQLite → PostgreSQL)

현재 SQLite를 사용 중이므로, PostgreSQL로 마이그레이션이 필요합니다.

### Option 1: 새로 시작 (권장)

Railway PostgreSQL이 자동으로 테이블을 생성합니다 (`Base.metadata.create_all`).

### Option 2: 데이터 이전

로컬 SQLite 데이터를 PostgreSQL로 이전:

```bash
# 1. 로컬 Railway CLI 설치
npm install -g @railway/cli

# 2. Railway 로그인
railway login

# 3. 프로젝트 연결
railway link

# 4. 데이터베이스 URL 가져오기
railway variables

# 5. Python 스크립트로 데이터 이전
# (별도 스크립트 필요)
```

---

## ✅ 배포 체크리스트

### Backend (Railway)
- [ ] PostgreSQL 데이터베이스 추가
- [ ] 환경 변수 설정 (DATABASE_URL, CORS_ORIGINS, SECRET_KEY)
- [ ] Root Directory를 `backend`로 설정
- [ ] 배포 성공 확인
- [ ] `/docs` 접속하여 API 문서 확인

### Frontend (Cloudflare Pages)
- [ ] Build 설정 완료 (framework: Next.js)
- [ ] Root Directory를 `frontend`로 설정
- [ ] `NEXT_PUBLIC_API_URL` 환경 변수 설정 (Railway URL)
- [ ] 배포 성공 확인
- [ ] CORS 에러 없이 API 호출 확인

### Database
- [ ] 테이블 자동 생성 확인
- [ ] 첫 원두 데이터 등록 테스트

---

## 🛠️ 트러블슈팅

### CORS 에러

Backend `main.py`의 `origins`에 Cloudflare Pages URL 추가:

```python
origins = [
    "http://localhost:3500",
    "https://your-app.pages.dev",  # 추가
]
```

### 데이터베이스 연결 실패

Railway 환경 변수에서 `DATABASE_URL` 확인:
- PostgreSQL URL 형식: `postgresql://user:pass@host:port/db`

### 빌드 실패 (Frontend)

- Node.js 버전 확인 (18.x 이상)
- `package.json`에 빌드 스크립트 존재 확인

---

## 📝 참고 링크

- [Railway 문서](https://docs.railway.app/)
- [Cloudflare Pages 문서](https://developers.cloudflare.com/pages/)
- [Next.js 배포 가이드](https://nextjs.org/docs/deployment)

---

## 🎉 배포 완료!

모든 단계가 완료되면:
1. Cloudflare Pages URL로 접속
2. 원두 등록 테스트
3. 모든 기능 동작 확인

문제 발생 시:
- Railway 로그 확인
- Cloudflare Pages 빌드 로그 확인
- 브라우저 개발자 도구 Network 탭 확인
