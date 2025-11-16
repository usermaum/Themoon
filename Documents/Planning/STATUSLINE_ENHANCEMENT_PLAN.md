# statusline 사용량 표시 기능 개선 플랜

> **프로젝트**: The Moon Drip BAR - 로스팅 비용 계산기
> **대상**: Claude Code statusline 커스터마이징
> **버전**: 1.1.0 (독립 실행 가능)
> **작성일**: 2025-11-16
> **방법론**: 7단계 체계적 개발 방법론

---

## 📋 목차

1. [Constitution (원칙)](#1-constitution-원칙)
2. [Specify (명세)](#2-specify-명세)
3. [Clarify (명확화)](#3-clarify-명확화)
4. [Plan (계획)](#4-plan-계획)
5. [Tasks (작업 분해)](#5-tasks-작업-분해)
6. [Technical Specifications (기술 사양)](#6-technical-specifications-기술-사양)
7. [Next Steps (다음 단계)](#7-next-steps-다음-단계)

---

## 1. Constitution (원칙)

### 1.1 프로젝트 기본 원칙

**목표:**
- Claude Desktop의 사용량 정보(모델, 프로젝트, 토큰, 비용)를 statusline에 실시간 표시
- 사용자에게 직관적이고 유용한 정보 제공
- 시각적으로 깔끔하고 이해하기 쉬운 인터페이스

**핵심 가치:**
1. **실용성**: 실제로 필요한 정보만 표시
2. **간결성**: 한 줄에 핵심 정보 집약
3. **확장성**: 향후 추가 정보 표시 용이
4. **성능**: statusline 업데이트가 작업 흐름을 방해하지 않음

### 1.2 제약사항

**기술적 제약:**
- WSL(Windows Subsystem for Linux) 환경에서 작동
- Claude Code가 제공하는 stdin JSON 구조에 의존
- ~/.config/claude/.claude.json 파일의 읽기 권한 필요
- Bash 스크립트 환경 (sh 호환)

**정보 제약:**
- Claude Desktop의 공식 API 없음 (내부 구조 역엔지니어링 필요)
- "플랜 사용량 50%" 같은 정확한 계산식 불명
- 주간 한도 정보의 정확한 소스 불명

**성능 제약:**
- 매 statusline 업데이트마다 실행 (빈번한 호출)
- 파일 I/O 최소화 필요
- 실행 시간 < 100ms 권장

### 1.3 기술 스택 결정 원칙

**선택 기준:**
1. 기존 시스템과의 호환성 (statusline.sh)
2. 최소 의존성 (외부 패키지 최소화)
3. 유지보수 용이성
4. 성능 (빠른 실행 속도)

**채택 기술:**
- **Bash**: 메인 스크립트 언어 (기존 사용 중)
- **jq**: JSON 파싱 (경량, 빠름)
- **bc**: 수치 계산 (기존 사용 중)

---

## 2. Specify (명세)

### 2.1 기능 요구사항

#### FR-1: 현재 모델 표시
- **입력**: stdin JSON의 `model` 필드
- **출력**: 간략화된 모델 이름 (예: `claude-sonnet-4-5-20250929` → `sonnet-4-5`)
- **형식**: `🤖 {model_name}`
- **우선순위**: 높음

#### FR-2: 프로젝트 이름 표시
- **입력**: 현재 작업 디렉토리 (PWD)
- **출력**: 프로젝트 디렉토리의 basename
- **형식**: `📁 {project_name}`
- **우선순위**: 높음

#### FR-3: 토큰 사용량 표시
- **입력**: stdin JSON의 `cost.total_input_tokens`, `cost.token_limit`
- **출력**: 토큰 수와 백분율
- **형식**: `🧠 {tokens}K ({percent}%)`
- **우선순위**: 높음

#### FR-4: 비용 정보 표시
- **입력**: stdin JSON의 `cost.total_cost_usd`, `cost.today_cost_usd`
- **출력**: 세션 비용 / 오늘 누적 비용
- **형식**: `💰 ${session_cost}/${today_cost}`
- **우선순위**: 중간

#### FR-5: 색상 코딩
- **조건**: 사용량 백분율에 따라 색상 변경
- **규칙**:
  - 0-50%: 녹색 (`\033[32m`)
  - 51-80%: 노란색 (`\033[33m`)
  - 81-100%: 빨간색 (`\033[31m`)
- **우선순위**: 낮음

### 2.2 비기능 요구사항

#### NFR-1: 성능
- 실행 시간: < 100ms
- 메모리 사용: < 10MB
- CPU 사용: 최소화

#### NFR-2: 안정성
- JSON 파싱 실패 시 fallback 동작
- 파일 접근 실패 시 에러 핸들링
- 모든 필드 optional 처리

#### NFR-3: 호환성
- Bash 4.0+ 호환
- 기존 statusline.sh 설정 유지
- UTF-8 이모티콘 지원

### 2.3 입출력 명세

#### 입력 (stdin JSON 구조)

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "cost": {
    "total_input_tokens": 25000,
    "total_output_tokens": 5000,
    "total_cache_creation_input_tokens": 0,
    "total_cache_read_input_tokens": 15000,
    "token_limit": 200000,
    "total_cost_usd": 0.15,
    "today_cost_usd": 0.50,
    "block_cost_usd": 0.10,
    "block_limit_usd": 0.20,
    "block_time_left_ms": 9000000
  },
  "exceeds_200k_tokens": false
}
```

#### 출력 형식 (3가지 옵션)

**옵션 A: 간결형 (추천)**
```
🤖 sonnet-4-5 | 📁 TheMoon_Project | 💰 $0.15/$0.50 | 🧠 25K (12%)
```

**옵션 B: 상세형**
```
🤖 sonnet-4-5 | 📁 TheMoon_Project | 💰 사용량: 50% (1h 30m left) | 🧠 25K/200K (12%)
```

**옵션 C: Claude Desktop 스타일**
```
💰 사용량: 50% (1h 30m 후 재설정) | 🧠 주간: 49% | 🤖 sonnet-4-5 | 📁 TheMoon
```

---

## 3. Clarify (명확화)

### 3.1 사용자 요구사항 확인

#### Q1: Claude Desktop의 '플랜 사용량 50%'는 어떤 기준으로 계산되나요?

**답변**: 잘 모르겠음. 하지만 플랜(Pro) 기반 사용량 한도 사용.

**결정사항**:
- 토큰 사용량 기반 추정치 사용
- `(total_input_tokens / token_limit) * 100`
- 정확한 플랜 한도는 추후 조사

#### Q2: 정확한 사용량 정보를 못 가져올 경우, 어떤 정보를 우선적으로 표시하시겠습니까?

**답변**: 현재 모델 이름, 프로젝트 이름, 토큰 사용량

**우선순위**:
1. 🤖 현재 모델 이름
2. 📁 프로젝트 이름
3. 🧠 토큰 사용량
4. 💰 비용 정보 (선택적)

#### Q3: statusline 업데이트 방식은 어떻게 하시겠습니까?

**답변**: ccusage 명령 활용

**결정사항**:
- 1차: statusline.sh 개선 (stdin JSON 활용)
- 2차: ccusage 통합 검토 (추후)

### 3.2 기술적 결정사항

| 항목 | 결정 | 이유 |
|------|------|------|
| **메인 방식** | statusline.sh 개선 | 기존 구조 유지, 최소 변경 |
| **JSON 파싱** | jq 사용 | 경량, 빠름, 안정적 |
| **프로젝트 정보** | PWD 기반 | .claude.json 복잡도 회피 |
| **모델 이름** | stdin JSON | Claude Code가 제공 |
| **색상 적용** | ANSI 코드 | 터미널 표준 |

---

## 4. Plan (계획)

### 4.1 아키텍처 개요

```
┌─────────────────────────────────────────────────────────┐
│                    Claude Code                          │
│          (매 메시지마다 stdin JSON 제공)                  │
└────────────────┬────────────────────────────────────────┘
                 │ JSON 입력
                 │ {model, cost, tokens...}
                 ▼
┌─────────────────────────────────────────────────────────┐
│              statusline.sh (Enhanced)                   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 1. stdin JSON 파싱 (jq)                          │  │
│  │    - model, tokens, cost 추출                    │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 2. 프로젝트 정보 수집                             │  │
│  │    - PWD에서 basename 추출                       │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 3. 데이터 가공                                    │  │
│  │    - 모델 이름 간략화                             │  │
│  │    - 토큰 포맷팅 (K, M 단위)                      │  │
│  │    - 백분율 계산                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │ 4. 출력 포맷팅                                    │  │
│  │    - 이모티콘 추가                                │  │
│  │    - 색상 코딩                                    │  │
│  │    - 구분자(|) 삽입                               │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────┘
                 │ 포맷팅된 문자열
                 ▼
┌─────────────────────────────────────────────────────────┐
│              Terminal Statusline                        │
│  🤖 sonnet-4-5 | 📁 TheMoon | 💰 $0.15 | 🧠 25K (12%)   │
└─────────────────────────────────────────────────────────┘
```

### 4.2 구현 방법 비교

#### 방법 1: statusline.sh 개선 (✅ 추천)

**개요:**
- 기존 statusline.sh 파일을 수정
- stdin JSON + PWD 정보 활용
- jq 추가 설치 필요

**장점:**
- ✅ 기존 구조 유지 (호환성 높음)
- ✅ 추가 의존성 최소화 (jq만 추가)
- ✅ 빠른 실행 속도 (Bash 네이티브)
- ✅ 디버깅 용이
- ✅ Claude Code와 자연스러운 통합

**단점:**
- ⚠️ jq 설치 필요 (WSL에서 간단)
- ⚠️ Bash 스크립트 복잡도 증가

**예상 코드 구조:**
```bash
#!/bin/bash
# Enhanced statusline for Claude Code

# 1. stdin JSON 읽기
input=$(cat)

# 2. 필드 추출 (jq)
model=$(echo "$input" | jq -r '.model // "unknown"')
tokens=$(echo "$input" | jq -r '.cost.total_input_tokens // 0')
token_limit=$(echo "$input" | jq -r '.cost.token_limit // 200000')
session_cost=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
today_cost=$(echo "$input" | jq -r '.cost.today_cost_usd // 0')

# 3. 프로젝트 이름 (PWD)
project_name=$(basename "$PWD")

# 4. 데이터 가공
model_short=$(simplify_model_name "$model")
token_percent=$(calc_percent "$tokens" "$token_limit")
tokens_formatted=$(format_tokens "$tokens")

# 5. 출력
printf "🤖 %s | 📁 %s | 💰 \$%.2f/\$%.2f | 🧠 %s (%d%%)" \
    "$model_short" \
    "$project_name" \
    "$session_cost" \
    "$today_cost" \
    "$tokens_formatted" \
    "$token_percent"
```

---

#### 방법 2: ccusage 직접 활용

**개요:**
- `npx ccusage@latest statusline` 명령 활용
- stdin JSON을 ccusage로 전달
- ccusage 출력 + 추가 정보 병합

**장점:**
- ✅ ccusage의 풍부한 통계 활용
- ✅ JSONL 히스토리 기반 분석 가능
- ✅ 향후 확장성 높음

**단점:**
- ❌ ccusage statusline이 stdin 입력 요구
- ❌ Node.js 실행 오버헤드 (느림)
- ❌ 추가 복잡도
- ❌ 프로젝트 이름 표시 어려움

**예상 코드 구조:**
```bash
#!/bin/bash
input=$(cat)

# ccusage에 stdin 전달
ccusage_output=$(echo "$input" | npx ccusage@latest statusline 2>/dev/null)

# 프로젝트 정보 추가
project_name=$(basename "$PWD")

# 병합
echo "📁 $project_name | $ccusage_output"
```

---

#### 방법 3: Python 스크립트 작성

**개요:**
- statusline.py 별도 작성
- Python으로 JSON 파싱 및 로직 처리
- Bash에서 Python 호출

**장점:**
- ✅ 복잡한 로직 처리 용이
- ✅ JSON 파싱 안정적
- ✅ 향후 확장 용이
- ✅ 테스트 작성 쉬움

**단점:**
- ❌ Bash보다 실행 속도 느림
- ❌ 추가 파일 관리 필요
- ❌ Python 환경 의존성

**예상 코드 구조:**
```python
#!/usr/bin/env python3
import json, sys, os
from pathlib import Path

# stdin JSON 읽기
stdin_data = json.load(sys.stdin)

# 데이터 추출
model = stdin_data.get('model', 'unknown')
tokens = stdin_data['cost']['total_input_tokens']
token_limit = stdin_data['cost']['token_limit']
session_cost = stdin_data['cost']['total_cost_usd']

# 프로젝트 정보
project_name = Path.cwd().name

# 출력
print(f"🤖 {simplify_model(model)} | "
      f"📁 {project_name} | "
      f"💰 ${session_cost:.2f} | "
      f"🧠 {format_tokens(tokens)} ({calc_percent(tokens, token_limit)}%)")
```

---

### 4.3 최종 선택: 방법 1 (statusline.sh 개선)

**선택 이유:**

| 기준 | 방법 1 | 방법 2 | 방법 3 |
|------|--------|--------|--------|
| **성능** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **호환성** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **확장성** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **단순성** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **의존성** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **총점** | **21/25** | **16/25** | **19/25** |

**결정**: 방법 1을 1차 목표로 구현, 향후 필요시 방법 3으로 전환

---

## 5. Tasks (작업 분해)

### Phase 1: 환경 준비 (예상: 5분)

#### Task 1.1: jq 설치 확인 및 설치
- **목표**: jq 명령어 사용 가능하게 만들기
- **방법**:
  ```bash
  # 설치 확인
  which jq || sudo apt-get install -y jq

  # 버전 확인
  jq --version
  ```
- **완료 조건**: `jq --version` 정상 출력
- **의존성**: 없음

#### Task 1.2: 현재 statusline.sh 백업
- **목표**: 기존 파일 보호
- **방법**:
  ```bash
  cp statusline.sh statusline.sh.backup-$(date +%Y%m%d)
  ```
- **완료 조건**: 백업 파일 생성 확인
- **의존성**: 없음

#### Task 1.3: stdin JSON 구조 분석
- **목표**: 실제 Claude Code가 제공하는 JSON 필드 확인
- **방법**:
  ```bash
  # 테스트 JSON 생성 및 확인
  echo '{"model":"test","cost":{}}' | ./statusline.sh
  ```
- **완료 조건**: JSON 구조 문서화
- **의존성**: 없음

---

### Phase 2: 핵심 함수 구현 (예상: 15분)

#### Task 2.1: get_current_project() 함수
- **목표**: 현재 프로젝트 이름 추출
- **입력**: 없음 (PWD 사용)
- **출력**: 프로젝트 디렉토리명
- **구현**:
  ```bash
  get_current_project() {
      basename "$PWD"
  }
  ```
- **테스트**:
  ```bash
  # 예상 출력: TheMoon_Project
  get_current_project
  ```
- **완료 조건**: 정상 출력 확인
- **의존성**: 없음

#### Task 2.2: simplify_model_name() 함수
- **목표**: 긴 모델 이름을 짧게 변환
- **입력**: `claude-sonnet-4-5-20250929`
- **출력**: `sonnet-4-5`
- **구현**:
  ```bash
  simplify_model_name() {
      local model="$1"
      # claude-sonnet-4-5-20250929 → sonnet-4-5
      echo "$model" | sed -E 's/claude-([a-z]+)-([0-9]+-[0-9]+).*/\1-\2/'
  }
  ```
- **테스트**:
  ```bash
  # 예상 출력: sonnet-4-5
  simplify_model_name "claude-sonnet-4-5-20250929"
  ```
- **완료 조건**: 여러 모델명으로 테스트 성공
- **의존성**: 없음

#### Task 2.3: format_tokens() 함수
- **목표**: 토큰 수를 K/M 단위로 포맷팅
- **입력**: `25000`
- **출력**: `25K`
- **구현**:
  ```bash
  format_tokens() {
      local tokens="$1"
      if [ "$tokens" -ge 1000000 ]; then
          echo "scale=1; $tokens / 1000000" | bc | sed 's/\.0$//'
          echo "M"
      elif [ "$tokens" -ge 1000 ]; then
          echo "scale=0; $tokens / 1000" | bc
          echo "K"
      else
          echo "$tokens"
      fi | tr -d '\n'
  }
  ```
- **테스트**:
  ```bash
  format_tokens 25000    # 25K
  format_tokens 1500000  # 1.5M
  format_tokens 500      # 500
  ```
- **완료 조건**: 모든 범위 테스트 성공
- **의존성**: bc

#### Task 2.4: calc_percent() 함수
- **목표**: 백분율 계산
- **입력**: `25000`, `200000`
- **출력**: `12`
- **구현**:
  ```bash
  calc_percent() {
      local used="$1"
      local limit="$2"
      if [ "$limit" -eq 0 ]; then
          echo "0"
      else
          echo "scale=0; ($used * 100) / $limit" | bc
      fi
  }
  ```
- **테스트**:
  ```bash
  calc_percent 25000 200000  # 12
  calc_percent 0 200000      # 0
  calc_percent 200000 0      # 0 (division by zero 방지)
  ```
- **완료 조건**: 엣지 케이스 포함 테스트 성공
- **의존성**: bc

#### Task 2.5: get_color_code() 함수
- **목표**: 사용량에 따른 색상 코드 반환
- **입력**: `50` (백분율)
- **출력**: `\033[32m` (녹색)
- **구현**:
  ```bash
  get_color_code() {
      local percent="$1"
      if [ "$percent" -lt 50 ]; then
          echo "\033[32m"  # 녹색
      elif [ "$percent" -lt 80 ]; then
          echo "\033[33m"  # 노란색
      else
          echo "\033[31m"  # 빨간색
      fi
  }
  ```
- **테스트**:
  ```bash
  get_color_code 30   # 녹색
  get_color_code 60   # 노란색
  get_color_code 90   # 빨간색
  ```
- **완료 조건**: 모든 범위 테스트 성공
- **의존성**: 없음

---

### Phase 3: statusline.sh 통합 (예상: 10분)

#### Task 3.1: 메인 로직 작성
- **목표**: 모든 함수를 통합하여 완전한 statusline.sh 작성
- **구현**:
  ```bash
  #!/bin/bash
  # Enhanced statusline for Claude Code

  # 함수 정의 (Task 2.1 ~ 2.5)
  # ...

  # stdin JSON 읽기
  input=$(cat)

  # JSON 파싱 (jq 사용)
  model=$(echo "$input" | jq -r '.model // "unknown"')
  total_tokens=$(echo "$input" | jq -r '.cost.total_input_tokens // 0')
  token_limit=$(echo "$input" | jq -r '.cost.token_limit // 200000')
  session_cost=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
  today_cost=$(echo "$input" | jq -r '.cost.today_cost_usd // 0')

  # 데이터 가공
  project_name=$(get_current_project)
  model_short=$(simplify_model_name "$model")
  tokens_fmt=$(format_tokens "$total_tokens")
  token_percent=$(calc_percent "$total_tokens" "$token_limit")
  color=$(get_color_code "$token_percent")

  # 출력
  printf "🤖 %s | 📁 %s | 💰 \$%.2f/\$%.2f | ${color}🧠 %s (%d%%)\033[0m" \
      "$model_short" \
      "$project_name" \
      "$session_cost" \
      "$today_cost" \
      "$tokens_fmt" \
      "$token_percent"
  ```
- **완료 조건**: 스크립트 문법 오류 없음
- **의존성**: Task 2.1 ~ 2.5 완료

#### Task 3.2: 에러 핸들링 추가
- **목표**: JSON 파싱 실패, 필드 누락 등 대응
- **구현**:
  ```bash
  # jq 설치 확인
  if ! command -v jq &> /dev/null; then
      echo "⚠️  jq not installed"
      exit 1
  fi

  # JSON 유효성 검사
  if ! echo "$input" | jq empty 2>/dev/null; then
      echo "⚠️  Invalid JSON"
      exit 1
  fi

  # 필드 기본값 처리 (위의 // 연산자로 이미 처리됨)
  ```
- **완료 조건**: 잘못된 입력에도 크래시 없음
- **의존성**: Task 3.1 완료

#### Task 3.3: 실행 권한 설정
- **목표**: statusline.sh 실행 가능하게 만들기
- **방법**:
  ```bash
  chmod +x statusline.sh
  ```
- **완료 조건**: `./statusline.sh` 직접 실행 가능
- **의존성**: Task 3.1, 3.2 완료

---

### Phase 4: 테스트 및 검증 (예상: 10분)

#### Task 4.1: 테스트 JSON 생성
- **목표**: 다양한 시나리오 테스트 데이터 준비
- **구현**:
  ```bash
  # 테스트 케이스 1: 정상 입력
  cat > test_normal.json <<'EOF'
  {
    "model": "claude-sonnet-4-5-20250929",
    "cost": {
      "total_input_tokens": 25000,
      "total_output_tokens": 5000,
      "token_limit": 200000,
      "total_cost_usd": 0.15,
      "today_cost_usd": 0.50
    }
  }
  EOF

  # 테스트 케이스 2: 높은 사용량
  cat > test_high_usage.json <<'EOF'
  {
    "model": "claude-opus-4-20250514",
    "cost": {
      "total_input_tokens": 180000,
      "total_output_tokens": 50000,
      "token_limit": 200000,
      "total_cost_usd": 5.25,
      "today_cost_usd": 12.80
    }
  }
  EOF

  # 테스트 케이스 3: 필드 누락
  cat > test_missing_fields.json <<'EOF'
  {
    "model": "claude-haiku-4-5-20250929"
  }
  EOF
  ```
- **완료 조건**: 3개 테스트 파일 생성
- **의존성**: 없음

#### Task 4.2: 수동 테스트 실행
- **목표**: 각 테스트 케이스로 스크립트 검증
- **방법**:
  ```bash
  # 테스트 1
  cat test_normal.json | ./statusline.sh
  # 예상 출력: 🤖 sonnet-4-5 | 📁 TheMoon_Project | 💰 $0.15/$0.50 | 🧠 25K (12%)

  # 테스트 2
  cat test_high_usage.json | ./statusline.sh
  # 예상 출력: 🤖 opus-4 | 📁 TheMoon_Project | 💰 $5.25/$12.80 | 🧠 180K (90%)

  # 테스트 3
  cat test_missing_fields.json | ./statusline.sh
  # 예상 출력: 에러 없이 기본값으로 처리
  ```
- **완료 조건**: 모든 출력 예상대로 작동
- **의존성**: Task 4.1, Phase 3 완료

#### Task 4.3: Claude Code 실제 환경 테스트
- **목표**: 실제 Claude Code에서 statusline 작동 확인
- **방법**:
  ```bash
  # Claude Code 설정 확인
  npx ccusage@latest statusline --help

  # statusline.sh를 Claude Code에 등록
  # (Claude Code 설정 방법은 공식 문서 참조)
  ```
- **완료 조건**: Claude Code에서 커스텀 statusline 표시 확인
- **의존성**: Task 4.2 완료

#### Task 4.4: 엣지 케이스 테스트
- **목표**: 예외 상황 대응 확인
- **테스트 케이스**:
  ```bash
  # 빈 JSON
  echo '{}' | ./statusline.sh

  # 잘못된 JSON
  echo '{invalid json}' | ./statusline.sh

  # token_limit = 0 (division by zero)
  echo '{"cost":{"total_input_tokens":100,"token_limit":0}}' | ./statusline.sh

  # 매우 큰 숫자
  echo '{"cost":{"total_input_tokens":5000000}}' | ./statusline.sh
  # 예상 출력: 5M
  ```
- **완료 조건**: 크래시 없이 모두 처리
- **의존성**: Task 4.2 완료

---

### Phase 5: 문서화 및 정리 (예상: 5분)

#### Task 5.1: README 업데이트
- **목표**: statusline 사용법 문서화
- **추가할 내용**:
  ```markdown
  ## statusline 커스터마이징

  ### 설치 방법
  1. jq 설치: `sudo apt-get install jq`
  2. statusline.sh 실행 권한: `chmod +x statusline.sh`

  ### 출력 형식
  🤖 모델 | 📁 프로젝트 | 💰 비용 | 🧠 토큰 (%)

  ### 테스트
  cat test_normal.json | ./statusline.sh
  ```
- **완료 조건**: README.md에 섹션 추가
- **의존성**: Phase 4 완료

#### Task 5.2: 백업 파일 정리
- **목표**: 불필요한 파일 정리
- **방법**:
  ```bash
  # 테스트 파일 삭제 (선택적)
  rm -f test_*.json

  # 백업 파일은 보관
  ```
- **완료 조건**: 작업 디렉토리 깔끔
- **의존성**: Task 5.1 완료

#### Task 5.3: Git 커밋
- **목표**: 변경사항 저장
- **방법**:
  ```bash
  git add statusline.sh
  git commit -m "feat: statusline에 모델/프로젝트/토큰 사용량 표시 추가"
  ```
- **완료 조건**: 커밋 완료
- **의존성**: Task 5.1, 5.2 완료

---

## 6. Technical Specifications (기술 사양)

### 6.1 시스템 요구사항

| 항목 | 요구사항 | 확인 방법 |
|------|----------|-----------|
| **OS** | Linux (WSL) | `uname -a` |
| **Shell** | Bash 4.0+ | `bash --version` |
| **jq** | 1.5+ | `jq --version` |
| **bc** | GNU bc 1.06+ | `bc --version` |
| **권한** | ~/.config/claude/ 읽기 | `ls -la ~/.config/claude/` |

### 6.2 의존성 목록

| 패키지 | 버전 | 용도 | 설치 명령 |
|--------|------|------|-----------|
| **jq** | 1.5+ | JSON 파싱 | `sudo apt-get install jq` |
| **bc** | 1.06+ | 수치 계산 | 이미 설치됨 |
| **sed** | 4.0+ | 문자열 처리 | 기본 설치 |

### 6.3 파일 구조

```
TheMoon_Project/
├── statusline.sh              # 개선된 statusline 스크립트
├── statusline.sh.backup-*     # 백업 파일
└── Documents/
    └── Planning/
        └── STATUSLINE_ENHANCEMENT_PLAN.md  # 이 문서
```

### 6.4 성능 목표

| 지표 | 목표 | 측정 방법 |
|------|------|-----------|
| **실행 시간** | < 100ms | `time cat test.json \| ./statusline.sh` |
| **메모리 사용** | < 10MB | `ps aux \| grep statusline` |
| **CPU 사용** | < 5% | `top -p $(pgrep statusline)` |

### 6.5 주요 함수 명세

#### `simplify_model_name(model_string)`
- **입력**: `claude-sonnet-4-5-20250929`
- **출력**: `sonnet-4-5`
- **로직**: 정규표현식으로 중간 부분 추출
- **예외**: 알 수 없는 형식은 원본 반환

#### `format_tokens(token_count)`
- **입력**: `25000`
- **출력**: `25K`
- **로직**: 1000 단위 K, 1000000 단위 M
- **예외**: 0 또는 음수는 `0`

#### `calc_percent(used, limit)`
- **입력**: `25000`, `200000`
- **출력**: `12`
- **로직**: `(used / limit) * 100`, 정수 반올림
- **예외**: limit=0이면 `0` 반환

#### `get_color_code(percent)`
- **입력**: `50`
- **출력**: `\033[32m`
- **로직**: 0-50 녹색, 51-80 노란색, 81+ 빨간색
- **예외**: 음수는 녹색

#### `get_current_project()`
- **입력**: 없음 (PWD 사용)
- **출력**: `TheMoon_Project`
- **로직**: `basename $PWD`
- **예외**: 없음

### 6.6 출력 형식 상세

#### 간결형 (추천)
```
🤖 {model} | 📁 {project} | 💰 ${session}/${today} | {color}🧠 {tokens} ({percent}%){reset}
```

**예시:**
```
🤖 sonnet-4-5 | 📁 TheMoon_Project | 💰 $0.15/$0.50 | 🧠 25K (12%)
```

**필드 설명:**
- `{model}`: 간략화된 모델 이름 (최대 15자)
- `{project}`: 프로젝트 디렉토리명 (최대 20자)
- `{session}`: 세션 비용 (소수점 2자리)
- `{today}`: 오늘 누적 비용 (소수점 2자리)
- `{color}`: ANSI 색상 코드 (사용량 기반)
- `{tokens}`: 포맷된 토큰 수 (K/M 단위)
- `{percent}`: 사용률 백분율 (0-100)
- `{reset}`: `\033[0m` (색상 리셋)

### 6.7 에러 처리

| 에러 상황 | 대응 | 출력 |
|-----------|------|------|
| **jq 미설치** | 에러 메시지 출력 후 종료 | `⚠️  jq not installed` |
| **잘못된 JSON** | 에러 메시지 출력 후 종료 | `⚠️  Invalid JSON` |
| **model 필드 없음** | 기본값 사용 | `unknown` |
| **cost 필드 없음** | 기본값 0 사용 | `$0.00/$0.00` |
| **token_limit = 0** | 백분율 0% 표시 | `0%` |
| **division by zero** | bc에서 자동 처리 | `0` |

---

## 7. Next Steps (다음 단계)

### 7.1 즉시 실행 가능한 작업

1. **jq 설치 확인**
   ```bash
   which jq || sudo apt-get install -y jq
   ```

2. **백업 생성**
   ```bash
   cp statusline.sh statusline.sh.backup-$(date +%Y%m%d-%H%M%S)
   ```

3. **테스트 JSON 생성**
   ```bash
   cat > test_normal.json <<'EOF'
   {
     "model": "claude-sonnet-4-5-20250929",
     "cost": {
       "total_input_tokens": 25000,
       "token_limit": 200000,
       "total_cost_usd": 0.15,
       "today_cost_usd": 0.50
     }
   }
   EOF
   ```

### 7.2 구현 진행 순서

```
1. Phase 1 완료 → 2. Phase 2 완료 → 3. Phase 3 완료 → 4. Phase 4 완료 → 5. Phase 5 완료
   (환경 준비)      (함수 구현)       (통합)          (테스트)         (문서화)
```

### 7.3 예상 소요 시간

| Phase | 예상 시간 | 누적 시간 |
|-------|-----------|-----------|
| Phase 1 | 5분 | 5분 |
| Phase 2 | 15분 | 20분 |
| Phase 3 | 10분 | 30분 |
| Phase 4 | 10분 | 40분 |
| Phase 5 | 5분 | **45분** |

**총 예상 시간**: 약 45분

### 7.4 체크리스트

**시작 전:**
- [ ] 이 플랜 문서 읽기 완료
- [ ] WSL 환경 접속
- [ ] 프로젝트 디렉토리 이동 (`cd /mnt/d/Ai/WslProject/TheMoon_Project`)
- [ ] Git 상태 확인 (`git status`)

**Phase 1:**
- [ ] jq 설치 확인
- [ ] statusline.sh 백업
- [ ] stdin JSON 구조 분석

**Phase 2:**
- [ ] get_current_project() 구현 및 테스트
- [ ] simplify_model_name() 구현 및 테스트
- [ ] format_tokens() 구현 및 테스트
- [ ] calc_percent() 구현 및 테스트
- [ ] get_color_code() 구현 및 테스트

**Phase 3:**
- [ ] 메인 로직 작성
- [ ] 에러 핸들링 추가
- [ ] 실행 권한 설정

**Phase 4:**
- [ ] 테스트 JSON 생성
- [ ] 수동 테스트 실행
- [ ] Claude Code 실제 테스트
- [ ] 엣지 케이스 테스트

**Phase 5:**
- [ ] README 업데이트
- [ ] 백업 파일 정리
- [ ] Git 커밋

### 7.5 향후 개선 방향

**1차 릴리스 (이 플랜):**
- ✅ 기본 정보 표시 (모델, 프로젝트, 토큰, 비용)
- ✅ 색상 코딩
- ✅ 간결한 출력

**2차 개선 (추후):**
- 🔄 ccusage 통합 (더 정확한 통계)
- 🔄 주간 한도 표시 (API 조사 필요)
- 🔄 시간 기반 사용량 표시 (5시간 block)
- 🔄 설정 파일로 출력 형식 커스터마이징

**3차 개선 (장기):**
- 🔄 Python 스크립트로 재작성 (확장성)
- 🔄 웹 대시보드 연동
- 🔄 사용량 알림 기능
- 🔄 비용 최적화 제안

### 7.6 문의 및 지원

**문제 발생 시:**
1. 이 플랜 문서의 "6.7 에러 처리" 섹션 참조
2. `bash -x statusline.sh < test.json` 디버그 모드 실행
3. GitHub Issues 등록

**피드백:**
- 출력 형식 개선 제안
- 추가 정보 표시 요청
- 성능 개선 아이디어

---

## 📌 부록

### A. 현재 statusline.sh 전체 코드 (백업용)

```bash
#!/bin/bash
# Custom statusline for Claude Code
# Block을 퍼센트로 표시

# stdin에서 JSON 데이터 읽기
input=$(cat)

# 비용 정보 추출
session_cost=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
today_cost=$(echo "$input" | jq -r '.cost.today_cost_usd // 0')
block_cost=$(echo "$input" | jq -r '.cost.block_cost_usd // 0')
block_limit=$(echo "$input" | jq -r '.cost.block_limit_usd // 0')
block_time_left=$(echo "$input" | jq -r '.cost.block_time_left_ms // 0')

# 토큰 사용량
tokens_used=$(echo "$input" | jq -r '.cost.total_input_tokens // 0')
tokens_limit=$(echo "$input" | jq -r '.cost.token_limit // 200000')

# 비율 계산
if [ "$block_limit" != "0" ] && [ "$block_limit" != "null" ]; then
    block_percent=$(echo "scale=0; ($block_cost / $block_limit) * 100" | bc 2>/dev/null || echo "0")
else
    block_percent="0"
fi

if [ "$tokens_limit" != "0" ] && [ "$tokens_limit" != "null" ]; then
    token_percent=$(echo "scale=0; ($tokens_used / $tokens_limit) * 100" | bc 2>/dev/null || echo "0")
else
    token_percent="0"
fi

# 시간 포맷 변환 (ms to 시:분)
if [ "$block_time_left" != "0" ] && [ "$block_time_left" != "null" ]; then
    hours=$(echo "scale=0; $block_time_left / 3600000" | bc 2>/dev/null || echo "0")
    minutes=$(echo "scale=0; ($block_time_left % 3600000) / 60000" | bc 2>/dev/null || echo "0")
    time_left="${hours}h ${minutes}m"
else
    time_left="N/A"
fi

# 비용 per hour 계산 (간단 버전)
cost_per_hour="N/A"

# 색상 코드 (block 사용량에 따라)
if [ "$block_percent" -lt 50 ]; then
    block_color="\033[32m"  # 녹색
elif [ "$block_percent" -lt 80 ]; then
    block_color="\033[33m"  # 노란색
else
    block_color="\033[31m"  # 빨간색
fi

# 출력 (기존 형식 + 사용량 퍼센트 추가)
printf "💰 \$%.2f session / \$%.2f today / ${block_color}사용량: %d%%\033[0m (%s left) | 🧠 %s (%d%%)" \
    "$session_cost" \
    "$today_cost" \
    "$block_percent" \
    "$time_left" \
    "$(numfmt --to=si $tokens_used 2>/dev/null || echo $tokens_used)" \
    "$token_percent"
```

### B. Claude Code에 statusline 등록하는 방법

#### 방법 1: npx ccusage statusline 사용 (공식)

```bash
# Claude Code 설정에서 statusline 활성화
npx ccusage@latest statusline --help

# 프로젝트 루트에 statusline.sh 생성 후
# Claude Code가 자동으로 인식
```

#### 방법 2: Claude Code 설정 파일 수정

**WSL 환경:**
```bash
# Claude Code 설정 파일 위치
~/.config/claude/settings.json

# 또는 프로젝트별 설정
.claude/settings.json
```

**설정 예시:**
```json
{
  "statusline": {
    "enabled": true,
    "command": "./statusline.sh"
  }
}
```

#### 방법 3: 환경 변수 설정

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export CLAUDE_STATUSLINE_COMMAND="/mnt/d/Ai/WslProject/TheMoon_Project/statusline.sh"
```

**적용:**
```bash
source ~/.bashrc
```

### C. 독립 실행 가이드 (다른 컴퓨터에서)

#### 🚀 빠른 시작 (5분 완료)

```bash
# 1. 프로젝트 클론 (또는 파일 복사)
cd /path/to/project

# 2. jq 설치 확인
which jq || sudo apt-get install -y jq

# 3. 기존 statusline.sh 백업
cp statusline.sh statusline.sh.backup-$(date +%Y%m%d)

# 4. 새 statusline.sh 작성 (아래 전체 코드 복사)
nano statusline.sh

# 5. 실행 권한 설정
chmod +x statusline.sh

# 6. 테스트
cat << 'EOF' | ./statusline.sh
{
  "model": "claude-sonnet-4-5-20250929",
  "cost": {
    "total_input_tokens": 25000,
    "total_output_tokens": 5000,
    "token_limit": 200000,
    "total_cost_usd": 0.15,
    "today_cost_usd": 0.50
  }
}
EOF

# 예상 출력:
# 🤖 sonnet-4-5 | 📁 프로젝트명 | 💰 $0.15/$0.50 | 🧠 25K (12%)
```

#### 📋 전체 코드 (복사해서 사용)

**새 statusline.sh 전체 코드:**

```bash
#!/bin/bash
# Enhanced statusline for Claude Code - v2.0
# 작성일: 2025-11-16

# ========== 함수 정의 ==========

# 프로젝트 이름 추출
get_current_project() {
    basename "$PWD"
}

# 모델 이름 간략화
simplify_model_name() {
    local model="$1"
    # claude-sonnet-4-5-20250929 → sonnet-4-5
    echo "$model" | sed -E 's/claude-([a-z]+)-([0-9]+-[0-9]+).*/\1-\2/' | sed 's/^claude-//'
}

# 토큰 포맷팅 (K/M 단위)
format_tokens() {
    local tokens="$1"
    if [ "$tokens" -ge 1000000 ]; then
        local value=$(echo "scale=1; $tokens / 1000000" | bc)
        echo "${value}M" | sed 's/\.0M$/M/'
    elif [ "$tokens" -ge 1000 ]; then
        local value=$(echo "scale=0; $tokens / 1000" | bc)
        echo "${value}K"
    else
        echo "$tokens"
    fi
}

# 백분율 계산
calc_percent() {
    local used="$1"
    local limit="$2"
    if [ "$limit" = "0" ] || [ -z "$limit" ]; then
        echo "0"
    else
        echo "scale=0; ($used * 100) / $limit" | bc 2>/dev/null || echo "0"
    fi
}

# 색상 코드 반환
get_color_code() {
    local percent="$1"
    if [ "$percent" -lt 50 ]; then
        echo "\033[32m"  # 녹색
    elif [ "$percent" -lt 80 ]; then
        echo "\033[33m"  # 노란색
    else
        echo "\033[31m"  # 빨간색
    fi
}

# ========== 메인 로직 ==========

# jq 설치 확인
if ! command -v jq &> /dev/null; then
    echo "⚠️  jq not installed. Run: sudo apt-get install jq"
    exit 1
fi

# stdin JSON 읽기
input=$(cat)

# JSON 유효성 검사
if ! echo "$input" | jq empty 2>/dev/null; then
    echo "⚠️  Invalid JSON input"
    exit 1
fi

# JSON 파싱
model=$(echo "$input" | jq -r '.model // "unknown"')
total_tokens=$(echo "$input" | jq -r '.cost.total_input_tokens // 0')
token_limit=$(echo "$input" | jq -r '.cost.token_limit // 200000')
session_cost=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
today_cost=$(echo "$input" | jq -r '.cost.today_cost_usd // 0')

# 데이터 가공
project_name=$(get_current_project)
model_short=$(simplify_model_name "$model")
tokens_fmt=$(format_tokens "$total_tokens")
token_percent=$(calc_percent "$total_tokens" "$token_limit")
color=$(get_color_code "$token_percent")

# 출력
printf "🤖 %s | 📁 %s | 💰 \$%.2f/\$%.2f | ${color}🧠 %s (%d%%)\033[0m" \
    "$model_short" \
    "$project_name" \
    "$session_cost" \
    "$today_cost" \
    "$tokens_fmt" \
    "$token_percent"
```

### D. 참고 자료

- [jq 공식 문서](https://stedolan.github.io/jq/manual/)
- [Bash 스크립트 가이드](https://www.gnu.org/software/bash/manual/)
- [ANSI 색상 코드](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [ccusage GitHub](https://github.com/ryoppippi/ccusage)
- [Claude Code 문서](https://docs.claude.com/claude-code)

### E. 용어 정리

| 용어 | 설명 |
|------|------|
| **statusline** | Claude Code의 하단 상태 표시줄 |
| **stdin** | 표준 입력 (Standard Input) |
| **jq** | JSON 파싱 커맨드라인 도구 |
| **bc** | Bash Calculator (수치 계산) |
| **ANSI 코드** | 터미널 색상/스타일 제어 코드 |
| **PWD** | Present Working Directory (현재 디렉토리) |

### F. FAQ

**Q1: jq를 꼭 설치해야 하나요?**
- A: 네, JSON 파싱에 필수입니다. 다만 Python으로 대체 가능합니다 (방법 3).

**Q2: 기존 statusline.sh는 어떻게 되나요?**
- A: 백업 후 덮어씁니다. 언제든지 복구 가능합니다.

**Q3: 출력 형식을 바꿀 수 있나요?**
- A: 네, Task 3.1의 printf 부분을 수정하면 됩니다.

**Q4: 성능이 느리면 어떻게 하나요?**
- A: jq 대신 Python으로 재작성하거나, 캐싱을 추가하세요.

**Q5: ccusage는 언제 쓰나요?**
- A: 2차 개선 단계에서 고려 예정입니다.

---

## 📝 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.1.0 | 2025-11-16 | 독립 실행 가이드 추가 (부록 A~F) |
| 1.0.0 | 2025-11-16 | 초안 작성 |

---

**문서 끝**
