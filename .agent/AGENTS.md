# AI Agents Common Manifesto (AGENTS.md)

> **Master Rules for All AI Agents**
> This file is the **Single Source of Truth** for strict project rules.
> Whether you are **Claude** or **Gemini**, you MUST follow these instructions.

---

## 🏗️ 아키텍처 원칙 (Clean Architecture Standard)

> **2025-12-23 도입**: 점진적 적용을 위한 하이브리드 전략
> **적용 대상**: `Bean` 모듈(Refactoring) 및 **모든 신규 기능**(Phase 2+)

### 1. Repository Pattern 필수 (Repository Pattern)

* **원칙**: `Service` Layer에서 `db.query()`, `db.add()`, `db.commit()` 등을 직접 호출하지 않습니다.
* **구현**: 모든 DB 접근은 `app/repositories/*` 패키지 내의 Repository 클래스를 통해서만 수행합니다.
* **이유**: 비즈니스 로직과 데이터 접근 기술(SQLAlchemy)의 분리, 테스트 용이성 확보, 장기적 유지보수성 향상.

### 2. 의존성 규칙 (Dependency Rule)

* ✅ `Controller (Router)` → `Service` → `Repository` → `Model`
* ❌ `Service`가 `Controller(HTTP Request 등)` 의존 금지.
* ❌ `Repository`가 `UI/Web` 관련 로직 의존 금지.

### 3. 서비스 순수성 (Service Purity)

* Service 메서드는 오직 **Pydantic Schema**나 **Primitive Type** 만을 인자로 받고 반환해야 합니다.
* `FastAPI.Request`, `FastAPI.Depends` 등의 웹 프레임워크 객체를 Service 내부로 침투시키지 마십시오.

---

## 🗣️ 언어 규칙 (MANDATORY)

**중요**: 사용자는 영어 초보자입니다. 모든 대화, **결과 설명, 체크 상황, 진행 상태** 등 사용자가 읽어야 하는 모든 텍스트는 **반드시 한글**로 작성해야 합니다.

* 코드, 로그, 에러 메시지 원본은 영어로 유지하되, **반드시 한글 설명**을 덧붙여야 합니다.
* "Checking..." 같은 진행 상황도 "확인 중..."과 같이 한글로 표현해야 합니다.

---

## 🛠️ 핵심 도구 및 기술 스택 (MANDATORY)

작업 시 다음 도구와 기술을 **무조건** 사용해야 합니다:

1. **AI 도구 & MCP**:

   * **Context7**: 라이브러리 문서 및 컨텍스트 검색  상황에따라 판단하여 사용 필수 아님.
2. **Frontend Tech Stack**:

   * **Framework**: Next.js (App Router)
   * **UI Library**: **Shadcn UI** (v2, CSS Modules)
3. **Documentation Tools**:

   * **Mermaid**: 모든 아키텍처, 플로우, ERD 다이어그램은 **반드시 Mermaid 문법**으로 작성합니다. (이미지 업로드 지양)
     * **v8.8.0 호환성 필수**: `subgraph ID [Label]` 문법 사용 금지 → `subgraph "Label"` 또는 `subgraph ID ["Label"]` 사용.
     * **특수문자 Quoting**: 괄호 `()`, 대괄호 `[]` 등이 포함된 노드 라벨은 반드시 쌍따옴표로 감싸야 합니다. 예: `Node["Label (Info)"]`
     * **Subgraph 연결 금지**: Subgraph 간 직접 연결 화살표 금지 → 내부 노드끼리 연결.

---

## 🎯 개발 프로세스 (7 Steps)

**모든 프로그래밍 작업은 이 순서를 따를 것!**

```text
1️⃣ Constitution (원칙) → 기본 원칙 수립
2️⃣ Specify (명세) → 무엇을 만들지 정의
3️⃣ Clarify (명확화) → 불분명한 부분 질문으로 해소
4️⃣ Plan (계획) → 기술 스택과 아키텍처 결정
5️⃣ Tasks (작업 분해) → 작은 단위로 쪼개기 (TodoWrite 사용)
6️⃣ Implement (구현) → 코드 작성 및 테스트 (Clean Architecture 준수)
7️⃣ Analyze (검증) → 명세 대비 검증
```

**❌ 금지**: 명세 없이 바로 코딩, 추측으로 진행, 검증 없이 완료

---

## 🚨 작업 완료 3단계 (필수)

**모든 작업은 아래 3단계를 완료해야만 "완료"**

```text
1️⃣ 코드/테스트 작성 완료
   ↓
2️⃣ git commit (한글 메시지)
   ↓
3️⃣ 문서 업데이트 (필수!) - 누락 시 작업 미완료 간주
   ✅ logs/CHANGELOG.md
   ✅ docs/Progress/SESSION_SUMMARY_YYYY-MM-DD.md
   ✅ README.md (버전 동기화)
   ✅ .agent/AGENTS.md (필요 시 업데이트)
```

**❌ 금지**: 커밋 후 문서 업데이트 없이 다음 작업으로 넘어가기

---

## 🔗 URL 작성 규칙 (MANDATORY)

**❌ 절대 금지**:

```text
웹앱은 http://localhost:3500에서 실행 중입니다!  ← URL 뒤에 한글 붙음
```

**✅ 반드시**:

```text
웹앱이 실행되었습니다:

http://localhost:3500

위 주소로 접속하세요.
```

**핵심**: URL 앞뒤로 반드시 공백/줄바꿈, URL 바로 뒤에 한글/특수문자 금지

---

## 💻 코딩 컨벤션

### Backend (Python/FastAPI)

* **타입 힌팅 필수**: `def get_user(user_id: int) -> User:`
* **Docstring**: 중요 함수에 작성
* **파일명**: `snake_case` (예: `bean_service.py`)
* **클래스**: `PascalCase` (예: `BeanService`)
* **함수**: `snake_case` (예: `get_bean_by_id`)
* **Lint**: `check_quality.sh` 통과 필수 (Black, Pylint, Mypy)

### Frontend (TypeScript/Next.js)

* **타입 정의 필수**: `interface`, `type` 활용
* **함수형 컴포넌트** 사용
* **컴포넌트**: `PascalCase` (예: `BeanCard.tsx`)
* **유틸**: `camelCase` (예: `formatPrice.ts`)
* **에러 핸들링**: try-catch 필수
* **Lint**: `npm run lint` 통과 필수

---

## 🔖 버전 관리

### 커밋 메시지 컨벤션

```bash
feat: 원두 관리 페이지 추가
fix: 가격 계산 오류 수정
refactor: Bean 서비스 리팩토링
docs: README 업데이트
chore: 패키지 업데이트
test: 테스트 추가
```

### 버전 업데이트 기준

**작업 완료 후**: `git commit` (버전 업데이트 ❌)

**세션 종료 시**: 누적 기준 확인 후 버전 올림

```text
PATCH: 버그 3개 이상 OR 문서 5개 이상 누적 (주 1~3회)
MINOR: 새 기능 3~4개 이상 추가 (월 1회)
MAJOR: 호환성 변경 (년 1~2회)
```

---

## 📋 세션 관리 (Session Protocol)

### 세션 시작 시

```bash
# 1. 체크리스트 확인
cat docs/Progress/SESSION_START_CHECKLIST.md

# 2. 최신 세션 요약 읽기
ls -lt docs/Progress/SESSION_SUMMARY_*.md | head -1
```

### 세션 종료 시

```bash
# 1. 종료 체크리스트 완료
cat docs/Progress/SESSION_END_CHECKLIST.md

# 2. 세션 요약 작성 (docs/Progress/SESSION_SUMMARY_YYYY-MM-DD.md)

# 3. 버전 업데이트 (누적 기준 충족 시)
./venv/bin/python logs/update_version.py --type patch --summary "요약"

# 4. 모든 문서 버전 동기화
```

---

## 🚫 절대 금지 사항

**원본 프로젝트 코드 복사 금지** (참조만 가능)

**새로운 세션 관리 파일 생성 금지** (기존 체계 유지)

**작은 변경사항마다 버전 올리기 금지** (세션 종료 시 일괄 처리)

**영어 답변 금지** (한글 설명 필수)

---

## 🔄 Context Handover Protocol (Last updated by Agent)

> **이 섹션은 AI가 세션을 시작할 때 자동으로 읽어들이는 "기억" 영역입니다.**
> **세션 종료 전 반드시 AI에게 "상태 저장해줘" 또는 "세션 종료"를 요청하여 이 부분을 업데이트하세요.**

### 📅 마지막 세션: 2025-12-25 (Premium UI & Admin Dashboard Enhancement)

**✅ 완료된 작업 (v0.5.2)**:
1. **Admin Dashboard 고도화**:
   - **System Metrics**: CPU, 메모리, 디스크 실시간 사용량 모니터링 카드 구현.
   - **Service Integration**: `MemoSection`을 시스템 설정 페이지로 통합하여 운영 효율 개선.
2. **Premium Restart Experience**:
   - **Mascot UI**: 관리자 냥이 비디오를 활용한 프리미엄 재시작 오버레이 구현.
   - **Ambient Effects**: 굴절과 하이라이트가 포함된 리얼 "Water Drops on Window" 효과 적용.
3. **시스템 안정화 및 복구**:
   - **SSR Conflict 해결**: Hydration 오류로 인한 500 에러 해결 및 견고한 포털 패턴 도입.
   - **Build Clean**: `.next` 캐시 클런 및 `tsconfig.json` 정규화로 빌드 환경 정상화.

**Git 상태**:
- 현재 브랜치: main
- 최신 커밋: Premium Water Drops UI and System Monitoring Integration

**🎯 다음 작업 (Immediate Next Step)**:
1. **Repository Pattern 확장**: `BeanRepository` 외 다른 도메인 모델에도 Repository 패턴 적용.
2. **로스팅 로그 고도화 (Phase 2)**: 신규 아키텍처를 로스팅 로그 생성 로직에 적용.
3. **마스코트 시스템 확장**: 관리자 냥이 테마를 에러 핸들링 및 각종 Empty State UI로 확대.
