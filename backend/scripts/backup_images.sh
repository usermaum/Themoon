#!/bin/bash
# backup_images.sh - 주간 백업 스크립트

BACKUP_DIR="/mnt/d/Ai/WslProject/Themoon/backups/images"
SOURCE_DIR="/mnt/d/Ai/WslProject/Themoon/backend/static/uploads/inbound"
DATE=$(date +%Y%m%d)

# 백업 디렉토리 생성
mkdir -p "$BACKUP_DIR"

# 증분 백업 (rsync) - 시간 우선 구조 활용
# WSL 환경을 고려하여 rsync 옵션 조정
rsync -avz --delete \
  "$SOURCE_DIR/" \
  "$BACKUP_DIR/invoices_$DATE/"

# 7일 이전 백업 삭제
find "$BACKUP_DIR" -type d -mtime +7 -name "invoices_*" -exec rm -rf {} \;

# 월별 압축 아카이브 (선택 사항)
YEAR=$(date +%Y)
MONTH=$(date +%m)

if [ -d "$SOURCE_DIR/$YEAR/$MONTH" ]; then
    ARCHIVE_PATH="$BACKUP_DIR/archive_${YEAR}_${MONTH}.tar.gz"
    # 이미 아카이브가 없는 경우에만 생성
    if [ ! -f "$ARCHIVE_PATH" ]; then
        tar -czf "$ARCHIVE_PATH" \
            -C "$SOURCE_DIR" "$YEAR/$MONTH"
    fi
fi
