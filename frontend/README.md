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

---

## 🔗 관련 문서

**← 상위**: [프로젝트 루트](../README.md)

**아키텍처 문서**:
- [시스템 개요](../Documents/Architecture/SYSTEM_OVERVIEW.md) - 전체 시스템 개요 및 핵심 기능
- [데이터 흐름도](../Documents/Architecture/DATA_FLOW.md) - 시스템 내 데이터 흐름 상세 분석
- [API 명세](../Documents/Architecture/API_SPECIFICATION.md) ⭐ - 모든 API 엔드포인트 상세 문서
- [기술 스택](../Documents/Architecture/TECHNOLOGY_STACK.md) ⭐ - 사용 기술 상세 설명
- [배포 아키텍처](../Documents/Architecture/DEPLOYMENT_ARCHITECTURE.md) ⭐ - 배포 환경 상세 구조

**개발 가이드**:
- [개발 가이드](../Documents/Architecture/DEVELOPMENT_GUIDE.md) - 5단계 개발 프로세스
- [컴포넌트 설계](../Documents/Architecture/COMPONENT_DESIGN.md) - UI 컴포넌트 설계 문서
- [문제 해결](../Documents/Architecture/TROUBLESHOOTING.md) - 16가지 오류 & 해결법

**Backend**:
- [Backend README](../backend/README.md) - Backend 개발 가이드

---

**버전:** 1.0.0
**최종 업데이트:** 2025-12-08
