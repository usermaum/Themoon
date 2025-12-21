# 🗄️ TheMoon 데이터베이스 스키마 (Database Schema)

> **작성일**: 2025-12-07
> **버전**: 0.0.6
> **DBMS**: PostgreSQL 15+ (Production), SQLite 3 (Development)

---

## 📋 목차

1. [ER Diagram](#er-diagram)
2. [테이블 상세](#테이블-상세)
3. [인덱스 전략](#인덱스-전략)
4. [데이터 무결성 규칙](#데이터-무결성-규칙)

---

## ER Diagram
 
```mermaid
erDiagram
    %% Relationships
    beans ||--o{ beans : "parent_bean_id"
    beans ||--o{ inventory_logs : "has_history"
    suppliers ||--o{ inbound_documents : "issues"
    inbound_documents ||--o{ inventory_logs : "triggers"
    inbound_documents ||--|| inbound_document_details : "has_details"
    inbound_documents ||--|| inbound_receivers : "has_receiver"
    inbound_documents ||--o{ inbound_items : "contains"
```

---

## 테이블 상세

### 1. beans (원두 통합 테이블)

**목적**: 생두, 원두, 블렌드 원두를 하나의 테이블에서 통합 관리

| 컬럼명                  | 타입         | 제약                    | 설명                                           |
| ----------------------- | ------------ | ----------------------- | ---------------------------------------------- |
| `id`                    | INTEGER      | PK, AUTO_INCREMENT      | 원두 ID                                        |
| `name`                  | VARCHAR(100) | NOT NULL                | 품목명 (예: 예가체프, 풀문)                    |
| `type`                  | VARCHAR(12)  | NOT NULL                | 품목 유형 (GREEN_BEAN/ROASTED_BEAN/BLEND_BEAN) |
| `sku`                   | VARCHAR(100) | UNIQUE                  | SKU 코드 (예: ETH-예가체프)                    |
| `name_ko`               | VARCHAR(100) | NULL                    | 품목명 (한글)                                  |
| `name_en`               | VARCHAR(200) | NULL                    | 품목명 (영문)                                  |
| `origin`                | VARCHAR(100) | NULL                    | 원산지 (생두용, 예: Ethiopia)                  |
| `origin_ko`             | VARCHAR(50)  | NULL                    | 원산지 (한글)                                  |
| `origin_en`             | VARCHAR(50)  | NULL                    | 원산지 (영문)                                  |
| `variety`               | VARCHAR(50)  | NULL                    | 품종 (예: Yirgacheffe)                         |
| `grade`                 | VARCHAR(50)  | NULL                    | 등급 (예: G2 Washed)                           |
| `processing_method`     | VARCHAR(50)  | NULL                    | 가공 방식 (Washed/Natural/Honey)               |
| `roast_profile`         | VARCHAR(6)   | NULL                    | 로스팅 프로필 (LIGHT/MEDIUM/DARK)              |
| `parent_bean_id`        | INTEGER      | FK → beans.id           | 원재료 생두 ID (원두인 경우)                   |
| `quantity_kg`           | FLOAT        | NOT NULL                | 현재 재고량 (kg)                               |
| `avg_price`             | FLOAT        | NOT NULL                | kg당 평균 단가 (원)                            |
| `purchase_price_per_kg` | FLOAT        | NULL                    | 최근 매입가 (참조용)                           |
| `cost_price`            | FLOAT        | NULL                    | 생산 원가 (로스팅 비용 포함)                   |
| `description`           | TEXT         | NULL                    | 설명                                           |
| `notes`                 | TEXT         | NULL                    | 내부 메모                                      |
| `expected_loss_rate`    | FLOAT        | NOT NULL                | 예상 로스팅 손실률 (0.15 = 15%)                |
| `created_at`            | DATETIME     | NOT NULL, DEFAULT NOW() | 생성일시                                       |
| `updated_at`            | DATETIME     | NULL                    | 수정일시                                       |

**Enum 값**:
- `type`: `'GREEN_BEAN'`, `'ROASTED_BEAN'`, `'BLEND_BEAN'`
- `roast_profile`: `'LIGHT'`, `'MEDIUM'`, `'DARK'`

**Self-Referential Relationship**:
```sql
parent_bean_id → beans.id
-- 원두(ROASTED_BEAN) → 생두(GREEN_BEAN) 참조
```

---

### 2. suppliers (공급처)

**목적**: 원두 및 자재 공급처 관리

| 컬럼명                | 타입    | 제약               | 설명           |
| --------------------- | ------- | ------------------ | -------------- |
| `id`                  | INTEGER | PK, AUTO_INCREMENT | 공급처 ID      |
| `name`                | VARCHAR | NOT NULL           | 공급처명       |
| `representative_name` | VARCHAR | NULL               | 대표자명       |
| `contact_phone`       | VARCHAR | NULL               | 연락처         |
| `contact_email`       | VARCHAR | NULL               | 이메일         |
| `address`             | VARCHAR | NULL               | 주소           |
| `registration_number` | VARCHAR | NULL               | 사업자등록번호 |

---

### 3. blends (블렌드 레시피)

**목적**: 커피 블렌드 레시피 저장

| 컬럼명               | 타입         | 제약                    | 설명                     |
| -------------------- | ------------ | ----------------------- | ------------------------ |
| `id`                 | INTEGER      | PK, AUTO_INCREMENT      | 블렌드 ID                |
| `name`               | VARCHAR(200) | NOT NULL                | 블렌드명 (예: Full Moon) |
| `description`        | TEXT         | NULL                    | 블렌드 설명              |
| `recipe`             | JSON         | NOT NULL                | 레시피 (JSON 배열)       |
| `target_roast_level` | VARCHAR(50)  | NULL                    | 목표 로스팅 레벨         |
| `notes`              | TEXT         | NULL                    | 내부 메모                |
| `created_at`         | DATETIME     | NOT NULL, DEFAULT NOW() | 생성일시                 |
| `updated_at`         | DATETIME     | NULL                    | 수정일시                 |

**recipe 구조 (JSON)**:
```json
[
  {"bean_id": 6, "ratio": 0.4},
  {"bean_id": 9, "ratio": 0.4}
]
```

---

### 4. inbound_documents (입고 내역서)

**목적**: OCR 스캔된 입고 내역서 헤더 정보

| 컬럼명            | 타입     | 제약               | 설명                   |
| ----------------- | -------- | ------------------ | ---------------------- |
| `id`              | INTEGER  | PK, AUTO_INCREMENT | 문서 ID                |
| `contract_number` | VARCHAR  | NULL               | 계약 번호              |
| `supplier_name`   | VARCHAR  | NULL               | 공급처명 (OCR 추출)    |
| `supplier_id`     | INTEGER  | FK → suppliers.id  | 매핑된 공급처 ID       |
| `receiver_name`   | VARCHAR  | NULL               | 받는 사람 (상호)       |
| `invoice_date`    | VARCHAR  | NULL               | 발행 일자 (YYYY-MM-DD) |
| `total_amount`    | FLOAT    | NULL               | 총 금액                |
| `image_url`       | VARCHAR  | NULL               | 원본 이미지 URL        |
| `drive_file_id`   | VARCHAR  | NULL               | 구글 드라이브 파일 ID  |
| `notes`           | TEXT     | NULL               | 메모                   |
| `created_at`      | DATETIME | NOT NULL           | 생성일시               |

---

### 5. inbound_document_details (입고 상세)

**목적**: 입고 내역서 상의 상세 공급자 및 재무 정보

| 컬럼명                     | 타입     | 제약                      | 설명                |
| -------------------------- | -------- | ------------------------- | ------------------- |
| `id`                       | INTEGER  | PK, AUTO_INCREMENT        | ID                  |
| `inbound_document_id`      | INTEGER  | FK → inbound_documents.id | 상위 문서 ID        |
| `document_number`          | VARCHAR  | NULL                      | 문서 번호           |
| `issue_date`               | VARCHAR  | NULL                      | 공급연월일 (작성일) |
| `delivery_date`            | VARCHAR  | NULL                      | 납품일자            |
| `payment_due_date`         | VARCHAR  | NULL                      | 지급기일            |
| `invoice_type`             | VARCHAR  | NULL                      | 영수/청구 구분      |
| `supplier_business_number` | VARCHAR  | NULL                      | 공급자 등록번호     |
| `supplier_address`         | TEXT     | NULL                      | 공급자 주소         |
| `supplier_phone`           | VARCHAR  | NULL                      | 공급자 전화         |
| `supplier_fax`             | VARCHAR  | NULL                      | 공급자 팩스         |
| `supplier_email`           | VARCHAR  | NULL                      | 공급자 이메일       |
| `supplier_representative`  | VARCHAR  | NULL                      | 공급자 대표자명     |
| `supplier_contact_person`  | VARCHAR  | NULL                      | 담당자              |
| `supplier_contact_phone`   | VARCHAR  | NULL                      | 담당자 연락처       |
| `subtotal`                 | FLOAT    | NULL                      | 공급가액 합계       |
| `tax_amount`               | FLOAT    | NULL                      | 세액 합계           |
| `grand_total`              | FLOAT    | NULL                      | 총 합계             |
| `currency`                 | VARCHAR  | NULL                      | 통화 단위           |
| `payment_terms`            | TEXT     | NULL                      | 결제 조건           |
| `shipping_method`          | VARCHAR  | NULL                      | 배송 방법           |
| `notes`                    | TEXT     | NULL                      | 비고                |
| `remarks`                  | TEXT     | NULL                      | 특이사항            |
| `created_at`               | DATETIME | NULL                      | 생성일시            |
| `updated_at`               | DATETIME | NULL                      | 수정일시            |

---

### 6. inbound_receivers (공급받는자)

**목적**: 입고 내역서 상의 공급받는자 정보

| 컬럼명                | 타입     | 제약                      | 설명         |
| --------------------- | -------- | ------------------------- | ------------ |
| `id`                  | INTEGER  | PK, AUTO_INCREMENT        | ID           |
| `inbound_document_id` | INTEGER  | FK → inbound_documents.id | 상위 문서 ID |
| `name`                | VARCHAR  | NULL                      | 상호(법인명) |
| `business_number`     | VARCHAR  | NULL                      | 등록번호     |
| `address`             | TEXT     | NULL                      | 사업장 주소  |
| `phone`               | VARCHAR  | NULL                      | 전화번호     |
| `contact_person`      | VARCHAR  | NULL                      | 담당자       |
| `created_at`          | DATETIME | NULL                      | 생성일시     |
| `updated_at`          | DATETIME | NULL                      | 수정일시     |

---

### 7. inbound_items (입고 품목)

**목적**: 입고 내역서 내 개별 품목 상세

| 컬럼명                | 타입     | 제약                      | 설명         |
| --------------------- | -------- | ------------------------- | ------------ |
| `id`                  | INTEGER  | PK, AUTO_INCREMENT        | ID           |
| `inbound_document_id` | INTEGER  | FK → inbound_documents.id | 상위 문서 ID |
| `item_order`          | INTEGER  | NOT NULL                  | 품목 순번    |
| `bean_name`           | VARCHAR  | NULL                      | 품목명 (OCR) |
| `specification`       | VARCHAR  | NULL                      | 규격         |
| `unit`                | VARCHAR  | NULL                      | 단위         |
| `quantity`            | FLOAT    | NULL                      | 수량         |
| `origin`              | VARCHAR  | NULL                      | 원산지/비고  |
| `unit_price`          | FLOAT    | NULL                      | 단가         |
| `supply_amount`       | FLOAT    | NULL                      | 공급가액     |
| `tax_amount`          | FLOAT    | NULL                      | 세액         |
| `notes`               | TEXT     | NULL                      | 비고         |
| `created_at`          | DATETIME | NULL                      | 생성일시     |
| `updated_at`          | DATETIME | NULL                      | 수정일시     |

---

### 8. inventory_logs (재고 이력)

**목적**: 모든 재고 변동 추적 (감사 로그)

| 컬럼명                | 타입        | 제약                      | 설명                      |
| --------------------- | ----------- | ------------------------- | ------------------------- |
| `id`                  | INTEGER     | PK, AUTO_INCREMENT        | 로그 ID                   |
| `bean_id`             | INTEGER     | FK → beans.id, NOT NULL   | 원두 ID                   |
| `change_type`         | VARCHAR(15) | NOT NULL                  | 변동 유형                 |
| `change_amount`       | FLOAT       | NOT NULL                  | 변동량 (+: 증가, -: 감소) |
| `current_quantity`    | FLOAT       | NOT NULL                  | 변동 후 잔고              |
| `notes`               | TEXT        | NULL                      | 비고/사유                 |
| `related_id`          | INTEGER     | NULL                      | 관련 ID (예: 로스팅 ID)   |
| `created_at`          | DATETIME    | NOT NULL, DEFAULT NOW()   | 발생일시                  |
| `inbound_document_id` | INTEGER     | FK → inbound_documents.id | 관련 입고 문서 ID         |

**Enum 값 (change_type)**:
- `PURCHASE`: 구매 입고 (+)
- `ROASTING_INPUT`: 로스팅 투입 (-)
- `ROASTING_OUTPUT`: 로스팅 산출 (+)
- `BLENDING_INPUT`: 블렌딩 투입 (-)
- `SALES`: 판매 출고 (-)
- `LOSS`: 손실/폐기 (-)
- `ADJUSTMENT`: 재고 조정 (±)

---

## 인덱스 전략

### beans 테이블

```sql
CREATE INDEX idx_beans_name ON beans(name);
CREATE INDEX idx_beans_type ON beans(type);
CREATE INDEX idx_beans_sku ON beans(sku);
CREATE UNIQUE INDEX idx_beans_sku_unique ON beans(sku);
CREATE INDEX idx_beans_created_at ON beans(created_at);

-- Full-text search (PostgreSQL)
CREATE INDEX idx_beans_search ON beans USING GIN (
  to_tsvector('simple', coalesce(name,'') || ' ' ||
                        coalesce(origin,'') || ' ' ||
                        coalesce(variety,''))
);
```

### blends 테이블

```sql
CREATE INDEX idx_blends_name ON blends(name);
CREATE INDEX idx_blends_created_at ON blends(created_at);
```

### inventory_logs 테이블

```sql
CREATE INDEX idx_inventory_logs_bean_id ON inventory_logs(bean_id);
CREATE INDEX idx_inventory_logs_change_type ON inventory_logs(change_type);
CREATE INDEX idx_inventory_logs_created_at ON inventory_logs(created_at DESC);

-- 복합 인덱스: 원두별 이력 조회 최적화
CREATE INDEX idx_inventory_logs_bean_created ON inventory_logs(bean_id, created_at DESC);
```

---

## 데이터 무결성 규칙

### 1. 재고 일관성

**규칙**: `beans.quantity_kg` = 모든 `inventory_logs` 변동량 합계

```sql
-- 검증 쿼리
SELECT
    b.id,
    b.name,
    b.quantity_kg AS current_stock,
    COALESCE(SUM(il.change_amount), 0) AS calculated_stock,
    (b.quantity_kg - COALESCE(SUM(il.change_amount), 0)) AS diff
FROM beans b
LEFT JOIN inventory_logs il ON b.id = il.bean_id
GROUP BY b.id, b.name, b.quantity_kg
HAVING ABS(b.quantity_kg - COALESCE(SUM(il.change_amount), 0)) > 0.01;
```

### 2. 블렌드 레시피 비율 합계

**규칙**: 블렌드 레시피의 모든 `ratio` 합 = 1.0

```python
# Python 검증 (Pydantic Validator)
def validate_recipe(recipe: List[dict]) -> List[dict]:
    total_ratio = sum(item['ratio'] for item in recipe)
    if not (0.99 <= total_ratio <= 1.01):  # 부동소수점 오차 허용
        raise ValueError(f"Recipe ratios must sum to 1.0, got {total_ratio}")
    return recipe
```

### 3. Foreign Key 제약

```sql
-- beans.parent_bean_id → beans.id
ALTER TABLE beans
ADD CONSTRAINT fk_beans_parent
FOREIGN KEY (parent_bean_id) REFERENCES beans(id)
ON DELETE SET NULL;

-- inventory_logs.bean_id → beans.id
ALTER TABLE inventory_logs
ADD CONSTRAINT fk_inventory_logs_bean
FOREIGN KEY (bean_id) REFERENCES beans(id)
ON DELETE CASCADE;  -- 원두 삭제 시 로그도 삭제
```

### 4. Check 제약

```sql
-- 재고는 음수 불가 (선택적)
ALTER TABLE beans
ADD CONSTRAINT chk_beans_quantity_nonnegative
CHECK (quantity_kg >= 0);

-- 가격은 양수
ALTER TABLE beans
ADD CONSTRAINT chk_beans_price_positive
CHECK (avg_price >= 0);

-- 손실률은 0~1 사이
ALTER TABLE beans
ADD CONSTRAINT chk_beans_loss_rate_range
CHECK (expected_loss_rate >= 0 AND expected_loss_rate < 1);
```

---

## 샘플 데이터

### beans 테이블 (생두)

```sql
INSERT INTO beans (name, type, origin, variety, grade, processing_method, quantity_kg, avg_price, expected_loss_rate)
VALUES
('예가체프', 'GREEN_BEAN', 'Ethiopia', 'Yirgacheffe', 'G2 Washed', 'Washed', 20.0, 12000, 0.15),
('모모라', 'GREEN_BEAN', 'Ethiopia', 'Mormora', 'G1 Natural', 'Natural', 15.0, 20000, 0.18),
('마사이', 'GREEN_BEAN', 'Kenya', 'Masai', 'AA FAQ', 'Washed', 15.0, 18000, 0.16);
```

### beans 테이블 (원두)

```sql
INSERT INTO beans (name, type, roast_profile, parent_bean_id, quantity_kg, avg_price, cost_price)
VALUES
('예가체프 원두', 'ROASTED_BEAN', 'MEDIUM', 1, 17.0, 14118, 14118);
```

### blends 테이블

```sql
INSERT INTO blends (name, description, recipe, target_roast_level)
VALUES
('Full Moon', '더문의 대표 하우스 블렌드',
 '[{"bean_id":6,"ratio":0.4},{"bean_id":9,"ratio":0.4},{"bean_id":2,"ratio":0.1},{"bean_id":5,"ratio":0.1}]',
 'Medium Dark');
```

### inventory_logs 테이블

```sql
INSERT INTO inventory_logs (bean_id, change_type, change_amount, current_quantity, notes)
VALUES
(1, 'PURCHASE', 20.0, 20.0, 'Initial Stock'),
(1, 'ROASTING_INPUT', -20.0, 0.0, 'Roasted to #2'),
(2, 'ROASTING_OUTPUT', 17.0, 17.0, 'From bean #1');
```

---

## 🔗 관련 문서

**← 상위**: [Documents README](../README.md) | [프로젝트 루트](../../README.md)

**아키텍처 문서**:
- [시스템 개요](SYSTEM_OVERVIEW.md) - 전체 시스템 개요 및 핵심 기능
- [데이터 흐름도](DATA_FLOW.md) - 시스템 내 데이터 흐름 상세 분석
- [API 명세](API_SPECIFICATION.md) ⭐ - 모든 API 엔드포인트 상세 문서
- [기술 스택](TECHNOLOGY_STACK.md) ⭐ - 사용 기술 상세 설명
- [배포 아키텍처](DEPLOYMENT_ARCHITECTURE.md) ⭐ - 배포 환경 상세 구조

**개발 가이드**:
- [개발 가이드](DEVELOPMENT_GUIDE.md) - 5단계 개발 프로세스
- [문제 해결](TROUBLESHOOTING.md) - 16가지 오류 & 해결법

---

**작성**: AI Assistant
**최종 업데이트**: 2025-12-08
**버전**: 0.0.6
