"""
프로젝트 설정 및 버전 정보 중앙 관리

이 파일은 프로젝트의 모든 버전 정보와 설정을 중앙에서 관리합니다.
logs/VERSION 파일을 Single Source of Truth로 사용하여 버전 정보를 동기화합니다.
"""

import os
from pathlib import Path
from datetime import datetime

# 프로젝트 루트 및 VERSION 파일 경로
PROJECT_ROOT = Path(__file__).parent.parent
VERSION_FILE = PROJECT_ROOT / "logs" / "VERSION"


def get_version() -> str:
    """
    logs/VERSION 파일에서 현재 버전 읽기
    
    Returns:
        str: 현재 버전 (예: "0.29.0")
    """
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "0.0.0"


def get_update_date() -> str:
    """
    logs/VERSION 파일의 최종 수정일 가져오기
    
    Returns:
        str: 최종 업데이트 날짜 (YYYY-MM-DD 형식)
    """
    if VERSION_FILE.exists():
        timestamp = VERSION_FILE.stat().st_mtime
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    return datetime.now().strftime("%Y-%m-%d")


# ============================================
# 프로젝트 정보 (Single Source of Truth)
# ============================================

# 버전 정보 (logs/VERSION에서 자동 로드)
VERSION = get_version()
UPDATE_DATE = get_update_date()

# 프로젝트 메타데이터
PROJECT_NAME = "더문드립바 로스팅 비용 계산기"
PROJECT_NAME_EN = "The Moon Drip BAR - Roasting Cost Calculator"
PROJECT_STATUS = "✅ Phase 1-5 완료 / 🚀 보고서 및 분석 시스템 구축 완료"

# UI 스타일
UI_STYLE = "Claude Desktop Style UI"

# 데이터베이스
DATABASE_PATH = PROJECT_ROOT / "data" / "roasting_data.db"

# 로깅
LOG_DIR = PROJECT_ROOT / "logs"


# ============================================
# 버전 정보 포맷팅 함수
# ============================================

def get_version_info() -> dict:
    """
    전체 버전 정보를 딕셔너리로 반환
    
    Returns:
        dict: 버전 정보 딕셔너리
    """
    return {
        "version": VERSION,
        "update_date": UPDATE_DATE,
        "project_name": PROJECT_NAME,
        "project_name_en": PROJECT_NAME_EN,
        "project_status": PROJECT_STATUS,
        "ui_style": UI_STYLE
    }


def format_version_display() -> str:
    """
    화면 표시용 버전 정보 포맷팅
    
    Returns:
        str: 포맷팅된 버전 문자열 (예: "v0.29.0")
    """
    return f"v{VERSION}"


def format_info_display() -> str:
    """
    정보 페이지용 전체 정보 포맷팅
    
    Returns:
        str: 포맷팅된 정보 문자열
    """
    return f"""ℹ️ **정보**

**{PROJECT_NAME} {format_version_display()}**

🚀 {UI_STYLE}  
📅 **업데이트**: {UPDATE_DATE}  
🎯 **상태**: {PROJECT_STATUS}
"""
