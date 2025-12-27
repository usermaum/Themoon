# Session Summary: 2025-12-26 (Environment Recovery & WSL Migration)

## 📌 요약 (Summary)
WSL 환경과 Windows 환경 혼용으로 인해 발생한 `next` 바이너리 실행 불가 및 `next: not found` 에러를 해결하고, 프로젝트 실행 환경을 **100% WSL 기반**으로 복구했습니다.

## 🛠️ 작업 내용 (Changes)

### 1. 환경 복구 및 의존성 재설치 (Environment Recovery)
- **Frontend (`node_modules`)**: Windows용 바이너리 제거 후 `swc-linux-x64-gnu` (WSL용) 컴파일러가 포함된 버전으로 재설치.
- **Backend (`venv`)**: `venv` 재생성 및 `pip install` 재실행으로 리눅스용 패키지 호환성 확보.

### 2. `dev.sh` 스크립트 수정
- **WSL 감지 로직 고도화**: WSL 내부에서 실행 시 불필요하게 `wsl` 커맨드를 호출하지 않도록 조건문 수정.
  - 기존: `/proc/version` 단순 문자열 검색
  - 수정: `WSL_DISTRO_NAME` 환경변수 체크 추가

### 3. 문서 업데이트 (Documentation)
- **`README.md`**: 최상단에 "WSL 환경 필수" 경고문 추가 (`dev.sh` 사용 권장).
- **`.agent/AGENTS.md`**: AI 에이전트가 Windows 환경에서 커맨드를 실행하지 못하도록 하는 Mandatory Rule 추가.

### 4. 문제 해결 (Troubleshooting)
- **Server Connectivity**: Windows Browser에서 `localhost` 접속이 불안정한 문제를 WSL Direct IP (`172.19.xxx.xxx`) 접속으로 우회 해결.
- **Build Crash**: `npm run build` 시 메모리 부족 추정 이슈 확인 (향후 `dev --turbo` 또는 Docker 컨테이너화 고려).

## 📅 다음 세션 계획 (Next Steps)
1. **Frontend Performance**: `next dev --turbo` 안정화 또는 메모리 최적화.
2. **Feature Development**: 로스팅 이력 필터링 및 데모 페이지 구현 (기존 작업 이어가기).
