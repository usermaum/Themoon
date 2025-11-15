#!/bin/bash
# EasyOCR Pillow 10.x 호환성 패치 스크립트
#
# 문제: Pillow 10.x에서 Image.ANTIALIAS 상수가 제거됨
# 해결: Image.LANCZOS로 치환
#
# 사용법:
#   ./scripts/patch_easyocr.sh
#
# 또는 pip install 후 자동 실행:
#   ./venv/bin/pip install easyocr==1.7.0 && ./scripts/patch_easyocr.sh

set -e

VENV_PATH="./venv"
EASYOCR_UTILS="${VENV_PATH}/lib/python3.12/site-packages/easyocr/utils.py"

echo "🔧 EasyOCR Pillow 호환성 패치 시작..."

if [ ! -f "$EASYOCR_UTILS" ]; then
    echo "❌ EasyOCR utils.py 파일을 찾을 수 없습니다: $EASYOCR_UTILS"
    echo "   먼저 easyocr를 설치하세요: ./venv/bin/pip install easyocr==1.7.0"
    exit 1
fi

# 백업 생성
if [ ! -f "${EASYOCR_UTILS}.backup" ]; then
    echo "📦 백업 생성 중..."
    cp "$EASYOCR_UTILS" "${EASYOCR_UTILS}.backup"
fi

# Image.ANTIALIAS → Image.LANCZOS 치환
echo "🔨 패치 적용 중..."
sed -i 's/Image\.ANTIALIAS/Image.LANCZOS/g' "$EASYOCR_UTILS"

# 패치 확인
if grep -q "Image.LANCZOS" "$EASYOCR_UTILS"; then
    echo "✅ 패치 완료!"
    echo "   변경 사항: Image.ANTIALIAS → Image.LANCZOS"
else
    echo "❌ 패치 실패: Image.LANCZOS를 찾을 수 없습니다."
    exit 1
fi

# 변경된 줄 수 확인
CHANGED_LINES=$(grep -c "Image.LANCZOS" "$EASYOCR_UTILS" || echo "0")
echo "   패치된 줄 수: $CHANGED_LINES"

echo ""
echo "🎉 EasyOCR 패치 완료!"
echo "   백업 파일: ${EASYOCR_UTILS}.backup"
