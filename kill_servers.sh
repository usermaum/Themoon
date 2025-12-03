#!/bin/bash
# TheMoon - 개별 서버 종료 스크립트
# Backend와 Frontend를 선택적으로 종료

echo "========================================="
echo "🛑 TheMoon - 서버 종료 도구"
echo "========================================="
echo ""

# 프로젝트 루트 디렉토리
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 현재 실행 중인 서버 확인
check_servers() {
    BACKEND_RUNNING=false
    FRONTEND_RUNNING=false

    if lsof -ti :8000 > /dev/null 2>&1; then
        BACKEND_RUNNING=true
        BACKEND_PID=$(lsof -ti :8000)
    fi

    if lsof -ti :3000 > /dev/null 2>&1; then
        FRONTEND_RUNNING=true
        FRONTEND_PID=$(lsof -ti :3000)
    fi
}

# 서버 상태 출력
check_servers

echo "📊 현재 서버 상태:"
echo ""

if [ "$BACKEND_RUNNING" = true ]; then
    echo "✅ Backend  (포트 8000) - PID: $BACKEND_PID"
else
    echo "❌ Backend  (포트 8000) - 실행 중 아님"
fi

if [ "$FRONTEND_RUNNING" = true ]; then
    echo "✅ Frontend (포트 3000) - PID: $FRONTEND_PID"
else
    echo "❌ Frontend (포트 3000) - 실행 중 아님"
fi

echo ""

# 실행 중인 서버가 없으면 종료
if [ "$BACKEND_RUNNING" = false ] && [ "$FRONTEND_RUNNING" = false ]; then
    echo "ℹ️  실행 중인 서버가 없습니다."
    exit 0
fi

echo "========================================="
echo "종료할 서버를 선택하세요:"
echo "========================================="
echo ""

# 옵션 구성
OPTIONS=()
OPTION_NUM=1

if [ "$BACKEND_RUNNING" = true ]; then
    echo "$OPTION_NUM) Backend만 종료 (포트 8000)"
    OPTIONS[$OPTION_NUM]="backend"
    OPTION_NUM=$((OPTION_NUM + 1))
fi

if [ "$FRONTEND_RUNNING" = true ]; then
    echo "$OPTION_NUM) Frontend만 종료 (포트 3000)"
    OPTIONS[$OPTION_NUM]="frontend"
    OPTION_NUM=$((OPTION_NUM + 1))
fi

if [ "$BACKEND_RUNNING" = true ] && [ "$FRONTEND_RUNNING" = true ]; then
    echo "$OPTION_NUM) 모든 서버 종료"
    OPTIONS[$OPTION_NUM]="all"
    OPTION_NUM=$((OPTION_NUM + 1))
fi

echo "$OPTION_NUM) 취소"
OPTIONS[$OPTION_NUM]="cancel"

echo ""
read -p "선택 (1-$OPTION_NUM): " choice

# 선택 확인
if [ -z "$choice" ] || [ "$choice" -lt 1 ] || [ "$choice" -gt $OPTION_NUM ]; then
    echo ""
    echo "❌ 잘못된 선택입니다."
    exit 1
fi

SELECTED=${OPTIONS[$choice]}

case $SELECTED in
    backend)
        echo ""
        echo "🔄 Backend 종료 중... (PID: $BACKEND_PID)"
        lsof -ti :8000 | xargs kill -9 2>/dev/null
        echo "✅ Backend가 종료되었습니다."
        ;;
    frontend)
        echo ""
        echo "🔄 Frontend 종료 중... (PID: $FRONTEND_PID)"
        lsof -ti :3000 | xargs kill -9 2>/dev/null
        echo "✅ Frontend가 종료되었습니다."
        ;;
    all)
        echo ""
        echo "🔄 모든 서버 종료 중..."
        if [ "$BACKEND_RUNNING" = true ]; then
            echo "  - Backend (PID: $BACKEND_PID)"
            lsof -ti :8000 | xargs kill -9 2>/dev/null
        fi
        if [ "$FRONTEND_RUNNING" = true ]; then
            echo "  - Frontend (PID: $FRONTEND_PID)"
            lsof -ti :3000 | xargs kill -9 2>/dev/null
        fi
        echo "✅ 모든 서버가 종료되었습니다."
        ;;
    cancel)
        echo ""
        echo "❌ 취소되었습니다."
        exit 0
        ;;
    *)
        echo ""
        echo "❌ 잘못된 선택입니다."
        exit 1
        ;;
esac

echo ""
