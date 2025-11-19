"""
애플리케이션 설정 및 상수 관리
"""

import os

# 기본 설정
APP_TITLE = "The Moon Drip BAR - Roasting Cost Calculator"
APP_SUBTITLE = "Premium Coffee Roasting Management System"
PAGE_ICON = "☕"

# 버전 및 상태 정보
VERSION = "v0.50.0"
UPDATE_DATE = "2025-11-19"
PROJECT_STATUS = "Production Ready"
UI_STYLE = "Claude Desktop Style"

# 로스팅 기본값
DEFAULT_ROASTING_LOSS_RATE = 17.0  # %
DEFAULT_ROASTING_COST_PER_KG = 2000.0  # KRW
DEFAULT_LABOR_COST_PER_HOUR = 15000.0  # KRW
DEFAULT_ROASTING_TIME_HOURS = 2.0  # Hours
DEFAULT_ELECTRICITY_COST = 5000.0  # KRW
DEFAULT_MISC_COST = 3000.0  # KRW

# 마진율 설정
DEFAULT_MARGIN_RATE = 2.5  # 2.5배

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
STYLE_CSS_PATH = os.path.join(ASSETS_DIR, "style.css")

# UI 설정
UI_CONFIG = {
    "app_title": APP_TITLE,
    "app_subtitle": APP_SUBTITLE,
    "page_icon": PAGE_ICON,
    "sidebar_state": "expanded"
}
