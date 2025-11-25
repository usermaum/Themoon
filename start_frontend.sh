#!/bin/bash
# Frontend Server Start Script
# TheMoon - Coffee Roasting Cost Calculator

echo "========================================="
echo "🎨 TheMoon Frontend Server"
echo "========================================="
echo ""

# 옵션 표시
echo "다음 중 하나를 선택하세요:"
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

# 1. Frontend 디렉토리로 이동
cd "$(dirname "$0")/frontend" || {
    echo "❌ Error: frontend 디렉토리를 찾을 수 없습니다."
    exit 1
}

# 2. 캐시 삭제 (옵션 2 선택 시)
if [ "$CLEAN_CACHE" = true ]; then
    if [ -d ".next" ]; then
        echo "🗑️  .next 캐시 삭제 중..."
        rm -rf .next
        echo "✅ 캐시 삭제 완료"
        echo ""
    else
        echo "ℹ️  .next 캐시가 없습니다."
        echo ""
    fi
fi

# 3. node_modules 확인
if [ ! -d "node_modules" ]; then
    echo "📦 의존성 설치 중..."
    npm install
    echo "✅ 설치 완료"
    echo ""
else
    # package.json이 변경되었는지 빠르게 확인
    if [ ! -f "node_modules/.package-lock.json" ] || [ "package.json" -nt "node_modules/.package-lock.json" ]; then
        echo "📦 의존성 업데이트 확인 중..."
        npm install
        echo ""
    fi
fi

# 4. 포트 충돌 확인 및 해결
if lsof -ti :3000 > /dev/null 2>&1; then
    echo "⚠️  Warning: 포트 3000이 이미 사용 중입니다."
    read -p "기존 프로세스를 종료하시겠습니까? (y/n): " answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        echo "🔄 기존 프로세스 종료 중..."
        lsof -ti :3000 | xargs kill -9
        echo "✅ 기존 프로세스 종료 완료"
        echo ""
    else
        echo "❌ 서버 시작을 취소합니다."
        exit 1
    fi
fi

# 5. 서버 시작
echo "========================================="
echo "✅ Frontend 서버 시작"
echo "========================================="
echo ""
echo "📍 URL: http://localhost:3000"
echo ""
echo "🛑 종료하려면 Ctrl+C를 누르세요."
echo ""

npm run dev
