# 더문(The Moon) 로스팅 및 재고 관리 운영 계획안 v2.0

## 1. 개요 (Overview)
본 문서는 '더문(The Moon)'의 효율적인 로스팅 생산 관리 및 재고 운영을 위한 기준 정보와 업무 시나리오를 정의합니다. 원두의 입고부터 로스팅, 블렌딩, 그리고 최종 제품 생산에 이르는 프로세스를 체계화하여 데이터 기반의 운영을 목표로 합니다.

### 1.1 용어 및 관리 기준 (Terminology & Standards)

**1. 재료 및 제품 분류**
*   **생두 (Green Bean)**: 로스팅 전의 원재료. 품종별로 관리합니다.
*   **원두 (Roasted Bean)**: 로스팅이 완료된 제품.
    *   **싱글 오리진 (Single Origin)**: 한 종류의 생두를 로스팅한 것. **로스팅 프로필(신콩/탄콩)**에 따라 별도 품목으로 관리됩니다.
    *   **블렌드 (Blend)**: 여러 생두를 배합하여 로스팅한 것.

**2. 로스팅 프로필 (Roasting Profile)**
싱글 오리진 원두는 로스팅 포인트에 따라 두 가지로 구분하여 생산 및 관리합니다.
*   **신콩 (Light/Medium Roast)**: 산미와 향미를 강조한 약~중볶음.
*   **탄콩 (Dark Roast)**: 바디감과 쓴맛을 강조한 강볶음.

**3. 재고 관리 단위 (SKU Logic)**
*   **생두**: `{품종명}` (예: 예가체프)
*   **싱글 원두**: `{품종명}-{프로필}` (예: 예가체프-신콩, 예가체프-탄콩)
*   **블렌드 원두**: `{블렌드명}` (예: 풀문, 뉴문)

---

## 2. 기준 정보 (Master Data)

### 2.1 생두 및 원두 마스터 (Bean Master List)
취급하는 모든 생두와 이를 가공한 원두의 표준 목록입니다.

| No | 표준 한글명 | 영문 표기 (명세서 기준) | 국가 | 등급/특이사항 | 비고 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | **예가체프** | Ethiopia G2 Yirgacheffe Washed | Eth | G2 Washed | |
| 2 | **모모라** | Ethiopia G1 Danse Mormora Natural | Eth | G1 Natural | 구지 지역 |
| 3 | **코케허니** | Ethiopia G1 Yirgacheffe Koke Honey Natural | Eth | G1 Honey | |
| 4 | **우라가** | Ethiopia G1 Guji Uraga Washed | Eth | G1 Washed | |
| 5 | **시다모** | Ethiopia G4 Sidamo Natural | Eth | G4 Natural | |
| 6 | **마사이** | Kenya AA FAQ | K | AA FAQ | |
| 7 | **키린야가** | Kenya PB TOP Kirinyaga | K | PB (Peaberry) | |
| 8 | **후일라** | Colombia Supremo Huila | Co | Supremo | |
| 9 | **안티구아** | Guatemala SHB Antigua | Gu | SHB | |
| 10 | **엘탄케** | Costa Rica El Tanque | Cos | | |
| 11 | **파젠다 카르모** | Brazil Fazenda Carmo Estate Natural | Br | SC16UP | |
| 12 | **산토스** | Brazil NY2 FC Santos | Br | NY2 FC | |
| 13 | **디카페 SDM** | Ethiopia Decaf (SDM) | Eth | Decaf | |
| 14 | **디카페 SM** | Colombia Supremo Popayan Sugarcane Decaf | Co | Decaf (Sugarcane) | |
| 15 | **스위스워터** | Brazil Swiss Water Decaf | Br | Decaf (Swiss Water) | |
| 16 | **게이샤** | Panama Elida Estate Geisha Natural | Pa | Specialty | 고가 품목 |

### 2.2 블렌딩 레시피 (Blending Recipes)
더문의 시그니처 블렌드 생산을 위한 표준 배합비입니다. 모든 블렌드는 **선배합 후로스팅 (Pre-roast Blending)** 방식을 따릅니다.

#### ① 풀문 (Full Moon)
*   **컨셉**: 더문의 대표 하우스 블렌드
*   **기준 손실률**: 각 품목별로 정확한 손실률을 계산하여 적용
*   **배합비**:
    *   마사이 (Kenya): **40%**
    *   안티구아 (Guatemala): **40%**
    *   모모라 (Ethiopia): **10%**
    *   시다모 (Ethiopia): **10%**

#### ② 뉴문 (New Moon)
*   **컨셉**: 대중적인 고소한 맛
*   **기준 손실률**: 각 품목별로 정확한 손실률을 계산하여 적용
*   **배합비**:
    *   산토스 (Brazil): **60%**
    *   후일라 (Colombia): **30%**
    *   시다모 (Ethiopia): **10%**

#### ③ 이클립스문 (Eclipse Moon)
*   **컨셉**: 디카페인 블렌드
*   **기준 손실률**: 각 품목별로 정확한 손실률을 계산하여 적용
*   **배합비**:
    *   디카페 SM (Colombia): **60%**
    *   스위스워터 (Brazil): **40%**

---

## 3. 운영 프로세스 (Operational Processes)

### 3.1 자재 입고 (Inbound)
1.  **문서 접수**: 거래명세서(이미지/PDF) 수취.
2.  **OCR 등록**: 시스템을 통해 품목, 수량, 단가 자동 추출.
3.  **검증 및 확정**: 추출 데이터와 실물 대조 후 입고 확정.
    *   *System Action*: 생두 재고 증가, 평균 매입 단가 갱신.

### 3.2 싱글 오리진 생산 (Single Origin Roasting)
1.  **계획**: 품목(예: 예가체프)과 프로필(예: 신콩) 선택, 목표 생산량 설정.
2.  **투입량 계산**: `목표량 / (1 - 예상손실률)` 공식으로 필요 생두량 산출.
3.  **로스팅**: 프로필에 맞춰 로스팅 수행.
4.  **결과 등록**: 실제 생산된 원두량 입력.
    *   *System Action*:
        *   생두 재고 차감 (투입량)
        *   원두 재고 증가 (생산량, `{품종}-{프로필}` SKU로 입고)
        *   실제 손실률 계산 및 이력 저장
        *   생산 원가 산출 (`투입 생두 비용 / 생산량`)

### 3.3 블렌드 생산 (Blending)
1.  **계획**: 블렌드 제품(예: 풀문) 선택, 목표 생산량 설정.
2.  **배합 계산**: 레시피 비율에 따라 각 생두별 필요량 자동 산출.
3.  **배합 및 로스팅**: 생두 계량 및 혼합 후 로스팅 수행.
4.  **결과 등록**: 실제 생산된 블렌드 원두량 입력.
    *   *System Action*:
        *   각 생두 재고 차감 (레시피 비율대로)
        *   블렌드 원두 재고 증가
        *   통합 손실률 계산
        *   가중 평균 원가 산출

---

## 4. 데이터 분석 (Data Analysis)

### 4.1 입고 데이터 요약 (Inbound Summary)
확보된 11건의 명세서 데이터를 기반으로 한 분석입니다.

*   **총 입고 기간**: 2024.12.24 ~ 2025.10.29 (약 10개월)
*   **주요 공급자**: 지에스씨인터내셔날(주), 아실로(온라인)

### 4.2 주요 품목별 단가 변동 추이
| 품목 | 최저가 (시기) | 최고가 (시기) | 변동률 | 비고 |
| :-- | :-- | :-- | :-- | :-- |
| **브라질 (NY2)** | 9,900원 ('24.12) | 13,100원 ('25.03) | ▲32% | 큰 폭 상승 |
| **콜롬비아 후일라** | 10,400원 ('24.12) | 14,500원 ('25.10) | ▲39% | 지속 상승세 |
| **예가체프 G2** | 11,600원 ('24.12) | 14,000원 ('25.10) | ▲20% | |
| **모모라 G1** | 18,500원 ('25.03) | 21,750원 ('25.08) | ▲17% | |

### 4.3 상세 입고 이력 (Reference)
**[중요]** 시스템 초기 데이터 구축 및 정밀 분석을 위한 **모든 상세 명세서 데이터**는 별도의 문서에 원본 그대로 보존되어 있습니다. 아래 링크를 참조하십시오.

👉 **[상세 입고 이력 보기 (Themoon_Inbound_History.md)](./Themoon_Inbound_History.md)**

*(본 문서에서는 주요 이력만 요약 관리합니다)*

*   **2025.10.29**: 콜롬비아, 디카페인 등 120kg (184.5만원)
*   **2025.09.26**: 스페셜티(우라가, 코케허니) 위주 140kg (305.8만원)
*   **2025.05.27**: 파나마 게이샤(24.9만원/kg) 포함 161kg (279.7만원)
*   **2024.12.24**: 브라질/콜롬비아 저점 대량 매수 200kg (254.2만원)

---

## 5. 시스템 요구사항 (System Requirements)

### 5.1 핵심 기능
1.  **로스팅 프로필 관리**: 품종별 신콩/탄콩 프로필 정의 및 생산 이력 관리.
# 더문(The Moon) 로스팅 및 재고 관리 운영 계획안 v2.0

## 1. 개요 (Overview)
본 문서는 '더문(The Moon)'의 효율적인 로스팅 생산 관리 및 재고 운영을 위한 기준 정보와 업무 시나리오를 정의합니다. 원두의 입고부터 로스팅, 블렌딩, 그리고 최종 제품 생산에 이르는 프로세스를 체계화하여 데이터 기반의 운영을 목표로 합니다.

### 1.1 용어 및 관리 기준 (Terminology & Standards)

**1. 재료 및 제품 분류**
*   **생두 (Green Bean)**: 로스팅 전의 원재료. 품종별로 관리합니다.
*   **원두 (Roasted Bean)**: 로스팅이 완료된 제품.
    *   **싱글 오리진 (Single Origin)**: 한 종류의 생두를 로스팅한 것. **로스팅 프로필(신콩/탄콩)**에 따라 별도 품목으로 관리됩니다.
    *   **블렌드 (Blend)**: 여러 생두를 배합하여 로스팅한 것.

**2. 로스팅 프로필 (Roasting Profile)**
싱글 오리진 원두는 로스팅 포인트에 따라 두 가지로 구분하여 생산 및 관리합니다.
*   **신콩 (Light/Medium Roast)**: 산미와 향미를 강조한 약~중볶음.
*   **탄콩 (Dark Roast)**: 바디감과 쓴맛을 강조한 강볶음.

**3. 재고 관리 단위 (SKU Logic)**
*   **생두**: `{품종명}` (예: 예가체프)
*   **싱글 원두**: `{품종명}-{프로필}` (예: 예가체프-신콩, 예가체프-탄콩)
*   **블렌드 원두**: `{블렌드명}` (예: 풀문, 뉴문)

---

## 2. 기준 정보 (Master Data)

### 2.1 생두 및 원두 마스터 (Bean Master List)
취급하는 모든 생두와 이를 가공한 원두의 표준 목록입니다.

| No | 표준 한글명 | 영문 표기 (명세서 기준) | 국가 | 등급/특이사항 | 비고 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | **예가체프** | Ethiopia G2 Yirgacheffe Washed | Eth | G2 Washed | |
| 2 | **모모라** | Ethiopia G1 Danse Mormora Natural | Eth | G1 Natural | 구지 지역 |
| 3 | **코케허니** | Ethiopia G1 Yirgacheffe Koke Honey Natural | Eth | G1 Honey | |
| 4 | **우라가** | Ethiopia G1 Guji Uraga Washed | Eth | G1 Washed | |
| 5 | **시다모** | Ethiopia G4 Sidamo Natural | Eth | G4 Natural | |
| 6 | **마사이** | Kenya AA FAQ | K | AA FAQ | |
| 7 | **키린야가** | Kenya PB TOP Kirinyaga | K | PB (Peaberry) | |
| 8 | **후일라** | Colombia Supremo Huila | Co | Supremo | |
| 9 | **안티구아** | Guatemala SHB Antigua | Gu | SHB | |
| 10 | **엘탄케** | Costa Rica El Tanque | Cos | | |
| 11 | **파젠다 카르모** | Brazil Fazenda Carmo Estate Natural | Br | SC16UP | |
| 12 | **산토스** | Brazil NY2 FC Santos | Br | NY2 FC | |
| 13 | **디카페 SDM** | Ethiopia Decaf (SDM) | Eth | Decaf | |
| 14 | **디카페 SM** | Colombia Supremo Popayan Sugarcane Decaf | Co | Decaf (Sugarcane) | |
| 15 | **스위스워터** | Brazil Swiss Water Decaf | Br | Decaf (Swiss Water) | |
| 16 | **게이샤** | Panama Elida Estate Geisha Natural | Pa | Specialty | 고가 품목 |

### 2.2 블렌딩 레시피 (Blending Recipes)
더문의 시그니처 블렌드 생산을 위한 표준 배합비입니다. 모든 블렌드는 **선배합 후로스팅 (Pre-roast Blending)** 방식을 따릅니다.

#### ① 풀문 (Full Moon)
*   **컨셉**: 더문의 대표 하우스 블렌드
*   **기준 손실률**: 각 품목별로 정확한 손실률을 계산하여 적용
*   **배합비**:
    *   마사이 (Kenya): **40%**
    *   안티구아 (Guatemala): **40%**
    *   모모라 (Ethiopia): **10%**
    *   시다모 (Ethiopia): **10%**

#### ② 뉴문 (New Moon)
*   **컨셉**: 대중적인 고소한 맛
*   **기준 손실률**: 각 품목별로 정확한 손실률을 계산하여 적용
*   **배합비**:
    *   산토스 (Brazil): **60%**
    *   후일라 (Colombia): **30%**
    *   시다모 (Ethiopia): **10%**

#### ③ 이클립스문 (Eclipse Moon)
*   **컨셉**: 디카페인 블렌드
*   **기준 손실률**: 각 품목별로 정확한 손실률을 계산하여 적용
*   **배합비**:
    *   디카페 SM (Colombia): **60%**
    *   스위스워터 (Brazil): **40%**

---

## 3. 운영 프로세스 (Operational Processes)

### 3.1 자재 입고 (Inbound)
1.  **문서 접수**: 거래명세서(이미지/PDF) 수취.
2.  **OCR 등록**: 시스템을 통해 품목, 수량, 단가 자동 추출.
3.  **검증 및 확정**: 추출 데이터와 실물 대조 후 입고 확정.
    *   *System Action*: 생두 재고 증가, 평균 매입 단가 갱신.

### 3.2 싱글 오리진 생산 (Single Origin Roasting)
1.  **계획**: 품목(예: 예가체프)과 프로필(예: 신콩) 선택, 목표 생산량 설정.
2.  **투입량 계산**: `목표량 / (1 - 예상손실률)` 공식으로 필요 생두량 산출.
3.  **로스팅**: 프로필에 맞춰 로스팅 수행.
4.  **결과 등록**: 실제 생산된 원두량 입력.
    *   *System Action*:
        *   생두 재고 차감 (투입량)
        *   원두 재고 증가 (생산량, `{품종}-{프로필}` SKU로 입고)
        *   실제 손실률 계산 및 이력 저장
        *   생산 원가 산출 (`투입 생두 비용 / 생산량`)

### 3.3 블렌드 생산 (Blending)
1.  **계획**: 블렌드 제품(예: 풀문) 선택, 목표 생산량 설정.
2.  **배합 계산**: 레시피 비율에 따라 각 생두별 필요량 자동 산출.
3.  **배합 및 로스팅**: 생두 계량 및 혼합 후 로스팅 수행.
4.  **결과 등록**: 실제 생산된 블렌드 원두량 입력.
    *   *System Action*:
        *   각 생두 재고 차감 (레시피 비율대로)
        *   블렌드 원두 재고 증가
        *   통합 손실률 계산
        *   가중 평균 원가 산출

---

## 4. 데이터 분석 (Data Analysis)

### 4.1 입고 데이터 요약 (Inbound Summary)
확보된 11건의 명세서 데이터를 기반으로 한 분석입니다.

*   **총 입고 기간**: 2024.12.24 ~ 2025.10.29 (약 10개월)
*   **주요 공급자**: 지에스씨인터내셔날(주), 아실로(온라인)

### 4.2 주요 품목별 단가 변동 추이
| 품목 | 최저가 (시기) | 최고가 (시기) | 변동률 | 비고 |
| :-- | :-- | :-- | :-- | :-- |
| **브라질 (NY2)** | 9,900원 ('24.12) | 13,100원 ('25.03) | ▲32% | 큰 폭 상승 |
| **콜롬비아 후일라** | 10,400원 ('24.12) | 14,500원 ('25.10) | ▲39% | 지속 상승세 |
| **예가체프 G2** | 11,600원 ('24.12) | 14,000원 ('25.10) | ▲20% | |
| **모모라 G1** | 18,500원 ('25.03) | 21,750원 ('25.08) | ▲17% | |

### 4.3 상세 입고 이력 (Reference)
**[중요]** 시스템 초기 데이터 구축 및 정밀 분석을 위한 **모든 상세 명세서 데이터**는 별도의 문서에 원본 그대로 보존되어 있습니다. 아래 링크를 참조하십시오.

👉 **[상세 입고 이력 보기 (Themoon_Inbound_History.md)](./Themoon_Inbound_History.md)**

*(본 문서에서는 주요 이력만 요약 관리합니다)*

*   **2025.10.29**: 콜롬비아, 디카페인 등 120kg (184.5만원)
*   **2025.09.26**: 스페셜티(우라가, 코케허니) 위주 140kg (305.8만원)
*   **2025.05.27**: 파나마 게이샤(24.9만원/kg) 포함 161kg (279.7만원)
*   **2024.12.24**: 브라질/콜롬비아 저점 대량 매수 200kg (254.2만원)

---

## 5. 시스템 요구사항 (System Requirements)

### 5.1 핵심 기능
1.  **로스팅 프로필 관리**: 품종별 신콩/탄콩 프로필 정의 및 생산 이력 관리.
2.  **손실률 자동 학습**: 로스팅 회차별 손실률을 누적하여, 다음 생산 계획 시 예상 손실률의 정확도 향상.
3.  **원가 대시보드**: 생두 단가 변동에 따른 원두/블렌드 원가 변화 추이 시각화.

### 5.2 확장 기능 (Roadmap)
1.  **자동 발주 추천**: 안전 재고 도달 시, 최근 소비 속도와 리드 타임을 고려한 발주량 추천.
2.  **컵핑 노트 연동**: 로스팅 결과물에 대한 품질 평가(Cupping Note) 기록 기능.
31.  **QR/바코드 관리**: 입고된 생두 포대 및 생산된 원두 봉투에 QR코드를 부착하여 재고 추적 자동화.

---

## 6. 상세 프로그램 개발 계획 (Detailed Program Development Plan)

본 계획은 `Themoon_Rostings.md`의 심층 분석을 바탕으로, 실제 운영 시나리오와 비즈니스 로직을 시스템에 완벽하게 구현하기 위한 구체적인 로드맵입니다.

### 6.1 기술 스택 (Tech Stack)
*   **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide React, Recharts (차트)
*   **Backend**: FastAPI (Python 3.10+), Pydantic, SQLAlchemy
*   **Database**: SQLite (Development), PostgreSQL (Production planned)
*   **AI Integration**: Google Gemini API (OCR for Inbound, Image Generation for Assets)

### 6.2 데이터 모델 및 SKU 전략 (Data Model & SKU Strategy)
시스템의 핵심인 '재고 관리'를 위해 다음과 같은 SKU(Stock Keeping Unit) 체계를 DB와 로직에 반영합니다.

1.  **생두 (Green Bean)**: `Bean` 테이블 (type='GREEN_BEAN')
    *   관리 단위: **품종** (예: 예가체프)
    *   주요 속성: 매입단가(avg_price), 재고량(quantity_kg)
2.  **싱글 오리진 원두 (Single Origin)**: `Bean` 테이블 (type='ROASTED_BEAN')
    *   관리 단위: **품종 + 로스팅 프로필** (예: 예가체프-신콩, 예가체프-탄콩)
    *   주요 속성: 생산원가(cost_price), 로스팅 포인트(roast_point), 재고량
    *   *Note*: 동일 품종이라도 프로필이 다르면 별도 SKU로 관리됨.
3.  **블렌드 원두 (Blend)**: `Blend` 테이블 (또는 `Bean` 테이블 통합 고려)
    *   관리 단위: **블렌드명** (예: 풀문)
    *   주요 속성: 표준 레시피(recipe), 가중평균원가, 재고량

### 6.3 단계별 개발 로드맵 (Phased Development Roadmap)

#### Phase 1: 기초 구축 (Foundation) - ✅ 완료
*   [x] **프로젝트 구조**: Frontend(Next.js) / Backend(FastAPI) 환경 설정
*   [x] **기본 DB 설계**: Beans, Blends, InventoryLogs 테이블 생성
*   [x] **UI 테마**: "Artistic Latte Art" 테마 적용

#### Phase 2: 데이터 모델 고도화 (Data Model Refinement) - 🚨 긴급 (Current Priority)
*   **목표**: 생두와 원두의 명확한 구분 및 SKU 체계 확립
*   [ ] **DB 스키마 변경 (`models/bean.py`)**:
    *   `type`: Enum ('GREEN_BEAN', 'ROASTED_BEAN') 추가
    *   `roast_profile`: Enum ('LIGHT', 'MEDIUM', 'DARK') 추가 (원두 전용)
    *   `parent_bean_id`: ForeignKey (원두가 어떤 생두에서 왔는지 추적)
    *   `cost_price`: 생산 원가 (매입가와 구분)
*   [ ] **API 및 UI 수정**:
    *   원두 등록 화면: "생두 등록" vs "원두 등록" 탭 분리
    *   재고 현황: 생두 재고와 원두 재고 탭 분리 표시

#### Phase 3: 핵심 비즈니스 로직 구현 (Business Logic Implementation) - 📅 예정
`Themoon_Rostings.md`의 운영 시나리오를 코드로 구현합니다.

*   **3-1. 자재 입고 (Inbound)**
    *   [ ] **기능**: 거래명세서 기반 생두 재고 추가
    *   [ ] **로직**: `기존 재고 * 기존 단가 + 신규 입고 * 신규 단가 / 총 재고` (이동평균법 단가 갱신)
    *   [ ] **OCR 연동**: Gemini API로 명세서 스캔 -> 품목/수량/단가 자동 추출

*   **3-2. 싱글 오리진 로스팅 (Single Origin Roasting)**
    *   [ ] **UI**: 생두 선택 -> 프로필(신콩/탄콩) 선택 -> 목표 생산량 입력
    *   [ ] **투입량 계산 로직**: `필요 생두량 = 목표 생산량 / (1 - 예상 손실률)`
    *   [ ] **생산 처리 로직**:
        1.  생두 재고 차감 (`-필요 생두량`)
        2.  원두 재고 증가 (`+목표 생산량`, SKU: `{품종}-{프로필}`)
        3.  손실률 기록 및 원가 계산 (`투입 생두 비용 / 생산량`)

*   **3-3. 블렌딩 생산 (Pre-roast Blending)**
    *   [ ] **UI**: 블렌드 레시피 선택 -> 목표 생산량 입력
    *   [ ] **배합 계산 로직**:
        1.  `총 필요 생두량 = 목표 생산량 / (1 - 블렌드 예상 손실률)`
        2.  `각 생두 필요량 = 총 필요 생두량 * 레시피 비율`
    *   [ ] **생산 처리 로직**:
        1.  구성 생두 재고 일괄 차감
        2.  블렌드 원두 재고 증가
        3.  가중 평균 원가 산출

#### Phase 4: 분석 및 고도화 (Analytics & Advanced)
*   [ ] **손실률 학습**: 로스팅 이력이 쌓일수록 예상 손실률의 정확도 보정
*   [ ] **대시보드**: 원두별 마진율, 재고 회전율 시각화
*   [ ] **모바일 최적화**: 현장에서 태블릿으로 로스팅 기록 가능하도록 UI 개선

### 6.4 디렉토리 구조 (Directory Structure)
```
TheMoon/
├── backend/
│   ├── app/
│   │   ├── models/     # bean.py (type, profile 추가), inventory_log.py
│   │   ├── schemas/    # Pydantic (GreenBean, RoastedBean 분리)
│   │   ├── services/   # roasting_service.py (핵심 비즈니스 로직)
│   │   └── api/        # v1/roasting (생산 관련 엔드포인트 신설)
├── frontend/
│   ├── app/
│   │   ├── inventory/  # 생두/원두 탭 분리 구현
│   │   └── roasting/   # 로스팅/블렌딩 작업 전용 페이지 신설
│   └── components/
│       └── roasting/   # Calculator, ProfileSelector 등
```
