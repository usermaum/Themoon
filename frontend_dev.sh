#!/bin/bash
# TheMoon - Automated Dev Server Script
# start_all.sh 기반 (메뉴 선택 없이 즉시 실행)

# 프로젝트 루트 디렉토리
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. 정리 (Cleanup)
echo "🧹 Force Cleanup Started..."

# Kill OTHER frontend_dev.sh instances
CURRENT_PID=$$
echo "🧹 Cleaning up other frontend_dev.sh instances..."
pgrep -f "frontend_dev.sh" | grep -v "$CURRENT_PID" | xargs kill -9 2>/dev/null || true
pkill -f "start_frontend.sh" || true
pkill -f "node" || true
pkill -f "next-server" || true

# Kill by port (3500)
ports=(3500)
for port in "${ports[@]}"; do
    # 1. Check if port is in use
    if lsof -ti :$port > /dev/null; then
        echo "⚠️  Port $port is in use. Killing procs..."
        pids=$(lsof -ti :$port)
        kill -9 $pids 2>/dev/null || true
        
        # 2. Wait for port to be free (Max 5 seconds)
        for i in {1..5}; do
            if ! lsof -ti :$port > /dev/null; then
                echo "✅ Port $port is now free."
                break
            fi
            echo "   Waiting for port $port to release... ($i/5)"
            sleep 1
        done
        
        # 3. Final Check
        if lsof -ti :$port > /dev/null; then
            echo "❌ Error: Port $port i핟s still in use after force kill."
            echo "   Common reason: Permission denied or zombie process."
            echo "   Please run 'lsof -ti :$port | xargs kill -9' manually."
            exit 1
        fi
    else
        echo "✅ Port $port is already free."
    fi
done

echo "✅ Cleanup Complete."

# Frontend 캐시 삭제
echo "🗑️  Frontend 캐시 삭제 중..."
rm -rf "$ROOT_DIR/frontend/.next"

echo ""
echo "========================================="
echo "🚀 서버 시작 중..."
echo "========================================="

# 2. 종료 시그널 처리 (Trap)
# 스크립트가 종료(Ctrl+C)될 때 자식 프로세스도 같이 종료
cleanup() {
    echo ""
    echo "🛑 서버 종료 중..."
    if [ ! -z "$FRONTEND_PID" ]; then kill $FRONTEND_PID 2>/dev/null; fi
    exit 0
}
trap cleanup SIGINT SIGTERM

# 4. Frontend 시작
cd "$ROOT_DIR/frontend"
# 로그 파일 비우기 및 시작
> ../logs/themoon_frontend.log
# 0.0.0.0으로 호스트 바인딩하여 외부 접속 허용하며 포트 3500 지정
npm run dev -- -H 0.0.0.0 -p 3500 > ../logs/themoon_frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend 시작됨 (PID: $FRONTEND_PID)"

cd ..

# WSL IP 추출 (첫 번째 IP)
WSL_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "🌍 Frontend (Local):   http://localhost:3500"
echo "🌍 Frontend (Internal): http://$WSL_IP:3500"
echo ""
echo "📊 실시간 로그 출력 중... (종료하려면 Ctrl+C)"
echo "========================================="

# 5. 로그 실시간 출력 (Blocking)
# 스크립트가 계속 실행 상태로 유지됨
tail -f ../logs/themoon_frontend.log
