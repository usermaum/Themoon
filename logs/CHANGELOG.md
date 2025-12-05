# 변경 로그 (Changelog)

모든 주목할 만한 프로젝트 변경사항은 이 파일에 문서화됩니다.

## 버전 관리 규칙 (Semantic Versioning)

- **MAJOR.MINOR.PATCH** 형식 사용
  - MAJOR: 대규모 기능 추가 또는 호환성 깨지는 변경
  - MINOR: 새로운 기능 추가 (하위 호환성 유지)
  - PATCH: 버그 수정 (하위 호환성 유지)

---

## [0.1.1] - 2025-12-06

### 🚑 Hotfixes
- **Inbound**: API 라우터 누락 수정 (404 Not Found 해결) 및 Mock OCR 모드 추가.
- **Server**: `BeanService` CRUD 함수 구현 및 의존성 라이브러리(`google-generativeai`) 설치.
- **UI**: 다크모드 문제 해결을 위한 Light Mode 강제 설정.
- **Database**: SQLite 스키마 동기화 (재구축).

---

## [0.1.0] - 2025-12-06

### ✨ Features (Major Update)

**블렌딩 관리 시스템 (Blending Management)**
- **UI**: 블렌드 레시피 생성 및 생산 관리 페이지 (`/blends`) 구현.
- **Backend**: `BlendService` 리팩토링 (Bean+Recipe 관계), 가중 평균 단가(Weighted Average Cost) 기반 생산 로직 적용.
- **Stock**: 생산 시 실시간 재료 재고 차감 및 블렌드 입고 처리 자동화.

**대시보드 고도화 (Advanced Dashboard)**
- **UI**: 실시간 재고 가치/중량, 안전 재고 경고, 최근 활동 로그 시각화.
- **Analytics**: `InventoryLog` 데이터 기반 정확한 자산 가치 산정.
- **Inbound**: 입고 시 영수증 OCR 품목명 자동 매칭 (Fuzzy Matching) 도입.

**기타 개선 사항 (Stabilization)**
- **Roasting**: 로스팅 이력(History) 조회 기능 및 손실률(Loss Rate) 표시 테이블 추가.
- **Settings**: 언어 설정 및 시스템 정보를 확인할 수 있는 설정 페이지(`settings/page.tsx`) 구현.

### 🛠️ Data Model
- **InventoryLog**: `TransactionType` 확장 (`BLENDING_IN/OUT`, `ROASTING_IN/OUT` 등 상세 구분).
- **Bean**: `cost_price` 필드 표준화 및 `avg_cost_price` 레거시 로직 제거.

---

## [Unreleased] - 2025-12-05

### ✨ Features

**원두 목록 필터링 (Bean Filtering)**
- 생두(Green Bean)와 원두(Roasted Bean) 구분 조회 기능 추가
- Backend: `roast_level` 쿼리 파라미터 및 필터링 로직 구현 (`bean_service.py`, `beans.py`)
- Frontend: 원두 관리 페이지 상단 필터 탭 UI 추가 (`beans/page.tsx`)

**언어 전환기 (Language Switcher)**
- 사이드바 하단에 언어 전환 버튼(KO/EN) 추가 (`Sidebar.tsx`)
- `LanguageSwitcher` 컴포넌트 통합

### 🐛 Bug Fixes

**페이지네이션 카운트 수정**
- 필터링 적용 시 전체 개수(`total`)가 갱신되지 않는 문제 해결 (`get_beans_count`)

### 🔧 Configuration

**IDE 설정**
- `.vscode/settings.json` 추가: Tailwind CSS 경고 억제

### 🚑 Hotfixes & UAT

**Dashboard Hydration Fix**
- `Dashboard` 컴포넌트 로직을 `app/page.tsx`로 이동하여 클라이언트 사이드 데이터 페칭 안정화.
- 초기 로딩 시 레이아웃 깨짐 및 Hydration Error 완벽 해결.

**UAT 최적화**
- `BeanForm`: 자동화 테스트 호환성을 위해 표준 HTML Input/Select로 리팩토링 (UI 스타일은 유지).
- `InventoryPage`: 로직 검증 완료 후 Premium UI (Mantine Button/ScrollArea) 복구.

---

## [Unreleased] - 2025-11-30

### ✨ Features

**사이드바 툴팁 시스템**
- 토글 버튼 툴팁 추가 (사이드바 펼치기/접기)
- 모든 메뉴 아이템 툴팁 추가 (Home, Beans, Blends, Inventory)
- Settings 버튼 툴팁 추가
- CSS group-hover 기반 커스텀 툴팁 구현
- 다크모드 완벽 대응
- z-index 계층 구조 정립 (Backdrop: 90, Sidebar: 100, Tooltips: 200)

### 🐛 Bug Fixes

**툴팁 표시 문제 해결**
- overflow-y-auto와 overflow-x-visible 동시 사용 불가 문제 해결
- nav/ul/li 태그의 overflow 제약 제거 (→ div로 교체)
- PageHero 컴포넌트 z-index 조정 (툴팁 가려짐 해결)
- main 요소 z-index 설정 (Sidebar보다 낮게)
- 불필요한 overflow-y-auto 완전 제거 (메뉴 4개로 스크롤 불필요)

**.gitignore 수정**
- logs/ 폴더 제외 → logs/*.log 파일만 제외
- 버전 관리 파일들은 정상 추적되도록 수정

### 🔧 Refactoring

**사이드바 구조 개선**
- nav 태그 → div 태그로 교체 (의미론적 HTML보다 실용성 우선)
- ul/li 태그 → div 태그로 교체 (overflow 문제 해결)
- 3중 구조 → 2중 구조로 단순화
- 메뉴 아이템 group 구조 개선 (li → div.relative.group)

### 📄 Documentation

**세션 문서**
- `SESSION_SUMMARY_2025-11-30.md` 상세 작성
- 툴팁 구현 및 문제 해결 과정 9단계 기록
- CSS overflow/z-index 관련 학습 내용 정리

### 🛠️ Technical Details

**변경된 파일** (5개)
- `.gitignore` - logs/ 폴더 제외 규칙 수정
- `frontend/components/layout/Sidebar.tsx` - 툴팁 추가 및 구조 개선
- `frontend/components/layout/AppLayout.tsx` - main z-index 설정
- `frontend/components/ui/PageHero.tsx` - z-index 조정

**커밋 통계**
- 총 커밋: 13개
- feat: 2개, fix: 10개, refactor: 1개

---

## [Unreleased] - 2025-11-29

### ✨ Features

**프론트엔드 레이아웃 시스템 개선**
- AppLayout 컴포넌트 추가 (사이드바 상태 관리)
- Sidebar 컴포넌트 추가 (접기/펴기 기능, lucide-react 아이콘)
- 쿠키 기반 사이드바 상태 저장 (1년 유지)
- 반응형 모바일 지원 (모바일 메뉴 버튼, 백드롭)
- 스크롤바 스타일 유틸리티 추가 (scrollbar-hide, scrollbar-thin)

**네비게이션 구조**
- Home, Beans, Blends, Inventory 메뉴 추가
- Settings 및 User 프로필 영역 추가
- 활성 페이지 하이라이트 (indigo 색상)

### 📄 Documentation

**로스팅 문서 정리 및 최적화**
- `Themoon_Rostings.md` 중복 제거 (625줄 → 466줄, 25% 감소)
- 섹션 2, 3, 6 중복 내용 제거 및 통합
- 명세서 데이터 4.2~4.11 복구 (11건 전체)

**Word 보고서 생성**
- 전문적인 Word 문서 `더문_로스팅_운영계획안.docx` 생성 (13KB)
- 5개 메인 섹션: 개요, 원두 마스터, 블렌딩 레시피, 운영 시나리오, 명세서 데이터
- 목차 자동 생성, 표 스타일, 색상 스키마 적용
- docx 라이브러리 사용 (Node.js)

**세션 관리**
- `SESSION_SUMMARY_2025-11-29.md` 작성
- 문서 정리 및 Word 생성 작업 기록

### 🛠️ Technical

**프론트엔드 컴포넌트**
- `frontend/components/layout/AppLayout.tsx` - 메인 레이아웃 컨테이너
- `frontend/components/layout/Sidebar.tsx` - 사이드바 네비게이션
- `frontend/app/globals.css` - 커스텀 스크롤바 유틸리티

**파일 생성**
- `create_roasting_manual.js` - Word 문서 생성 스크립트
- `package.json`, `package-lock.json` - Node.js 프로젝트 설정

---

## [0.0.3] - 2025-11-26

### 🚀 Render.com 배포 완료 및 Production 환경 구축

#### 🎯 주요 작업

**PostgreSQL 호환성 개선 (2025-11-26 추가)**
- SQLite → PostgreSQL 마이그레이션을 위한 모델 타입 수정
  - String 타입에 명시적 길이 지정 (PostgreSQL 필수)
    - `blend.py`: name(200), target_roast_level(50)
    - `inventory_log.py`: transaction_type(20)
  - 긴 텍스트 필드를 Text 타입으로 변경
    - `blend.py`: description, notes
    - `inventory_log.py`: reason
  - DateTime 타임스탬프 개선
    - `func.now()` → `func.current_timestamp()`로 변경 (PostgreSQL 호환성)
  - 영향 받는 파일: `bean.py`, `blend.py`, `inventory_log.py`

**Render.com 배포 설정**
- `render.yaml` 완전 구성 (Backend, Frontend, PostgreSQL 18)
- Backend: `/health` 엔드포인트 추가
- Frontend: `NEXT_PUBLIC_API_URL` 환경 변수 설정
- Database: PostgreSQL 18 + 자동 연결 (`themoon_p922`)

**Production 빌드 오류 해결**
1. PostgreSQL 버전: 16 → 18로 변경
2. Backend 의존성 단순화: 38개 → 10개 필수 패키지
3. Frontend 의존성 구조 개선: devDependencies → dependencies 이동
   - `autoprefixer`, `postcss`, `tailwindcss`
   - `typescript`, `@types/node`, `@types/react`, `@types/react-dom`
4. Path Alias 해결: 3단계 설정
   - `tsconfig.json`: moduleResolution "node", baseUrl "."
   - `jsconfig.json`: 신규 생성
   - `next.config.js`: 명시적 webpack alias

**Database 연결 및 검증 로직**
- `backend/app/database.py`: postgres:// → postgresql:// 자동 변환
- `backend/app/main.py`: lifespan 이벤트 (테이블 자동 생성)
- 연결 정보 디버그 로깅 추가

**Data Validation 개선**
- `backend/app/schemas/bean.py`: @field_validator 추가
  - 빈 문자열('') → None 자동 변환
  - Optional 필드 검증 강화

**UI 개선**
- 메뉴: "Dashboard" → "Home" 변경
- `frontend/components/layout/Navbar.tsx` 수정

**개발 환경 최적화**
- `start_backend.sh`: venv 자동 관리, 포트 충돌 해결
- `start_frontend.sh`: 캐시 삭제 옵션, 대화형 메뉴
- `start_all.sh`: Backend + Frontend 동시 실행
- CRLF → LF 라인 엔딩 수정

#### 🐛 해결된 오류

1. **PostgreSQL 버전 다운그레이드 불가**: 16 → 18
2. **metadata-generation-failed**: 의존성 단순화
3. **autoprefixer 모듈 누락**: dependencies 이동
4. **Path Alias 해결 실패**: 3단계 설정
5. **TypeScript 패키지 누락**: dependencies 이동
6. **원두 등록 실패**: field_validator 추가
7. **원두 목록 로드 실패**: Database URL 변환 + 로깅
8. **스크립트 라인 엔딩**: CRLF → LF

#### 📊 통계
- 수정된 파일: 12개
- 추가된 파일: 6개 (스크립트 3개, 설정 파일 3개)
- 해결된 배포 오류: 8건
- Git 커밋: 15개

#### 🔗 배포 URL
- Backend: `https://themoon-api.onrender.com`
- Frontend: `https://themoon-frontend.onrender.com`
- Database: `dpg-d4is05qli9vc73epqth0-a.oregon-postgres.render.com/themoon_p922`

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
