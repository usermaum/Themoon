"""
텍스트 파싱 유틸리티

OCR 결과 텍스트에서 구조화된 데이터를 추출합니다.
"""

import re
from typing import Optional, List, Tuple, Dict
from datetime import date, datetime
import dateparser
from Levenshtein import distance as levenshtein_distance


def normalize_text(text: str) -> str:
    """
    텍스트 정규화

    - 공백 정리 (여러 공백 → 하나)
    - 양쪽 공백 제거
    - 소문자 변환 (영문)

    Args:
        text: 원본 텍스트

    Returns:
        정규화된 텍스트
    """
    if not text:
        return ""

    # 여러 공백 → 하나
    normalized = re.sub(r'\s+', ' ', text)

    # 양쪽 공백 제거
    normalized = normalized.strip()

    return normalized


def extract_bean_name(text: str) -> Optional[str]:
    """
    원두명 추출 (휴리스틱 기반)

    전략:
    1. 영문 단어 조합 찾기 (국가명 + 등급 + 특징)
       예: "Ethiopia G1 Yirgacheffe"
    2. 한글 원두명 찾기
       예: "에티오피아 예가체프 G1"

    Args:
        text: OCR 텍스트

    Returns:
        추출된 원두명 (없으면 None)
    """
    # 패턴 1: 영문 원두명 (국가명 포함)
    # 예: Brazil NY2, Ethiopia G1, Colombia Supremo
    bean_pattern_en = r'[A-Z][a-z]+(?:\s+[A-Z0-9][a-zA-Z0-9/\-]*){1,5}'

    # 패턴 2: 한글 원두명
    # 예: 에티오피아 예가체프 G1, 브라질 산토스
    bean_pattern_kr = r'[가-힣]+(?:\s+[가-힣A-Z0-9]+){1,4}'

    # 영문 우선 검색
    match_en = re.search(bean_pattern_en, text)
    if match_en:
        return normalize_text(match_en.group(0))

    # 한글 검색
    match_kr = re.search(bean_pattern_kr, text)
    if match_kr:
        return normalize_text(match_kr.group(0))

    return None


def extract_quantity(text: str) -> Optional[float]:
    """
    수량 추출 (kg 단위로 변환)

    지원 형식:
    - "10kg", "10 kg", "10KG"
    - "10,000g", "10000 g"
    - "10.5kg"

    Args:
        text: OCR 텍스트

    Returns:
        수량 (kg 단위, 없으면 None)
    """
    # 패턴 1: kg 단위
    pattern_kg = r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*[Kk][Gg]'
    match_kg = re.search(pattern_kg, text)

    if match_kg:
        quantity_str = match_kg.group(1).replace(',', '')
        return float(quantity_str)

    # 패턴 2: g 단위 (1000g = 1kg)
    pattern_g = r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*[Gg](?![Gg])'  # 'g'만 매칭 (gg 제외)
    match_g = re.search(pattern_g, text)

    if match_g:
        quantity_str = match_g.group(1).replace(',', '')
        return float(quantity_str) / 1000  # g → kg

    return None


def extract_price(text: str) -> Optional[float]:
    """
    가격 추출 (원 단위)

    지원 형식:
    - "₩15,000", "￦15,000"
    - "15,000원", "15000원"
    - "15,000", "15000" (fallback)

    Args:
        text: OCR 텍스트

    Returns:
        가격 (원 단위, 없으면 None)
    """
    # 패턴 1: ₩/￦ 기호
    pattern_won_symbol = r'[₩￦]\s*(\d+(?:,\d{3})*)'
    match_symbol = re.search(pattern_won_symbol, text)

    if match_symbol:
        price_str = match_symbol.group(1).replace(',', '')
        return float(price_str)

    # 패턴 2: "원" 문자
    pattern_won_char = r'(\d+(?:,\d{3})*)\s*원'
    match_char = re.search(pattern_won_char, text)

    if match_char:
        price_str = match_char.group(1).replace(',', '')
        return float(price_str)

    # 패턴 3: 숫자만 (fallback, 가장 큰 숫자)
    # 예: "15000" (쉼표 있거나 없거나)
    pattern_number = r'(\d{4,})(?:,\d{3})*'
    matches = re.findall(pattern_number, text)

    if matches:
        # 가장 큰 숫자 선택 (총액일 가능성)
        prices = [float(m.replace(',', '')) for m in matches]
        return max(prices)

    return None


def extract_date(text: str) -> Optional[date]:
    """
    날짜 추출 (dateparser 사용 + 한글 패턴 개선)

    지원 형식:
    - "2025-11-12", "2025/11/12", "2025.11.12"
    - "2025년 11월 12일"
    - "11/12/2025"
    - "10월 29일", "108 29일" (OCR 오인식)
    - "2025-11-12 14:30" (시간 포함, 날짜만 반환)

    Args:
        text: OCR 텍스트

    Returns:
        추출된 날짜 (없으면 None)
    """
    # 1. 패턴 기반 우선 (YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD)
    # OCR이 표 전체를 읽으면 날짜가 다른 숫자와 섞일 수 있음
    date_pattern = r'(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})'
    match = re.search(date_pattern, text)

    if match:
        year, month, day = match.groups()
        try:
            return date(int(year), int(month), int(day))
        except ValueError:
            pass

    # 1-2. "YYYY년 MM월 DD일" 또는 "YYYY = MM9 DD일" (OCR 오인식) 패턴
    # 예: "2025년 10월 29일", "2025 = 109 29일"
    korean_full_date_pattern = r'(\d{4})\s*[년=\-]\s*(\d{1,3})\s*[월9oO]\s*(\d{1,2})\s*일'
    match = re.search(korean_full_date_pattern, text)
    if match:
        year_str, month_str, day_str = match.groups()
        year = int(year_str)
        # OCR 오인식: "109" → "10"
        month = int(month_str[-2:]) if len(month_str) > 2 else int(month_str)
        day = int(day_str)

        # 유효성 검사
        if 1 <= month <= 12 and 1 <= day <= 31:
            try:
                return date(year, month, day)
            except ValueError:
                pass

    # 2. 한글 날짜 패턴 (OCR 오인식 대응)
    # "10월 29일", "108 29일", "10 8 29 일" (공백 포함)
    korean_date_pattern = r'(\d{1,3})\s*월?\s*(\d{1,2})\s*일'
    match = re.search(korean_date_pattern, text)
    if match:
        month_str, day_str = match.groups()
        # OCR 오인식: "108" → "10"
        month = int(month_str[-2:]) if len(month_str) > 2 else int(month_str)
        day = int(day_str)

        # 월/일 유효성 검사
        if 1 <= month <= 12 and 1 <= day <= 31:
            # 현재 연도 사용
            current_year = datetime.now().year
            try:
                return date(current_year, month, day)
            except ValueError:
                pass

    # 3. dateparser 설정
    settings = {
        'PREFER_DAY_OF_MONTH': 'first',  # 날짜 우선 (MM/DD vs DD/MM)
        'PREFER_DATES_FROM': 'past',     # 과거 날짜 우선
        'RETURN_AS_TIMEZONE_AWARE': False
    }

    # 한글 + 영문 파싱
    parsed = dateparser.parse(text, languages=['ko', 'en'], settings=settings)

    if parsed:
        return parsed.date()

    return None


def fuzzy_match_bean(
    ocr_name: str,
    beans: List['Bean'],  # Bean 모델 리스트
    threshold: float = 0.65  # 임계값 하향 조정 (0.7 → 0.65)
) -> Tuple[Optional['Bean'], float]:
    """
    원두명 유사도 매칭 (개선된 알고리즘)

    개선 사항:
    1. Levenshtein Distance (전체 문자열 유사도)
    2. 토큰 기반 매칭 (단어별 비교)
    3. 부분 문자열 매칭 (일부 포함 여부)
    4. 가중 평균으로 최종 점수 계산

    Args:
        ocr_name: OCR로 추출한 원두명
        beans: DB에 저장된 Bean 객체 리스트
        threshold: 최소 유사도 (0~1, 기본값 0.65)

    Returns:
        (매칭된 Bean 객체, 유사도 점수)
        매칭 실패 시 (None, 0.0)
    """
    if not ocr_name or not beans:
        return None, 0.0

    # 정규화
    ocr_name_normalized = normalize_text(ocr_name.lower())
    ocr_tokens = set(ocr_name_normalized.split())

    best_bean = None
    best_score = 0.0

    for bean in beans:
        bean_name_normalized = normalize_text(bean.name.lower())
        bean_tokens = set(bean_name_normalized.split())

        # 1. Levenshtein Distance (가중치 40%)
        max_len = max(len(ocr_name_normalized), len(bean_name_normalized))
        if max_len == 0:
            continue

        dist = levenshtein_distance(ocr_name_normalized, bean_name_normalized)
        lev_similarity = 1 - (dist / max_len)

        # 2. 토큰 기반 Jaccard 유사도 (가중치 40%)
        # 교집합 / 합집합
        if ocr_tokens and bean_tokens:
            intersection = len(ocr_tokens & bean_tokens)
            union = len(ocr_tokens | bean_tokens)
            token_similarity = intersection / union if union > 0 else 0
        else:
            token_similarity = 0

        # 3. 부분 문자열 매칭 (가중치 20%)
        substring_similarity = 0
        if ocr_name_normalized in bean_name_normalized or bean_name_normalized in ocr_name_normalized:
            substring_similarity = 0.8  # 부분 일치 시 보너스

        # 4. 가중 평균
        final_similarity = (
            lev_similarity * 0.4 +
            token_similarity * 0.4 +
            substring_similarity * 0.2
        )

        # 최고 점수 업데이트
        if final_similarity > best_score:
            best_score = final_similarity
            best_bean = bean

    # 임계값 이상만 반환
    if best_score >= threshold:
        return best_bean, best_score
    else:
        return None, best_score


def extract_supplier_name(text: str) -> Optional[str]:
    """
    공급업체명 추출

    패턴:
    - (주)회사명, 주식회사 회사명
    - 영문 회사명 (대문자 시작)

    Args:
        text: OCR 텍스트

    Returns:
        공급업체명 (없으면 None)
    """
    # 패턴 1: (주)회사명
    pattern_corp_1 = r'\(주\)\s*([가-힣A-Za-z0-9\s]+)'
    match_1 = re.search(pattern_corp_1, text)
    if match_1:
        return normalize_text(match_1.group(0))

    # 패턴 2: 주식회사 회사명
    pattern_corp_2 = r'주식회사\s+([가-힣A-Za-z0-9\s]+)'
    match_2 = re.search(pattern_corp_2, text)
    if match_2:
        return normalize_text(match_2.group(0))

    # 패턴 3: 영문 회사명 (대문자 2개 이상 + 선택적 소문자)
    # 예: "GSC GREEN COFFEE"
    pattern_corp_en = r'[A-Z]{2,}(?:\s+[A-Z]{2,}){0,3}'
    match_en = re.search(pattern_corp_en, text)
    if match_en:
        return normalize_text(match_en.group(0))

    return None


def extract_total_amount(text: str) -> Optional[float]:
    """
    총액 추출

    패턴:
    - "합계금액: 150,000원"
    - "총액: ₩150,000"
    - "Total: 150000"

    Args:
        text: OCR 텍스트

    Returns:
        총액 (원 단위, 없으면 None)
    """
    # 패턴 1: "합계금액", "총액", "합계"
    keywords = ['합계금액', '총액', '합계', 'Total', 'TOTAL', '학계금액', '학계금9']  # OCR 오인식 포함

    for keyword in keywords:
        # 키워드 뒤에 오는 숫자 찾기 (괄호, 쉼표, 공백 허용)
        # 예: "1,845,000", "1845000", "1825003)", "18-5000"
        pattern = rf'{keyword}\s*[:：]?\s*[₩￦]?\s*(\d+(?:[,\-\s]\d{{3,}})*)\s*[)）]?\s*원?'
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            amount_str = match.group(1)
            # 쉼표, 하이픈, 공백 제거
            amount_str = amount_str.replace(',', '').replace('-', '').replace(' ', '')

            # 숫자만 남기고 파싱
            try:
                return float(amount_str)
            except ValueError:
                continue

    return None


def extract_origin(text: str) -> Optional[str]:
    """
    원산지 추출

    일반적인 커피 생산 국가:
    - 영문: Brazil, Ethiopia, Colombia, Kenya, Guatemala, etc.
    - 한글: 브라질, 에티오피아, 콜롬비아, 케냐, 과테말라, etc.

    Args:
        text: OCR 텍스트

    Returns:
        원산지 (없으면 None)
    """
    # 주요 커피 생산 국가 목록
    origins_en = [
        'Brazil', 'Ethiopia', 'Colombia', 'Kenya', 'Guatemala',
        'Costa Rica', 'Honduras', 'Peru', 'Panama', 'Rwanda',
        'Indonesia', 'Vietnam', 'India', 'Yemen', 'Jamaica'
    ]

    origins_kr = [
        '브라질', '에티오피아', '콜롬비아', '케냐', '과테말라',
        '코스타리카', '온두라스', '페루', '파나마', '르완다',
        '인도네시아', '베트남', '인도', '예멘', '자메이카'
    ]

    # 영문 원산지 검색
    for origin in origins_en:
        if origin in text:
            return origin

    # 한글 원산지 검색
    for origin in origins_kr:
        if origin in text:
            return origin

    return None


def parse_invoice_basic(ocr_text: str) -> Dict:
    """
    기본 명세서 파싱 (범용)

    OCR 텍스트에서 필수/선택 정보 추출

    Args:
        ocr_text: OCR 결과 텍스트

    Returns:
        {
            'bean_name': str | None,
            'quantity': float | None,  # kg 단위
            'unit_price': float | None,  # 원/kg
            'invoice_date': date | None,
            'supplier': str | None,
            'total_amount': float | None,
            'origin': str | None
        }
    """
    return {
        'bean_name': extract_bean_name(ocr_text),
        'quantity': extract_quantity(ocr_text),
        'unit_price': extract_price(ocr_text),
        'invoice_date': extract_date(ocr_text),
        'supplier': extract_supplier_name(ocr_text),
        'total_amount': extract_total_amount(ocr_text),
        'origin': extract_origin(ocr_text)
    }


def calculate_amount(quantity: float, unit_price: float) -> float:
    """
    공급가액 계산

    Args:
        quantity: 수량 (kg)
        unit_price: 단가 (원/kg)

    Returns:
        공급가액 (원)
    """
    return quantity * unit_price


def validate_parsed_data(parsed_data: Dict) -> Tuple[bool, List[str]]:
    """
    파싱된 데이터 검증

    필수 필드:
    - bean_name (원두명)
    - quantity (수량)
    - unit_price (단가) 또는 total_amount (총액)
    - invoice_date (거래일자)

    Args:
        parsed_data: parse_invoice_basic() 반환값

    Returns:
        (검증 성공 여부, 경고 메시지 리스트)
    """
    warnings = []

    # 필수 필드 확인
    if not parsed_data.get('bean_name'):
        warnings.append("⚠️ 원두명을 찾을 수 없습니다")

    if not parsed_data.get('quantity'):
        warnings.append("⚠️ 수량을 찾을 수 없습니다")

    if not parsed_data.get('unit_price') and not parsed_data.get('total_amount'):
        warnings.append("⚠️ 가격 정보를 찾을 수 없습니다")

    if not parsed_data.get('invoice_date'):
        warnings.append("⚠️ 거래일자를 찾을 수 없습니다")

    # 성공 여부 (경고 없으면 성공)
    is_valid = len(warnings) == 0

    return is_valid, warnings


# ========================================
# GSC 명세서 전용 파싱 로직
# ========================================

def detect_invoice_type(ocr_text: str) -> str:
    """
    명세서 타입 감지 (개선된 버전)

    Args:
        ocr_text: OCR 결과 텍스트

    Returns:
        'GSC' | 'HACIELO' | 'UNKNOWN'
    """
    ocr_upper = ocr_text.upper()

    # GSC 명세서 시그니처 (더 유연하게 개선)
    # 1. "GSC" 키워드 (대소문자 무관)
    # 2. "coffeegsc" 이메일 도메인
    # 3. 사업자번호 "197-04-00506" 또는 OCR 오인식 패턴 (157-04, 197-04, 922507661582)
    # 4. "거래명세서" 키워드
    # 5. "사업장" + 테이블 구조 패턴
    gsc_indicators = [
        'GSC' in ocr_upper,
        'ESL' in ocr_upper,  # EasyOCR "GSC" 오인식
        'COFFEEGSC' in ocr_upper,
        '197-04-00506' in ocr_text,
        '922507661582' in ocr_text,  # 사업자번호 OCR 오인식 (@AMAR 등)
        '157-04' in ocr_text,  # OCR 오인식 패턴
        '197-04' in ocr_text,  # 부분 매칭
        '거래명세서' in ocr_text or '거 래 명 세 서' in ocr_text,  # 공백 포함 패턴
        ('사업장' in ocr_text and '우스' in ocr_text),  # "사업장 ... 우스" 패턴
        'coffeegsc' in ocr_text.lower()  # 이메일 도메인
    ]

    # 2개 이상의 지표가 매칭되면 GSC로 판정
    if sum(gsc_indicators) >= 2:
        return 'GSC'

    # 확실한 단일 지표만으로도 GSC 판정
    if 'COFFEEGSC' in ocr_upper or '197-04-00506' in ocr_text or '922507661582' in ocr_text:
        return 'GSC'

    # HACIELO 명세서 시그니처
    if 'HACIELO' in ocr_upper or '최근 3개월 주문내역' in ocr_text:
        return 'HACIELO'

    return 'UNKNOWN'


def parse_gsc_invoice(ocr_text: str) -> Dict:
    """
    GSC 명세서 전용 파싱 로직

    테이블 형식을 파싱하여 다중 원두 추출

    Args:
        ocr_text: OCR 결과 텍스트

    Returns:
        {
            'invoice_date': date | None,
            'supplier': str,
            'contract_number': str | None,
            'total_amount': float | None,
            'total_weight': float | None,
            'items': [
                {
                    'no': int,
                    'bean_name': str,
                    'spec': str,          # 규격 (1kg, 5kg, ...)
                    'quantity': int,      # 수량 (포장 개수)
                    'weight': float,      # 중량 (kg)
                    'unit_price': float,  # 단가 (원/kg)
                    'amount': float       # 공급가액 (원)
                },
                ...
            ]
        }
    """
    result = {
        'supplier': 'GSC GREEN COFFEE',
        'invoice_date': None,
        'contract_number': None,
        'total_weight': None,
        'total_amount': None,
        'items': []
    }

    # 1. 계약일자 추출 (하단)
    # 패턴: "계약일자 : 2025년 11월 12일"
    date_pattern = r'계약일자\s*[:：]\s*(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일'
    date_match = re.search(date_pattern, ocr_text)
    if date_match:
        year, month, day = date_match.groups()
        try:
            result['invoice_date'] = date(int(year), int(month), int(day))
        except ValueError:
            pass

    # 2. 계약번호 추출
    # 패턴: "계약번호 : ABC123"
    contract_pattern = r'계약번호\s*[:：]\s*([A-Z0-9\-]+)'
    contract_match = re.search(contract_pattern, ocr_text)
    if contract_match:
        result['contract_number'] = contract_match.group(1)

    # 3. 총 중량 추출 (하단)
    # 패턴: "총 중량 : 100kg", "총중량: 100Kg"
    weight_pattern = r'총\s*중량\s*[:：]\s*(\d+(?:\.\d+)?)\s*[Kk]g'
    weight_match = re.search(weight_pattern, ocr_text)
    if weight_match:
        result['total_weight'] = float(weight_match.group(1))

    # 4. 합계금액 추출 (하단)
    # 패턴: "합계금액 : 1,500,000원"
    amount_pattern = r'합계금액\s*[:：]\s*([\d,]+)\s*원'
    amount_match = re.search(amount_pattern, ocr_text)
    if amount_match:
        result['total_amount'] = float(amount_match.group(1).replace(',', ''))

    # 5. 테이블 파싱 (핵심 로직)
    items = parse_gsc_table(ocr_text)
    result['items'] = items

    return result


def parse_gsc_table(ocr_text: str) -> List[Dict]:
    """
    GSC 명세서 테이블 파싱

    테이블 형식:
    NO. | 품목 | 규격 | 수량 | 중량 | 단가 | 공급가액

    전략:
    1. 테이블 헤더 위치 찾기 ("NO.", "품목", "규격", ...)
    2. 헤더 아래 라인들을 순회
    3. 각 라인에서 7개 필드 추출
    4. 숫자가 아닌 라인은 건너뛰기 (빈 행)

    Args:
        ocr_text: OCR 결과 텍스트

    Returns:
        파싱된 항목 리스트 (List[Dict])
    """
    items = []

    # 테이블 섹션 추출 (NO.부터 하단 정보 전까지)
    # 시작: "NO." 키워드
    table_start = ocr_text.find('NO.')

    # 종료: 하단 정보 키워드 중 하나 (벤슬비, 계약일자, 총중량 등)
    end_keywords = ['벤슬비', '계약일자', '총 중량', '총중량', '합계금액']
    table_end = -1

    for keyword in end_keywords:
        pos = ocr_text.find(keyword)
        if pos != -1:
            if table_end == -1 or pos < table_end:
                table_end = pos

    if table_start == -1 or table_end == -1:
        return items

    table_text = ocr_text[table_start:table_end]
    lines = table_text.split('\n')

    # 헤더 라인 건너뛰기 (첫 2줄: "NO." 라인 + 컬럼명 라인)
    for line in lines[2:]:
        # 빈 라인 건너뛰기
        if not line.strip():
            continue

        # NO. 숫자로 시작하는 라인만 처리
        if not re.match(r'^\s*\d+', line):
            continue

        # 라인 파싱
        item = parse_gsc_table_row(line)
        if item:
            items.append(item)

    return items


def parse_gsc_table_row(line: str) -> Optional[Dict]:
    """
    GSC 테이블 한 행 파싱

    패턴:
    1  Colombia Supreme Hulls  1kg  30  30  14,500  435,000

    주의:
    - 원두명이 길어서 여러 단어로 구성 (Brazil NY2 FC 17/18 M-Y TYPE)
    - 숫자는 쉼표 포함 가능 (14,500)

    Args:
        line: 테이블 행 텍스트

    Returns:
        파싱된 항목 (Dict) 또는 None (파싱 실패 시)
    """
    # 정규식: NO. | 원두명 (여러 단어) | 규격 | 수량 | 중량 | 단가 | 공급가액
    # 원두명은 greedy하게 최대한 많이 매칭 (.+?)
    pattern = r'''
        ^\s*(\d+)                           # NO.
        \s+(.+?)                            # 원두명 (non-greedy, 나머지 필드 남기기)
        \s+(\d+\s*[Kk][Gg])                 # 규격 (1kg, 5kg, ...)
        \s+(\d+)                            # 수량
        \s+(\d+(?:\.\d+)?)                  # 중량 (소수점 가능)
        \s+([\d,]+)                         # 단가 (쉼표 가능)
        \s+([\d,]+)                         # 공급가액 (쉼표 가능)
    '''

    match = re.search(pattern, line, re.VERBOSE)

    if not match:
        return None

    no, bean_name, spec, quantity, weight, unit_price, amount = match.groups()

    # 원두명 정리 (양쪽 공백 제거)
    bean_name = normalize_text(bean_name)

    # 숫자 변환
    try:
        no = int(no)
        quantity = int(quantity)
        weight = float(weight)
        unit_price = float(unit_price.replace(',', ''))
        amount = float(amount.replace(',', ''))
    except ValueError:
        return None

    return {
        'no': no,
        'bean_name': bean_name,
        'spec': spec.strip(),
        'quantity': quantity,
        'weight': weight,
        'unit_price': unit_price,
        'amount': amount
    }


def parse_invoice(ocr_text: str) -> Dict:
    """
    명세서 타입 자동 감지 및 파싱

    Args:
        ocr_text: OCR 결과 텍스트

    Returns:
        파싱된 데이터 (Dict)
        - 타입별로 다른 구조 반환
        - 공통 필드: 'invoice_type', 'supplier', 'invoice_date', 'items'
    """
    invoice_type = detect_invoice_type(ocr_text)

    if invoice_type == 'GSC':
        result = parse_gsc_invoice(ocr_text)
        result['invoice_type'] = 'GSC'
        return result

    elif invoice_type == 'HACIELO':
        # HACIELO 파싱 로직 (TODO: 향후 구현)
        result = parse_invoice_basic(ocr_text)
        result['invoice_type'] = 'HACIELO'
        result['items'] = []
        return result

    else:
        # UNKNOWN: 기본 파싱
        result = parse_invoice_basic(ocr_text)
        result['invoice_type'] = 'UNKNOWN'
        result['items'] = []
        return result
