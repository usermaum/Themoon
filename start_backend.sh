#!/bin/bash
# Backend Server Start Script
# TheMoon - Coffee Roasting Cost Calculator

echo "========================================="
echo "🚀 TheMoon Backend Server"
echo "========================================="
echo ""

# 1. Backend 디렉토리로 이동
cd "$(dirname "$0")/backend" || {
    echo "❌ Error: backend 디렉토리를 찾을 수 없습니다."
    exit 1
}

# 2. Python 가상환경 확인
if [ ! -d "../venv" ]; then
    echo "⚠️  venv가 없습니다. 생성 중..."
    python3 -m venv ../venv
    source ../venv/bin/activate
    echo "📦 의존성 설치 중..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    echo "✅ 초기 설정 완료"
else
    source ../venv/bin/activate
    # 의존성이 이미 설치되어 있는지 빠르게 확인
    if ! python -c "import fastapi" 2>/dev/null; then
        echo "📦 의존성 설치 중..."
        pip install -q -r requirements.txt
    fi
fi

# 3. 포트 충돌 확인 및 해결
if lsof -ti :8000 > /dev/null 2>&1; then
    echo "⚠️  Warning: 포트 8000이 이미 사용 중입니다."
    read -p "기존 프로세스를 종료하시겠습니까? (y/n): " answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        echo "🔄 기존 프로세스 종료 중..."
        lsof -ti :8000 | xargs kill -9
        echo "✅ 기존 프로세스 종료 완료"
    else
        echo "❌ 서버 시작을 취소합니다."
        exit 1
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

uvicorn app.main:app --reload --port 8000
