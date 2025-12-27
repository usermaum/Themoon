# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

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
