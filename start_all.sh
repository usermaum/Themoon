#!/bin/bash
# TheMoon - All Servers Start Script
# Backend + Frontend 동시 실행

echo "========================================="
echo "🚀 TheMoon - All Servers"
echo "========================================="
echo ""

# 프로젝트 루트 디렉토리
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 옵션 선택
echo "Frontend 시작 옵션을 선택하세요:"
echo ""
echo "1) 일반 시작 (캐시 유지)"
echo "2) 캐시 삭제 후 시작 (rm -rf .next)"
echo "3) 취소"
echo ""
read -p "선택 (1-3): " choice

case $choice in
    1)
        CLEAN_CACHE=false
        echo ""
        echo "✅ 일반 시작 모드"
        ;;
    2)
        CLEAN_CACHE=true
        echo ""
        echo "✅ 캐시 삭제 모드"
        ;;
    3)
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
echo "========================================="
echo "🔧 서버 준비 중..."
echo "========================================="
echo ""

# ==========================================
# 1. Backend 준비
# ==========================================
cd "$ROOT_DIR/backend" || {
    echo "❌ Error: backend 디렉토리를 찾을 수 없습니다."
    exit 1
}

# 가상환경 확인 및 활성화
if [ ! -d "$ROOT_DIR/venv" ]; then
    echo "⚠️  [Backend] venv 생성 중..."
    python3 -m venv "$ROOT_DIR/venv"
    source "$ROOT_DIR/venv/bin/activate"
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
else
    source "$ROOT_DIR/venv/bin/activate"
    # 의존성이 이미 설치되어 있는지 빠르게 확인 (0.1초 미만)
    if ! python -c "import fastapi, uvicorn" 2>/dev/null; then
        echo "📦 [Backend] 의존성 설치 중..."
        pip install -q --upgrade pip
        pip install -q -r requirements.txt
    fi
fi

# 포트 충돌 확인
if lsof -ti :8000 > /dev/null 2>&1; then
    echo "🔄 [Backend] 포트 8000 기존 프로세스 종료 중..."
    lsof -ti :8000 | xargs kill -9
fi

echo ""

# ==========================================
# 2. Frontend 준비
# ==========================================
cd "$ROOT_DIR/frontend" || {
    echo "❌ Error: frontend 디렉토리를 찾을 수 없습니다."
    exit 1
}

# 캐시 삭제
if [ "$CLEAN_CACHE" = true ]; then
    if [ -d ".next" ]; then
        echo "🗑️  [Frontend] .next 캐시 삭제 중..."
        rm -rf .next
        echo "✅ [Frontend] 캐시 삭제 완료"
    fi
fi

# node_modules 확인
if [ ! -d "node_modules" ]; then
    echo "📦 [Frontend] 의존성 설치 중..."
    npm install
elif [ "package.json" -nt "node_modules/.modules.yaml" ] 2>/dev/null; then
    # package.json이 변경된 경우에만
    echo "📦 [Frontend] 의존성 업데이트 중..."
    npm install
fi

# 포트 충돌 확인
if lsof -ti :3500 > /dev/null 2>&1; then
    echo "🔄 [Frontend] 포트 3500 기존 프로세스 종료 중..."
    lsof -ti :3500 | xargs kill -9
fi

echo ""

# ==========================================
# 3. 서버 시작
# ==========================================
echo "========================================="
echo "✅ 서버 시작"
echo "========================================="
echo ""
# WSL IP 추출
WSL_IP=$(hostname -I | awk '{print $1}')

echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo "📍 Frontend: http://localhost:3500 (Local)"
echo "📍 Frontend: http://$WSL_IP:3500 (Internal)"
echo ""
echo "🛑 종료하려면 Ctrl+C를 누르세요."
echo "   (모든 서버가 동시에 종료됩니다)"
echo ""
echo "========================================="
echo ""

# 종료 시그널 처리
cleanup() {
    echo ""
    echo ""
    echo "========================================="
    echo "🛑 서버 종료 중..."
    echo "========================================="

    # Backend 프로세스 종료
    if [ ! -z "$BACKEND_PID" ]; then
        echo "🔄 Backend 종료 중... (PID: $BACKEND_PID)"
        kill $BACKEND_PID 2>/dev/null
    fi

    # Frontend 프로세스 종료
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "🔄 Frontend 종료 중... (PID: $FRONTEND_PID)"
        kill $FRONTEND_PID 2>/dev/null
    fi

    echo "✅ 모든 서버가 종료되었습니다."
    exit 0
}

trap cleanup SIGINT SIGTERM

# Backend 시작 (백그라운드)
cd "$ROOT_DIR/backend"
source "$ROOT_DIR/venv/bin/activate"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > /tmp/themoon_backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend 시작됨 (PID: $BACKEND_PID)"

# 잠시 대기 (Backend가 시작될 시간)
sleep 2

# Frontend 시작 (백그라운드)
cd "$ROOT_DIR/frontend"
npm run dev -- -H 0.0.0.0 -p 3500 > /tmp/themoon_frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend 시작됨 (PID: $FRONTEND_PID)"

echo ""
echo "========================================="
echo "📊 로그 보기:"
echo "========================================="
echo "Backend:  tail -f /tmp/themoon_backend.log"
echo "Frontend: tail -f /tmp/themoon_frontend.log"
echo ""

# 로그 실시간 출력 (두 서버 모두)
tail -f /tmp/themoon_backend.log /tmp/themoon_frontend.log
