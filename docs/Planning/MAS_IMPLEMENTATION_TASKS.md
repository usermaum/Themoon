# MAS Implementation Tasks

> **작성일**: 2025-12-27
> **목적**: Multi-Agent System 실행 계획 및 작업 체크리스트
> **담당**: Agent 1 (Project Architect)

---

## 📊 현재 상태 (Status)

### ✅ 완료된 작업 (Completed)
- [x] MAS 개념 정의 (`AGENTS.md` 초기 작성)
- [x] 에이전트별 역할 분담 설계
- [x] MAS Enhancement Plan 문서 작성
- [x] `AGENTS.md` 스킬/도구 매핑 업데이트
- [x] 역할 전환 프로토콜 명시

### 🚧 진행 중 (In Progress)
- [ ] 실전 테스트 (Phase 2)
- [ ] 사용자 가이드 문서 작성 (Phase 3)

---

## 🎯 Phase 1: Core Setup (완료 ✅)

### Task 1.1: AGENTS.md 업데이트 ✅
**담당**: Agent 1 (Project Architect)
**우선순위**: ⭐⭐⭐ (Critical)

**체크리스트**:
- [x] 에이전트별 할당 스킬 명시
- [x] 허용 도구(Tools) 리스트 추가
- [x] 협업 프로토콜 예시 추가
- [x] 역할 전환 규칙 테이블 작성
- [x] 스킬 호출 문법 가이드 추가

**결과물**:
- `.agent/AGENTS.md` (스킬/도구 매핑 섹션 추가)

---

## 🧪 Phase 2: Practical Testing (다음 단계)

### Task 2.1: Agent 2 - Frontend Design 스킬 테스트
**담당**: Agent 2 (Frontend Specialist)
**우선순위**: ⭐⭐⭐ (High)
**예상 시간**: 30분

**목표**: `frontend-design` 스킬을 사용하여 실제 컴포넌트 생성 검증

**작업 내용**:
1. **마스코트 에러 페이지 생성**
   - `/frontend-design "404 에러 페이지 - 귀여운 커피 마스코트 테마"`
   - 컴포넌트: `frontend/app/not-found.tsx` (기존 파일 개선)
   - 애니메이션 및 Tailwind CSS 활용

2. **검증 항목**:
   - [ ] `frontend-design` 스킬 정상 호출
   - [ ] 생성된 컴포넌트 품질 확인 (심미성, 반응형)
   - [ ] Shadcn UI 컴포넌트 재사용성 확인
   - [ ] 타입 에러 없음 (`npm run build` 통과)

3. **협업 테스트**:
   - [ ] Agent 2가 API 데이터 필요 시 Agent 3에게 요청 시뮬레이션
   - [ ] Agent 3의 응답 프로토콜 검증

**성공 기준**:
- 스킬 호출 후 5분 내 작동하는 컴포넌트 생성
- 에러 없이 빌드 통과
- 디자인 품질 사용자 승인

---

### Task 2.2: Agent 3 - Repository Pattern 확장
**담당**: Agent 3 (Backend Engineer)
**우선순위**: ⭐⭐ (Medium)
**예상 시간**: 45분

**목표**: `feature-dev` 스킬을 사용하여 Clean Architecture 적용 확대

**작업 내용**:
1. **Roasting Log Repository 생성**
   - `/feature-dev "RoastingLogRepository 구현 - Bean Repository 패턴 참조"`
   - 파일: `backend/app/repositories/roasting_log_repository.py`
   - 기존 `roasting_log_service.py`에서 DB 접근 로직 분리

2. **검증 항목**:
   - [ ] Repository Pattern 일관성 (Bean Repository와 동일한 구조)
   - [ ] Service Layer 순수성 유지 (Pydantic Schema만 사용)
   - [ ] 타입 힌팅 완벽 준수
   - [ ] 테스트 코드 작성 가능 (Mock 가능 구조)

3. **협업 테스트**:
   - [ ] Agent 3이 API 스펙 변경 시 Agent 2에게 통보
   - [ ] Agent 2가 `frontend/lib/api/roasting.ts` 타입 업데이트

**성공 기준**:
- Repository 패턴 적용 완료
- `check_quality.sh` 통과 (Pylint, Mypy)
- Agent 2와 협업 프로토콜 정상 작동

---

### Task 2.3: Agent 4 - PR 리뷰 및 품질 검증
**담당**: Agent 4 (System Maintainer)
**우선순위**: ⭐⭐ (Medium)
**예상 시간**: 20분

**목표**: `pr-review-toolkit` 스킬을 사용하여 코드 품질 검증

**작업 내용**:
1. **Task 2.1, 2.2 완료 후 통합 리뷰**
   - `/review-pr` (현재 변경사항 리뷰)
   - Frontend 컴포넌트 및 Backend Repository 품질 검증

2. **검증 항목**:
   - [ ] 코드 스타일 일관성 (Frontend: ESLint, Backend: Pylint)
   - [ ] 타입 안전성 (TypeScript, Python Type Hints)
   - [ ] Clean Architecture 원칙 준수
   - [ ] 에러 핸들링 적절성
   - [ ] 성능 이슈 없음

3. **에러 수정 시나리오**:
   - [ ] 에러 발견 시 `@Agent2/3: {수정 방법}` 통보
   - [ ] 긴급 시 직접 수정 (Cross-Cutting 권한 활용)

**성공 기준**:
- 모든 린트 검사 통과
- 보안 취약점 없음
- Agent 2/3과 협업 원활

---

## 📚 Phase 3: Documentation (우선순위 낮음)

### Task 3.1: 사용자 가이드 작성
**담당**: Agent 1 (Project Architect)
**우선순위**: ⭐ (Low)
**예상 시간**: 30분

**작업 내용**:
1. **MAS 사용자 가이드 작성**
   - 파일: `docs/Guides/MAS_USAGE_GUIDE.md`
   - 내용: 에이전트 호출 방법, 협업 시나리오 예시, FAQ

2. **체크리스트**:
   - [ ] 에이전트 호출 방법 (명시적/자동)
   - [ ] 스킬 사용 예시 (각 에이전트별)
   - [ ] 협업 시나리오 케이스 스터디 3개 이상
   - [ ] 트러블슈팅 FAQ 5개 이상

---

### Task 3.2: 아키텍처 다이어그램 업데이트
**담당**: Agent 1 (Project Architect)
**우선순위**: ⭐ (Low)
**예상 시간**: 20분

**작업 내용**:
1. **MAS 협업 플로우 다이어그램 추가**
   - 파일: `docs/Architecture/MAS_FLOW.md`
   - Mermaid 다이어그램으로 에이전트 간 협업 흐름 시각화

2. **체크리스트**:
   - [ ] Mermaid v8.8.0 호환성 확인
   - [ ] 사용자 → Agent → 협업 → 완료 플로우
   - [ ] 각 에이전트별 스킬 호출 시점 표시

---

## 🔄 Phase 4: Continuous Improvement (지속적)

### Task 4.1: 협업 패턴 개선
**담당**: All Agents
**우선순위**: 지속적 개선
**예상 시간**: 세션마다 10분

**작업 내용**:
1. **협업 시 발생한 문제점 기록**
   - 파일: `docs/Progress/MAS_RETROSPECTIVE.md`
   - 협업 실패 사례, 개선 방안 기록

2. **분기별 회고**:
   - [ ] 에이전트 역할 분담 적절성 검토
   - [ ] 스킬 활용도 분석
   - [ ] 협업 프로토콜 개선점 도출

---

## 📋 즉시 실행 가능한 Next Steps

### 🎯 우선순위 1 (오늘 완료 목표)
1. **Task 2.1**: Agent 2가 `frontend-design` 스킬로 마스코트 에러 페이지 생성
   - 예상 시간: 30분
   - 명령: `@Agent2 /frontend-design "404 에러 페이지 - 귀여운 커피 마스코트 테마"`

### 🎯 우선순위 2 (이번 주 목표)
2. **Task 2.2**: Agent 3이 Roasting Log Repository 구현
   - 예상 시간: 45분
   - 명령: `@Agent3 RoastingLogRepository 패턴 적용`

3. **Task 2.3**: Agent 4가 PR 리뷰 및 품질 검증
   - 예상 시간: 20분
   - 명령: `@Agent4 /review-pr`

### 🎯 우선순위 3 (다음 주 목표)
4. **Task 3.1**: Agent 1이 사용자 가이드 작성
   - 예상 시간: 30분

---

## 🎨 협업 시나리오 예시 (Quick Reference)

### 시나리오 1: Frontend 개발 중 API 수정 필요
```
[사용자] "@Agent2 로스팅 이력에 커피 종류 필터 추가해줘"
    ↓
[Agent 2] "API에 coffee_type 필드 필요 → @Agent3: /api/roasting/logs에 coffee_type 쿼리 파라미터 추가 요청"
    ↓
[Agent 3] "coffee_type 필터 추가 완료. 타입: Optional[str]"
    ↓
[Agent 2] "frontend 필터 UI 구현 완료"
```

### 시나리오 2: Backend 개발 후 Frontend 타입 동기화
```
[Agent 3] "RoastingLog 스키마에 batch_number 필드 추가 → @Agent2: 타입 정의 업데이트 필요"
    ↓
[Agent 2] "frontend/lib/api/roasting.ts의 RoastingLog 인터페이스에 batch_number 추가 완료"
```

### 시나리오 3: 빌드 에러 발생
```
[Agent 2] "빌드 에러: Type 'string' is not assignable to type 'number'"
    ↓
[Agent 2] "@Agent4: 타입 에러 디버깅 요청"
    ↓
[Agent 4] "원인: API 응답 타입 불일치 → @Agent3: /api/beans/{id} 응답 스키마 확인 필요"
    ↓
[Agent 3] "스키마 수정 완료"
    ↓
[Agent 4] "빌드 에러 해결 확인"
```

---

## 📊 성공 지표 (Success Metrics)

### Phase 2 완료 기준
- [ ] 3개 에이전트(2, 3, 4) 모두 스킬 정상 사용
- [ ] 협업 프로토콜 3회 이상 성공적 실행
- [ ] 코드 품질 검사 모두 통과 (ESLint, Pylint, Mypy)
- [ ] 빌드 에러 0건

### Phase 3 완료 기준
- [ ] 사용자 가이드 문서 완성도 90% 이상
- [ ] Mermaid 다이어그램 3개 이상
- [ ] FAQ 5개 이상 작성

---

## 🚀 실행 순서 요약

```
1️⃣ 오늘 (2025-12-27)
   └─ Task 2.1: Agent 2가 마스코트 에러 페이지 생성

2️⃣ 이번 주 (2025-12-27 ~ 2025-12-31)
   ├─ Task 2.2: Agent 3이 Repository 패턴 확장
   └─ Task 2.3: Agent 4가 PR 리뷰

3️⃣ 다음 주 (2026-01-01 ~ 2026-01-07)
   ├─ Task 3.1: 사용자 가이드 작성
   └─ Task 3.2: 아키텍처 다이어그램

4️⃣ 지속적 (매 세션)
   └─ Task 4.1: 협업 패턴 회고 및 개선
```

---

## 📝 보고 (Report)

### 현재 상태
- **Phase 1 (Core Setup)**: ✅ 100% 완료
- **Phase 2 (Practical Testing)**: 🚧 0% (대기 중)
- **Phase 3 (Documentation)**: ⏸️ 대기
- **Phase 4 (Continuous Improvement)**: ⏸️ 대기

### 다음 액션
1. **즉시 실행**: Task 2.1 (Agent 2 - Frontend Design 테스트)
2. **사용자 결정 필요**: 마스코트 에러 페이지 디자인 방향성 승인

### 예상 완료 시점
- Phase 2: 2025-12-31 (이번 주 내)
- Phase 3: 2026-01-07 (다음 주)
- Phase 4: 지속적 개선

---

**문서 작성**: Agent 1 (Project Architect)
**작성 일시**: 2025-12-27
**다음 리뷰**: Phase 2 완료 후
