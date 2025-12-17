#!/bin/bash
# TheMoon - Automated Dev Server Script
# start_all.sh 기반 (메뉴 선택 없이 즉시 실행)

# 프로젝트 루트 디렉토리
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. 정리 (Cleanup)
# 기존 실행 중인 프로세스 정리
if lsof -ti :3500,8000 > /dev/null 2>&1; then
    echo "🔄 기존 서버 프로세스 종료 중..."
    lsof -ti :3500,8000 | xargs kill -9 2>/dev/null
fi

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
    if [ ! -z "$BACKEND_PID" ]; then kill $BACKEND_PID 2>/dev/null; fi
    if [ ! -z "$FRONTEND_PID" ]; then kill $FRONTEND_PID 2>/dev/null; fi
    exit 0
}
trap cleanup SIGINT SIGTERM

# 3. Backend 시작
cd "$ROOT_DIR/backend"
if [ -d "../venv" ]; then

    source "../venv/bin/activate"
elif [ -d "venv" ]; then
    source "venv/bin/activate"
fi

# 로그 파일 비우기 및 시작
> ../logs/themoon_backend.log
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../logs/themoon_backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend 시작됨 (PID: $BACKEND_PID)"

cd ..

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
echo "🌍 API Docs:           http://localhost:8000/docs"
echo ""
echo "📊 실시간 로그 출력 중... (종료하려면 Ctrl+C)"
echo "========================================="

# 5. 로그 실시간 출력 (Blocking)
# 스크립트가 계속 실행 상태로 유지됨
tail -f logs/themoon_backend.log logs/themoon_frontend.log
