# 변경 로그 (Changelog)

모든 주목할 만한 프로젝트 변경사항은 이 파일에 문서화됩니다.

## 버전 관리 규칙 (Semantic Versioning)

- **MAJOR.MINOR.PATCH** 형식 사용
  - MAJOR: 대규모 기능 추가 또는 호환성 깨지는 변경
  - MINOR: 새로운 기능 추가 (하위 호환성 유지)
  - PATCH: 버그 수정 (하위 호환성 유지)

---

## [0.0.2] - 2025-11-24

### ✨ Phase 3 완료 - 블렌드 레시피 및 재고 관리 시스템

#### 🎯 주요 기능

**Backend (FastAPI)**
- 블렌드 레시피 관리 API (CRUD)
  - `backend/app/api/v1/endpoints/blends.py` - 블렌드 엔드포인트
  - `backend/app/models/blend.py` - 블렌드 모델
  - `backend/app/schemas/blend.py` - 블렌드 스키마
  - `backend/app/services/blend_service.py` - 블렌드 비즈니스 로직

- 재고 관리 시스템 (입출고 처리)
  - `backend/app/api/v1/endpoints/inventory_logs.py` - 재고 엔드포인트
  - `backend/app/models/inventory_log.py` - 재고 로그 모델
  - `backend/app/schemas/inventory_log.py` - 재고 로그 스키마
  - `backend/app/services/inventory_log_service.py` - 재고 비즈니스 로직

**Frontend (Next.js)**
- 블렌드 레시피 페이지
  - `frontend/app/blends/page.tsx` - 블렌드 목록
  - `frontend/app/blends/new/page.tsx` - 블렌드 등록
  - `frontend/app/blends/[id]/page.tsx` - 블렌드 상세
  - `frontend/components/blends/BlendForm.tsx` - 블렌드 폼 컴포넌트

- 재고 관리 페이지
  - `frontend/app/inventory/page.tsx` - 재고 현황 및 입출고 관리

- 원두 관리 페이지
  - `frontend/app/beans/page.tsx` - 원두 목록
  - `frontend/app/beans/new/page.tsx` - 원두 등록
  - `frontend/app/beans/[id]/page.tsx` - 원두 상세
  - `frontend/components/beans/BeanForm.tsx` - 원두 폼 컴포넌트

**UI/UX 개선**
- 배경 이미지 적용
  - `frontend/public/beans_background.png` - 원두 관리 배경
  - `frontend/public/blends_background.png` - 블렌드 배경
  - `frontend/public/inventory_background.png` - 재고 관리 배경

- 공통 컴포넌트
  - `frontend/components/ui/PageHero.tsx` - 페이지 히어로 (배경 이미지 지원)
  - `frontend/components/ui/Card.tsx` - 카드 컴포넌트
  - `frontend/components/ui/Carousel.tsx` - 캐러셀 컴포넌트
  - `frontend/components/layout/Navbar.tsx` - 네비게이션 바
  - `frontend/components/layout/Footer.tsx` - 푸터
  - `frontend/components/home/Hero.tsx` - 홈 히어로

**배포 설정**
- `DEPLOYMENT.md` - 배포 가이드
- `DEPLOYMENT_FREE.md` - 무료 배포 가이드
- `backend/Procfile` - Heroku 배포 설정
- `backend/runtime.txt` - Python 버전 명시
- `backend/.env.example` - 환경 변수 예시
- `render.yaml` - Render.com 배포 설정

#### 📊 통계
- 추가된 파일: 37개
- 수정된 파일: 13개
- 추가된 코드: 9,446줄
- 삭제된 코드: 183줄

---

## [0.0.1] - 2025-11-23

### 🎉 초기 릴리스 (Initial Release): Clean Slate - 프로젝트 완전 재시작

#### 📝 개요

Gemini 3 Pro가 작성한 복잡한 마이그레이션 구조를 완전히 제거하고, **깨끗한 프로젝트로 재시작**했습니다.

**원본 프로젝트:** `/mnt/d/Ai/WslProject/TheMoon_Project/` (Streamlit 기반)
**새 프로젝트:** `/mnt/d/Ai/WslProject/Themoon/` (Next.js + FastAPI)

#### 🎯 전략: Clean Slate (Option 3)

기존 Streamlit 앱을 **참조용으로만** 사용하고, 모든 코드를 **최신 Best Practice**로 새로 작성합니다.

#### 📊 주요 성과

| 항목 | Before (Gemini) | After (Clean Slate) | 개선율 |
|------|-----------------|---------------------|--------|
| **총 크기** | 17MB | 36KB | **99.8% ↓** |
| **총 파일** | 632개 | 17개 | **97% ↓** |
| **Backend 파일** | 538개 | 8개 | **98.5% ↓** |
| **Frontend 파일** | 미완성 | 9개 | **완성** |
| **코드 중복** | 심각 (2곳) | 0% | **완전 제거** |

#### 🗑️ 삭제된 구조 (Gemini 작업물)

```
❌ 삭제:
- app/               (94개 Python 파일, 1.9MB)   - 원본 Streamlit 복사
- backend/           (538개 Python 파일, 15MB)   - 7배 비대화된 구조
- frontend/          (48KB)                       - 미완성 Next.js
- infrastructure/    (Docker 설정)
- implementation_plan.md, run_*.sh
```

#### ✅ 생성된 깨끗한 구조

**Backend (FastAPI) - 8개 파일, 20KB**
```
backend/
├── app/
│   ├── __init__.py          # 버전 정보
│   ├── main.py              # FastAPI 앱 (50줄)
│   ├── config.py            # 설정 관리
│   └── database.py          # DB 연결
├── requirements.txt         # 필수 의존성만
└── README.md                # 개발 가이드
```

**Frontend (Next.js) - 9개 파일, 16KB**
```
frontend/
├── app/
│   ├── page.tsx             # 메인 페이지
│   ├── layout.tsx           # 레이아웃
│   └── globals.css          # 스타일
├── lib/
│   └── api.ts               # API 클라이언트
├── package.json
├── tsconfig.json
└── README.md
```

#### 📚 작성된 문서

1. **README.md** (405줄, 완전 재작성)
   - 원본 프로젝트 참조 시스템
   - 개발 원칙 3가지
   - 원본 대응표
   - 기술 스택 상세

2. **Documents/Progress/SESSION_SUMMARY_2025-11-23.md**
   - 세션 전체 진행 상황
   - Before/After 비교
   - 다음 단계 계획

3. **Documents/Planning/CLEAN_SLATE_STRATEGY.md**
   - 전략 수립 과정
   - 3가지 옵션 비교
   - 실행 계획 및 결과

#### 🎓 핵심 원칙

1. **완전 재작성 (Clean Slate)**
   - 원본 코드를 참조용으로만 사용
   - 모든 코드를 최신 Best Practice로 새로 작성
   - 기술 부채 없이 깨끗하게 시작

2. **원본 로직 보존**
   - 비즈니스 로직은 원본과 동일하게 작동
   - 계산 로직, 데이터 모델 구조 유지
   - 기능 동등성 (Feature Parity) 보장

3. **모던 아키텍처**
   - Frontend/Backend 완전 분리
   - RESTful API 기반
   - TypeScript 타입 안정성
   - 테스트 우선 개발

#### 🛠️ 기술 스택

**Backend:**
- FastAPI 0.109+
- Python 3.12+
- PostgreSQL 15+
- SQLAlchemy 2.0+
- Pydantic 2.5+
- JWT 인증

**Frontend:**
- Next.js 14.1+
- TypeScript 5.3+
- React 18.2+
- Tailwind CSS 3.4+
- shadcn/ui

#### 🔗 커밋

- `73e7bfa`: refactor: Gemini 복잡한 구조 제거, 완전히 깨끗한 프로젝트로 재시작
  - 119 files changed, 929 insertions(+), 32288 deletions(-)
  - 97% 코드 감소
  - 중복 완전 제거

- `f674174`: fix: FastAPI import 오류 수정 및 README.md 전면 개편
  - ImportError 해결 (crud 모듈 제거)
  - README.md 884줄 재작성

#### 🚀 다음 단계

**Week 1-2: Backend 기초**
- [ ] Bean 모델 (원본 참조)
- [ ] Bean 스키마 (Pydantic)
- [ ] Bean 서비스 (원본 로직)
- [ ] Bean API 엔드포인트
- [ ] Bean 테스트

**Week 3-4: Frontend 기초**
- [ ] Bean 관리 페이지
- [ ] API 연동
- [ ] UI 컴포넌트
- [ ] 상태 관리

---

**참고:**
- 이전 버전 기록 (0.50.4 이하)은 원본 프로젝트 참조: `/mnt/d/Ai/WslProject/TheMoon_Project/logs/CHANGELOG.md`
