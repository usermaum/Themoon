# Configuration Management System Plan

## 1. 개요 (Overview)

현재 파편화된 JSON 설정 파일(`ocr_prompt_structure.json`, `image_processing_config.json`)을 중앙 집중식 관리 시스템으로 통합하고, 향후 **Admin UI**를 통한 동적 제어를 지원하기 위한 아키텍처를 설계합니다.

## 2. 목표 (Goals)

1. **Centralization**: 모든 서비스 설정을 `system_config.json` 하나의 파일(또는 명확한 구조)로 통합 관리.
2. **Maintainability**: 설정과 코드는 분리하되, 설정 파일의 구조를 명확히 정의하여 유지보수성을 높임.
3. **Extensibility**: 향후 새로운 서비스나 모듈 추가 시 쉽게 설정을 확장할 수 있는 구조.
4. **Admin UI Support**: 프론트엔드에서 설정 스키마와 값을 조회하고 수정할 수 있는 API 지원.

## 3. 제안 아키텍처 (Proposed Architecture)

### 3.1. 통합 설정 파일 구조 (`backend/app/configs/system_config.json`)

기존의 개별 파일을 하나의 큰 JSON 구조로 병합합니다. 각 서비스는 자신의 Key(섹션)만 참조합니다.

```json
{
  "_meta": {
    "version": "1.0",
    "last_updated": "2024-12-23"
  },
  "ocr_service": {
    "prompt_schema": { ... },  // (구) ocr_prompt_structure.json
    "provider_settings": {
      "default_model": "gemini-1.5-flash-latest",
      "fallback_enabled": true
    }
  },
  "image_service": {
    "preprocessing": { ... }    // (구) image_processing_config.json
  },
  "system_settings": {
    "debug_mode": true,
    "log_level": "INFO"
  }
}
```

### 3.2. ConfigService (단일 진실 공급원)

설정 파일을 로드하고, 각 서비스에 필요한 설정 객체(Pydantic Model)를 제공하는 **싱글톤 서비스**를 구현합니다.

* **역할**:
  * 앱 시작 시 `system_config.json` 로드.
  * 설정 변경 시 파일 쓰기 (Admin UI 저장 요청).
  * Hot-reload 지원 (파일 변경 감지 또는 API로 갱신).
  * Type-safe한 설정 객체 반환 (`get_ocr_config()`, `get_image_config()`).

### 3.3. Admin API Endpoints

프론트엔드 관리자 페이지를 위한 API를 제공합니다.

* `GET /api/v1/config`: 전체 설정 조회 (또는 섹션별 조회).
* `PATCH /api/v1/config/{section}`: 특정 섹션 설정 업데이트.
* `GET /api/v1/config/schema`: 설정 UI 구성을 위한 메타데이터(설명, 타입, 범위 등) 제공.

## 4. 구현 단계 (Implementation Steps)

### Step 1: 디렉토리 및 파일 구조 재편

* `backend/app/schemas/*.json` 및 `backend/app/resources/*.json` 제거.
* `backend/app/configs/` 디렉토리 생성.
* `system_config.json` 생성 및 기존 내용 마이그레이션.

### Step 2: ConfigService 구현

* `backend/app/services/config_service.py` 작성.
* Pydantic 모델을 사용하여 설정 유효성 검사 로직 포함.

### Step 3: 기존 서비스 리팩토링

* `OCRService`, `ImageService`가 직접 파일을 읽는 대신 `ConfigService`를 주입받아 설정을 사용하도록 수정.

### Step 4: Admin API 구현 (Future)

* 설정 관리용 Router 및 Controller 추가.

## 5. 기대 효과

* **파일 관리 용이**: 하나의 파일에서 시스템 전체 동작을 파악 가능.
* **안정성**: Pydantic을 통한 설정 값 검증으로 오타나 잘못된 타입 방지.
* **확장성**: Admin 패널 개발 시 백엔드 수정 최소화.
