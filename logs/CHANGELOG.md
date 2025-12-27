# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [0.6.3.1] - 2025-12-28

### Added
- **Database**: SQLite migration script for `order_number` column
  - `backend/migrations/add_order_number_to_inbound_items_sqlite.sql`
  - Indexed VARCHAR(100) column for performance optimization
- **Documentation**: Final verification report
  - `docs/Progress/MULTI_ORDER_SYSTEM_VERIFICATION.md`
  - 6-layer verification checklist (DB/OCR/API/Frontend/Docs/Tests)
  - Production deployment guide
- **Testing**: OCR post-processing test passed
  - 3-order grouping verified (IMG_1660.JPG mock)
  - Subtotal calculation: 1,794,000원

### Fixed
- **Migration**: Applied `order_number` column to production database
- **Backend**: API server verified running on port 8000

### Changed
- **Docs**: Updated GEMINI_TASKS.md with Phase 26
- **Docs**: Updated CLAUDE.md session context (2025-12-28)

## [0.6.3] - 2025-12-27

### Added
- **Multi-Order Processing System**: Complete implementation
  - **Backend** (Agent 3):
    - `InboundItem` model: `order_number` column (nullable, indexed)
    - OCR prompt: STEP 5-1 order number extraction instructions
    - OCR service: `_post_process_ocr_result()` for grouping by order_number
    - Pydantic schema: `OCRItem.order_number` field
    - API endpoint: `/api/v1/inbound/analyze` saves order_number
  - **Frontend** (Agent 2):
    - TypeScript interfaces: `OrderGroup`, updated `InboundItem`
    - 8 state variables for multi-order workflow
    - 6 event handlers (accept, cancel, add, confirm)
    - 4 UI components: Multi-Order Modal, Cancel Dialog, Add Dialog, Pending List
    - Amber/Red theme alert dialogs with clear warnings
  - **Testing**:
    - Mock data: `mock_multi_order_ocr_response.json` (3 orders)
    - Unit test: `test_multi_order_processing.py` (all passed)
    - 6-layer verification script
  - **Documentation**:
    - `backend/docs/OCR_ORDER_NUMBER_EXTRACTION.md`
    - `docs/Progress/MULTI_ORDER_FRONTEND_IMPLEMENTATION.md`
    - `backend/IMPLEMENTATION_SUMMARY_MULTI_ORDER.md`

### Technical Details
- **Parallel Agent Execution**: Agent 2 (Frontend) + Agent 3 (Backend) ran simultaneously
- **User-Driven Workflow**: Manual order selection (not automatic splitting)
- **Date Extraction**: YYYYMMDD → YYYY-MM-DD conversion
- **Format Validation**: YYYYMMDD-XXXXX pattern with regex verification

## [0.6.2] - 2025-12-27

### Added
- **MAS Claude Plugin**: Multi-Agent System plugin for Claude Code
  - `.claude/plugins/mas-agents/`: Plugin structure with 3 agents
  - Agent 2 (Frontend): `agent-2-frontend.md`
  - Agent 3 (Backend): `agent-3-backend.md`
  - Agent 4 (Maintainer): `agent-4-maintainer.md`
- **Repository Pattern**: Extended to RoastingLog, Inbound, Blend
  - `RoastingLogRepository`: Enhanced with DDD patterns
  - Unit tests: `test_roasting_log_repository.py`
- **Inbound Schema**: Added detailed OCR response fields
- **Roasting Schema**: Added stock validation fields

### Changed
- **Architecture**: AGENTS.md with comprehensive plugin integration guide
- **Testing**: Added conftest.py with shared fixtures

## [0.6.0] - 2025-12-27

### Added
- **MAS (Multi-Agent System)**: 4인 에이전트 체제 도입 (Architect, Frontend, Backend, Maintainer)
  - 에이전트별 Claude Marketplace 스킬 매핑 (`frontend-design`, `pr-review-toolkit`, `code-review`, etc.)
  - 역할 전환 프로토콜 및 협업 시나리오 정의
  - 허용 도구(Tools) 명시 및 권한 체계 확립
- **Frontend**: 404 에러 페이지 개선
  - 떠다니는 커피 원두 애니메이션 6개 (각각 다른 속도와 궤도)
  - 부드러운 3색 그라데이션 배경 (Latte 테마)
  - 버튼 hover 효과 강화 (scale, shadow)
- **Documentation**: MAS 관련 문서 체계 구축
  - `docs/Planning/MAS_ENHANCEMENT_PLAN.md`: MAS 개선 플랜
  - `docs/Planning/MAS_IMPLEMENTATION_TASKS.md`: 구현 작업 체크리스트
  - `.agent/AGENTS.md`: 스킬/도구 매핑 및 협업 프로토콜 추가

### Changed
- **Architecture**: Clean Architecture 적용 범위 명시 (신규 기능 필수)
- **Tailwind**: 커스텀 애니메이션 추가 (float-slow, float-medium, float-fast, float-reverse)

## [0.5.5] - 2025-12-26

### Fixed
- **Environment**: Fixed `next: not found` error by reinstalling `node_modules` with Linux (WSL) specific binaries.
- **Script**: Updated `dev.sh` to correctly detect WSL environment and prevent recursive `wsl` command execution.
- **Docs**: Added mandatory "WSL Environment Only" warnings to `README.md` and `AGENTS.md`.

### Changed
- **Dependencies**: Re-initialized frontend (`node_modules`) and backend (`venv`) dependencies for clean WSL compatibility.

## [v0.5.4] - 2025-12-26
- Recovery of environment and E2E verification success.
