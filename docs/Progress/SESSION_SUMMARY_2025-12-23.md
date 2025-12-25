# Session Summary: 2025-12-23 (Real-time OCR Feedback)

## 🎯 목표 (Goal)
- **실시간 OCR 분석 피드백 (Phase 15)**: 사용자가 긴 분석 시간 동안 진행 상황을 알 수 있도록 단계별 상태 메시지(전처리, 모델 호출, 매칭 등)를 실시간으로 스트리밍.

## ✅ 달성 사항 (Achievements)

### 1. Backend (FastAPI)
- **Generator 패턴 적용**: `OCRService`와 `Inbound` 엔드포인트에 비동기 제너레이터 도입.
- **StreamingResponse 구현**: NDJSON(Newline Delimited JSON) 포맷으로 상태 메시지 스트리밍.
- **리소스 관리 최적화**: `StreamingResponse` 사용 시 발생하는 `UploadFile` 조기 종료(`I/O on closed file`) 문제를 해결하기 위해 파일 읽기 시점 조정.

### 2. Frontend (Next.js)
- **Stream Reader 구현**: `fetch` API의 `body.getReader()`를 사용하여 스트리밍 응답 파싱.
- **UI 반응성 향상**: "분석 시작" 버튼을 상태 메시지 표시기로 전환하여 사용자 경험 개선.

### 3. Verification
- **검증 스크립트 작성**: `backend/tests/verify_streaming_api.py`를 통해 스트리밍 동작 및 에러 처리 검증 완료.

## 📝 주요 변경 파일
- `backend/app/services/ocr_service.py`
- `backend/app/api/v1/endpoints/inbound.py`
- `frontend/app/inventory/inbound/page.tsx`

### 4. OCR 디버깅 및 고도화 (Phase 16)
- **Claude 모델 ID 수정**: 잘못된 모델 ID 404 오류 해결, `claude-sonnet-4-5` 적용.
- **JSON 파싱 견고성 강화**: 정규식 도입으로 마크다운 코드 블록 및 사족이 포함된 응답 처리 개선.
- **치명적 버그 수정**: 이미지 전처리 시 MIME Type 불일치(PNG→JPEG) 문제 해결, Claude 400 오류 근본 원인 제거.
- **문서 정리**: Phase 2, 3, 4, 9 완료 처리.

### 5. UI/UX 개선 (Currency Formatting - Phase 17)
- **전역 통화 포맷팅 적용**: 소수점 없는 정수형 원화 표시(`formatCurrency` 유틸리티 도입).
- **적용 범위 확대**:
  - **Analytics**: 자산 가치 테이블, 원가 추이 차트, 공급자 파이 차트.
  - **Inventory/Inbound**: 명세서 분석 결과, 명세서 목록/상세, 입고 아이템.
  - **Beans**: 구매 단가 표시.
  - **Roasting**: 싱글/블렌드 로스팅 원가 시뮬레이션 및 결과.
- **코드 일관성 확보**: 개별 컴포넌트의 산재된 포맷팅 로직을 `frontend/lib/utils.ts`로 통합.

---

## [0.4.7] - 2025-12-23

### 🏗️ 아키텍처 및 설정 관리 (Architecture & Configuration)

#### Admin & System Evolution (Phase 1 Planning)
- **Master Plan 수립**: 관리자 페이지 및 시스템 진화 마스터 플랜(`ADMIN_AND_SYSTEM_EVOLUTION_PLAN.md`) 작성.
  - 4단계 로드맵: Foundation(통합 설정) → Observability(모니터링) → Data Safety(백업) → AI Lab(지능화).
  - 시스템 아키텍처 다이어그램(Mermaid) 추가.
- **Configuration Management**: 통합 설정 관리 시스템 설계안(`CONFIGURATION_MANAGEMENT_PLAN.md`) 수립.
  - 파편화된 JSON 설정 파일(`ocr_prompt_structure.json`, `image_processing_config.json`)을 중앙화.
  - `ConfigService` 아키텍처 설계.

#### 🔧 Refactoring & Chore
- **Resource Directory**: `backend/app/schemas/*.json` → `backend/app/resources/*.json`으로 이동 및 코드 경로 수정.
- **OCR Model Config**: 기본 모델을 Gemini 1.5 Flash로 변경 및 모델 우선순위 조정 로직 리팩토링.
- **VS Code Settings**: FontAwesome 스타일 및 Mermaid 테마 설정 추가로 개발 환경 개선.
- **Bug Fix**: 터미널 캐싱 오류 해결.
- **Documentation Fix (Mermaid v8.8.0 Downgrade)**:
  - VS Code 확장 프로그램의 Mermaid 구버전(v8.8.0) 제약 사항으로 인한 문법 오류 전체 수정.
  - `flowchart` → `graph` (Legacy 키워드 복구)
  - `actor` → `participant` (Sequence Diagram)
  - `Attribute Constraints` ("GREEN | ...") 제거 (ER Diagram)
  - 한글 Link Label 및 Node Label 전체 Quoting 처리.
  - `SYSTEM_ARCHITECTURE.md`, `FEATURE_FLOWS.md` 등 전체 문서 호환성 확보 완료.

## 🔜 다음 단계 (Next Steps)
- 로스팅 로그 연동 고도화 (잔여 작업 점검)
- 명세서 목록 UI 필터 기능 개선

