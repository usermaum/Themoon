# 📡 API 명세서 (API Specification)

> **프로젝트**: TheMoon - 커피 로스팅 원가 계산 시스템
> **API 버전**: v1
> **Base URL**: `http://localhost:8000/api/v1` (개발), `https://themoon-api.onrender.com/api/v1` (프로덕션)
> **작성일**: 2025-12-08

---

## 📋 목차

1. [API 개요](#api-개요)
2. [인증 및 보안](#인증-및-보안)
3. [공통 응답 형식](#공통-응답-형식)
4. [에러 코드 표준](#에러-코드-표준)
5. [엔드포인트 목록](#엔드포인트-목록)
   - [Beans API](#beans-api)
   - [Roasting API](#roasting-api)
   - [Blends API](#blends-api)
   - [Inventory Logs API](#inventory-logs-api)

---

## API 개요

**TheMoon API**는 커피 로스팅 원가 계산 및 재고 관리를 위한 RESTful API입니다.

### 주요 특징

- **RESTful 설계**: 표준 HTTP 메서드 (GET, POST, PUT, PATCH, DELETE) 사용
- **JSON 기반**: 모든 요청/응답은 JSON 형식
- **FastAPI 기반**: 자동 문서화 지원 (Swagger UI, ReDoc)
- **타입 검증**: Pydantic 스키마를 통한 요청/응답 검증
- **CORS 지원**: 프론트엔드 통신을 위한 CORS 설정 완료

### 자동 문서화 (Interactive API Docs)

FastAPI는 자동으로 인터랙티브 API 문서를 생성합니다:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 인증 및 보안

### 현재 버전 (v0.0.6)

- **인증 없음**: 개발 단계로 인증 없이 모든 엔드포인트 접근 가능
- **CORS**: 모든 Origin 허용 (`allow_origins=["*"]`)

### 향후 계획 (Roadmap)

- **JWT 인증**: Bearer Token 방식 인증 추가 예정
- **역할 기반 접근 제어 (RBAC)**: 관리자/사용자 역할 구분
- **Rate Limiting**: API 요청 제한 (DDoS 방지)

---

## 공통 응답 형식

### 성공 응답

모든 성공 응답은 HTTP 상태 코드 `2xx`와 함께 JSON 형식으로 반환됩니다.

**예시 (단일 객체)**:

```json
{
  "id": 1,
  "name": "과테말라 안티구아",
  "type": "GREEN_BEAN",
  "origin": "Guatemala",
  "quantity_kg": 50.0,
  "avg_price": 15000
}
```

**예시 (목록 + 페이지네이션)**:

```json
{
  "items": [
    { "id": 1, "name": "..." },
    { "id": 2, "name": "..." }
  ],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

### 에러 응답

모든 에러 응답은 HTTP 상태 코드 `4xx` 또는 `5xx`와 함께 JSON 형식으로 반환됩니다.

**에러 응답 형식**:

```json
{
  "detail": "에러 메시지"
}
```

**예시 (404 Not Found)**:

```json
{
  "detail": "Bean not found"
}
```

**예시 (422 Validation Error)**:

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "input_weight"],
      "msg": "Input should be greater than 0",
      "input": -10
    }
  ]
}
```

---

## 에러 코드 표준

### HTTP 상태 코드

| 코드 | 설명 | 발생 상황 |
|------|------|-----------|
| **200 OK** | 성공 | GET, PUT, PATCH 요청 성공 |
| **201 Created** | 생성 완료 | POST 요청으로 리소스 생성 성공 |
| **204 No Content** | 성공 (응답 없음) | DELETE 요청 성공 |
| **400 Bad Request** | 잘못된 요청 | 비즈니스 로직 위반 (예: 재고 부족) |
| **404 Not Found** | 리소스 없음 | 요청한 ID의 리소스가 존재하지 않음 |
| **422 Unprocessable Entity** | 검증 실패 | 요청 데이터 타입/형식 오류 |
| **500 Internal Server Error** | 서버 오류 | 예기치 않은 서버 내부 오류 |

### 비즈니스 로직 에러 메시지

#### Beans API

| 에러 메시지 | 발생 조건 |
|------------|-----------|
| `Bean not found` | 존재하지 않는 Bean ID 조회/수정/삭제 |
| `Insufficient quantity` | 재고 차감 시 재고량 부족 |

#### Roasting API

| 에러 메시지 | 발생 조건 |
|------------|-----------|
| `Green bean not found` | 존재하지 않는 생두 ID로 로스팅 시도 |
| `Insufficient green bean stock` | 생두 재고 부족 |
| `Blend not found` | 존재하지 않는 블렌드 ID로 로스팅 시도 |

#### Blends API

| 에러 메시지 | 발생 조건 |
|------------|-----------|
| `Blend not found` | 존재하지 않는 블렌드 ID 조회/수정/삭제 |
| `Invalid recipe: ratios must sum to 1.0` | 블렌드 레시피 비율 합이 1.0이 아님 |

#### Inventory Logs API

| 에러 메시지 | 발생 조건 |
|------------|-----------|
| `Inventory log not found` | 존재하지 않는 로그 ID 조회/수정/삭제 |
| `Invalid change_type` | 유효하지 않은 거래 유형 |

---

## 엔드포인트 목록

### Beans API

생두(GREEN_BEAN) 및 원두(ROASTED_BEAN) 관리 API

#### 1. 원두 목록 조회

**Endpoint**: `GET /api/v1/beans/`

**설명**: 페이지네이션 및 검색을 지원하는 원두 목록 조회

**쿼리 파라미터**:

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|--------|------|
| `page` | integer | ❌ | 1 | 페이지 번호 (1부터 시작) |
| `size` | integer | ❌ | 10 | 페이지당 항목 수 (최대 100) |
| `search` | string | ❌ | null | 검색어 (이름, 원산지, 품종) |

**응답 (200 OK)**:

```json
{
  "items": [
    {
      "id": 1,
      "name": "과테말라 안티구아",
      "type": "GREEN_BEAN",
      "sku": "GB001",
      "origin": "Guatemala",
      "variety": "Bourbon",
      "grade": "SHB",
      "processing_method": "Washed",
      "roast_profile": null,
      "parent_bean_id": null,
      "quantity_kg": 50.0,
      "avg_price": 15000.0,
      "purchase_price_per_kg": 15000.0,
      "cost_price": null,
      "description": "과테말라 안티구아 지역 SHB 등급",
      "notes": null,
      "expected_loss_rate": 0.15,
      "created_at": "2025-12-01T10:00:00",
      "updated_at": null
    }
  ],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

**예시 요청**:

```bash
# 기본 조회
curl http://localhost:8000/api/v1/beans/

# 페이지네이션
curl "http://localhost:8000/api/v1/beans/?page=2&size=20"

# 검색
curl "http://localhost:8000/api/v1/beans/?search=과테말라"
```

---

#### 2. 원두 상세 조회

**Endpoint**: `GET /api/v1/beans/{bean_id}`

**설명**: 특정 원두의 상세 정보 조회

**경로 파라미터**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `bean_id` | integer | 원두 ID |

**응답 (200 OK)**:

```json
{
  "id": 1,
  "name": "과테말라 안티구아",
  "type": "GREEN_BEAN",
  "origin": "Guatemala",
  "quantity_kg": 50.0,
  "avg_price": 15000.0,
  "created_at": "2025-12-01T10:00:00"
}
```

**에러 (404 Not Found)**:

```json
{
  "detail": "Bean not found"
}
```

**예시 요청**:

```bash
curl http://localhost:8000/api/v1/beans/1
```

---

#### 3. 새 원두 등록

**Endpoint**: `POST /api/v1/beans/`

**설명**: 생두 또는 원두 등록

**요청 본문 (BeanCreate)**:

```json
{
  "name": "과테말라 안티구아",
  "type": "GREEN_BEAN",
  "sku": "GB001",
  "origin": "Guatemala",
  "variety": "Bourbon",
  "grade": "SHB",
  "processing_method": "Washed",
  "quantity_kg": 50.0,
  "avg_price": 15000.0,
  "purchase_price_per_kg": 15000.0,
  "expected_loss_rate": 0.15,
  "description": "과테말라 안티구아 지역 SHB 등급"
}
```

**응답 (201 Created)**:

```json
{
  "id": 1,
  "name": "과테말라 안티구아",
  "type": "GREEN_BEAN",
  "created_at": "2025-12-08T10:00:00"
}
```

**에러 (422 Validation Error)**:

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "name"],
      "msg": "Field required"
    }
  ]
}
```

**예시 요청**:

```bash
curl -X POST http://localhost:8000/api/v1/beans/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "과테말라 안티구아",
    "type": "GREEN_BEAN",
    "origin": "Guatemala",
    "quantity_kg": 50.0,
    "avg_price": 15000.0
  }'
```

---

#### 4. 원두 정보 수정

**Endpoint**: `PUT /api/v1/beans/{bean_id}`

**설명**: 원두 정보 전체 수정 (부분 수정 가능)

**경로 파라미터**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `bean_id` | integer | 원두 ID |

**요청 본문 (BeanUpdate)**:

```json
{
  "quantity_kg": 60.0,
  "notes": "재고 입고 완료"
}
```

**응답 (200 OK)**:

```json
{
  "id": 1,
  "name": "과테말라 안티구아",
  "quantity_kg": 60.0,
  "notes": "재고 입고 완료",
  "updated_at": "2025-12-08T11:00:00"
}
```

**에러 (404 Not Found)**:

```json
{
  "detail": "Bean not found"
}
```

**예시 요청**:

```bash
curl -X PUT http://localhost:8000/api/v1/beans/1 \
  -H "Content-Type: application/json" \
  -d '{
    "quantity_kg": 60.0,
    "notes": "재고 입고 완료"
  }'
```

---

#### 5. 원두 삭제

**Endpoint**: `DELETE /api/v1/beans/{bean_id}`

**설명**: 원두 삭제 (재고 로그도 함께 삭제됨 - CASCADE)

**경로 파라미터**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `bean_id` | integer | 원두 ID |

**응답 (204 No Content)**: (응답 본문 없음)

**에러 (404 Not Found)**:

```json
{
  "detail": "Bean not found"
}
```

**예시 요청**:

```bash
curl -X DELETE http://localhost:8000/api/v1/beans/1
```

---

#### 6. 전체 원두 개수 조회

**Endpoint**: `GET /api/v1/beans/stats/count`

**설명**: 전체 원두 개수 조회

**응답 (200 OK)**:

```json
{
  "count": 42
}
```

**예시 요청**:

```bash
curl http://localhost:8000/api/v1/beans/stats/count
```

---

#### 7. 원두 재고량 조정

**Endpoint**: `PATCH /api/v1/beans/{bean_id}/quantity`

**설명**: 원두 재고량 증감 (입고/출고/조정)

**경로 파라미터**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `bean_id` | integer | 원두 ID |

**쿼리 파라미터**:

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `quantity_change` | float | ✅ | 재고 변경량 (kg, 음수 가능) |

**응답 (200 OK)**:

```json
{
  "id": 1,
  "name": "과테말라 안티구아",
  "quantity_kg": 55.0,
  "updated_at": "2025-12-08T12:00:00"
}
```

**에러 (404 Not Found)**:

```json
{
  "detail": "Bean not found"
}
```

**예시 요청**:

```bash
# 재고 증가 (입고)
curl -X PATCH "http://localhost:8000/api/v1/beans/1/quantity?quantity_change=10.0"

# 재고 감소 (출고)
curl -X PATCH "http://localhost:8000/api/v1/beans/1/quantity?quantity_change=-5.0"
```

---

### Roasting API

로스팅 프로세스 (생두 → 원두 변환) 관리 API

#### 1. 싱글 오리진 로스팅

**Endpoint**: `POST /api/v1/roasting/single-origin`

**설명**: 싱글 오리진 로스팅 기록 (생두 재고 차감 → 원두 재고 생성)

**요청 본문 (SingleOriginRoastingRequest)**:

```json
{
  "green_bean_id": 1,
  "input_weight": 10.0,
  "output_weight": 8.5,
  "roast_profile": "LIGHT",
  "notes": "City Roast, 1차 크랙 종료 시점 배출"
}
```

**필드 설명**:

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `green_bean_id` | integer | ✅ | 생두 ID |
| `input_weight` | float | ✅ | 생두 투입량 (kg, > 0) |
| `output_weight` | float | ✅ | 원두 생산량 (kg, ≥ 0) |
| `roast_profile` | enum | ✅ | 로스팅 프로필 (`LIGHT`, `DARK`) |
| `notes` | string | ❌ | 로스팅 노트 |

**응답 (200 OK)**:

```json
{
  "success": true,
  "message": "Single origin roasting logged successfully",
  "roasted_bean": {
    "id": 2,
    "name": "과테말라 안티구아 (라이트)",
    "type": "ROASTED_BEAN",
    "roast_profile": "LIGHT",
    "parent_bean_id": 1,
    "quantity_kg": 8.5,
    "cost_price": 17647.06,
    "created_at": "2025-12-08T13:00:00"
  },
  "loss_rate_percent": 15.0,
  "production_cost": 17647.06
}
```

**에러 (404 Not Found)**:

```json
{
  "detail": "Green bean not found"
}
```

**에러 (400 Bad Request)**:

```json
{
  "detail": "Insufficient green bean stock"
}
```

**예시 요청**:

```bash
curl -X POST http://localhost:8000/api/v1/roasting/single-origin \
  -H "Content-Type: application/json" \
  -d '{
    "green_bean_id": 1,
    "input_weight": 10.0,
    "output_weight": 8.5,
    "roast_profile": "LIGHT",
    "notes": "City Roast"
  }'
```

---

#### 2. 블렌드 로스팅

**Endpoint**: `POST /api/v1/roasting/blend`

**설명**: 블렌드 레시피를 기반으로 여러 생두를 혼합하여 로스팅

**요청 본문 (BlendRoastingRequest)**:

```json
{
  "blend_id": 1,
  "output_weight": 10.0,
  "input_weight": 11.5,
  "notes": "Full Moon Blend 생산"
}
```

**필드 설명**:

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `blend_id` | integer | ✅ | 블렌드 ID |
| `output_weight` | float | ✅ | 원두 목표 생산량 (kg, > 0) |
| `input_weight` | float | ❌ | 실제 투입량 (kg, > 0) |
| `notes` | string | ❌ | 로스팅 노트 |

**응답 (200 OK)**:

```json
{
  "success": true,
  "message": "Blend roasting logged successfully",
  "roasted_bean": {
    "id": 3,
    "name": "Full Moon Blend",
    "type": "ROASTED_BEAN",
    "roast_profile": "DARK",
    "quantity_kg": 10.0,
    "cost_price": 18500.0,
    "created_at": "2025-12-08T14:00:00"
  },
  "loss_rate_percent": 13.04,
  "production_cost": 18500.0
}
```

**에러 (404 Not Found)**:

```json
{
  "detail": "Blend not found"
}
```

**에러 (400 Bad Request)**:

```json
{
  "detail": "Insufficient stock for bean: 과테말라 안티구아"
}
```

**예시 요청**:

```bash
curl -X POST http://localhost:8000/api/v1/roasting/blend \
  -H "Content-Type: application/json" \
  -d '{
    "blend_id": 1,
    "output_weight": 10.0,
    "input_weight": 11.5,
    "notes": "Full Moon Blend 생산"
  }'
```

---

### Blends API

블렌드 레시피 관리 API

#### 1. 블렌드 목록 조회

**Endpoint**: `GET /api/v1/blends/`

**설명**: 블렌드 레시피 목록 조회

**쿼리 파라미터**:

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|--------|------|
| `skip` | integer | ❌ | 0 | 건너뛸 항목 수 |
| `limit` | integer | ❌ | 100 | 최대 항목 수 |

**응답 (200 OK)**:

```json
[
  {
    "id": 1,
    "name": "Full Moon Blend",
    "description": "균형잡힌 바디감과 초콜릿 풍미",
    "recipe": [
      { "bean_id": 1, "ratio": 0.6 },
      { "bean_id": 2, "ratio": 0.4 }
    ],
    "target_roast_level": "DARK",
    "notes": null,
    "created_at": "2025-12-01T10:00:00",
    "updated_at": null
  }
]
```

**예시 요청**:

```bash
curl http://localhost:8000/api/v1/blends/
```

---

#### 2. 블렌드 상세 조회

**Endpoint**: `GET /api/v1/blends/{blend_id}`

**설명**: 특정 블렌드의 상세 정보 조회

**경로 파라미터**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `blend_id` | integer | 블렌드 ID |

**응답 (200 OK)**:

```json
{
  "id": 1,
  "name": "Full Moon Blend",
  "description": "균형잡힌 바디감과 초콜릿 풍미",
  "recipe": [
    { "bean_id": 1, "ratio": 0.6 },
    { "bean_id": 2, "ratio": 0.4 }
  ],
  "target_roast_level": "DARK",
  "created_at": "2025-12-01T10:00:00"
}
```

**에러 (404 Not Found)**:

```json
{
  "detail": "Blend not found"
}
```

**예시 요청**:

```bash
curl http://localhost:8000/api/v1/blends/1
```

---

#### 3. 새 블렌드 생성

**Endpoint**: `POST /api/v1/blends/`

**설명**: 새 블렌드 레시피 생성

**요청 본문 (BlendCreate)**:

```json
{
  "name": "Full Moon Blend",
  "description": "균형잡힌 바디감과 초콜릿 풍미",
  "recipe": [
    { "bean_id": 1, "ratio": 0.6 },
    { "bean_id": 2, "ratio": 0.4 }
  ],
  "target_roast_level": "DARK",
  "notes": "60% 과테말라, 40% 브라질"
}
```

**필드 설명**:

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `name` | string | ✅ | 블렌드 이름 |
| `description` | string | ❌ | 블렌드 설명 |
| `recipe` | array | ✅ | 블렌드 레시피 (비율 합 = 1.0) |
| `recipe[].bean_id` | integer | ✅ | 원두 ID |
| `recipe[].ratio` | float | ✅ | 혼합 비율 (0.0 ~ 1.0) |
| `target_roast_level` | string | ❌ | 목표 로스팅 레벨 |
| `notes` | string | ❌ | 노트 |

**응답 (201 Created)**:

```json
{
  "id": 1,
  "name": "Full Moon Blend",
  "recipe": [
    { "bean_id": 1, "ratio": 0.6 },
    { "bean_id": 2, "ratio": 0.4 }
  ],
  "created_at": "2025-12-08T15:00:00"
}
```

**에러 (400 Bad Request)**:

```json
{
  "detail": "Invalid recipe: ratios must sum to 1.0"
}
```

**예시 요청**:

```bash
curl -X POST http://localhost:8000/api/v1/blends/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Full Moon Blend",
    "recipe": [
      { "bean_id": 1, "ratio": 0.6 },
      { "bean_id": 2, "ratio": 0.4 }
    ],
    "target_roast_level": "DARK"
  }'
```

---

#### 4. 블렌드 정보 수정

**Endpoint**: `PUT /api/v1/blends/{blend_id}`

**설명**: 블렌드 정보 수정

**경로 파라미터**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `blend_id` | integer | 블렌드 ID |

**요청 본문 (BlendUpdate)**:

```json
{
  "description": "업데이트된 설명",
  "notes": "레시피 수정 완료"
}
```

**응답 (200 OK)**:

```json
{
  "id": 1,
  "name": "Full Moon Blend",
  "description": "업데이트된 설명",
  "notes": "레시피 수정 완료",
  "updated_at": "2025-12-08T16:00:00"
}
```

**에러 (404 Not Found)**:

```json
{
  "detail": "Blend not found"
}
```

**예시 요청**:

```bash
curl -X PUT http://localhost:8000/api/v1/blends/1 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "업데이트된 설명"
  }'
```

---

#### 5. 블렌드 삭제

**Endpoint**: `DELETE /api/v1/blends/{blend_id}`

**설명**: 블렌드 삭제

**경로 파라미터**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `blend_id` | integer | 블렌드 ID |

**응답 (204 No Content)**: (응답 본문 없음)

**에러 (404 Not Found)**:

```json
{
  "detail": "Blend not found"
}
```

**예시 요청**:

```bash
curl -X DELETE http://localhost:8000/api/v1/blends/1
```

---

### Inventory Logs API

재고 입출고 기록 관리 API

#### 1. 재고 로그 조회

**Endpoint**: `GET /api/v1/inventory-logs/`

**설명**: 재고 입출고 기록 조회

**쿼리 파라미터**:

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|--------|------|
| `bean_id` | integer | ❌ | null | 특정 원두의 로그만 조회 |
| `skip` | integer | ❌ | 0 | 건너뛸 항목 수 |
| `limit` | integer | ❌ | 100 | 최대 항목 수 |

**응답 (200 OK)**:

```json
[
  {
    "id": 1,
    "bean_id": 1,
    "change_type": "PURCHASE",
    "change_amount": 50.0,
    "current_quantity": 50.0,
    "notes": "신규 입고",
    "created_at": "2025-12-01T10:00:00"
  },
  {
    "id": 2,
    "bean_id": 1,
    "change_type": "ROASTING_INPUT",
    "change_amount": -10.0,
    "current_quantity": 40.0,
    "notes": "로스팅 사용",
    "created_at": "2025-12-01T11:00:00"
  }
]
```

**change_type 값**:

- `PURCHASE`: 생두 구매 입고
- `ROASTING_INPUT`: 로스팅 투입 (차감)
- `ROASTING_OUTPUT`: 로스팅 생산 (증가)
- `SALES`: 판매 (차감)
- `LOSS`: 손실 (차감)
- `ADJUSTMENT`: 재고 조정
- `BLENDING_INPUT`: 블렌딩 투입 (차감)

**예시 요청**:

```bash
# 전체 로그 조회
curl http://localhost:8000/api/v1/inventory-logs/

# 특정 원두 로그 조회
curl "http://localhost:8000/api/v1/inventory-logs/?bean_id=1"
```

---

#### 2. 재고 로그 생성

**Endpoint**: `POST /api/v1/inventory-logs/`

**설명**: 수동 재고 입출고 기록 생성

**요청 본문 (InventoryLogCreate)**:

```json
{
  "bean_id": 1,
  "change_type": "ADJUSTMENT",
  "change_amount": 5.0,
  "notes": "재고 실사 조정"
}
```

**필드 설명**:

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `bean_id` | integer | ✅ | 원두 ID |
| `change_type` | string | ✅ | 거래 유형 (위 참조) |
| `change_amount` | float | ✅ | 재고 변경량 (양수: 증가, 음수: 감소) |
| `notes` | string | ❌ | 비고 |

**응답 (201 Created)**:

```json
{
  "id": 10,
  "bean_id": 1,
  "change_type": "ADJUSTMENT",
  "change_amount": 5.0,
  "current_quantity": 45.0,
  "notes": "재고 실사 조정",
  "created_at": "2025-12-08T17:00:00"
}
```

**에러 (400 Bad Request)**:

```json
{
  "detail": "Invalid change_type"
}
```

**예시 요청**:

```bash
curl -X POST http://localhost:8000/api/v1/inventory-logs/ \
  -H "Content-Type: application/json" \
  -d '{
    "bean_id": 1,
    "change_type": "ADJUSTMENT",
    "change_amount": 5.0,
    "notes": "재고 실사 조정"
  }'
```

---

#### 3. 재고 로그 수정

**Endpoint**: `PUT /api/v1/inventory-logs/{log_id}`

**설명**: 재고 로그 수정 (변경량 및 노트)

**경로 파라미터**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `log_id` | integer | 로그 ID |

**쿼리 파라미터**:

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `change_amount` | float | ✅ | 새로운 변경량 |
| `notes` | string | ❌ | 새로운 노트 |

**응답 (200 OK)**:

```json
{
  "id": 10,
  "bean_id": 1,
  "change_type": "ADJUSTMENT",
  "change_amount": 7.0,
  "current_quantity": 47.0,
  "notes": "재고 실사 재조정",
  "created_at": "2025-12-08T17:00:00"
}
```

**에러 (404 Not Found)**:

```json
{
  "detail": "Inventory log not found"
}
```

**예시 요청**:

```bash
curl -X PUT "http://localhost:8000/api/v1/inventory-logs/10?change_amount=7.0&notes=재고%20실사%20재조정"
```

---

#### 4. 재고 로그 삭제

**Endpoint**: `DELETE /api/v1/inventory-logs/{log_id}`

**설명**: 재고 로그 삭제 (원두 재고량도 함께 롤백)

**경로 파라미터**:

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `log_id` | integer | 로그 ID |

**응답 (204 No Content)**: (응답 본문 없음)

**에러 (404 Not Found)**:

```json
{
  "detail": "Inventory log not found"
}
```

**예시 요청**:

```bash
curl -X DELETE http://localhost:8000/api/v1/inventory-logs/10
```

---

## 📝 추가 정보

### FastAPI 자동 문서화

개발 서버 실행 후 브라우저에서 접속:

```
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
```

### Pydantic 스키마 위치

모든 요청/응답 스키마는 다음 경로에 정의되어 있습니다:

- `backend/app/schemas/bean.py` - Bean 스키마
- `backend/app/schemas/roasting.py` - Roasting 스키마
- `backend/app/schemas/blend.py` - Blend 스키마
- `backend/app/schemas/inventory_log.py` - InventoryLog 스키마

### API 엔드포인트 위치

모든 API 라우터는 다음 경로에 구현되어 있습니다:

- `backend/app/api/v1/endpoints/beans.py` - Beans API
- `backend/app/api/v1/roasting.py` - Roasting API
- `backend/app/api/v1/endpoints/blends.py` - Blends API
- `backend/app/api/v1/endpoints/inventory_logs.py` - Inventory Logs API

### 데이터베이스 스키마

데이터베이스 스키마는 다음 문서를 참조하세요:

- [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)

---

## 🔗 관련 문서

**← 상위**: [Documents README](../README.md) | [프로젝트 루트](../../README.md)

**아키텍처 문서**:
- [시스템 개요](SYSTEM_OVERVIEW.md) - 전체 시스템 개요 및 핵심 기능
- [데이터 흐름도](DATA_FLOW.md) - 시스템 내 데이터 흐름 상세 분석
- [데이터베이스 스키마](DATABASE_SCHEMA.md) - 테이블 구조 및 관계도
- [기술 스택](TECHNOLOGY_STACK.md) ⭐ - 사용 기술 상세 설명
- [배포 아키텍처](DEPLOYMENT_ARCHITECTURE.md) ⭐ - 배포 환경 상세 구조

**개발 가이드**:
- [개발 가이드](DEVELOPMENT_GUIDE.md) - 5단계 개발 프로세스
- [문제 해결](TROUBLESHOOTING.md) - 16가지 오류 & 해결법

---

**문서 버전**: v1.0
**최종 업데이트**: 2025-12-08
**작성자**: Claude (TheMoon Project Team)
