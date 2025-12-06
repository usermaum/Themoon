# 세션 요약: The Green Bean Vault 및 서버 최적화 (2025-12-06)

## 1. 🎯 오늘 한 일

* **Green Bean Vault (생두 보관소) 컨셉 페이지 구현**:
  * `Themoon_Rostings_v2.md` 데이터를 기반으로 한 생두 재고 현황 페이지 (`/design-sample/green-bean-vault`) 개발.
  * High-Fidelity CSS & SVG Implementation: 이미지 생성 제한에 대응하기 위해 CSS 텍스처(마대자루, 크라프트지)와 CSS 필터(로스팅 원두 -> 생두 변환)를 사용하여 고품질 시각 효과 구현.
  * 인터랙티브 UI: 마우스 호버 효과, 애니메이션 로고, 재고량에 따른 상태 표시 등.
* **원두 이미지 프롬프트 체계화**:
  * **V2 (생두)**: 질감 중심의 Full-frame Macro 스타일 프롬프트 작성.
  * **V3 (원두)**: 로스팅 포인트(Light/Dark)별 시각적 차이를 반영한 프롬프트 작성. (블렌드 3종 포함)
  * 폴더 구조 제안: `public/images/raw-material/` 및 `public/images/roasted/`로 이원화.
* **서버 연결 문제 해결 및 최적화**:
  * **WSL ↔ Windows 네트워크 문제 해결**: `0.0.0.0` 호스트 바인딩 적용 및 포트 충돌 해결.
  * **Frontend 포트 변경**: 충돌 방지를 위해 `3000` -> `3500` 포트로 변경.
  * **내부 IP 접속 지원**: `localhost` 연결 거부 시 사용할 수 있는 WSL 내부 IP 접속 링크 자동 생성 기능 추가 (`dev.sh`, `start_all.sh`).
* **Frontend 엔진 대규모 업데이트**:
  * **Clean Install**: `node_modules` 전체 삭제 후 재설치.
  * **Version Update**: Next.js 14 (Stable), React 18, Tailwind CSS 3 등 안정적인 최신 버전으로 엔진 교체 (초기 Next 16 베타 호환성 문제 해결).

## 2. ✅ 완료된 작업

* [x] `app/design-sample/green-bean-vault/page.tsx` 구현 완료
* [x] `Documents/Planning/Bean_Image_Prompts_V2.md` (생두) 작성 완료
* [x] `Documents/Planning/Bean_Image_Prompts_V3.md` (원두 Light/Dark) 작성 완료
* [x] `dev.sh` 및 `start_all.sh` 서버 시작 스크립트 수정 (0.0.0.0 바인딩, 포트 3500, 내부 IP 출력)
* [x] Frontend `package.json` 의존성 최신화 및 안정화

## 3. 🔧 기술 세부사항

* **Visual Engineering**: AI 이미지 생성이 막힌 상황에서 CSS `filter: hue-rotate()`와 SVG `path` 조작을 통해 생두 이미지를 시뮬레이션하고 빈티지 로고를 직접 코드로 그림.
* **Network Config**: WSL2 환경에서 `localhost` 포워딩 이슈 해결을 위해 `next dev -H 0.0.0.0 -p 3500` 옵션 사용.
* **Dependency Management**: Next.js 16 (Canary/RC) 도입 시도 후 Peer Dependency 충돌 발생 -> Next.js 14 (LTS)로 롤백하여 안정성 확보.

## 4. ⏳ 다음 세션에서 할 일

* **이미지 생성**: 할당량 리셋 후 V2(생두), V3(원두) 프롬프트를 사용하여 실제 고해상도 이미지 생성 및 적용.
* **로스팅 프로세스 UI**: 실제 로스팅 기록 및 관리 기능을 위한 Dashboard UI 구현.
* **블렌딩 시스템**: 싱글 오리진을 조합하여 블렌드(풀문, 뉴문 등)를 만드는 인터페이스 구현.

## 5. 🛠️ 현재 설정 & 규칙

* **Frontend Port**: `3500` (기존 3000에서 변경됨)
* **Backend Port**: `8000`
* **이미지 경로**: `public/images/beans/` (향후 `raw-material` 및 `roasted`로 분리 예정)
* **서버 실행**: `wsl bash dev.sh` 또는 `wsl bash start_all.sh` (자동으로 내부 IP 안내됨)
