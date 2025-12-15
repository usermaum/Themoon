# 변경 로그 (Changelog)

모든 주목할 만한 프로젝트 변경사항은 이 파일에 문서화됩니다.

## 버전 관리 규칙 (Semantic Versioning)

- **MAJOR.MINOR.PATCH** 형식 사용
  - MAJOR: 대규모 기능 추가 또는 호환성 깨지는 변경
  - MINOR: 새로운 기능 추가 (하위 호환성 유지)
  - PATCH: 버그 수정 (하위 호환성 유지)

---

## [Unreleased]

## [0.0.9] - 2025-12-15

### 🐛 Fixed

- **Unknown Bean Matching**: 블렌드 페이지 및 인벤토리에서 'Unknown Bean'이 표시되는 문제 해결.
  - 원인: 프론트엔드 SWR 훅(`useBeans`, `useInventoryLogs`)에서 `skip`/`limit` 파라미터를 사용했으나, 백엔드는 `page`/`size`를 기대함. 백엔드가 `limit` 파라미터를 무시하고 기본값(page=1, size=10)을 적용하여 10번째 이후 항목이 리스트에서 누락됨.
  - 해결: `useBeans`와 `useInventoryLogs` 훅을 수정하여 `skip`/`limit`을 `page`/`size` 파라미터로 올바르게 변환하여 전송하도록 변경.

- **Bean Type Mismatch**: '원두' 탭에 블렌드가 표시되고 '블렌드' 탭이 비어있는 문제 수정.
  - 원인: DB 내 블렌드 상품들의 타입이 `ROASTED_BEAN`으로 잘못 설정됨.
  - 해결: 데이터 마이그레이션을 통해 해당 상품들의 타입을 `BLEND_BEAN`으로 수정.

### ✨ Features

- **Blend Recipes UI**: 블렌드 레시피 구성 비율 막대에 애니메이션 효과 적용.
  - `design-showcase`의 Progress 애니메이션 스타일 이식.
  - 레시피 비율이 부드럽게 차오르는 모션 추가.

- **Beans Filtering**: 원두 목록 페이지에 탭 기반 필터링 기능 추가.
  - 분류: 전체 / 생두 / 원두 / 블렌드.
  - 즉각적인 리스트 필터링 및 페이지네이션 연동.

- **Beans Empty State Logic**: 데이터 없음 화면 개선.
  - 검색 결과가 없을 때: 검색 초기화 버튼 제공.
  - 탭별(블렌드/원두 등) 데이터 없을 때:
    - 블렌드: "블렌드 생성 (Pre-Roast)" 버튼 표시 (링크: `/roasting/blend`).
    - 원두: "싱글 오리진 로스팅" 버튼 표시.
    - 생두/전체: "첫 번째 원두 등록하기" 버튼 표시.
  - 데이터 없는 경우 페이징(1/1) 컨트롤 숨김 처리.
  - 컴포넌트 (통계 카드, 알림 배지, 버튼, 폼 요소)
  - 레이아웃 (대시보드, 그리드)
  - 인터랙션 (호버 효과, 로딩 상태, 애니메이션)
  - Sidebar에 Design Demo 메뉴 추가
- **Inventory UX**: 재고 관리 페이지 탭 전환 애니메이션 개선 (Slide Up + Fade).

### 📝 Documentation

- **문서 동기화 개선**: 문서 4종 세트 → 5종 세트로 확장.
  - `.gemini/GEMINI.md` 추가 (Gemini용 프로젝트 가이드)
  - `.claude/CLAUDE.md`와 함께 버전 동기화 대상 관리

### 🐛 Fixed

- **Inventory Pagination**: 재고 현황 페이징 시 입출고 기록이 불필요하게 재조회되는 문제 해결 (State Isolation).
- **Bean Name Display**: 입출고 기록 테이블에서 페이징 시 원두 이름이 잘못 표시되거나 사라지는 문제 수정 (Backend Schema Update & Frontend Logic Fix).

## [0.0.8] - 2025-12-09

### ✨ Features

- **Animation Page**: `design-sample/animation` 페이지 추가. Shadcn UI + Framer Motion 활용한 애니메이션 갤러리 구현.

### 🐛 Fixed

- **Dashboard Crash**: `app/page.tsx`에서 `recentLogs.map` 런타임 오류 수정 (API 응답 타입 안전성 강화).
- **Inventory Logs**: 재고 관리 페이지에서 입출고/수정/삭제 후 목록 갱신 시 `fetchLogs` 인자 누락(`logTab`)으로 인한 빌드/런타임 오류 수정.

## [0.0.7] - 2025-12-08

### ✨ Features

- **Roasted Bean Images**: 전체 원두 및 블렌드 로스팅 이미지 생성 완료 (19종, 35개 파일).
  - 전체 리스트: `frontend/public/images/roasted/`
  - V3 프롬프트 적용 완료.

- **Components Demo Page**: Shadcn UI 컴포넌트 데모 페이지 확장 (`frontend/app/components-demo/page.tsx`).
  - 추가된 컴포넌트: Accordion, Dialog, Carousel, Table, Calendar 등 모든 기본 UI 요소 통합.

### 🐛 Fixed

- **Carousel Component**: `Carousel` 컴포넌트의 Named Export 누락 오류 수정.
  - `CarouselContent`, `CarouselItem`, `CarouselNext`, `CarouselPrevious` export 추가.

- **Mobile Sidebar**: 모바일 환경에서 사이드바가 닫혔을 때 화면 밖으로 완전히 사라지지 않던 문제 해결 (`-translate-x-full` 클래스 적용).
- **Sidebar Margin**: 데스크탑에서 사이드바가 닫혔을 때 메인 컨텐츠 영역의 여백이 사이드바 너비(80px)와 맞지 않던 문제 해결 (`ml-16` -> `ml-[80px]`).
- **Bean Image Mapping**: 원두 목록 페이지(`beans`)에서 로스팅된 원두 및 블렌드 원두의 이미지가 올바르게 표시되도록 매핑 로직(`getBeanImage`) 개선.
- **Blend Image Logic**: '풀문', '뉴문', '이클립스' 등 특정 블렌드 이름이 포함된 경우 '블렌드' 키워드가 없어도 올바른 이미지를 표시하도록 수정.
- **Pagination**: 원두 목록 페이지의 페이징 상태를 URL 쿼리 파라미터(`?page=N`)와 동기화하여 새로고침 시에도 현재 페이지가 유지되도록 개선.
- **Inventory Pagination**: 재고 관리 페이지(`inventory`)의 '현재 재고 현황' 및 '입출고 기록' 테이블에 페이징 기능 추가. `?beanPage=N&logPage=N`으로 URL과 상태 동기화.
- **Inventory Filtering**: 재고 현황 탭(전체/생두/원두) 클릭 시 서버 사이드 필터링 적용 및 페이징 연동. API/Service에 `bean_types` 필터 지원 추가.
- **Inventory Tabs**: '블렌드' 탭 추가 및 '원두' 탭을 싱글 오리진 전용으로 분리하여 필터링 정확도 개선. 탭 상태(`?tab=...`) URL 동기화 적용.
- **Mobile Responsive**: 재고 관리 페이지의 테이블이 모바일 환경에서 깔끔하게 보이도록 일부 컬럼(유형, 특징, 원산지 등)을 숨기고 가로 스크롤 및 배치 최적화.

### 📄 Documentation

- **Architecture Documentation (6종)**: 프로젝트 아키텍처 문서 체계 완성
  - `API_SPECIFICATION.md`: RESTful API 엔드포인트 명세 (요청/응답/에러 코드) ⭐ NEW!
  - `TECHNOLOGY_STACK.md`: 기술 스택 선정 이유 및 버전 정보 ⭐ NEW!
  - `DEPLOYMENT_ARCHITECTURE.md`: Render.com 배포 구조 및 CI/CD 파이프라인 ⭐ NEW!
  - `SYSTEM_OVERVIEW.md`: 시스템 전체 개요 및 핵심 기능 정의
  - `DATA_FLOW.md`: 데이터 흐름도 및 프로세스 간 상호작용
  - `DATABASE_SCHEMA.md`: PostgreSQL 데이터베이스 스키마 (ERD, 테이블 정의)

- **Document Navigation Links**: 전체 문서 네비게이션 링크 추가
  - `Documents/README.md`: 모든 문서 이름을 클릭 가능한 링크로 변환 (50+ 문서)
  - `Documents/Architecture/*.md`: 양방향 네비게이션 링크 추가 (6개 문서)
  - `backend/README.md`, `frontend/README.md`: 아키텍처 문서 링크 추가
  - 루트 `README.md`: 핵심 아키텍처 문서 섹션 추가

- **Render.com Deployment System**: Render.com 자동 배포 시스템 구축 ⭐ NEW!
  - `Documents/Guides/RENDER_DEPLOY_GUIDE.md`: 배포 가이드 문서 작성 (수동/자동 배포 방법, Troubleshooting)
  - `deploy-render.sh`: 자동 배포 스크립트 작성 (main 병합, 빌드 테스트, 자동 푸시)
  - 배포 브랜치: `claude/render-deeply-016Jz7DRD33bXZjAo158y3Ck`

- **Session Summary**: 2025-12-08 세션 진행 상황 및 다음 단계 업데이트.
- **Bean Image Prompts**: V3 문서 업데이트 (모든 이미지 생성 완료 상태로 변경).

---

## [0.0.6] - 2025-12-07

### ✨ Features

- **SWR Data Fetching**: 프론트엔드 데이터 페칭 시스템 도입
  - `swr` 패키지 설치 및 전역 설정 (`lib/swr-config.tsx`)
  - 커스텀 훅: `use-beans.ts`, `use-blends.ts`, `use-inventory.ts`
  - 자동 재검증, 에러 재시도, 포커스 시 리프레시 기능
  - 백엔드 재시작 시 프론트엔드 자동 데이터 갱신

- **Roasting Menu**: 사이드바에 'Roasting' 메뉴 추가 (`/roasting/single-origin`).

- **Roasted Bean Images**: V3 프롬프트 기반 로스팅 원두 이미지 생성
  - 16개 완료 (1~8번 품목 신콩/탄콩)
  - 저장 경로: `frontend/public/images/roasted/`

### 🐛 Fixed

- **Variety Data Normalization**: 품종 필드 "한글 (영문)" 형식으로 통일
  - `fix_variety.py` 스크립트로 16개 품목 DB 직접 수정
  - 예: `Mormora` → `모모라 (Mormora)`

- **Bean Image Matching**: `getBeanImage()` 함수 개선
  - 키린야가/마사이 구분 (둘 다 Kenya origin)
  - 모모라 검색어 추가 (모모라, 모르모라 둘 다 체크)
  - 후일라 검색어 추가 (후일라, 우일라)

- **Inventory API 404**: `inventory_logs` 라우터 등록 완료.
- **Inventory Schema Mismatch**: Pydantic/SQLAlchemy 필드명 불일치 해결.
- **Frontend API Types**: `InventoryLog`, `InventoryLogCreateData` 완전 구현.
- **Sidebar Border/Shadow**: 사이드바 접힘 시 세로 줄무늬 해결.
- **Database Synchronization**: DB 파일 위치 오류 해결.
- **CORS Configuration**: 프론트엔드 포트 CORS 설정 추가.

### 🔧 Refactoring

- **Home Hero**: 메인 페이지 Hero 컴포넌트 스타일 통일.
- **Single Origin Roasting**: 목표 생산량 기반 자동 계산 로직 및 UI 개선.
- **Blend Roasting**: 블렌드 로스팅 기능 구현.

### 📄 Documentation

- **Documents 폴더 재구조화**: 6개 분류 체계 정립
  - Architecture, Guides, Planning, Progress, Reports, Resources
- **Documents/README.md**: 문서 인덱스 생성
- **루트 문서 이동**: DEPLOYMENT.md, TEST_REPORT.md 등 적절한 폴더로 이동
- **Session Summary**: 2025-12-07 세션 요약 작성

- **Roasting Validation**: 로스팅 비즈니스 로직(싱글/블렌드) 검증 스크립트(`test_roasting_logic.py`) 작성 및 테스트 완료.
- **Mobile Responsive**: 모바일 화면에서 사이드바가 닫혀 있을 때 완전히 숨겨지도록 수정.

---

## [0.1.0] - 2025-12-06

### ✨ Features

**Cafe Latte Art Theme Integration**

- **Global Theme**: 전체 프론트엔드에 'Cafe Latte Art' 디자인 테마 적용 (크림색 배경, Serif 폰트, 둥근 모서리).
- **Shadcn UI**: `Button`, `Input`, `Badge`, `Card` 등 핵심 컴포넌트를 Shadcn UI 기반으로 새로 구현 및 테마 스타일링.
- **Design System**: Tailwind CSS 설정에 `latte` 색상 팔레트 및 `blob` 포인트 컬러 추가.

### 🔧 Refactoring

**Page Refactoring**

- **Home**: 대시보드 통계 카드 및 최근 활동 테이블에 새로운 디자인 적용.
- **Beans**: 원두 관리 페이지 테이블 및 검색 UI 개선.
- **Blends**: 블렌드 레시피 카드 디자인 고도화.
- **Inventory**: 재고 관리 페이지 모달 및 테이블 UI를 Shadcn 컴포넌트로 전면 교체.

**Component Upgrades**

- **PageHero**: 배경 블롭(Blob) 효과 및 아이콘 통합으로 시각적 퀄리티 향상.
- **Card**: Compound Component 패턴(`CardHeader`, `CardContent` 등) 도입으로 유연성 확보.

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

## [0.0.4] - 2025-12-06

### 추가됨 (Added)

- **Green Bean Vault**: 생두 재고 현황 시각화 페이지 구현 (app/design-sample/green-bean-vault).
- **Bean Prompts V2/V3**: 생두(V2) 및 원두(V3) 이미지 생성을 위한 고해상도 프롬프트 문서 작성.
- **Server Scripts Enhancement**: WSL 내부 IP 접속 지원 및 포트 3500 변경 (dev.sh, start_all.sh).

### 변경됨 (Changed)

- **Frontend Engine**: Next.js 14, React 18, Tailwind CSS 3로 엔진 업데이트 및 안정화.
- **Network Config**: 로컬호스트 바인딩 오류 해결을 위해 0.0.0.0 호스트 설정 적용.

### 수정됨 (Fixed)

- WSL2 환경에서 윈도우 업데이트 후 발생한 localhost 연결 거부 문제 해결.

- **Roasting Process Implementation**:
  - Backend: `Bean`(고도화), `InventoryLog`(Enum 적용) 모델 및 스키마 업데이트.
  - Backend: `create_single_origin_roasting` 서비스 로직 및 API 엔드포인트 구현.
  - Frontend: `roasting/single-origin` 로스팅 UI 페이지 구현 (생두 선택, 손실률 계산).
  - Database: `recreate_db` 스크립트 작성 및 자동 시딩 로직(`lifespan`) 추가.
