# Inbound System Upgrade & Data Integrity Plan
> **Document Status**: Draft
> **Target Version**: 0.2.0
> **Related Feature**: Inbound OCR & Inventory Management

---

## 1. 개요 (Overview)

본 문서는 '자재 입고(Inbound)' 시스템의 데이터 무결성을 보장하고, 실제 비즈니스 현장에서의 활용도를 극대화하기 위한 시스템 고도화 계획입니다.
단순한 입고 기록을 넘어, **계약 기반의 중복 방지**와 **공급사/담당자 관리**를 포함한 전문적인 자재 수급 시스템으로 발전시키는 것을 목표로 합니다.

## 2. 핵심 개선 사항 (Key Improvements)

### 2.1 중복 입고 방지 매커니즘 (Robust Duplicate Detection)

기존의 단순 값 비교 방식을 폐기하고, **계약 번호(Contract Number)**를 고유 식별자(Unique Key)로 하는 2단계 검증 로직을 도입합니다.

#### [Algorithm] 입고 중복 검사 로직

1.  **1차 검증 (Primary Check) - 절대 기준**
    *   **기준**: `contract_number` (계약/주문 번호)
    *   대부분의 정식 거래 명세서에는 고유한 문서 번호가 존재합니다.
    *   **Logic**:
        ```sql
        SELECT id FROM inbound_documents WHERE contract_number = :extracted_contract_number AND contract_number IS NOT NULL;
        ```
    *   **결과**: 매칭되는 레코드가 존재하면 **즉시 입고 차단** 및 '이미 등록된 명세서' 경고창 출력.

2.  **2차 검증 (Secondary Check) - 보조 기준**
    *   **기준**: `contract_number`가 없는 간이 영수증이나 손상된 문서일 경우.
    *   **Composite Key**: `supplier_name` + `invoice_date` + `total_amount`
    *   **Logic**:
        *   위 3가지 항목이 모두 100% 일치하는 과거 내역이 있는 경우.
    *   **결과**: '중복 의심' 경고 출력 후, 사용자에게 **강제 진행 여부**를 묻습니다 (동일 금액의 재주문일 수 있으므로).

---

### 2.2 데이터 스키마 확장 (Schema Expansion)

현업에서 필요한 '소통(Communication)'과 '추적(Tracking)'이 가능하도록 데이터 구조를 확장합니다.

#### [Table] `inbound_documents`
기존 테이블에 다음 컬럼들을 추가(Add Columns)합니다.

| 필드명 (Column) | 데이터 타입 | 설명 (Description) | 필수 여부 |
| :-- | :-- | :-- | :-- |
| **contract_number** | `VARCHAR(100)` | **계약/주문/견적 번호** (Unique Index 권장) | ⭐ Critical |
| **receiver_name** | `VARCHAR(100)` | 공급 받는 자 (법인명/지점명) | Optional |
| **supplier_phone** | `VARCHAR(50)` | 공급처 대표 전화 또는 담당자 직통 | Optional |
| **supplier_email** | `VARCHAR(100)` | 공급처 이메일 (계산서 발행란 등) | Optional |
| **supplier_rep_name** | `VARCHAR(50)` | 공급처 담당자명 (영업 사원 등) | Optional |
### 2.2 공급처 마스터 분리 (Supplier Master Data Normalization)

사용자 요청에 따라 **즉시 3차 정규화를 적용**하여 공급처 정보를 체계적으로 관리합니다.

#### [New Table] `suppliers`
공급처 정보를 관리하는 전용 테이블을 생성합니다.

| 필드명 (Column) | 데이터 타입 | 설명 (Description) | 필수 여부 |
| :-- | :-- | :-- | :-- |
| **id** | `Integer` | Primary Key | PK |
| **name** | `String(100)` | 공급처명 (Unique) | ⭐ Critical |
| **representative_name** | `String(50)` | 대표자명 | Optional |
| **contact_phone** | `String(50)` | 대표/담당자 연락처 | Optional |
| **contact_email** | `String(100)` | 이메일 | Optional |
| **address** | `String(200)` | 사업장 주소 | Optional |
| **registration_number** | `String(50)` | 사업자 등록 번호 | Optional |

#### [Modified Table] `inbound_documents`
기존의 텍스트 필드를 Foreign Key로 교체하거나 연결합니다.

| 필드명 (Column) | 변경 사항 |
| :-- | :-- |
| **contract_number** | **[NEW]** 계약/주문 번호 (Unique, 중복 체크용) |
| **supplier_id** | **[NEW]** `suppliers.id` 참조 (Foreign Key) |
| `supplier_name` | **[KEEP]** OCR 원본 데이터 보존용 (Snapshot) |
| **receiver_name** | **[NEW]** 공급 받는 자 |

> **Process**:
> 1. OCR이 공급처명 인식
> 2. DB `suppliers` 테이블에서 이름 검색
> 3. **Exist**: 기존 ID 연결
> 4. **New**: 새로운 Supplier 레코드 자동 생성 후 ID 연결 (또는 사용자 선택)

---

### 2.3 AI(OCR) 분석 역량 강화 (Prompt Engineering)

Gemini 1.5 Flash 모델에게 전달하는 프롬프트를 고도화하여 정밀한 정보를 추출합니다.

**[New Prompt Strategy]**
*   **Role**: "You are a professional Data Entry Specialist."
*   **Task**: "Extract specific business details from the invoice."
*   **Target Fields**:
    *   `contract_number`: Look for "No.", "Order No", "견적 번호", "문서 번호"
    *   `contact_info`: Look for "Tel", "Fax", "Phone", "Mobile", "H.P"
    *   `email`: Look for "@" pattern in header/footer area.
*   **Noise Filtering**: 사업자 등록 번호와 일반 전화번호를 구분하도록 지시.

---

## 3. 구현 로드맵 (Implementation Roadmap)

### Phase 1: 기반 마련 (Backend & DB)
1.  **DB Migration**: `inbound_documents` 테이블에 위 2.2의 컬럼 추가 스크립트 작성 및 실행.
2.  **Backend Logic**: `InboundConfirmRequest` 스키마 업데이트 및 중복 체크 로직 (`check_duplicate_inbound`) 구현.

### Phase 2: 지능 강화 (AI Service)
1.  **Prompt Upgrade**: `ocr_service.py`의 프롬프트를 수정하여 확장된 데이터를 JSON으로 반환받도록 변경.
2.  **Parsing Logic**: 반환된 JSON을 새로운 Pydantic 모델에 매핑.

### Phase 3: 사용자 경험 (Frontend UI)
1.  **Form Expansion**: 입고 확정 화면에 `계약 번호`, `담당자`, `연락처` 입력 필드 추가 (OCR 결과 자동 채움).
2.  **Duplicate Warning**: 저장 클릭 시 중복 발생하면 팝업(Alert)으로 차단 또는 안내.

## 4. 기대 효과 (Expected Outcomes)

1.  **무결성**: 중복 입고로 인한 재고 뻥튀기(Inflation) 사고 원천 차단.
2.  **편의성**: 명세서를 보고 일일이 연락처를 찾을 필요 없이, 시스템 내에서 바로 확인/연락 가능.
3.  **확장성**: 추후 '발주 관리(Ordering)' 시스템 도입 시 공급처 데이터베이스의 기초 자료로 활용.

---
**작성자**: AntiGravity Agent
**작성일**: 2025-12-16
