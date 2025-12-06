# 세션 요약: 로스팅 프로세스 구현 및 안정화 (0.0.5)

**날짜**: 2025-12-06 (심야)
**버전**: 0.0.5

## 1. 주요 성과

- **로스팅 메뉴 추가**: 사이드바에 'Roasting' 메뉴 생성 (`/roasting/single-origin`).
- **DB 시딩 문제 해결**: `recreate_db.py` 실행 시 발생하는 경로 문제(루트 vs backend 폴더)를 해결하여 `themoon.db` 동기화 완료.
- **API CORS 해결**: 프론트엔드(3500)와 백엔드(8000) 간의 통신 문제(`Network Error`)를 `config.py` 수정을 통해 해결.
- **WSL 환경 이슈 해결**: 윈도우와 WSL 간의 명령어 혼선 및 포트 충돌(`EADDRINUSE`) 문제 해결 가이드 확립.

## 2. 발생한 문제 및 해결책 (Troubleshooting)

### Q1. DB에 데이터가 안 들어감 (No beans found)

- **원인**: `recreate_db.py`를 프로젝트 루트에서 실행하면 루트에 `themoon.db`가 생기지만, 서버(`uvicorn`)는 `backend` 폴더에서 실행되어 `backend/themoon.db`를 참조함.
- **해결**: 시딩 스크립트를 반드시 `backend` 폴더 내부에서 실행하도록 변경.

  ```bash
  cd backend
  ../venv/bin/python scripts/recreate_db.py
  ```

### Q2. Axios Network Error

- **원인**: `frontend`는 3500 포트, `backend`는 3000 포트만 CORS 허용함.
- **해결**: `backend/app/config.py`의 `BACKEND_CORS_ORIGINS`에 `http://localhost:3500` 추가.

### Q3. EADDRINUSE (포트 충돌)

- **원인**: 터미널을 여러 개 띄워놓고 `dev.sh`를 중복 실행하거나, 비정상 종료 후 프로세스가 남음.
- **해결**: 모든 터미널 종료 후 프로세스 강제 정리.

  ```bash
  lsof -ti :3500,8000 | xargs kill -9
  ```

## 3. 남은 과제

- **블렌드 기능**: 현재 `/blends` 페이지 및 API가 미구현 상태임. 다음 세션의 최우선 과제.
- **테스트 코드**: 로스팅 로직에 대한 단위 테스트 추가 필요.
- **배포**: 변경된 DB 스키마 및 설정을 프로덕션(Render.com)에 적용해야 함.

## 4. 실행 가이드 (최종)

```bash
# 1. 서버 실행
./dev.sh

# 2. (필요 시) DB 데이터 초기화
cd backend
../venv/bin/python scripts/recreate_db.py
```
