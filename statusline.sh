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
    # claude-opus-4-20250514 → opus-4
    if [[ "$model" =~ claude-([a-z]+)-([0-9]+)-([0-9]+)-.* ]]; then
        echo "${BASH_REMATCH[1]}-${BASH_REMATCH[2]}-${BASH_REMATCH[3]}"
    elif [[ "$model" =~ claude-([a-z]+)-([0-9]+)-.* ]]; then
        echo "${BASH_REMATCH[1]}-${BASH_REMATCH[2]}"
    else
        echo "$model" | sed 's/^claude-//'
    fi
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
