#!/bin/bash
# TheMoon - 프론트엔드 캐시 삭제 스크립트
# Frontend가 실행 중일 때도 .next 캐시만 안전하게 삭제

echo "========================================="
echo "🗑️  TheMoon - Frontend 캐시 삭제 도구"
echo "========================================="
echo ""

# 프로젝트 루트 디렉토리
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

# Frontend 디렉토리 확인
if [ ! -d "$FRONTEND_DIR" ]; then
    echo "❌ Error: frontend 디렉토리를 찾을 수 없습니다."
    exit 1
fi

# .next 디렉토리 확인
if [ ! -d "$FRONTEND_DIR/.next" ]; then
    echo "ℹ️  삭제할 캐시가 없습니다."
    echo "   (.next 디렉토리가 존재하지 않음)"
    exit 0
fi

# 캐시 크기 확인
CACHE_SIZE=$(du -sh "$FRONTEND_DIR/.next" 2>/dev/null | cut -f1)

echo "📊 현재 캐시 상태:"
echo ""
echo "   위치: $FRONTEND_DIR/.next"
echo "   크기: $CACHE_SIZE"
echo ""

# Frontend 실행 상태 확인
FRONTEND_RUNNING=false
if lsof -ti :3000 > /dev/null 2>&1; then
    FRONTEND_RUNNING=true
    FRONTEND_PID=$(lsof -ti :3000)
    echo "⚠️  주의: Frontend가 실행 중입니다 (PID: $FRONTEND_PID)"
    echo "   캐시 삭제 후 자동으로 재빌드됩니다."
else
    echo "ℹ️  Frontend가 실행 중이지 않습니다."
fi

echo ""
echo "========================================="
echo "작업을 선택하세요:"
echo "========================================="
echo ""
echo "1) .next 캐시 삭제 ($CACHE_SIZE)"
echo "2) .next 캐시 삭제 + Frontend 재시작 (실행 중일 때만)"
echo "3) 취소"
echo ""
read -p "선택 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🗑️  .next 캐시 삭제 중..."
        rm -rf "$FRONTEND_DIR/.next"

        if [ $? -eq 0 ]; then
            echo "✅ 캐시가 삭제되었습니다."

            if [ "$FRONTEND_RUNNING" = true ]; then
                echo ""
                echo "ℹ️  Frontend가 실행 중입니다."
                echo "   Next.js가 자동으로 재빌드할 것입니다."
                echo "   (첫 페이지 로딩 시 시간이 걸릴 수 있음)"
            fi
        else
            echo "❌ 캐시 삭제 중 오류가 발생했습니다."
            exit 1
        fi
        ;;

    2)
        if [ "$FRONTEND_RUNNING" = false ]; then
            echo ""
            echo "ℹ️  Frontend가 실행 중이지 않습니다."
            echo "   캐시만 삭제합니다..."
            rm -rf "$FRONTEND_DIR/.next"
            echo "✅ 캐시가 삭제되었습니다."
        else
            echo ""
            echo "🔄 작업 진행 중..."
            echo ""

            # 1. Frontend 종료
            echo "  1/3 Frontend 종료 중... (PID: $FRONTEND_PID)"
            lsof -ti :3000 | xargs kill -9 2>/dev/null
            sleep 1

            # 2. 캐시 삭제
            echo "  2/3 캐시 삭제 중..."
            rm -rf "$FRONTEND_DIR/.next"

            # 3. Frontend 재시작
            echo "  3/3 Frontend 재시작 중..."
            cd "$FRONTEND_DIR"
            npm run dev > /tmp/themoon_frontend.log 2>&1 &
            NEW_PID=$!

            echo ""
            echo "✅ 작업 완료!"
            echo ""
            echo "📍 Frontend: http://localhost:3000"
            echo ""
            echo "   새 PID: $NEW_PID"
            echo "   로그: tail -f /tmp/themoon_frontend.log"
        fi
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
