"""
상수 정의 모듈
더문드립바 (The Moon Drip BAR) - 로스팅 관리 시스템
분석 데이터 기반 (2025-10-24)
"""

# ═══════════════════════════════════════════════════════════════
# 📊 원두 데이터 (13종)
# ═══════════════════════════════════════════════════════════════

BEANS_DATA = [
    {
        "no": 1,
        "country_code": "Eth",
        "country_name": "에티오피아",
        "name": "예가체프",
        "roast_level": "W",
        "description": "밝은 산미, 꽃향기",
        "price_per_kg": 0.0  # 미정
    },
    {
        "no": 2,
        "country_code": "",
        "country_name": "에티오피아",
        "name": "모모라",
        "roast_level": "N",
        "description": "균형잡힌 맛",
        "price_per_kg": 0.0
    },
    {
        "no": 3,
        "country_code": "",
        "country_name": "에티오피아",
        "name": "코케허니",
        "roast_level": "N",
        "description": "부드러운 바디",
        "price_per_kg": 0.0
    },
    {
        "no": 4,
        "country_code": "",
        "country_name": "에티오피아",
        "name": "우라가",
        "roast_level": "W",
        "description": "상큼한 맛",
        "price_per_kg": 0.0
    },
    {
        "no": 5,
        "country_code": "K",
        "country_name": "케냐",
        "name": "AA FAQ",
        "roast_level": "W",
        "description": "풍부한 풍미",
        "price_per_kg": 0.0
    },
    {
        "no": 6,
        "country_code": "",
        "country_name": "케냐",
        "name": "키린야가",
        "roast_level": "Pb",
        "description": "독특한 맛",
        "price_per_kg": 0.0
    },
    {
        "no": 7,
        "country_code": "Co",
        "country_name": "콜롬비아",
        "name": "후일라",
        "roast_level": "W",
        "description": "깊은 바디",
        "price_per_kg": 0.0
    },
    {
        "no": 8,
        "country_code": "Gu",
        "country_name": "과테말라",
        "name": "안티구아",
        "roast_level": "W",
        "description": "풍부한 맛",
        "price_per_kg": 0.0
    },
    {
        "no": 9,
        "country_code": "Cos",
        "country_name": "코스타리카",
        "name": "엘탄케",
        "roast_level": "Rh",
        "description": "특수 로스팅",
        "price_per_kg": 0.0
    },
    {
        "no": 10,
        "country_code": "Br",
        "country_name": "브라질",
        "name": "파젠다카르모",
        "roast_level": "N",
        "description": "견과류 풍미",
        "price_per_kg": 0.0
    },
    {
        "no": 11,
        "country_code": "eth",
        "country_name": "에티오피아",
        "name": "디카페 SDM",
        "roast_level": "SD",
        "description": "카페인 제거",
        "price_per_kg": 0.0
    },
    {
        "no": 12,
        "country_code": "co",
        "country_name": "콜롬비아",
        "name": "디카페 SM",
        "roast_level": "SC",
        "description": "카페인 제거",
        "price_per_kg": 0.0
    },
    {
        "no": 13,
        "country_code": "Br",
        "country_name": "브라질",
        "name": "스위스워터",
        "roast_level": "SD",
        "description": "카페인 제거",
        "price_per_kg": 0.0
    }
]

# 원두 인덱싱 (빠른 조회용)
BEANS_BY_NO = {bean["no"]: bean for bean in BEANS_DATA}
BEANS_BY_NAME = {bean["name"]: bean for bean in BEANS_DATA}

# ═══════════════════════════════════════════════════════════════
# 🎨 블렌딩 레시피 (2가지 타입 × 7개)
# ═══════════════════════════════════════════════════════════════

BLENDS_DATA = [
    # 풀문 블렌드 (Full Moon Blend) - 저녁~밤
    {
        "id": 1,
        "name": "마사이",
        "type": "풀문",
        "description": "깊고 풍부한 맛의 블렌드",
        "recipes": [
            {"bean_no": 1, "bean_name": "예가체프", "portion": 4, "ratio": 40},  # 4개
        ],
        "total_portion": 4,
        "price_suggested": 22000  # 분석 결과
    },
    {
        "id": 2,
        "name": "안티구아",
        "type": "풀문",
        "description": "풍부하고 부드러운 맛",
        "recipes": [
            {"bean_no": 8, "bean_name": "안티구아", "portion": 4, "ratio": 40},  # 4개
        ],
        "total_portion": 4,
        "price_suggested": 0.0
    },
    {
        "id": 3,
        "name": "풀문 블렌드",
        "type": "풀문",
        "description": "4가지 원두의 완벽한 조화",
        "recipes": [
            {"bean_no": 1, "bean_name": "예가체프", "portion": 4, "ratio": 40},
            {"bean_no": 8, "bean_name": "안티구아", "portion": 4, "ratio": 40},
            {"bean_no": 2, "bean_name": "모모라", "portion": 1, "ratio": 10},
            {"bean_no": 13, "bean_name": "G4 (시다모)", "portion": 1, "ratio": 10},  # 편의상 13번
        ],
        "total_portion": 10,
        "price_suggested": 22000
    },
    # 뉴문 블렌딩 (New Moon Blending) - 아침~오후
    {
        "id": 4,
        "name": "브라질",
        "type": "뉴문",
        "description": "부드럽고 부드러운 맛",
        "recipes": [
            {"bean_no": 10, "bean_name": "파젠다카르모", "portion": 6, "ratio": 60},  # 6개
        ],
        "total_portion": 6,
        "price_suggested": 4000  # 분석 결과
    },
    {
        "id": 5,
        "name": "콜롬비아",
        "type": "뉴문",
        "description": "밝고 상큼한 맛",
        "recipes": [
            {"bean_no": 7, "bean_name": "후일라", "portion": 3, "ratio": 30},  # 3개
        ],
        "total_portion": 3,
        "price_suggested": 0.0
    },
    {
        "id": 6,
        "name": "뉴문 블렌딩",
        "type": "뉴문",
        "description": "3가지 원두의 균형있는 조합",
        "recipes": [
            {"bean_no": 10, "bean_name": "파젠다카르모", "portion": 6, "ratio": 60},
            {"bean_no": 7, "bean_name": "후일라", "portion": 3, "ratio": 30},
            {"bean_no": 13, "bean_name": "G4 (시다모)", "portion": 1, "ratio": 10},  # 편의상 13번
        ],
        "total_portion": 10,
        "price_suggested": 4000
    },
    # 기타 블렌드 (향후 추가 가능)
    {
        "id": 7,
        "name": "시즈널 블렌드",
        "type": "시즈널",
        "description": "계절 한정 특별 블렌드",
        "recipes": [
            {"bean_no": 1, "bean_name": "예가체프", "portion": 2, "ratio": 40},      # W
            {"bean_no": 5, "bean_name": "AA FAQ", "portion": 2, "ratio": 40},        # W
            {"bean_no": 10, "bean_name": "파젠다카르모", "portion": 1, "ratio": 20}  # N
        ],
        "total_portion": 5,
        "price_suggested": 25000.0
    }
]

BLENDS_BY_TYPE = {
    "풀문": [b for b in BLENDS_DATA if b["type"] == "풀문"],
    "뉴문": [b for b in BLENDS_DATA if b["type"] == "뉴문"],
    "시즈널": [b for b in BLENDS_DATA if b["type"] == "시즈널"]
}

# ═══════════════════════════════════════════════════════════════
# 📊 로스팅 레벨 정의 (6가지)
# ═══════════════════════════════════════════════════════════════

ROAST_LEVELS = {
    "W": {"name": "Light/White", "description": "밝은 맛, 강한 산미", "count": 5},
    "N": {"name": "Normal", "description": "균형잡힌 맛", "count": 3},
    "Pb": {"name": "Plus Black", "description": "특수 로스팅", "count": 1},
    "Rh": {"name": "Rheuma", "description": "특수 로스팅", "count": 1},
    "SD": {"name": "Semi-Dark", "description": "깊은 맛", "count": 2},
    "SC": {"name": "Semi-Dark", "description": "깊은 맛", "count": 1}
}

# ═══════════════════════════════════════════════════════════════
# 🌍 국가 코드 정의 (6개국)
# ═══════════════════════════════════════════════════════════════

COUNTRIES = {
    "Eth": "에티오피아",
    "K": "케냐",
    "Co": "콜롬비아",
    "Gu": "과테말라",
    "Cos": "코스타리카",
    "Br": "브라질"
}

# ═══════════════════════════════════════════════════════════════
# ⚙️ 비용 설정 (기본값)
# ═══════════════════════════════════════════════════════════════

DEFAULT_COST_SETTINGS = {
    "roasting_loss_rate": 0.167,              # 16.7% (로스팅 손실)
    "roasting_cost_per_kg": 2000,             # ₩2,000/kg
    "labor_cost_per_hour": 15000,             # ₩15,000/hour
    "roasting_time_hours": 2.0,               # 2시간
    "electricity_cost": 5000,                 # ₩5,000
    "misc_cost": 3000,                        # ₩3,000
    "default_margin_rate": 2.5,               # 2.5배 마진율
}

# ═══════════════════════════════════════════════════════════════
# 📈 통계 & 분석 설정
# ═══════════════════════════════════════════════════════════════

ANALYTICS_CONFIG = {
    "min_inventory_alert": 2.0,               # 재고 부족 알림 (kg)
    "min_inventory_warning": 5.0,             # 재고 주의 (kg)
    "inventory_max_days": 30,                 # 최대 재고 일수
}

# ═══════════════════════════════════════════════════════════════
# 🎨 UI 설정
# ═══════════════════════════════════════════════════════════════

UI_CONFIG = {
    "app_title": "더문드립바",
    "app_subtitle": "The Moon Drip BAR - 로스팅 관리 시스템",
    "color_primary": "#1F4E78",
    "color_secondary": "#4472C4",
    "color_success": "#70AD47",
    "color_warning": "#FFC000",
    "color_danger": "#C41E3A",
    "page_icon": "☕",
}

# ═══════════════════════════════════════════════════════════════
# 🔄 데이터베이스 설정
# ═══════════════════════════════════════════════════════════════

DATABASE_CONFIG = {
    "database_path": "Data/roasting_data.db",
    "check_same_thread": False,
    "timeout": 30,
}

# ═══════════════════════════════════════════════════════════════
# 📊 통계 요약 (분석 결과)
# ═══════════════════════════════════════════════════════════════

ANALYSIS_SUMMARY = {
    "total_beans": 13,
    "total_blends": 7,
    "full_moon_blends": 4,  # 풀문: 마사이, 안티구아, 모모라, G4
    "new_moon_blends": 3,   # 뉴문: 브라질, 콜롬비아, G4
    "total_portions": 20,   # 풀문(10) + 뉴문(10)
    "countries": 6,
    "roast_levels": 6,
    "analysis_date": "2025-10-24",
}

# ═══════════════════════════════════════════════════════════════
# 🔍 조회 헬퍼 함수
# ═══════════════════════════════════════════════════════════════

def get_bean_by_no(no: int) -> dict:
    """번호로 원두 조회"""
    return BEANS_BY_NO.get(no, {})

def get_bean_by_name(name: str) -> dict:
    """이름으로 원두 조회"""
    return BEANS_BY_NAME.get(name, {})

def get_blends_by_type(blend_type: str) -> list:
    """타입별 블렌드 조회"""
    return BLENDS_BY_TYPE.get(blend_type, [])

def get_country_name(code: str) -> str:
    """국가 코드로 국가명 조회"""
    return COUNTRIES.get(code, "기타")

def get_roast_level_info(level: str) -> dict:
    """로스팅 레벨 정보 조회"""
    return ROAST_LEVELS.get(level, {})

if __name__ == "__main__":
    # 테스트 출력
    print("✅ 원두 데이터 로드 완료")
    print(f"   - 총 원두: {len(BEANS_DATA)}종")
    print(f"   - 총 블렌드: {len(BLENDS_DATA)}종")
    print(f"   - 로스팅 레벨: {len(ROAST_LEVELS)}가지")
    print(f"   - 국가: {len(COUNTRIES)}개국")
