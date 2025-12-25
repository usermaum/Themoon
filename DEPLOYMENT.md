# 배포 및 실행 가이드 (Deployment Guide)

개발 환경(Python, Node.js 등)이 전혀 설치되지 않은 새로운 컴퓨터에서 "The Moon" 프로젝트를 실행하기 위한 방법은 크게 두 가지가 있습니다.

## 1. Docker 컨테이너 사용 (가장 추천)
**Docker**는 서버나 서비스를 배포할 때 사용하는 업계 표준 방식입니다. 컴퓨터에 "가상 컨테이너 환경"을 만들어, 그 안에 Python, Node.js 등 모든 실행 환경을 미리 담아두는 방식입니다.

### 장점
*   **환경 일치**: 개발한 컴퓨터와 100% 동일한 환경에서 돌아갑니다. "내 자리에선 되는데 너네 자리에선 안 돼" 문제가 없습니다.
*   **설치 간편**: 대상 컴퓨터에 **Docker Desktop** 프로그램 하나만 설치하면, 나머지(Python, DB 등)는 명령어 한 줄로 자동 설치 및 실행됩니다.

### 실행 방법
1.  새 컴퓨터에 [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치
2.  프로젝트 폴더 내 `docker-compose.yml` 파일 생성 (필요 시 작성해 드립니다)
3.  터미널에서 `docker-compose up` 실행
    *   알아서 Python 다운로드, Node 다운로드, DB 설정, 서버 시작까지 한 번에 완료됩니다.

---

## 2. 포터블(Portable) / 실행 파일 만들기 (단독 실행)
Docker조차 설치하기 어려운 상황이라면, 프로그램을 하나의 실행 파일(`.exe`)이나 폴더로 묶어서 배포하는 방법입니다.

### Python Backend (PyInstaller)
*   **PyInstaller**라는 도구를 사용하여, 우리가 만든 Python 코드와 Python 실행기, 필요한 라이브러리를 모두 합쳐 `themoon_backend.exe` 파일 하나로 만듭니다.
*   사용자는 이 파일만 더블 클릭하면 백엔드 서버가 켜집니다.

### Frontend (Standalone Build / Serve)
*   **Next.js Standalone**: 프론트엔드 빌드 결과물을 `node.exe` 파일과 함께 묶습니다.
*   배치 파일(`.bat`)을 하나 만들어, 이 안에 포함된 `node.exe`로 서버를 켜도록 설정합니다.

### 실행 방법
1.  개발자(저)가 미리 "빌드(Build)" 작업을 통해 `.exe` 파일과 `dist` 폴더를 생성합니다.
2.  이 결과물 폴더를 USB나 클라우드로 새 컴퓨터에 복사합니다.
3.  `start_services.bat`(가칭)을 더블 클릭하면 설치 없이 바로 실행됩니다.

---

## ✅ 추천: Docker
장기적인 서비스 운영 및 유지보수를 위해서는 **1번 Docker** 방식을 강력히 추천합니다. 
