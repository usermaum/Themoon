### 1. beans (생두,)

**목적**: 생두, 원두, 블렌드 원두를 하나의 테이블에서 통합 관리

| 컬럼명 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| `id` | INTEGER | PK, NOT NULL | Primary Key |
| `name` | VARCHAR(100) | NOT NULL | 품목명 |
| `type` | VARCHAR(12) | NOT NULL | 품목 유형 (GREEN_BEAN/ROASTED_BEAN/BLEND_BEAN) |
| `sku` | VARCHAR(100) | NULL | SKU 코드 |
| `name_ko` | VARCHAR(100) | NULL | 품목명 (한글) |
| `name_en` | VARCHAR(200) | NULL | 품목명 (영문) |
| `origin` | VARCHAR(100) | NULL | 원산지 |
| `origin_ko` | VARCHAR(50) | NULL | 원산지 (한글) |
| `origin_en` | VARCHAR(50) | NULL | 원산지 (영문) |
| `variety` | VARCHAR(50) | NULL |  |
| `grade` | VARCHAR(50) | NULL |  |
| `processing_method` | VARCHAR(50) | NULL |  |
| `roast_profile` | VARCHAR(6) | NULL |  |
| `parent_bean_id` | INTEGER | NULL |  |
| `quantity_kg` | FLOAT | NOT NULL | 현재 재고량 (kg) |
| `avg_price` | FLOAT | NOT NULL | 평균 단가 |
| `purchase_price_per_kg` | FLOAT | NULL |  |
| `cost_price` | FLOAT | NULL |  |
| `description` | TEXT | NULL |  |
| `notes` | TEXT | NULL | 비고 / 메모 |
| `expected_loss_rate` | FLOAT | NOT NULL |  |
| `created_at` | DATETIME | NULL | 생성일시 |
| `updated_at` | DATETIME | NULL | 수정일시 |

**Foreign Keys**:
- `parent_bean_id` → `beans.id`

---

### 2. suppliers (공급처)

**목적**: 공급처 관리

| 컬럼명 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| `id` | INTEGER | PK, NOT NULL | Primary Key |
| `name` | VARCHAR | NOT NULL | 품목명 |
| `representative_name` | VARCHAR | NULL |  |
| `contact_phone` | VARCHAR | NULL |  |
| `contact_email` | VARCHAR | NULL |  |
| `address` | VARCHAR | NULL |  |
| `registration_number` | VARCHAR | NULL |  |

---

### 3. blends (커피)

**목적**: 커피 블렌드 레시피 저장

| 컬럼명 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| `id` | INTEGER | PK, NOT NULL | Primary Key |
| `name` | VARCHAR(200) | NOT NULL | 품목명 |
| `description` | TEXT | NULL |  |
| `recipe` | JSON | NOT NULL |  |
| `target_roast_level` | VARCHAR(50) | NULL |  |
| `notes` | TEXT | NULL | 비고 / 메모 |
| `created_at` | DATETIME | NULL, DEFAULT CURRENT_TIMESTAMP | 생성일시 |
| `updated_at` | DATETIME | NULL | 수정일시 |

---

### 4. inbound_documents (입고)

**목적**: 입고 내역서 메인 정보 (OCR 결과)

| 컬럼명 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| `id` | INTEGER | PK, NOT NULL | Primary Key |
| `contract_number` | VARCHAR | NULL | 계약 번호 |
| `supplier_name` | VARCHAR | NULL | 공급처명 |
| `supplier_id` | INTEGER | NULL |  |
| `receiver_name` | VARCHAR | NULL |  |
| `invoice_date` | VARCHAR | NULL |  |
| `total_amount` | FLOAT | NULL | 총 금액 |
| `image_url` | VARCHAR | NULL | 원본 이미지 URL |
| `drive_file_id` | VARCHAR | NULL |  |
| `notes` | TEXT | NULL | 비고 / 메모 |
| `created_at` | DATETIME | NULL | 생성일시 |

**Foreign Keys**:
- `supplier_id` → `suppliers.id`

---

### 5. inbound_document_details (입고)

**목적**: 입고 내역서 상세 정보 (공급자, 금액 등)

| 컬럼명 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| `id` | INTEGER | PK, NOT NULL | Primary Key |
| `inbound_document_id` | INTEGER | NOT NULL |  |
| `document_number` | VARCHAR | NULL |  |
| `issue_date` | VARCHAR | NULL |  |
| `delivery_date` | VARCHAR | NULL |  |
| `payment_due_date` | VARCHAR | NULL |  |
| `invoice_type` | VARCHAR | NULL |  |
| `supplier_business_number` | VARCHAR | NULL |  |
| `supplier_address` | TEXT | NULL |  |
| `supplier_phone` | VARCHAR | NULL |  |
| `supplier_fax` | VARCHAR | NULL |  |
| `supplier_email` | VARCHAR | NULL |  |
| `supplier_representative` | VARCHAR | NULL |  |
| `supplier_contact_person` | VARCHAR | NULL |  |
| `supplier_contact_phone` | VARCHAR | NULL |  |
| `subtotal` | FLOAT | NULL |  |
| `tax_amount` | FLOAT | NULL |  |
| `grand_total` | FLOAT | NULL |  |
| `currency` | VARCHAR | NULL |  |
| `payment_terms` | TEXT | NULL |  |
| `shipping_method` | VARCHAR | NULL |  |
| `notes` | TEXT | NULL | 비고 / 메모 |
| `remarks` | TEXT | NULL |  |
| `created_at` | DATETIME | NULL | 생성일시 |
| `updated_at` | DATETIME | NULL | 수정일시 |

**Foreign Keys**:
- `inbound_document_id` → `inbound_documents.id`

---

### 6. inbound_receivers (입고)

**목적**: 입고 내역서 공급받는자 정보

| 컬럼명 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| `id` | INTEGER | PK, NOT NULL | Primary Key |
| `inbound_document_id` | INTEGER | NOT NULL |  |
| `name` | VARCHAR | NULL | 품목명 |
| `business_number` | VARCHAR | NULL |  |
| `address` | TEXT | NULL |  |
| `phone` | VARCHAR | NULL |  |
| `contact_person` | VARCHAR | NULL |  |
| `created_at` | DATETIME | NULL | 생성일시 |
| `updated_at` | DATETIME | NULL | 수정일시 |

**Foreign Keys**:
- `inbound_document_id` → `inbound_documents.id`

---

### 7. inbound_items (입고)

**목적**: 입고 내역서 품목 상세

| 컬럼명 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| `id` | INTEGER | PK, NOT NULL | Primary Key |
| `inbound_document_id` | INTEGER | NOT NULL |  |
| `item_order` | INTEGER | NOT NULL |  |
| `bean_name` | VARCHAR | NULL |  |
| `specification` | VARCHAR | NULL |  |
| `unit` | VARCHAR | NULL |  |
| `quantity` | FLOAT | NULL |  |
| `origin` | VARCHAR | NULL | 원산지 |
| `unit_price` | FLOAT | NULL |  |
| `supply_amount` | FLOAT | NULL |  |
| `tax_amount` | FLOAT | NULL |  |
| `notes` | TEXT | NULL | 비고 / 메모 |
| `created_at` | DATETIME | NULL | 생성일시 |
| `updated_at` | DATETIME | NULL | 수정일시 |

**Foreign Keys**:
- `inbound_document_id` → `inbound_documents.id`

---

### 8. inventory_logs (모든)

**목적**: 모든 재고 변동 추적 (감사 로그)

| 컬럼명 | 타입 | 제약 | 설명 |
| --- | --- | --- | --- |
| `id` | INTEGER | PK, NOT NULL | Primary Key |
| `bean_id` | INTEGER | NOT NULL |  |
| `change_type` | VARCHAR(15) | NOT NULL |  |
| `change_amount` | FLOAT | NOT NULL |  |
| `current_quantity` | FLOAT | NOT NULL |  |
| `notes` | TEXT | NULL | 비고 / 메모 |
| `related_id` | INTEGER | NULL |  |
| `created_at` | DATETIME | NULL | 생성일시 |
| `inbound_document_id` | INTEGER | NULL |  |

**Foreign Keys**:
- `inbound_document_id` → `inbound_documents.id`
- `bean_id` → `beans.id`

---
