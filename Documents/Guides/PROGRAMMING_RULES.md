# 프로그래밍 규칙 (Programming Rules)

> **TheMoon 프로젝트 개발 시 반드시 준수해야 할 프로그래밍 규칙**
>
> 출처: `.claude/CLAUDE.md` 기반 정리

---

## 📋 목차

1. [7단계 체계적 개발 방법론](#7단계-체계적-개발-방법론)
2. [작업 완료 3단계 필수](#작업-완료-3단계-필수)
3. [코딩 컨벤션](#코딩-컨벤션)
4. [문서화 규칙](#문서화-규칙)
5. [버전 관리 규칙](#버전-관리-규칙)
6. [세션 관리](#세션-관리)
7. [금지 사항](#금지-사항)

---

## 🎯 7단계 체계적 개발 방법론

**모든 프로그래밍 및 플랜 작성 시 반드시 이 순서를 따를 것!**

### 1️⃣ Constitution (원칙)

- **목적**: 프로젝트 기본 원칙, 목표, 제약사항, 기술 스택 결정 원칙 수립
- **산출물**: 기본 원칙 문서, 제약사항 목록

### 2️⃣ Specify (명세)

- **목적**: 무엇을 만들지 상세하게 정의 (기능 요구사항, 입출력, 데이터 구조)
- **산출물**: 기능 명세서, API 스펙, 데이터 모델 정의

### 3️⃣ Clarify (명확화)

- **목적**: 불분명한 부분을 사용자에게 질문하여 해소
- **산출물**: Q&A 문서, 결정사항 기록
- **도구**: `AskUserQuestion` 활용

### 4️⃣ Plan (계획)

- **목적**: 기술 스택과 아키텍처 결정 (어떻게 구현할지)
- **산출물**: 아키텍처 다이어그램, DB 스키마, 파일 구조

### 5️⃣ Tasks (작업 분해)

- **목적**: 실행 가능한 작은 단위로 쪼개기
- **산출물**: 작업 목록 (독립적이고 테스트 가능한 단위)
- **도구**: `TodoWrite` 필수 사용!

### 6️⃣ Implement (구현)

- **목적**: 실제 코드 작성 및 테스트 코드 작성
- **산출물**: 소스 코드, 테스트 코드, 커밋

### 7️⃣ Analyze (검증)

- **목적**: 명세와 코드 일치 여부 확인, 품질 검증, 커버리지 측정
- **산출물**: 테스트 리포트, 커버리지 리포트, 검증 문서

### ❌ 절대 하지 말 것

- 명세 없이 바로 코딩 시작
- 불명확한 부분을 추측으로 진행
- 큰 작업을 분해 없이 한 번에 구현
- 검증 없이 완료 처리

### ✅ 반드시 할 것

- 각 단계의 산출물 확인
- Clarify 단계에서 모든 불확실성 제거
- Tasks 단계에서 TodoWrite 사용
- Analyze 단계에서 명세 대비 검증

---

## 🚨 작업 완료 3단계 필수

**문제**: 코드 작성 후 문서 업데이트를 반복적으로 잊어먹는 현상 발생

**해결**: 모든 작업은 반드시 아래 3단계를 완료해야만 "완료"로 간주

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

### ❌ 절대 하지 말 것

- 커밋 후 문서 업데이트 없이 다음 작업으로 넘어가기
- "나중에 한 번에 업데이트하면 되지" 생각하기
- 사용자가 지적하기 전까지 잊고 있기

### ✅ 반드시 할 것

- 커밋 직후 바로 문서 4종 세트 체크
- 하나라도 빠뜨리면 TodoWrite로 "문서 업데이트" 태스크 추가
- 세션 종료 전 반드시 모든 문서 동기화 확인

---

## 💻 코딩 컨벤션

### 언어별 규칙

#### Python (Backend - FastAPI)

```python
# 1. 타입 힌팅 필수
def get_user(user_id: int) -> User:
    pass

# 2. Docstring 작성 (중요 함수)
def calculate_cost(beans: List[Bean]) -> Decimal:
    """원가를 계산합니다.
    
    Args:
        beans: 원두 리스트
        
    Returns:
        총 원가 (Decimal)
    """
    pass

# 3. Pydantic 모델 활용
from pydantic import BaseModel

class BeanSchema(BaseModel):
    name: str
    price: Decimal
```

#### TypeScript (Frontend - Next.js)

```typescript
// 1. 타입 정의 필수
interface Bean {
  id: number;
  name: string;
  price: number;
}

// 2. 함수형 컴포넌트 사용
export default function BeanCard({ bean }: { bean: Bean }) {
  return <div>{bean.name}</div>;
}

// 3. API 호출 시 에러 핸들링
try {
  const response = await fetch('/api/beans');
  const data = await response.json();
} catch (error) {
  console.error('Failed to fetch beans:', error);
}
```

### 파일 명명 규칙

```
Backend:
- 파일명: snake_case (예: bean_service.py)
- 클래스: PascalCase (예: BeanService)
- 함수: snake_case (예: get_bean_by_id)

Frontend:
- 컴포넌트: PascalCase (예: BeanCard.tsx)
- 유틸: camelCase (예: formatPrice.ts)
- 상수: UPPER_SNAKE_CASE (예: API_BASE_URL)
```

### URL 작성 규칙 (MANDATORY)

#### ❌ 절대 하지 말 것

```
웹앱은 http://localhost:3000에서 실행 중입니다!  ← URL 뒤에 한글 붙음 (클릭 불가)
- URL: http://localhost:3000                        ← URL 뒤에 줄바꿈 없음
```

#### ✅ 반드시 할 것

```
웹앱이 실행되었습니다:

http://localhost:3000

위 주소로 접속하세요.
```

**또는:**

```
접속 정보:

- URL: http://localhost:3000
- 상태: 실행 중
```

**핵심 규칙:**

1. URL 앞: 최소 1개 공백 또는 줄바꿈
2. URL 뒤: 최소 1개 공백 또는 줄바꿈
3. URL 바로 뒤에 한글/특수문자/이모지 절대 금지

---

## 📚 문서화 규칙

### 코드 주석

```python
# ✅ 좋은 예: 왜(Why)를 설명
# 원두 가격 변동성이 크므로 Decimal 사용
price: Decimal

# ❌ 나쁜 예: 무엇(What)을 반복
# 가격을 저장
price: Decimal
```

### README 작성

- 프로젝트 설명 (1-2문장)
- 설치 방법
- 실행 방법
- 주요 기능
- 기여 방법 (선택)

### API 문서

- FastAPI 자동 문서 활용 (`/docs`)
- Endpoint별 설명, 파라미터, 응답 예시 작성

---

## 🔖 버전 관리 규칙

### 빠른 버전 관리 참고

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

### 커밋 메시지 컨벤션

```bash
# 타입: 설명 (한글)
feat: 원두 관리 페이지 추가
fix: 가격 계산 오류 수정
refactor: Bean 서비스 리팩토링
docs: README 업데이트
chore: 패키지 의존성 업데이트
test: 원가 계산 테스트 추가
```

### 버전 동기화 (세션 종료 시 필수!)

```bash
# 현재 버전 확인
CURRENT_VERSION=$(cat logs/VERSION)

# 📄 README.md의 모든 버전 정보를 logs/VERSION과 일치시킬 것!
# - Line 3: 타이틀 버전
# - Line 7: 프로젝트 상태 버전
# - 기타 모든 버전 표기

# 📄 .claude/CLAUDE.md의 버전도 동기화할 것!
# - Line 4: 버전 정보
```

---

## 📋 세션 관리

### 세션 시작 시 (매번 필수)

```bash
# 1. 체크리스트 확인
cat Documents/Progress/SESSION_START_CHECKLIST.md

# 2. 지난 세션 요약 읽기
ls -lt Documents/Progress/SESSION_SUMMARY_*.md | head -1

# 3. 버전 규칙 확인 (필요시)
cat logs/VERSION_MANAGEMENT.md | head -50
```

### 작업 완료 후 처리 (각 작업마다)

```bash
# 1. 변경사항 확인
git status

# 2. 커밋
git add .
git commit -m "type: 한글 설명"

# 3. 최종 확인
git log --oneline -1
```

### 세션 종료 시 (매번 필수)

```bash
# 1. 종료 체크리스트 완료
cat Documents/Progress/SESSION_END_CHECKLIST.md

# 2. 세션 요약 작성
# Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md

# 3. 버전 업데이트 (누적 기준 충족 시)
./venv/bin/python logs/update_version.py \
  --type patch \
  --summary "이번 세션의 작업 요약"

# 4. README.md, CLAUDE.md 버전 동기화
```

---

## 🚫 금지 사항

### 파일 생성 금지

**❌ 절대 하지 말 것**: 공식 세션 관리 파일 외에 새로운 파일 생성

```
금지 예시:
❌ .claude/SESSION_CONTEXT.md
❌ .claude/RULES_CHECKLIST.md
❌ .claude/NEXT_SESSION_PROMPT.md
```

**✅ 대신 할 것**: 기존 6개 파일만 사용

1. `Documents/Progress/SESSION_START_CHECKLIST.md`
2. `Documents/Progress/SESSION_END_CHECKLIST.md`
3. `logs/VERSION_MANAGEMENT.md`
4. `Documents/Progress/SESSION_SUMMARY_*.md`
5. `logs/CHANGELOG.md`
6. `logs/VERSION`

### 코드 작성 금지

**❌ 절대 하지 말 것**:

- 원본 프로젝트(`/mnt/d/Ai/WslProject/TheMoon_Project/`)에서 코드 복사
- 명세 없이 코딩 시작
- 테스트 없이 기능 구현
- 문서 업데이트 없이 커밋

### 버전 관리 금지

**❌ 절대 하지 말 것**:

- 작은 변경사항마다 버전 올리기
- 커밋 없이 버전만 올리기
- 버전 동기화 없이 세션 종료

---

## 📖 참고 문서

| 문서 | 위치 | 용도 |
|------|------|------|
| **개발 가이드** | `Documents/Architecture/DEVELOPMENT_GUIDE.md` | 5단계 개발 프로세스 |
| **시스템 아키텍처** | `Documents/Architecture/SYSTEM_ARCHITECTURE.md` | 3계층 아키텍처 & 데이터 흐름 |
| **문제 해결** | `Documents/Architecture/TROUBLESHOOTING.md` | 16가지 오류 & 해결법 |
| **자주 하는 작업** | `Documents/Architecture/COMMON_TASKS.md` | 25가지 작업 단계 가이드 |
| **버전 관리** | `logs/VERSION_MANAGEMENT.md` | 공식 버전 관리 가이드 |
| **버전 전략** | `logs/VERSION_STRATEGY.md` | 효율적인 버전관리 전략 |

---

## 🎯 체크리스트

### 코딩 전 체크

- [ ] 명세서 작성 완료?
- [ ] 불명확한 부분 질문으로 해소?
- [ ] 작업 단위로 분해 완료? (TodoWrite 사용)

### 코딩 중 체크

- [ ] 타입 힌팅/정의 추가?
- [ ] 주요 함수에 docstring/주석?
- [ ] 에러 핸들링 구현?
- [ ] 테스트 코드 작성?

### 커밋 전 체크

- [ ] 코드 리뷰 (self-review)?
- [ ] 테스트 통과?
- [ ] 커밋 메시지 작성 (타입: 설명)?

### 커밋 후 체크

- [ ] logs/CHANGELOG.md 업데이트?
- [ ] SESSION_SUMMARY 업데이트?
- [ ] README.md 확인? (필요 시)
- [ ] .claude/CLAUDE.md 확인? (필요 시)

### 세션 종료 전 체크

- [ ] 모든 커밋 완료?
- [ ] 버전 업데이트 필요? (누적 기준 확인)
- [ ] 모든 문서 버전 동기화?
- [ ] SESSION_END_CHECKLIST 완료?

---

**마지막 업데이트**: 2025-11-29  
**기반 문서**: `.claude/CLAUDE.md`  
**프로젝트**: TheMoon v0.0.3
