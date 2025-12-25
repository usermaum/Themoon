#!/bin/bash

# Configuration
LOG_FILE="logs/quality_report.txt"
mkdir -p logs

# Header
echo "🔍 Code Quality Guard Started: $(date)" | tee "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"

# 1. Backend Checks
echo "" | tee -a "$LOG_FILE"
echo "🐍 [Backend] Starting Static Analysis..." | tee -a "$LOG_FILE"

# Activate Virtual Environment
source venv/bin/activate

echo "   1.1 Running Black (Formatter)..." | tee -a "$LOG_FILE"
black backend/app --check | tee -a "$LOG_FILE"
if [ $? -eq 0 ]; then echo "      ✅ Black Passed"; else echo "      ⚠️ Black Found Issues (Run 'black backend/app' to fix)"; fi

echo "   1.2 Running Mypy (Type Checker)..." | tee -a "$LOG_FILE"
mypy backend/app | tee -a "$LOG_FILE"

echo "   1.3 Running Pylint (Code Quality)..." | tee -a "$LOG_FILE"
pylint backend/app | tee -a "$LOG_FILE"

# 2. Frontend Checks
echo "" | tee -a "$LOG_FILE"
echo "⚛️ [Frontend] Starting Static Analysis..." | tee -a "$LOG_FILE"
cd frontend
npm run lint | tee -a "../$LOG_FILE"
cd ..

# Footer
echo "" | tee -a "$LOG_FILE"
echo "==================================================" | tee -a "$LOG_FILE"
echo "✅ Check Complete." | tee -a "$LOG_FILE"
echo "📄 Report saved to: $LOG_FILE"
