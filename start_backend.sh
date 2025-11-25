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
    echo "⚠️  Warning: venv가 없습니다. 생성합니다..."
    python3 -m venv ../venv
    echo "✅ venv 생성 완료"
fi

# 3. 가상환경 활성화
echo "📦 가상환경 활성화 중..."
source ../venv/bin/activate

# 4. 의존성 설치 확인
echo "📦 의존성 확인 중..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# 5. 포트 충돌 확인 및 해결
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

# 6. 서버 시작
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
