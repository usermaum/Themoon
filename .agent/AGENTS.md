# AGENTS.md

> **TheMoon - 커피 로스팅 원가 계산 시스템**
> **Stack**: Next.js (App Router) + FastAPI + PostgreSQL (Prod) / SQLite (Dev)
> **Version**: 0.3.0
> **OS**: Windows (WSL2 Environment)

---

## 🗣️ Language Rules (MANDATORY)

**CRITICAL**: The user is a **beginner in English**. To ensure clear communication, you must perform all interactions in **Korean**.

- **Output**: All explanations, status updates ("Checking..."), and results must be in **Korean**.
- **Exceptions**: Keep code, original error messages, and log outputs in English, but **always** append a Korean explanation.
- **Tone**: Professional, helpful, and concise.

---

## 🛠️ Setup & Commands

### Development Server

**ALWAYS** use the provided script to start the environment. **NEVER** use `start_all.sh` or `npm run dev`/`uvicorn` directly unless debugging specific isolated components.

```bash
# Clean start (clears cache & restarts servers)
wsl bash dev.sh
```

### Process Management

Before starting servers, ensure ports are free.

```bash
# Kill existing processes on ports 3500 (Frontend) and 8000 (Backend)
lsof -ti :3500,8000 | xargs kill -9
```

### Version Management

To upgrade the project version (perform only at the end of a session):

```bash
# Example: Patch update
./venv/bin/python logs/update_version.py --type patch --summary "Session summary here"
```

---

## 🏗️ Constitution (Workflows)

### 1. 7-Step Development Methodology (MANDATORY)

Follow this sequence for **ALL** programming tasks.

1. **Constitution (원칙)**: Establish basic principles and constraints.
2. **Specify (명세)**: Define detailed requirements (Input/Output, Data Structures).
3. **Clarify (명확화)**: Ask questions to resolve ambiguities. **Do not guess.**
4. **Plan (계획)**: Decide tech stack and architecture. Create `implementation_plan.md`.
5. **Tasks (작업 분해)**: Break down work into small, testable items. Use `task.md`.
6. **Implement (구현)**: Write code and tests.
7. **Analyze (검증)**: Verify against the specification.

### 2. Definition of Done (3-Step Rule)

A task is **NOT complete** until all 3 steps are finished.

1. **Code/Test**: Write code and pass tests.
2. **Commit**: `git commit` (Do not update version here).
3. **Documentation (The "5-Set")**: Update these files immediately after commit:
   - `logs/CHANGELOG.md`
   - `Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md`
   - `README.md` (Sync version)
   - `.claude/CLAUDE.md` (Sync version)
   - `.gemini/GEMINI.md` (Sync version)

---

## 💻 Tech Stack & Conventions

### Frontend

- **Framework**: Next.js 14 (App Router)
- **UI Library**: Shadcn UI (v2) + Tailwind CSS
- **Language**: TypeScript (Strict Mode)
- **Conventions**:
  - Components: `PascalCase` (e.g., `BeanCard.tsx`)
  - Utils: `camelCase` (e.g., `formatPrice.ts`)
  - Functional Components required.

### Backend

- **Framework**: FastAPI
- **Language**: Python 3.10+
- **Database**: SQLite (Dev) / PostgreSQL (Prod)
- **ORM**: SQLAlchemy
- **Conventions**:
  - Files: `snake_case` (e.g., `bean_service.py`)
  - Classes: `PascalCase` (e.g., `BeanService`)
  - Functions: `snake_case` (e.g., `get_bean_by_id`)
  - **Type Hinting**: Mandatory for all functions (e.g., `def func(a: int) -> str:`).

### Tools

- **Mermaid**: **MANDATORY** for all diagrams (Architecture, Flow, ERD). No image uploads.

---

## 📝 Documentation Rules

### URL Formatting

**Strictly** follow this format to ensure clickable links in the user's interface.

**❌ BAD**:
`App running at http://localhost:3000!` (No space after URL)
`Check http://localhost:3000` (No newline before)

**✅ GOOD**:

```text
웹앱이 실행되었습니다:

http://localhost:3000

위 주소로 접속하세요.
```

### Version Update Criteria

- **PATCH** (0.0.x → 0.0.y): 3+ bugs fixed OR 5+ docs updated.
- **MINOR** (0.x.0 → 0.y.0): 3-4 new features accumulated.
- **MAJOR** (x.0.0 → y.0.0): Breaking changes.

---

## 📋 Session Management

### Files

- `Documents/Progress/SESSION_START_CHECKLIST.md`: Read at start.
- `Documents/Progress/SESSION_END_CHECKLIST.md`: Complete at end.
- `Documents/Progress/SESSION_SUMMARY_*.md`: Read latest at start / Create new at end.

### Protocol

1. **Start**: Read checklist -> Read latest summary -> Check version strategy.
2. **End**: Complete checklist -> Write session summary -> Update version (if criteria met) -> Sync all docs.

---

## 📂 Core Directories

- `backend/`: FastAPI source
- `frontend/`: Next.js source
- `Documents/Architecture/`: System design & specs (Source of Truth)
- `logs/`: Version control & Changelogs
- `data/`: Local SQLite database location

---

*Generated based on .claude/CLAUDE.md and .gemini/GEMINI.md*
