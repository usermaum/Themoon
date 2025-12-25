# CLAUDE.md - 프로젝트 가이드 네비게이터

> **TheMoon - 커피 로스팅 원가 계산 시스템 (Modern Stack)**
> 버전: 0.4.0 · 스택: Next.js + FastAPI + PostgreSQL · Clean Slate

---

## ⚡ 빠른 버전 관리 참고

**작업 완료 후**: `git commit` (버전 업데이트 ❌)

**세션 종료 시**: 다음 기준 확인 후 버전 올림

```
✅ PATCH 올림 (1.5.2 → 1.5.3)
   조건: 버그 3개+ OR 문서 5개+ 누적
   주기: 주 1~3회

✅ MINOR 올림 (1.5.0 → 1.6.0)
   조건: 새 기능 3~4개+ 누적
   주기: 월 1회

✅ MAJOR 올림 (1.0.0 → 2.0.0)
   조건: 호환성 깨지는 변경
   주기: 년 1~2회 (거의 없음)
```

**📌 참고**:

- `logs/VERSION_STRATEGY.md` - 상세 전략
- `logs/VERSION_MANAGEMENT.md` - 사용법

---

## 🔗 URL 작성 규칙 (MANDATORY - 절대 위반 금지!)

**❌ 절대 하지 말 것:**

```
웹앱은 http://localhost:8501에서 실행 중입니다!  ← URL 뒤에 한글 붙음 (클릭 불가)
- URL: http://localhost:8501                        ← URL 뒤에 줄바꿈 없음
```

**✅ 반드시 할 것:**

```
웹앱이 실행되었습니다:

http://localhost:8501

위 주소로 접속하세요.
```

**또는:**

```
접속 정보:

- URL: http://localhost:8501
- 상태: 실행 중
```

**핵심 규칙:**

1. URL 앞: 최소 1개 공백 또는 줄바꿈
2. URL 뒤: 최소 1개 공백 또는 줄바꿈
3. URL 바로 뒤에 한글/특수문자/이모지 절대 금지

**상세 내용:** `.claude/instructions.md` 참조

---

## 🎯 필수 규칙 (CRITICAL)

### 🚨 작업 완료 = 3단계 필수 (절대 무시 금지!)

**문제:** 코드 작성 후 문서 업데이트를 반복적으로 잊어먹는 현상 발생

**해결:** 모든 작업은 반드시 아래 3단계를 완료해야만 "완료"로 간주

```
1️⃣ 코드/테스트 작성 완료
   ↓
2️⃣ git commit
   ↓
3️⃣ 문서 5종 세트 업데이트 ← 이것 없으면 작업 미완료!
   - [ ] logs/CHANGELOG.md (변경 로그 추가)
   - [ ] Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md (세션 요약 작성/업데이트)
   - [ ] README.md (버전, 테스트 통계 등 6개 위치 확인)
   - [ ] .claude/CLAUDE.md (버전 동기화 확인)
   - [ ] .gemini/GEMINI.md (버전 동기화 확인)
```

**❌ 절대 하지 말 것:**

- 커밋 후 문서 업데이트 없이 다음 작업으로 넘어가기
- "나중에 한 번에 업데이트하면 되지" 생각하기
- 사용자가 지적하기 전까지 잊고 있기

**✅ 반드시 할 것:**

- 커밋 직후 바로 문서 5종 세트 체크
- 하나라도 빠뜨리면 TodoWrite로 "문서 업데이트" 태스크 추가
- 세션 종료 전 반드시 모든 문서 동기화 확인

---

### 🎯 7단계 체계적 개발 방법론 (필수 준수!)

**모든 프로그래밍 및 플랜 작성 시 반드시 이 순서를 따를 것!**

```
1️⃣ Constitution (원칙)
   └─ 프로젝트 기본 원칙, 목표, 제약사항, 기술 스택 결정 원칙 수립
   └─ 산출물: 기본 원칙 문서, 제약사항 목록

2️⃣ Specify (명세)
   └─ 무엇을 만들지 상세하게 정의 (기능 요구사항, 입출력, 데이터 구조)
   └─ 산출물: 기능 명세서, API 스펙, 데이터 모델 정의

3️⃣ Clarify (명확화)
   └─ 불분명한 부분을 사용자에게 질문하여 해소 (AskUserQuestion 활용)
   └─ 산출물: Q&A 문서, 결정사항 기록

4️⃣ Plan (계획)
   └─ 기술 스택과 아키텍처 결정 (어떻게 구현할지)
   └─ 산출물: 아키텍처 다이어그램, DB 스키마, 파일 구조

5️⃣ Tasks (작업 분해)
   └─ 실행 가능한 작은 단위로 쪼개기 (TodoWrite 필수 사용!)
   └─ 산출물: 작업 목록 (독립적이고 테스트 가능한 단위)

6️⃣ Implement (구현)
   └─ 실제 코드 작성 및 테스트 코드 작성
   └─ 산출물: 소스 코드, 테스트 코드, 커밋

7️⃣ Analyze (검증)
   └─ 명세와 코드 일치 여부 확인, 품질 검증, 커버리지 측정
   └─ 산출물: 테스트 리포트, 커버리지 리포트, 검증 문서
```

**❌ 절대 하지 말 것:**

- 명세 없이 바로 코딩 시작
- 불명확한 부분을 추측으로 진행
- 큰 작업을 분해 없이 한 번에 구현
- 검증 없이 완료 처리

**✅ 반드시 할 것:**

- 각 단계의 산출물 확인
- Clarify 단계에서 모든 불확실성 제거
- Tasks 단계에서 TodoWrite 사용
- Analyze 단계에서 명세 대비 검증

**참고 문서:**

- 구현 레벨 가이드: `Documents/Architecture/DEVELOPMENT_GUIDE.md` (5단계 개발 프로세스)
- 이 7단계는 상위 레벨 방법론으로, DEVELOPMENT_GUIDE의 5단계는 6️⃣ Implement 단계의 세부 절차

---

✅ **개발 환경 구성**

```bash
# Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (Next.js)
cd frontend
npm install
npm run dev
```

✅ **모든 응답 및 상태/결과 설명은 반드시 한글로 작성** (MANDATORY)

- 사용자는 영어를 읽지 못함
- 체크 상황, 진행 상태, 결과 리포트 등 모든 "설명" 텍스트는 한글 필수
- 코드/오류 메시지 원본은 유지하되 한글 설명 추가
  ✅ **원본 프로젝트 참조** (코드 복사 금지)
- 원본 위치: `/mnt/d/Ai/WslProject/TheMoon_Project/`
- 참조용으로만 사용, 모든 코드는 새로 작성

---

## 📁 핵심 문서 위치

| 문서                      | 위치                                              | 용도                         |
| ------------------------- | ------------------------------------------------- | ---------------------------- |
| **파일 구조**       | `Documents/Architecture/FILE_STRUCTURE.md`      | 프로젝트 파일 맵             |
| **개발 가이드**     | `Documents/Architecture/DEVELOPMENT_GUIDE.md`   | 5단계 개발 프로세스          |
| **시스템 아키텍처** | `Documents/Architecture/SYSTEM_ARCHITECTURE.md` | 3계층 아키텍처 & 데이터 흐름 |
| **문제 해결**       | `Documents/Architecture/TROUBLESHOOTING.md`     | 16가지 오류 & 해결법         |
| **자주 하는 작업**  | `Documents/Architecture/COMMON_TASKS.md`        | 25가지 작업 단계 가이드      |
| **진행 현황**       | `Documents/Progress/SESSION_SUMMARY_*.md`       | 세션별 진행 상황             |

---

## 🚀 빠른 시작

```bash
# 1. Backend (FastAPI) 실행
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# → http://localhost:8000

# 2. Frontend (Next.js) 실행
cd frontend
npm install
npm run dev
# → http://localhost:3000

# 3. Git 커밋 (한글 설명)
git add .
git commit -m "feat: 새 기능 설명"

# 4. 포트 충돌 해결
lsof -ti :8000 | xargs kill -9  # Backend
lsof -ti :3000 | xargs kill -9  # Frontend
```

---

## 📌 프로젝트 구조

```
Themoon/                    # 신규 프로젝트 (Next.js + FastAPI)
├── .claude/                # Claude Code 설정
├── backend/                # FastAPI 백엔드 (8개 파일, 20KB)
│   ├── app/
│   │   ├── __init__.py   # 버전 정보
│   │   ├── main.py       # FastAPI 앱 (50줄)
│   │   ├── config.py     # 설정 관리
│   │   └── database.py   # DB 연결
│   ├── README.md          # 개발 가이드
│   └── requirements.txt   # 의존성
├── frontend/               # Next.js 프론트엔드 (9개 파일, 16KB)
│   ├── app/
│   │   ├── page.tsx      # 메인 페이지
│   │   ├── layout.tsx    # 레이아웃
│   │   └── globals.css   # 스타일
│   ├── lib/
│   │   └── api.ts        # API 클라이언트
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── tsconfig.json
├── Documents/              # 프로젝트 문서
│   ├── Architecture/       # 아키텍처 (8개 문서)
│   ├── Guides/             # 가이드 (4개 문서)
│   ├── Implementation/     # 구현 문서 (2개)
│   ├── Planning/           # 계획 문서 (15개)
│   ├── Progress/           # 진행 상황 (40+ 세션)
│   └── Resources/          # 자료 (엑셀, 문서 등)
├── logs/                   # 버전 관리
│   ├── VERSION            # 현재: 0.0.3
│   └── CHANGELOG.md       # 변경 로그
├── data/                   # 데이터베이스 (원본 참조용)
├── venv/                   # Python 가상환경 (원본 참조용)
└── README.md               # 프로젝트 소개
```

**원본 프로젝트 (참조용):**

```
/mnt/d/Ai/WslProject/TheMoon_Project/  # Streamlit 기반 원본
├── app/                    # Streamlit 애플리케이션
│   ├── app.py            # 메인 진입점
│   ├── pages/            # 9개 페이지
│   ├── services/         # 6개 서비스 (비즈니스 로직 참조)
│   ├── models/           # SQLAlchemy 모델 (참조)
│   └── components/       # 15+ 재사용 컴포넌트 (참조)
├── data/                  # SQLite 데이터베이스
└── Documents/            # 원본 문서
```

---

## 🔗 문서 로드 전략

새로운 세션에서는 다음 순서로 확인:

1. **SESSION_SUMMARY_*.md** - 지난 세션 진행 상황
2. **필요한 아키텍처 문서** 로드 (위의 표 참조)
3. **COMMON_TASKS.md** - 자주 하는 작업 참고

**전체 구조:** `Documents/` → Architecture(설계), Guides(가이드), Progress(진행), Planning(계획), Resources(자료)

---

## 🎯 세션 관리 시스템 (PRIMARY SOURCE OF TRUTH)

> ⚠️ **매우 중요**: 아래의 세 파일이 모든 세션 관리의 기준입니다.
> 새로운 파일이나 규칙을 만들기 전에 항상 이 파일들을 먼저 확인하세요!

### 필수 파일 (어제 정한 공식 시스템)

| 파일                              | 위치                                              | 용도                     | 필수 여부 |
| --------------------------------- | ------------------------------------------------- | ------------------------ | --------- |
| **SESSION_START_CHECKLIST** | `Documents/Progress/SESSION_START_CHECKLIST.md` | 세션 시작 시 반드시 확인 | ✅ 필수   |
| **SESSION_END_CHECKLIST**   | `Documents/Progress/SESSION_END_CHECKLIST.md`   | 세션 종료 시 반드시 완료 | ✅ 필수   |
| **VERSION_MANAGEMENT**      | `logs/VERSION_MANAGEMENT.md`                    | 버전 관리 규칙           | ✅ 필수   |
| **SESSION_SUMMARY**         | `Documents/Progress/SESSION_SUMMARY_*.md`       | 각 세션별 진행 기록      | ✅ 필수   |
| **CHANGELOG**               | `logs/CHANGELOG.md`                             | 프로젝트 변경 로그       | ✅ 필수   |
| **VERSION**                 | `logs/VERSION`                                  | 현재 버전 파일           | ✅ 필수   |

### 세션 시작 (매번 필수)

```bash
# 1단계: SESSION_START_CHECKLIST 읽기
cat Documents/Progress/SESSION_START_CHECKLIST.md

# 2단계: 지난 세션 요약 읽기
ls -lt Documents/Progress/SESSION_SUMMARY_*.md | head -1
# 가장 최신 파일 읽기

# 3단계: 버전 관리 규칙 확인 (필요시)
cat logs/VERSION_MANAGEMENT.md | head -50
```

### 작업 완료 후 처리 (각 작업마다)

```bash
# ⚡ 빠른 처리 (1분)
# 1단계: 변경사항 확인
git status

# 2단계: 변경사항 커밋
git add .
git commit -m "type: 한글 설명"

# 3단계: 최종 확인
git log --oneline -1
```

### ⚠️ 모든 문서의 버전 동기화 (매 세션 종료 시 필수!)

```bash
# 현재 버전 확인
CURRENT_VERSION=$(cat logs/VERSION)

# 📄 README.md의 모든 버전 정보를 logs/VERSION과 일치시킬 것!
# - Line 3: v1.2.0 → v$CURRENT_VERSION (타이틀)
# - Line 7: v1.2.0 → v$CURRENT_VERSION (프로젝트 상태)
# - Line 11, 67, 492, 503, 537: 모든 버전 표기
# - Line 501: 최근 커밋 해시 업데이트

# 📄 .claude/CLAUDE.md의 버전도 동기화할 것!
# - Line 4: 버전: 1.2.0 → 버전: $CURRENT_VERSION
```

**💡 중요**:

- README.md의 모든 버전이 logs/VERSION과 일치해야 함
- CLAUDE.md(Line 4)의 버전도 logs/VERSION과 일치해야 함

**커밋 타입**:

- `feat`: 새로운 기능
- `fix`: 버그 수정
- `refactor`: 코드 정리/리팩토링
- `docs`: 문서 작성/수정
- `chore`: 설정 변경, 패키지 업데이트

### 📌 버전 업데이트 규칙 (명시적)

**각 작업 완료 후:**

```bash
# ✅ 커밋만 한다 (버전 업데이트 ❌)
git add .
git commit -m "type: 설명"
```

**세션 종료 시 (최종 1회만):**

```bash
# ✅ 이번 세션의 모든 변경사항을 합쳐서 버전 한 번에 업데이트
# logs/VERSION_MANAGEMENT.md 참조하여 적절한 타입 선택 (patch/minor/major)

./venv/bin/python logs/update_version.py \
  --type patch \
  --summary "이번 세션의 작업 요약"

# 그 후 README.md의 버전 동기화
```

**⚠️ 중요**:

- 작업마다 → **커밋만**
- 세션 종료 → **버전 업데이트** (logs/VERSION_MANAGEMENT.md 참조)

---

### 세션 종료 (매번 필수)

```bash
# 1단계: SESSION_END_CHECKLIST 모든 항목 완료
cat Documents/Progress/SESSION_END_CHECKLIST.md

# 2단계: SESSION_SUMMARY 작성
# 파일명: Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md

# 3단계: 커밋 확인
git status
```

### 버전 관리 규칙 (핵심 3가지)

모든 버전 업데이트는 다음 파일을 따릅니다:

- **logs/VERSION_STRATEGY.md** - 📌 효율적인 버전관리 전략 (우선 읽기!)
- **logs/VERSION_MANAGEMENT.md** - 공식 버전 관리 가이드 사용법
- **logs/CHANGELOG.md** - 변경 로그 기록
- **logs/VERSION** - 현재 버전 저장

**버전 올리기 기준** (필수 암기):

```
PATCH: 버그 3개 이상 OR 문서 5개 이상 누적 (주 1~3회)
MINOR: 새 기능 3~4개 이상 추가 (월 1회)
MAJOR: 호환성 변경 (년 1~2회)
```

**⚠️ 주의**: 작은 변경사항으로 매번 버전 올리지 말 것!
→ 누적 기준 만족 시에만 버전 올림

---

## ⚠️ 중요한 주의사항

### 새로운 파일을 만들지 말 것

❌ **하지 말 것**: 위의 6개 파일 외에 새로운 세션 관리 파일을 만드는 것

```
예시 - 하지 말 것:
❌ .claude/SESSION_CONTEXT.md
❌ .claude/RULES_CHECKLIST.md
❌ .claude/NEXT_SESSION_PROMPT.md
```

✅ **대신 할 것**: 위의 6개 파일만 사용하기

### 이전 세션의 결정 존중

각 세션에서 정한 규칙과 체계는 **다음 세션에서도 그대로 따릅니다**.

- 새 규칙을 만들기 전에 이전 규칙이 있는지 확인
- 기존 체계를 그대로 사용
- 필요시 기존 파일을 수정 (새 파일 생성 금지)

---

마지막 업데이트: 2025-10-28
세션 관리 시스템 확립: v1.2.0

---

## 🕒 최근 작업 상태 (Latest Context)

> **이 섹션은 AI가 세션을 시작할 때 자동으로 읽어들이는 "기억" 영역입니다.**
> **세션 종료 전 반드시 AI에게 "상태 저장해줘" 또는 "세션 종료"를 요청하여 이 부분을 업데이트하세요.**

### 🔄 Context Handover Protocol

**세션 간 연속성을 위한 3단계 프로토콜:**

1. **세션 종료 시**: "상태 저장해줘" 명령으로 진행 상황 자동 기록
2. **컴퓨터 간 이동**: Git Sync 필수 (`git commit && git push` → `git pull`)
3. **새 세션 시작**: 자동으로 마지막 상태 로드 및 제안

---

### 📅 마지막 세션: 2025-12-21

**✅ 완료된 작업**:

1. ✅ Statusline 빠른 동기화 기능 구현

   - `/config` 64% vs statusline 22% 불일치 문제 해결
   - `--quick-sync (-q)` 옵션 추가: `python3 .claude/statusline.py -q 64`
   - 1초 만에 완료되는 간편한 동기화
   - README에 사용법 섹션 추가
2. ✅ 문서 업데이트

   - CHANGELOG.md: Unreleased 섹션에 변경사항 추가
   - SESSION_SUMMARY_2025-12-21.md: 오후 세션 내용 추가
   - README.md: "📊 Claude Code Statusline 사용법" 섹션 추가
3. ✅ 기술 분석 및 학습

   - Anthropic API 사용량 조회 시도 (엔드포인트 없음 확인)
   - ccusage 명령어 분석 (블록 데이터만 제공)
   - 실용적 해결책 선택: 수동 입력 + 자동 추적

**Git 상태**:

- 현재 브랜치: main
- 원격보다 30커밋 앞서 있음
- Working tree: modified (문서 업데이트 예정)
- 최종 커밋: c47cf05 (Analytics UI Polish & Docs)

**🎯 다음 작업 옵션**:

1. Invoice 페이지를 실제 OCR 데이터와 연동
2. OCR 기능 전체 플로우 테스트
3. 생두 매칭 시스템 추가 개선 (Fuzzy matching 고려)
4. UI/UX 개선 (인쇄, 다운로드 기능)
