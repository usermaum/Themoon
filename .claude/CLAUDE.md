# CLAUDE.md - 프로젝트 가이드 네비게이터

> **The Moon Drip BAR - 로스팅 비용 계산기**
> 버전: 0.12.0 · 스택: Streamlit + SQLite · 환경: ./venv/

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

## 🎯 필수 규칙 (CRITICAL)

### 🚨 작업 완료 = 3단계 필수 (절대 무시 금지!)

**문제:** 코드 작성 후 문서 업데이트를 반복적으로 잊어먹는 현상 발생

**해결:** 모든 작업은 반드시 아래 3단계를 완료해야만 "완료"로 간주

```
1️⃣ 코드/테스트 작성 완료
   ↓
2️⃣ git commit
   ↓
3️⃣ 문서 4종 세트 업데이트 ← 이것 없으면 작업 미완료!
   - [ ] logs/CHANGELOG.md (변경 로그 추가)
   - [ ] Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md (세션 요약 작성/업데이트)
   - [ ] README.md (버전, 테스트 통계 등 6개 위치 확인)
   - [ ] .claude/CLAUDE.md (버전 동기화 확인)
```

**❌ 절대 하지 말 것:**
- 커밋 후 문서 업데이트 없이 다음 작업으로 넘어가기
- "나중에 한 번에 업데이트하면 되지" 생각하기
- 사용자가 지적하기 전까지 잊고 있기

**✅ 반드시 할 것:**
- 커밋 직후 바로 문서 4종 세트 체크
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

✅ **항상 프로젝트 venv 사용** (절대 `python3` 금지)
```bash
./venv/bin/python script.py
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true
./venv/bin/pip install package_name
```

✅ **모든 응답은 한글로 작성** (코드/오류는 원본 유지)

---

## 📁 핵심 문서 위치

| 문서 | 위치 | 용도 |
|------|------|------|
| **파일 구조** | `Documents/Architecture/FILE_STRUCTURE.md` | 프로젝트 파일 맵 |
| **개발 가이드** | `Documents/Architecture/DEVELOPMENT_GUIDE.md` | 5단계 개발 프로세스 |
| **시스템 아키텍처** | `Documents/Architecture/SYSTEM_ARCHITECTURE.md` | 3계층 아키텍처 & 데이터 흐름 |
| **문제 해결** | `Documents/Architecture/TROUBLESHOOTING.md` | 16가지 오류 & 해결법 |
| **자주 하는 작업** | `Documents/Architecture/COMMON_TASKS.md` | 25가지 작업 단계 가이드 |
| **진행 현황** | `Documents/Progress/SESSION_SUMMARY_*.md` | 세션별 진행 상황 |

---

## 🚀 빠른 시작

```bash
# 1. 앱 실행
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true
# → http://localhost:8501

# 2. 테스트 데이터 생성
./venv/bin/python app/test_data.py

# 3. Git 커밋 (한글 설명)
git add .
git commit -m "feat: 새 기능 설명"

# 4. 포트 충돌 해결
lsof -ti :8501 | xargs kill -9
```

---

## 📌 프로젝트 구조

```
TheMoon_Project/
├── venv/                   # 프로젝트 격리 환경 (Python 3.12.3)
├── app/                    # Streamlit 애플리케이션
│   ├── app.py            # 메인 진입점
│   ├── pages/            # 9개 페이지
│   ├── services/         # 6개 서비스 (비즈니스 로직)
│   ├── models/           # SQLAlchemy 모델
│   └── components/       # 15+ 재사용 컴포넌트
├── Data/                  # SQLite 데이터베이스
├── Documents/            # 28개 분류별 문서
└── logs/                 # 버전 관리 (VERSION, CHANGELOG.md)
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

| 파일 | 위치 | 용도 | 필수 여부 |
|------|------|------|---------|
| **SESSION_START_CHECKLIST** | `Documents/Progress/SESSION_START_CHECKLIST.md` | 세션 시작 시 반드시 확인 | ✅ 필수 |
| **SESSION_END_CHECKLIST** | `Documents/Progress/SESSION_END_CHECKLIST.md` | 세션 종료 시 반드시 완료 | ✅ 필수 |
| **VERSION_MANAGEMENT** | `logs/VERSION_MANAGEMENT.md` | 버전 관리 규칙 | ✅ 필수 |
| **SESSION_SUMMARY** | `Documents/Progress/SESSION_SUMMARY_*.md` | 각 세션별 진행 기록 | ✅ 필수 |
| **CHANGELOG** | `logs/CHANGELOG.md` | 프로젝트 변경 로그 | ✅ 필수 |
| **VERSION** | `logs/VERSION` | 현재 버전 파일 | ✅ 필수 |

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

### 새로운 파일을 만들지 말 것!

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
