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
