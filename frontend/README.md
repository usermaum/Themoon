# TheMoon Frontend (Next.js)

커피 로스팅 원가 계산 시스템 프론트엔드

## 📌 원본 참조

이 프로젝트는 Streamlit 기반 원본을 Next.js로 완전히 재작성한 버전입니다.

**원본 프로젝트:** `/mnt/d/Ai/WslProject/TheMoon_Project/app/pages/`

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 설정

`.env.local` 파일 생성:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. 개발 서버 실행

```bash
npm run dev
```

**접속:** http://localhost:3000

## 📁 프로젝트 구조

```
frontend/
├── app/
│   ├── page.tsx           # 메인 페이지
│   ├── layout.tsx         # 레이아웃
│   └── globals.css        # 글로벌 스타일
├── components/
│   └── ui/                # UI 컴포넌트
├── lib/
│   └── api.ts             # API 클라이언트
├── public/
├── package.json
└── README.md
```

## 🔗 원본 대응표

| 원본 (Streamlit) | 신규 (Next.js) | 설명 |
|------------------|----------------|------|
| `pages/Dashboard.py` | `app/page.tsx` | 메인 대시보드 |
| `pages/BeanManagement.py` | `app/beans/page.tsx` | 원두 관리 |
| `pages/BlendManagement.py` | `app/blends/page.tsx` | 블렌드 관리 |
| `components/` | `components/` | 재사용 컴포넌트 |

## 🎨 스타일링

- **Tailwind CSS:** 유틸리티 기반 스타일링
- **shadcn/ui:** 재사용 가능한 컴포넌트 라이브러리

## 📚 개발 가이드

원본 프로젝트의 UI/UX를 참조하되, 모던한 웹 표준으로 재작성합니다:

1. **페이지 작성:** 원본 `TheMoon_Project/app/pages/` 참조
2. **컴포넌트 작성:** 재사용 가능하도록 설계
3. **API 통신:** `lib/api.ts` 사용
4. **상태 관리:** React Hooks (useState, useEffect)

## 🔧 빌드

```bash
# 프로덕션 빌드
npm run build

# 프로덕션 실행
npm run start
```

## 🚢 Render.com 배포

### 자동 배포 (추천)

Backend와 함께 자동으로 배포됩니다. 프로젝트 루트의 `render.yaml` 파일에서 설정됩니다.

**1. GitHub 연동**
- Render.com 대시보드에서 "New +" → "Blueprint" 선택
- GitHub 저장소 연결
- `render.yaml` 파일이 자동으로 감지됨

**2. 환경 변수 (자동 설정)**

Render가 자동으로 설정하는 환경 변수:
- `NEXT_PUBLIC_API_URL`: Backend API URL (themoon-api에서 자동 참조)

**3. 배포 확인**
- 배포 로그에서 빌드 진행 상황 확인
- 배포 완료 후 제공되는 URL로 접속

**배포 URL 예시:**

https://themoon-frontend.onrender.com

### 수동 배포 (개별 서비스)

개별적으로 Frontend만 배포하려면:

**1. Render 대시보드에서 "New +" → "Web Service"**

**2. 설정**
```
Name: themoon-frontend
Runtime: Node
Build Command: npm install && npm run build
Start Command: npm start
Branch: main (또는 원하는 브랜치)
Root Directory: frontend
```

**3. 환경 변수 추가**
```
NEXT_PUBLIC_API_URL=https://your-backend-api.onrender.com
```

### 주요 설정 파일

- `render.yaml`: Render 배포 설정 (프로젝트 루트)
- `.env.example`: 환경 변수 템플릿
- `package.json`: 빌드 스크립트 정의
- `next.config.js`: Next.js 설정

### 트러블슈팅

**문제: API 연결 오류**
```
해결: NEXT_PUBLIC_API_URL 환경 변수가 올바르게 설정되었는지 확인
      브라우저 콘솔에서 API URL 확인
```

**문제: 빌드 실패**
```
해결: package.json의 의존성 버전 확인
      Node.js 버전 확인 (권장: 18.x 이상)
```

**문제: 환경 변수가 적용되지 않음**
```
해결: NEXT_PUBLIC_ 접두사가 있는지 확인
      Next.js는 클라이언트 사이드 환경 변수에 NEXT_PUBLIC_ 필요
      빌드 시점에 환경 변수가 번들에 포함됨
```

### 배포 후 CORS 설정

Frontend 배포 후, Backend의 CORS 설정을 업데이트해야 합니다:

**Backend Render 환경 변수 업데이트:**
```
BACKEND_CORS_ORIGINS='["https://themoon-frontend.onrender.com"]'
```

---

**버전:** 0.0.1
**최종 업데이트:** 2025-11-25 (Render.com 배포 설정 추가)
