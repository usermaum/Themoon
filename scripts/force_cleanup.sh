#!/bin/bash
# force_cleanup.sh

echo "🧹 Force Cleanup Started..."

# Kill specific patterns
pkill -f "dev.sh" || echo "No dev.sh found"
pkill -f "node" || echo "No node found"
pkill -f "uvicorn" || echo "No uvicorn found"
pkill -f "python" || echo "No python found"
pkill -f "next-server" || echo "No next-server found"

# Kill by port
ports=(3500 8000)
for port in "${ports[@]}"; do
    echo "Checking port $port..."
    pids=$(lsof -ti :$port)
    if [ ! -z "$pids" ]; then
        echo "Killing PIDs on port $port: $pids"
        kill -9 $pids
    else
        echo "Port $port is free."
    fi
done

# Wait a moment
sleep 2

# Verify
echo "🔍 Verification:"
lsof -i :3000,3500,8000
if [ $? -ne 0 ]; then
    echo "✅ All ports are clear."
else
    echo "❌ Some ports are still in use!"
    lsof -i :3500,8000
    exit 1
fi
