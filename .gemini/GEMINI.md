# AI Assistant Instructions for TheMoon Project

> **프로젝트**: TheMoon - 커피 로스팅 원가 계산 시스템
> **스택**: Next.js (Frontend) + FastAPI (Backend) + PostgreSQL
> **버전**: 0.0.6

---

## 🗣️ 언어 규칙 (MANDATORY)

**중요**: 사용자는 영어를 전혀 읽지 못합니다. 모든 대화, **결과 설명, 체크 상황, 진행 상태** 등 사용자가 읽어야 하는 모든 텍스트는 **반드시 한글**로 작성해야 합니다.

* 코드, 로그, 에러 메시지 원본은 영어로 유지하되, **반드시 한글 설명**을 덧붙여야 합니다.
* "Checking..." 같은 진행 상황도 "확인 중..."과 같이 한글로 표현해야 합니다.

## 🛠️ 핵심 도구 및 기술 스택 (MANDATORY)

작업 시 다음 도구와 기술을 **무조건** 사용해야 합니다:

1. **AI 도구 & MCP**:
    * **Context7**: 라이브러리 문서 및 컨텍스트 검색 시 필수 사용.
    * **Sequential Thinking**: 복잡한 작업, 계획 수립, 디버깅 시 **반드시** 이 도구를 사용하여 사고 과정을 전개할 것.

2. **Frontend Tech Stack**:
    * **Framework**: Next.js (App Router)
    * **UI Library**: **Shadcn UI** (v2, CSS Modules)

---

## 🎯 필수 참조 문서

모든 작업 시 **반드시** 다음 문서를 참조하세요:

1. **프로그래밍 규칙**: `Documents/Guides/PROGRAMMING_RULES.md`
2. **프로젝트 가이드**: `.gemini/GEMINI.md`
3. **개발 가이드**: `Documents/Architecture/DEVELOPMENT_GUIDE.md`
4. **시스템 아키텍처**: `Documents/Architecture/SYSTEM_ARCHITECTURE.md`

---

## 🚨 핵심 원칙 (절대 규칙)

### 1. 7단계 체계적 개발 방법론

**모든 프로그래밍 작업은 이 순서를 따를 것!**

```text
1️⃣ Constitution (원칙) → 기본 원칙 수립
2️⃣ Specify (명세) → 무엇을 만들지 정의
3️⃣ Clarify (명확화) → 불분명한 부분 질문으로 해소
4️⃣ Plan (계획) → 기술 스택과 아키텍처 결정
5️⃣ Tasks (작업 분해) → 작은 단위로 쪼개기 (TodoWrite 사용)
6️⃣ Implement (구현) → 코드 작성 및 테스트
7️⃣ Analyze (검증) → 명세 대비 검증
```

**❌ 금지**: 명세 없이 바로 코딩, 추측으로 진행, 검증 없이 완료

---

### 2. 작업 완료 = 3단계 필수

**모든 작업은 아래 3단계를 완료해야만 "완료"**

```text
1️⃣ 코드/테스트 작성 완료
   ↓
2️⃣ git commit
   ↓
3️⃣ 문서 4종 세트 업데이트 (필수!)
   ✅ logs/CHANGELOG.md
   ✅ Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md
   ✅ README.md (버전 동기화)
   ✅ .gemini/GEMINI.md (버전 동기화)
```

**❌ 금지**: 커밋 후 문서 업데이트 없이 다음 작업으로 넘어가기

---

### 3. URL 작성 규칙 (MANDATORY)

**❌ 절대 금지**:

```text
웹앱은 http://localhost:3000에서 실행 중입니다!  ← URL 뒤에 한글 붙음
```

**✅ 반드시**:

```text
웹앱이 실행되었습니다:

http://localhost:3000

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

### Frontend (TypeScript/Next.js)

* **타입 정의 필수**: `interface`, `type` 활용
* **함수형 컴포넌트** 사용
* **컴포넌트**: `PascalCase` (예: `BeanCard.tsx`)
* **유틸**: `camelCase` (예: `formatPrice.ts`)
* **에러 핸들링**: try-catch 필수

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
PATCH (0.0.3 → 0.0.4): 버그 3개+ OR 문서 5개+ 누적
MINOR (0.0.0 → 0.1.0): 새 기능 3~4개+ 누적
MAJOR (0.0.0 → 1.0.0): 호환성 깨지는 변경
```

---

## 📋 세션 관리

### 세션 시작 시

```bash
# 1. 체크리스트 확인
cat Documents/Progress/SESSION_START_CHECKLIST.md

# 2. 최신 세션 요약 읽기
ls -lt Documents/Progress/SESSION_SUMMARY_*.md | head -1
```

### 세션 종료 시

```bash
# 1. 종료 체크리스트 완료
cat Documents/Progress/SESSION_END_CHECKLIST.md

# 2. 세션 요약 작성
# Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md

# 3. 버전 업데이트 (누적 기준 충족 시)
./venv/bin/python logs/update_version.py --type patch --summary "요약"

# 4. 모든 문서 버전 동기화 (필수!)
```

---

## 🚫 절대 금지 사항

1. **원본 프로젝트 코드 복사 금지**
   * 참조 위치: `/mnt/d/Ai/WslProject/TheMoon_Project/`
   * 용도: 참조용으로만 사용, 모든 코드는 새로 작성

2. **새로운 세션 관리 파일 생성 금지**
   * ❌ `.gemini/SESSION_CONTEXT.md`
   * ❌ `.gemini/RULES_CHECKLIST.md`
   * ✅ 기존 6개 파일만 사용

3. **작은 변경사항마다 버전 올리기 금지**
   * 누적 기준 확인 후 세션 종료 시에만 업데이트

---

## ✅ 작업 체크리스트

### 코딩 전

* [ ] 명세서 작성 완료?
* [ ] 불명확한 부분 질문으로 해소? (Clarify)
* [ ] 작업 분해 완료? (TodoWrite)

### 커밋 전

* [ ] 타입 힌팅/정의 추가?
* [ ] 테스트 통과?
* [ ] 커밋 메시지 작성? (type: 설명)

### 커밋 후 (필수!)

* [ ] logs/CHANGELOG.md 업데이트?
* [ ] SESSION_SUMMARY 업데이트?
* [ ] README.md 확인? (버전 동기화)
* [ ] .gemini/GEMINI.md 확인? (버전 동기화)

### 세션 종료 전

* [ ] SESSION_END_CHECKLIST 완료?
* [ ] 버전 업데이트 필요? (누적 기준)
* [ ] 모든 문서 버전 동기화?

---

## 🎯 응답 규칙

1. **모든 응답은 한글로 작성** (코드/오류는 원본 유지)
2. **불명확한 부분은 반드시 질문** (추측 금지)
3. **큰 작업은 반드시 TodoWrite로 분해**
4. **검증 없이 완료 처리 금지**
2. **프로젝트 가이드**: `.gemini/GEMINI.md`
3. **개발 가이드**: `Documents/Architecture/DEVELOPMENT_GUIDE.md`
4. **시스템 아키텍처**: `Documents/Architecture/SYSTEM_ARCHITECTURE.md`

---

## 🚨 핵심 원칙 (절대 규칙)

### 1. 7단계 체계적 개발 방법론

**모든 프로그래밍 작업은 이 순서를 따를 것!**

```text
1️⃣ Constitution (원칙) → 기본 원칙 수립
2️⃣ Specify (명세) → 무엇을 만들지 정의
3️⃣ Clarify (명확화) → 불분명한 부분 질문으로 해소
4️⃣ Plan (계획) → 기술 스택과 아키텍처 결정
5️⃣ Tasks (작업 분해) → 작은 단위로 쪼개기 (TodoWrite 사용)
6️⃣ Implement (구현) → 코드 작성 및 테스트
7️⃣ Analyze (검증) → 명세 대비 검증
```

**❌ 금지**: 명세 없이 바로 코딩, 추측으로 진행, 검증 없이 완료

---

### 2. 작업 완료 = 3단계 필수

**모든 작업은 아래 3단계를 완료해야만 "완료"**

```text
1️⃣ 코드/테스트 작성 완료
   ↓
2️⃣ git commit
   ↓
3️⃣ 문서 4종 세트 업데이트 (필수!)
   ✅ logs/CHANGELOG.md
   ✅ Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md
   ✅ README.md (버전 동기화)
   ✅ .gemini/GEMINI.md (버전 동기화)
```

**❌ 금지**: 커밋 후 문서 업데이트 없이 다음 작업으로 넘어가기

---

### 3. URL 작성 규칙 (MANDATORY)

**❌ 절대 금지**:

```text
웹앱은 http://localhost:3000에서 실행 중입니다!  ← URL 뒤에 한글 붙음
```

**✅ 반드시**:

```text
웹앱이 실행되었습니다:

http://localhost:3000

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

### Frontend (TypeScript/Next.js)

* **타입 정의 필수**: `interface`, `type` 활용
* **함수형 컴포넌트** 사용
* **컴포넌트**: `PascalCase` (예: `BeanCard.tsx`)
* **유틸**: `camelCase` (예: `formatPrice.ts`)
* **에러 핸들링**: try-catch 필수

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
PATCH (0.0.3 → 0.0.4): 버그 3개+ OR 문서 5개+ 누적
MINOR (0.0.0 → 0.1.0): 새 기능 3~4개+ 누적
MAJOR (0.0.0 → 1.0.0): 호환성 깨지는 변경
```

---

## 📋 세션 관리

### 세션 시작 시

```bash
# 1. 체크리스트 확인
cat Documents/Progress/SESSION_START_CHECKLIST.md

# 2. 최신 세션 요약 읽기
ls -lt Documents/Progress/SESSION_SUMMARY_*.md | head -1
```

### 세션 종료 시

```bash
# 1. 종료 체크리스트 완료
cat Documents/Progress/SESSION_END_CHECKLIST.md

# 2. 세션 요약 작성
# Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md

# 3. 버전 업데이트 (누적 기준 충족 시)
./venv/bin/python logs/update_version.py --type patch --summary "요약"

# 4. 모든 문서 버전 동기화 (필수!)
```

---

## 🚫 절대 금지 사항

1. **원본 프로젝트 코드 복사 금지**
   * 참조 위치: `/mnt/d/Ai/WslProject/TheMoon_Project/`
   * 용도: 참조용으로만 사용, 모든 코드는 새로 작성

2. **새로운 세션 관리 파일 생성 금지**
   * ❌ `.gemini/SESSION_CONTEXT.md`
   * ❌ `.gemini/RULES_CHECKLIST.md`
   * ✅ 기존 6개 파일만 사용

3. **작은 변경사항마다 버전 올리기 금지**
   * 누적 기준 확인 후 세션 종료 시에만 업데이트

---

## ✅ 작업 체크리스트

### 코딩 전

* [ ] 명세서 작성 완료?
* [ ] 불명확한 부분 질문으로 해소? (Clarify)
* [ ] 작업 분해 완료? (TodoWrite)

### 커밋 전

* [ ] 타입 힌팅/정의 추가?
* [ ] 테스트 통과?
* [ ] 커밋 메시지 작성? (type: 설명)

### 커밋 후 (필수!)

* [ ] logs/CHANGELOG.md 업데이트?
* [ ] SESSION_SUMMARY 업데이트?
* [ ] README.md 확인? (버전 동기화)
* [ ] .gemini/GEMINI.md 확인? (버전 동기화)

### 세션 종료 전

* [ ] SESSION_END_CHECKLIST 완료?
* [ ] 버전 업데이트 필요? (누적 기준)
* [ ] 모든 문서 버전 동기화?

---

## 🎯 응답 규칙

1. **모든 응답은 한글로 작성** (코드/오류는 원본 유지)
2. **불명확한 부분은 반드시 질문** (추측 금지)
3. **큰 작업은 반드시 TodoWrite로 분해**
4. **검증 없이 완료 처리 금지**

---

**참고**: 상세 내용은 `Documents/Guides/PROGRAMMING_RULES.md` 참조

**마지막 업데이트**: 2025-12-07  
**프로젝트 버전**: 0.0.5
