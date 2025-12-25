# 세션 요약: 2025-12-19 (Inbound OCR & Duplicate Check)

## 🎯 오늘 한 일 (Objectives)

1.  **입고(Inbound) 계약 번호(Contract Number) 인식률 개선**:
    - OCR 프롬프트를 고도화하여 계약 번호, 이메일, 전화번호, 수신자 정보 인식 성공.
    - 'Debug First' 전략 (전체 텍스트 먼저 스캔 후 추출) 도입.
2.  **계약 번호 중복 체크 기능 구현**:
    - Backend: `/check-duplicate/{contract_number}` API 추가 및 `confirm` 로직에 중복 방지 강화.
    - Frontend: 입력 필드 `onBlur` 시점 및 OCR 완료 시점 자동 중복 체크 트리거.
3.  **UI/UX 개선**:
    - 중복 발생 시 "⚠️ 이미 등록된 명세서(계약번호)입니다." 라는 명확한 에러 메시지 제공.
    - 입력 필드 옆 실시간 상태 아이콘(체크/경고) 추가.

## ✅ 완료된 작업 (Accomplished Tasks)

- [x] **Backend**: `ocr_service.py` 프롬프트 수정 (Debug Raw Text 추가).
- [x] **Backend**: `inbound.py` 엔드포인트 수정 및 데이터 매핑 버그 수정 (Contract Number, Email, Phone 누락 해결).
- [x] **Frontend**: `InboundPage` (`page.tsx`) 중복 체크 로직 및 에러 핸들링 추가.
- [x] **Test**: `test_ocr_script.py` 작성 및 검증 (Sample File `명세서_1650.PNG` 완벽 인식 확인).

## 🔧 기술 세부사항 (Technical Details)

- **OCR Strategy**: `Gemini` 모델에게 먼저 "헤더 영역의 모든 텍스트를 그대로 적으라(debug_raw_text)"고 지시한 후, 그 텍스트 내에서 패턴(예: `S`로 시작하는 문자열)을 찾도록 유도하여 환각(Hallucination) 및 누락 방지.
- **API Mapping**: `OCRService`가 반환하는 딕셔너리와 `inbound.py`의 `OCRResponse` 스키마 간의 필드 매핑 일치시킴.
- **Duplicate Check**:
  - `GET /api/v1/inbound/check-duplicate/{id}`: 단순 존재 여부 확인 (UI용).
  - `POST /api/v1/inbound/confirm`: 저장 시 최종 방어 (DB 무결성용).

## ⏳ 다음 세션에서 할 일 (Next Session)

1.  **입고 자동화 안정화**: 다양한 명세서 형식에 대한 추가 테스트.
2.  **재고(Inventory) 연동 확인**: 입고 확정 시 실제 재고 수량(Beans Table) 및 로그(Log Table)가 정확히 쌓이는지 모니터링.
3.  **기능 확장**: 필요 시 공급처(Supplier) 관리 페이지 고도화.

## 🛠️ 현재 설정 & 규칙 (Current Setup)

- **Version**: Updated to `0.0.4` (Patch Update 예정).
- **Run Command**: `wsl bash dev.sh` (Cache Clear & Start).
- **Test Script**: `python test_ocr_script.py` (Backend OCR Test).
