# MAS (Multi-Agent System) 사용자 가이드

> **작성일**: 2025-12-27
> **대상**: TheMoon 프로젝트 개발자 및 AI 협업자
> **목적**: MAS를 효과적으로 활용하여 개발 품질과 속도 향상

---

## 📌 개요

TheMoon 프로젝트는 **4인 1조 전문가 팀** 체제로 운영됩니다. 각 AI 에이전트는 특정 역할에 집중하여 높은 품질의 결과물을 생산합니다.

### 🎭 4인 에이전트 팀

| Agent | 역할 | 전문 분야 | 주요 스킬 |
|:------|:-----|:---------|:---------|
| **Agent 1** | Project Architect (PM) | 기획, 문서, 관리 | `commit-commands`, `hookify`, `plugin-dev` |
| **Agent 2** | Frontend Specialist | UI, UX, 디자인 | `frontend-design` ⭐, `feature-dev` |
| **Agent 3** | Backend Engineer | 서버, DB, 로직 | `feature-dev`, `code-review` |
| **Agent 4** | System Maintainer | QA, 버그, 인프라 | `pr-review-toolkit` ⭐, `code-review` |

---

## 🚀 빠른 시작 (Quick Start)

### 1. 에이전트 호출 방법

#### 자동 전환 (작업 키워드 기반)
```
"로스팅 대시보드 디자인 개선해줘"
→ Agent 2 (Frontend) 자동 활성화
```

#### 명시적 호출
```
@Agent2 404 페이지 애니메이션 추가해줘
@Agent3 Bean Repository 패턴 적용해줘
@Agent4 빌드 에러 해결해줘
@Agent1 세션 요약 작성해줘
```

### 2. 스킬 사용 방법

#### Claude Code (직접 실행)
```bash
# Agent 2
/frontend-design "404 에러 페이지 - 귀여운 커피 마스코트 테마"

# Agent 4
/review-pr 123

# Agent 1
/commit -m "feat: 로스팅 필터 기능 추가"
```

#### Gemini 3 Pro (시뮬레이션)
```
[Agent 2] frontend-design 스킬을 시뮬레이션합니다.
1. read_file: 기존 컴포넌트 구조 파악
2. write_file: React/Tailwind 코드 작성
...
[Agent 2] ✅ frontend-design 시뮬레이션 완료
```

---

## 🎯 사용 시나리오

### 시나리오 1: 새로운 기능 추가

**요청**: "로스팅 이력에 커피 종류 필터를 추가해줘"

#### 단계별 진행

**1단계: Agent 1이 요구사항 분석**
```
[Agent 1] 작업 분석:
- Frontend: 필터 UI 추가 (Agent 2)
- Backend: API 필터 파라미터 추가 (Agent 3)
- 검증: 통합 테스트 (Agent 4)
```

**2단계: Agent 2가 Frontend 구현**
```
[사용자] "@Agent2 로스팅 이력 필터 UI 만들어줘"

[Agent 2] frontend-design 스킬 사용:
- 파일: frontend/components/roasting/RoastingHistoryFilters.tsx
- 디자인: Dropdown + Search + Clear 버튼
- 반응형: 모바일 대응
✅ 완료
```

**3단계: Agent 3이 Backend 구현**
```
[Agent 2] "@Agent3: /api/roasting/logs에 coffee_type 쿼리 파라미터 추가 요청"

[Agent 3] 구현 완료:
- Repository: get_multi() 필터 로직 추가
- Schema: 타입 힌팅 추가
- 반환 타입: List[RoastingLog]
✅ 완료. 타입: Optional[str]
```

**4단계: Agent 2가 연동 완료**
```
[Agent 2] Backend API 연동:
- api/roasting.ts에 coffee_type 파라미터 추가
- 필터 컴포넌트와 연결
✅ 빌드 성공
```

**5단계: Agent 4가 품질 검증**
```
[Agent 4] pr-review-toolkit 사용:
- ESLint: ✅ 통과
- Pylint: ✅ 통과
- 타입 체크: ✅ 통과
- 보안: ✅ 이슈 없음
✅ 승인 (Approve)
```

**결과**: 4명의 에이전트가 협업하여 30분 내 완성

---

### 시나리오 2: 버그 수정

**요청**: "로그인 후 대시보드가 안 떠요"

#### 단계별 진행

**1단계: Agent 4가 디버깅**
```
[Agent 4] 로그 확인:
- 브라우저 콘솔: TypeError: Cannot read property 'name'
- 원인: User 객체가 null
```

**2단계: Agent 4가 원인 파악**
```
[Agent 4] 코드 분석:
- frontend/app/dashboard/page.tsx:42
- user.name 접근 전 null 체크 누락
- @Agent2: Optional chaining 추가 필요
```

**3단계: Agent 2가 수정**
```
[Agent 2] 수정 완료:
- user.name → user?.name
- user.email → user?.email
✅ 빌드 성공
```

**4단계: Agent 4가 재검증**
```
[Agent 4] 테스트:
- 로그인 후 대시보드: ✅ 정상
- 비로그인 상태: ✅ 정상 (리다이렉트)
✅ 버그 해결 확인
```

**결과**: 10분 내 버그 해결

---

### 시나리오 3: 아키텍처 개선

**요청**: "Inventory 모듈에 Repository 패턴 적용해줘"

#### 단계별 진행

**1단계: Agent 1이 계획 수립**
```
[Agent 1] 작업 계획:
- Bean Repository 패턴 참조
- 타입 힌팅 일관성 확보
- Service Layer 순수성 검증
→ @Agent3 담당
```

**2단계: Agent 3이 구현**
```
[Agent 3] InventoryRepository 생성:
- 파일: backend/app/repositories/inventory_repository.py
- 타입: Session, Optional, List, Dict
- 메서드: get_by_bean_id(), get_multi(), get_fifo_cost()
✅ 완료
```

**3단계: Agent 3이 Service 리팩토링**
```
[Agent 3] inventory_service.py 수정:
- db.query() 직접 호출 → Repository 사용
- Service 순수성 유지
✅ Mypy 통과
```

**4단계: Agent 4가 리뷰**
```
[Agent 4] code-review 스킬:
- Clean Architecture: ✅ 준수
- 타입 안전성: ✅ 완벽
- 테스트 필요: ⚠️ 유닛 테스트 추가 권장
✅ 승인 (Approve with Comments)
```

**결과**: 45분 내 아키텍처 개선 완료

---

## 💡 협업 패턴

### 패턴 1: Frontend → Backend 요청

**상황**: Frontend 개발 중 API 수정 필요

```
[Agent 2] "현재 API 응답에 created_at 필드가 없습니다."
[Agent 2] "@Agent3: /api/beans/{id} 응답에 created_at 추가 요청"

[Agent 3] "Bean Schema에 created_at 추가 완료"
[Agent 3] "@Agent2: 타입: datetime (ISO 8601 형식)"

[Agent 2] "타입 정의 업데이트 완료"
```

### 패턴 2: Backend → Frontend 통보

**상황**: Backend API 스펙 변경

```
[Agent 3] "RoastingLog API 응답 구조 변경"
[Agent 3] "@Agent2: batch_no 필드 타입이 int → str로 변경됨"

[Agent 2] "frontend/lib/api/roasting.ts 타입 업데이트 완료"
[Agent 2] "영향받은 컴포넌트 3개 수정 완료"
```

### 패턴 3: 긴급 에러 해결

**상황**: 빌드 또는 런타임 에러

```
[Agent 2] "TypeError: undefined is not a function"
[Agent 2] "@Agent4: 디버깅 요청"

[Agent 4] "원인: lodash import 누락"
[Agent 4] "해결: npm install lodash @types/lodash"
✅ 직접 수정 완료
```

---

## 🎨 에이전트별 작업 예시

### Agent 1 (Project Architect)

**전문 분야**:
- 세션 시작/종료 관리
- 문서 작성 (CHANGELOG, SESSION_SUMMARY)
- 아키텍처 설계
- 에이전트 간 조율

**작업 예시**:
```
"세션 요약 작성해줘"
"다음 Phase 계획 수립해줘"
"AGENTS.md 업데이트해줘"
```

**금지 사항**:
- ❌ 직접적인 코딩 (문서 제외)
- ❌ 추측으로 문제 해결

---

### Agent 2 (Frontend Specialist)

**전문 분야**:
- React 컴포넌트 설계
- Tailwind CSS 스타일링
- 애니메이션 구현
- UX 최적화

**작업 예시**:
```
"@Agent2 로스팅 차트 컴포넌트 만들어줘"
"@Agent2 404 페이지 디자인 개선"
"/frontend-design 로스팅 대시보드 Bento Grid"
```

**금지 사항**:
- ❌ `backend/` 폴더 접근
- ❌ API 로직 수정 (Agent 3에게 요청)

**협업 예시**:
```
[Agent 2] "@Agent3: API에 date_range 필터 추가 필요"
```

---

### Agent 3 (Backend Engineer)

**전문 분야**:
- FastAPI 엔드포인트
- Repository Pattern
- 데이터 무결성
- 비즈니스 로직

**작업 예시**:
```
"@Agent3 Bean API 필터 추가해줘"
"@Agent3 Repository 패턴 적용"
"@Agent3 FIFO 원가 계산 로직 검증"
```

**금지 사항**:
- ❌ `frontend/components` 직접 수정

**협업 예시**:
```
[Agent 3] "@Agent2: API 엔드포인트 응답 구조 변경됨"
```

---

### Agent 4 (System Maintainer)

**전문 분야**:
- 디버깅
- 코드 리뷰
- 빌드 에러 해결
- 시스템 통합

**작업 예시**:
```
"@Agent4 빌드 에러 해결해줘"
"@Agent4 PR 리뷰해줘"
"/review-pr 123"
```

**특별 권한**:
- ✅ 긴급 시 모든 파일 수정 가능
- ✅ 에이전트 간 충돌 조정

**협업 예시**:
```
[Agent 4] "@Agent2: 타입 에러 발견, 수정 방법 제시"
```

---

## 🔧 고급 활용법

### 1. 병렬 작업 요청

**단일 요청으로 여러 에이전트 활성화**:
```
"로스팅 기능을 개선하고 싶어요:
- Frontend: 필터 UI 추가 (@Agent2)
- Backend: 통계 API 추가 (@Agent3)
- 문서: 기능 명세 작성 (@Agent1)"
```

**결과**: 3명이 동시에 작업 시작

---

### 2. 단계별 검증 요청

**각 단계마다 Agent 4 검증**:
```
[Agent 2] "404 페이지 완성"
[@Agent4 코드 리뷰]
✅ 승인

[Agent 3] "API 구현 완료"
[@Agent4 코드 리뷰]
✅ 승인

[@Agent4 통합 테스트]
✅ 전체 승인
```

---

### 3. 아키텍처 논의

**Agent 1과 Agent 3의 설계 협의**:
```
[사용자] "@Agent1 Inventory 모듈 리팩토링 계획 세워줘"

[Agent 1] "계획 수립 완료. @Agent3 리뷰 요청"

[Agent 3] "Repository 패턴 적용 동의. 단, FIFO 로직은 Service에 유지 제안"

[Agent 1] "Agent 3 제안 반영. 최종 계획 업데이트"
```

---

## ❓ FAQ (자주 묻는 질문)

### Q1: 에이전트를 명시적으로 호출해야 하나요?

**A**: 아니요, 선택사항입니다.

- **자동 전환**: 작업 키워드로 자동 감지
  - "디자인" → Agent 2
  - "API" → Agent 3
  - "에러" → Agent 4

- **명시적 호출**: 더 정확한 제어 원할 때
  - `@Agent2 ...`

### Q2: 여러 에이전트가 동시에 작업할 수 있나요?

**A**: 네, 가능합니다.

병렬 작업 예시:
```
"@Agent2 Frontend 구현
@Agent3 Backend 구현"
```

### Q3: 에이전트가 실수하면 어떻게 하나요?

**A**: Agent 4에게 요청하세요.

```
"@Agent4 Agent 2가 만든 코드 리뷰해줘"
```

Agent 4는 모든 에이전트의 작업을 검증할 수 있습니다.

### Q4: Claude Code와 Gemini 3 Pro의 차이는?

**A**: 스킬 실행 방식이 다릅니다.

| 항목 | Claude Code | Gemini 3 Pro |
|:-----|:-----------|:------------|
| 스킬 실행 | 직접 실행 (`/frontend-design`) | 시뮬레이션 (도구 조합) |
| 품질 | 동일 | 동일 |
| 문서 | AGENTS.md "🔵 Claude Code" | AGENTS.md "🟢 Gemini 3 Pro" |

### Q5: 테스트는 누가 담당하나요?

**A**: Agent 4 (System Maintainer)

- 유닛 테스트 작성
- E2E 테스트 시나리오
- PR 리뷰 시 테스트 검증

### Q6: 문서는 누가 작성하나요?

**A**: Agent 1 (Project Architect)

- CHANGELOG.md
- SESSION_SUMMARY_*.md
- 아키텍처 문서
- 계획 문서

### Q7: 긴급한 버그는?

**A**: Agent 4에게 즉시 요청

```
"@Agent4 프로덕션 에러 발생! 로그인 안 됨"
```

Agent 4는 모든 파일 수정 권한이 있어 빠르게 대응합니다.

### Q8: 에이전트 간 의견 충돌이 발생하면?

**A**: Agent 1이 최종 결정

```
[Agent 2] "컴포넌트 A 방식 제안"
[Agent 3] "컴포넌트 B 방식 선호"
[Agent 1] "프로젝트 일관성을 위해 A 방식 채택"
```

### Q9: 스킬을 직접 호출할 수 있나요?

**A**: Claude Code에서만 가능

```bash
# Claude Code ✅
/frontend-design "..."
/review-pr 123

# Gemini 3 Pro ❌
# 대신 에이전트에게 요청
"@Agent2 frontend-design 스킬 사용해서 ..."
```

### Q10: 작업 진행 상황을 어떻게 확인하나요?

**A**: TodoWrite 도구 사용

각 에이전트는 작업 시작 시 Todo 작성:
```
1. [in_progress] 404 페이지 디자인 생성 중
2. [pending] 타입 힌팅 검증
3. [pending] 빌드 테스트
```

---

## 📚 참고 자료

### 필수 문서
- `.agent/AGENTS.md` - MAS 마스터 룰
- `docs/Planning/MAS_ENHANCEMENT_PLAN.md` - 개선 전략
- `docs/Planning/MAS_IMPLEMENTATION_TASKS.md` - 작업 체크리스트

### 추천 읽기
- `docs/Guides/AI_COLLABORATION_WORKFLOW.md` - AI 협업 워크플로우
- `docs/Guides/PROGRAMMING_RULES.md` - 코딩 컨벤션
- `docs/Architecture/SYSTEM_OVERVIEW.md` - 시스템 아키텍처

### 외부 링크
- [Claude Marketplace](https://claudemarketplaces.com/plugins/anthropics-claude-code)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

## 🎓 학습 팁

### 초보자를 위한 조언

1. **작은 작업부터 시작**: "404 페이지 수정"
2. **에이전트 명시적 호출**: `@Agent2 ...`
3. **피드백 요청**: "이 코드 괜찮은지 @Agent4 리뷰해줘"

### 숙련자를 위한 조언

1. **병렬 작업 활용**: 여러 에이전트 동시 실행
2. **아키텍처 논의**: Agent 1, 3과 설계 협의
3. **자동화**: 반복 작업은 Hook으로 자동화

---

**작성자**: Agent 1 (Project Architect)
**최종 업데이트**: 2025-12-27
**버전**: v1.0
