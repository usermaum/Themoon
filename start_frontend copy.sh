#!/bin/bash
# TheMoon - Automated Dev Server Script

# 프로젝트 루트 디렉토리
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Default values
CLEAN_CACHE=false
AUTO_MODE=false

# Argument Parsing
for i in "$@"
do
case $i in
    --clean)
    CLEAN_CACHE=true
    shift
    ;;
    --auto)
    AUTO_MODE=true
    shift
    ;;
    *)
    # unknown option
    ;;
esac
done

# 1. 정리 (Cleanup)
echo "🧹 Force Cleanup Started..."

# Kill OTHER frontend_dev.sh / start_frontend.sh instances
CURRENT_PID=$$
echo "🧹 Cleaning up other frontend process instances..."
pgrep -f "frontend_dev.sh" | grep -v "$CURRENT_PID" | xargs kill -9 2>/dev/null || true
pgrep -f "start_frontend.sh" | grep -v "$CURRENT_PID" | xargs kill -9 2>/dev/null || true
pkill -f "node" || true
pkill -f "next-server" || true

# Kill by port (3500)
ports=(3500)
for port in "${ports[@]}"; do
    if lsof -ti :$port > /dev/null; then
        echo "⚠️  Port $port is in use. Killing procs..."
        pids=$(lsof -ti :$port)
        kill -9 $pids 2>/dev/null || true
        for i in {1..5}; do
            if ! lsof -ti :$port > /dev/null; then
                echo "✅ Port $port is now free."
                break
            fi
            sleep 1
        done
    else
        echo "✅ Port $port is already free."
    fi
done

echo "✅ Cleanup Complete."

# Frontend 캐시 삭제 (조건부)
if [ "$CLEAN_CACHE" = true ]; then
    echo "🗑️  Frontend 캐시 삭제 중..."
    rm -rf "$ROOT_DIR/frontend/.next"
    echo "✅ 캐시 삭제 완료"
fi

echo ""
echo "========================================="
echo "🚀 서버 시작 중..."
echo "========================================="

# 2. 종료 시그널 처리 (Trap)
cleanup() {
    echo ""
    echo "🛑 서버 종료 중..."
    if [ ! -z "$FRONTEND_PID" ]; then kill $FRONTEND_PID 2>/dev/null; fi
    exit 0
}
trap cleanup SIGINT SIGTERM

# 4. Frontend 시작
cd "$ROOT_DIR/frontend"
> ../logs/themoon_frontend.log
npm run dev -- -H 0.0.0.0 -p 3500 > ../logs/themoon_frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend 시작됨 (PID: $FRONTEND_PID)"

cd ..

# 5. 로그 실시간 출력 (Blocking - Interactive Only)
if [ "$AUTO_MODE" = false ]; then
    WSL_IP=$(hostname -I | awk '{print $1}')
    echo ""
    echo "🌍 Frontend (Local):   http://localhost:3500"
    echo "🌍 Frontend (Internal): http://$WSL_IP:3500"
    echo ""
    echo "📊 실시간 로그 출력 중... (종료하려면 Ctrl+C)"
    echo "========================================="
    tail -f ../logs/themoon_frontend.log
fi
