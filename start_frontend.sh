#!/bin/bash
# TheMoon - Frontend Server Start Script

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLEAN_CACHE=false
AUTO_MODE=false

# Argument Parsing
for i in "$@"; do
    case $i in
        --clean) CLEAN_CACHE=true ;;
        --auto) AUTO_MODE=true ;;
    esac
done

echo "🧹 Cleaning up previous processes..."

# Kill existing frontend processes & scripts
CURRENT_PID=$$
pgrep -f "frontend_dev.sh|start_frontend.sh" | grep -v "$CURRENT_PID" | xargs kill -9 2>/dev/null || true
pkill -f "node|next-server" || true

# Free port 3500
if lsof -ti :3500 > /dev/null; then
    lsof -ti :3500 | xargs kill -9 2>/dev/null || true
    for i in {1..5}; do
        ! lsof -ti :3500 > /dev/null && break
        sleep 1
    done
fi

# Apply clean cache if requested
if [ "$CLEAN_CACHE" = true ]; then
    echo "🗑️  Cleaning build cache (.next)..."
    rm -rf "$ROOT_DIR/frontend/.next"
fi

# Handle script termination
cleanup() {
    echo -e "\n🛑 Stopping server..."
    [ ! -z "$FRONTEND_PID" ] && kill $FRONTEND_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

echo "🚀 Starting Frontend server..."

cd "$ROOT_DIR/frontend"
> ../logs/themoon_frontend.log
npm run dev -- -H 0.0.0.0 -p 3500 > ../logs/themoon_frontend.log 2>&1 &
FRONTEND_PID=$!

if [ "$AUTO_MODE" = false ]; then
    WSL_IP=$(hostname -I | awk '{print $1}')
    echo -e "\n🌍 URL: http://localhost:3500 (Network: http://$WSL_IP:3500)"
    echo -e "📊 Monitoring logs... (Ctrl+C to stop)\n"
    tail -f ../logs/themoon_frontend.log
else
    echo "✅ Frontend started in background (PID: $FRONTEND_PID)"
fi
