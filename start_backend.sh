#!/bin/bash
# Backend Server Start Script
# TheMoon - Coffee Roasting Cost Calculator

echo "========================================="
echo "🚀 TheMoon Backend Server"
echo "========================================="
echo ""

# Default values
FORCE_KILL=false
AUTO_MODE=false

# Argument Parsing
for i in "$@"
do
case $i in
    --force)
    FORCE_KILL=true
    shift
    ;;
    --auto)
    AUTO_MODE=true
    shift
    ;;
    *)
    ;;
esac
done

if [ "$AUTO_MODE" = true ]; then
    # 로그 디렉토리 확인
    mkdir -p ../logs
    echo "" >> ../logs/themoon_backend.log
    echo "🔄 [System] Backend Server Restarting..." >> ../logs/themoon_backend.log
    echo "" >> ../logs/themoon_backend.log

    # 0. 초기화 및 기존 프로세스 정리 (Early Aggressive Cleanup)
    echo "🧹 [System] Cleaning up previous processes..." >> ../logs/themoon_backend.log
    
    # 1. Kill backend processes (Name-based)
    pkill -f "uvicorn" 2>/dev/null || true
    pkill -f "python backend/app/main.py" 2>/dev/null || true
    
    # 2. Kill port 8000
    lsof -ti :8000 | xargs kill -9 2>/dev/null || true
    
    # Wait for release
    sleep 2
fi

# 1. Backend 디렉토리로 이동
cd "$(dirname "$0")/backend" || {
    echo "❌ Error: backend 디렉토리를 찾을 수 없습니다."
    exit 1
}

# 2. Python 가상환경 확인 및 활성화
if [ ! -d "../venv" ]; then
    echo "⚠️  venv가 없습니다. 생성 중..."
    python3 -m venv ../venv
    source ../venv/bin/activate
    echo "📦 의존성 설치 중..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo "✅ 초기 설정 완료"
    echo ""
else
    source ../venv/bin/activate
    # 의존성이 이미 설치되어 있는지 빠르게 확인 (0.1초 미만)
    if ! python -c "import fastapi, uvicorn" 2>/dev/null; then
        echo "📦 의존성 설치 중..."
        pip install -q --upgrade pip
        pip install -q -r requirements.txt
        echo "✅ 설치 완료"
        echo ""
    fi
fi

# 3. 포트 및 프로세스 확인 (Interactive Only with Robust Check)
if [ "$AUTO_MODE" = false ]; then
    IS_RUNNING=false
    
    # 1. Port Check
    if lsof -ti :8000 > /dev/null; then
        IS_RUNNING=true
        echo "⚠️  Port 8000 is in use."
    fi
    
    # 2. Name Check (Uvicorn / Python)
    if pgrep -f "uvicorn" > /dev/null; then
        IS_RUNNING=true
        echo "⚠️  'uvicorn' process is running."
    fi

    if [ "$IS_RUNNING" = true ]; then
        echo ""
        read -p "기존 서버가 감지되었습니다. 종료하고 시작하시겠습니까? (y/n): " answer
        if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
            echo "🧹 Cleaning up..."
            pkill -f "uvicorn" 2>/dev/null || true
            pkill -f "python backend/app/main.py" 2>/dev/null || true
            lsof -ti :8000 | xargs kill -9 2>/dev/null || true
            sleep 2
            echo "✅ Cleanup complete."
        else
            echo "❌ Cancelled."
            exit 1
        fi
    fi
fi

# 4. 서버 시작
echo ""
echo "========================================="
echo "✅ Backend 서버 시작"
echo "========================================="
echo ""
echo "📍 URL: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 종료하려면 Ctrl+C를 누르세요."
echo ""

# 로그 디렉토리 확인
mkdir -p ../logs

echo "📝 Output redirected to logs/themoon_backend.log"
nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../logs/themoon_backend.log 2>&1 &
echo "✅ Backend server started in background."

if [ "$AUTO_MODE" = false ]; then
    echo ""
    echo "📊 실시간 로그를 출력합니다. (모니터링 종료: Ctrl+C)"
    echo "   (서버는 백그라운드에서 계속 실행됩니다)"
    echo "========================================="
    tail -f ../logs/themoon_backend.log
fi
