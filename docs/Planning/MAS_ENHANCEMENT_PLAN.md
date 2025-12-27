# MAS (Multi-Agent System) Enhancement Plan

> **작성일**: 2025-12-27
> **목적**: Claude Code 환경에 맞는 실행 가능한 MAS 프로토콜 구축
> **현재 상태**: 개념적 역할만 정의됨 → **실행 도구 매핑 필요**

---

## 🎯 목표 (Objectives)

### 현재 문제점
- ❌ `AGENTS.md`에 역할(Role)만 명시되고 실제 **실행 도구(Skills/Tools)** 연결 없음
- ❌ 에이전트 간 **협업 프로토콜** 불명확 (누가 언제 어떻게 협력하는지)
- ❌ 역할 **전환 메커니즘** 구체적이지 않음 (사용자 호명 방식만 존재)
- ❌ Gemini API 기반 플랜을 Claude Code로 변환 필요

### 개선 목표
- ✅ 각 에이전트에 **Claude Marketplace 스킬** 매핑
- ✅ 에이전트별 **허용 도구(Tools)** 명시
- ✅ **역할 전환 프로토콜** 자동화 (작업 성격 기반 자동 전환)
- ✅ **협업 시나리오** 구체화 (예: Agent 2가 API 수정 필요 시 Agent 3 호출)

---

## 🧙 에이전트별 스킬 & 도구 매핑

### 🧑‍💼 Agent 1: Project Architect (PM)

**책임**:
- 세션 시작/종료 관리
- `task.md`, `CHANGELOG.md` 업데이트
- 아키텍처 설계 및 문서화
- 에이전트 간 조율 및 역할 배정

**할당 스킬** (Claude Marketplace):
- `commit-commands` - 커밋/푸시/PR 관리
- `hookify` - Hook 규칙 자동 설정
- `plugin-dev` - 플러그인 구조 설계

**허용 도구**:
- Read, Write, Edit (문서 전용)
- Bash (git, 문서 관련 명령만)
- TodoWrite (작업 관리)
- Grep, Glob (정보 검색)

**금지 사항**:
- ❌ 직접적인 코딩 (`frontend/`, `backend/` 수정 금지)
- ❌ 추측으로 문제 해결 시도 (전문가에게 위임)

---

### 🎨 Agent 2: Frontend Specialist

**책임**:
- React 컴포넌트 설계 및 구현
- Tailwind CSS, Shadcn UI 활용
- 애니메이션 및 사용자 경험(UX) 최적화
- 디자인 시스템 유지

**할당 스킬** (Claude Marketplace):
- **`frontend-design`** ⭐ (주력 스킬) - 프론트엔드 디자인 생성
- `feature-dev` - 기능 개발 가이드

**허용 도구**:
- Read, Write, Edit (`frontend/` 디렉토리)
- Bash (npm, Node.js 관련)
- Grep, Glob (컴포넌트 검색)
- LSP (TypeScript 지원)

**금지 사항**:
- ❌ `backend/` 폴더 접근 금지
- ❌ API 로직 수정 금지 → Agent 3에게 요청

**협업 프로토콜**:
```
[Agent 2] API 수정 필요 감지
    ↓
[Agent 2] "@Agent3: API 엔드포인트 {endpoint}에 {field} 필드 추가 요청"
    ↓
[Agent 3] backend 수정 및 응답
    ↓
[Agent 2] frontend 연동 완료
```

---

### ⚙️ Agent 3: Backend Engineer

**책임**:
- FastAPI 엔드포인트 설계 및 구현
- DB 스키마 관리 (SQLAlchemy)
- 비즈니스 로직 구현 (Clean Architecture)
- Repository Pattern 적용

**할당 스킬** (Claude Marketplace):
- `feature-dev` - 기능 개발 가이드
- `code-review` - 백엔드 코드 품질 검증

**허용 도구**:
- Read, Write, Edit (`backend/`, `frontend/lib/api.ts`)
- Bash (Python, uvicorn, pytest)
- Grep, Glob (백엔드 검색)
- LSP (Python 지원)

**금지 사항**:
- ❌ `frontend/components` 직접 수정 지양 (API 스펙만 제공)

**협업 프로토콜**:
```
[Agent 3] API 스펙 변경 시
    ↓
[Agent 3] "API 엔드포인트 {endpoint} 응답 구조 변경: {변경사항}"
    ↓
[Agent 2] frontend 타입 정의 업데이트
```

---

### 🛠️ Agent 4: System Maintainer (The Fixer)

**책임**:
- "안 돼요", "에러 나요" 해결
- WSL 환경 설정 (`dev.sh`, 의존성)
- 전체 시스템 디버깅 및 통합 테스트
- PR 리뷰 및 코드 품질 관리

**할당 스킬** (Claude Marketplace):
- **`pr-review-toolkit`** ⭐ (주력 스킬) - PR 종합 리뷰
- `code-review` - 코드 품질 검증
- `commit-commands` - 긴급 커밋/롤백

**허용 도구**:
- **All Tools** (긴급 상황 시 Cross-Cutting 권한)
- Bash (시스템 명령, 디버깅)
- Read, Write, Edit (모든 파일)
- LSP (통합 검증)

**특별 권한**:
- ✅ 긴급 시 모든 파일 수정 가능
- ✅ 에이전트 간 충돌 조정 권한

**협업 프로토콜**:
```
[Agent 2/3] "에러 발생: {에러 메시지}"
    ↓
[Agent 4] 디버깅 및 원인 파악
    ↓
[Agent 4] "@Agent2/3: {수정 방법} 또는 직접 수정"
    ↓
[해당 Agent] 수정 완료 또는 Agent 4가 직접 수정
```

---

## 🔄 역할 전환 프로토콜 (Automatic Role Switching)

### 자동 전환 규칙

| 작업 키워드 | 자동 전환 대상 | 예시 |
|:-----------|:-------------|:-----|
| "디자인", "컴포넌트", "UI", "애니메이션" | **Agent 2** | "로스팅 대시보드 디자인 개선" |
| "API", "엔드포인트", "DB", "스키마" | **Agent 3** | "Bean API에 필터 추가" |
| "에러", "안 돼요", "버그", "디버깅" | **Agent 4** | "로그인 안 돼요" |
| "문서", "계획", "아키텍처", "세션" | **Agent 1** | "세션 요약 작성" |

### 명시적 호출 방법

사용자가 직접 지정:
```
@Agent2 로스팅 차트 컴포넌트 만들어줘
@Agent3 Bean Repository 패턴 적용해줘
@Agent4 빌드 에러 해결해줘
```

### 협업 호출 방법

에이전트 간 호출:
```python
# Agent 2가 Agent 3에게 요청
"@Agent3: /api/roasting/logs 엔드포인트에 date_range 필터 파라미터 추가 필요"

# Agent 3 응답
"@Agent2: date_range 필터 추가 완료. 타입: { start_date: str, end_date: str }"
```

---

## 🛠️ 스킬 호출 프로토콜 (Skill Invocation)

### 스킬 사용 문법

```bash
# Agent 2가 frontend-design 스킬 사용
/frontend-design "로스팅 대시보드 Bento Grid 레이아웃"

# Agent 4가 PR 리뷰
/review-pr 123

# Agent 1이 커밋
/commit -m "feat: 로스팅 필터 기능 추가"
```

### 스킬 사용 규칙

1. **스킬 사용 전 선언**:
   ```
   [Agent 2] frontend-design 스킬을 사용하여 디자인 생성합니다.
   ```

2. **스킬 사용 후 보고**:
   ```
   [Agent 2] ✅ frontend-design 스킬 완료: RoastingDashboard.tsx 생성
   ```

3. **스킬 실패 시 에스컬레이션**:
   ```
   [Agent 2] ❌ frontend-design 실패 → @Agent4 디버깅 요청
   ```

---

## 📋 작업 프로세스 (Enhanced 7 Steps)

기존 7단계에 **에이전트 역할 명시** 추가:

```text
0️⃣ Role Assignment (역할 배정) → Agent 1이 작업 성격 파악 후 에이전트 배정
    ↓
1️⃣ Constitution (원칙) → 담당 Agent가 기본 원칙 수립
    ↓
2️⃣ Specify (명세) → 무엇을 만들지 정의
    ↓
3️⃣ Clarify (명확화) → 불분명한 부분 질문 (필요 시 Agent 1과 협의)
    ↓
4️⃣ Plan (계획) → 기술 스택 결정 (Agent 1 승인 필요)
    ↓
5️⃣ Tasks (작업 분해) → TodoWrite 사용 (모든 Agent)
    ↓
6️⃣ Implement (구현) → 코드 작성 (스킬 활용)
    ↓
7️⃣ Analyze (검증) → 명세 대비 검증 (Agent 4 최종 검토)
```

---

## 🚀 구현 단계 (Implementation Phases)

### Phase 1: AGENTS.md 업데이트 (우선순위 ⭐⭐⭐)
- [ ] 에이전트별 스킬 매핑 추가
- [ ] 허용 도구(Tools) 명시
- [ ] 역할 전환 프로토콜 추가
- [ ] 협업 시나리오 예시 추가

### Phase 2: 실전 테스트 (우선순위 ⭐⭐)
- [ ] Agent 2: `frontend-design` 스킬로 마스코트 에러 페이지 생성
- [ ] Agent 3: `feature-dev` 스킬로 Bean Repository 확장
- [ ] Agent 4: `pr-review-toolkit`으로 코드 리뷰

### Phase 3: 문서화 (우선순위 ⭐)
- [ ] `docs/Guides/MAS_USAGE_GUIDE.md` 작성 (사용자 가이드)
- [ ] 협업 시나리오 케이스 스터디 추가
- [ ] FAQ 섹션 추가

---

## 📝 예상 효과 (Expected Benefits)

1. **명확한 역할 분담**: 각 에이전트가 자신의 전문 영역에만 집중
2. **도구 활용 극대화**: Claude Marketplace 스킬을 최대한 활용
3. **에러 감소**: Agent 4의 체계적 디버깅으로 품질 향상
4. **문서 일관성**: Agent 1의 중앙 관리로 문서 동기화 보장
5. **개발 속도 향상**: 역할별 전문화로 병렬 작업 가능

---

## ⚠️ 주의사항 (Caveats)

1. **과도한 역할 분리 금지**: 간단한 작업은 단일 에이전트가 완료
2. **협업 오버헤드 최소화**: 불필요한 에이전트 호출 지양
3. **컨텍스트 공유**: 에이전트 전환 시 충분한 컨텍스트 전달
4. **Agent 1의 조율 역할**: 혼란 시 Agent 1이 최종 결정

---

## 🔗 참고 자료

- [Claude Marketplace - Plugins](https://claudemarketplaces.com/plugins/anthropics-claude-code)
- [Feature Dev Skill](https://github.com/anthropics/claude-code-plugins)
- [Frontend Design Skill](https://github.com/anthropics/claude-code-plugins)

---

**Next Action**: AGENTS.md 업데이트 및 실전 테스트 시작
