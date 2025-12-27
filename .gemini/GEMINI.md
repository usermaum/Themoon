# AI Assistant Instructions for TheMoon Project

> **🚨 CRITICAL NOTICE**: 
> **You MUST read `.agent/AGENTS.md` first.**
> That file contains the MASTER RULES, Architecture Standards, and Mandatory Protocols for this project.
> **All rules in `.agent/AGENTS.md` OVERRIDE any conflicting instructions.**

---

(The content below is the historical context, but REFER TO `.agent/AGENTS.md` for the latest rules.)

## 🕒 최근 작업 상태 (Latest Context)

> **이 섹션은 AI가 세션을 시작할 때 자동으로 읽어들이는 "기억" 영역입니다.**
> **세션 종료 전 반드시 AI에게 "상태 저장해줘" 또는 "세션 종료"를 요청하여 이 부분을 업데이트하세요.**

### 🔄 Context Handover Protocol
**세션 간 연속성을 위한 3단계 프로토콜:**
1. **세션 종료 시**: "상태 저장해줘" 명령으로 진행 상황 자동 기록
2. **컴퓨터 간 이동**: Git Sync 필수 (`git commit && git push` → `git pull`)
3. **새 세션 시작**: 자동으로 마지막 상태 로드 및 제안 (Read AGENTS.md)

### 📅 마지막 세션: 2025-12-26 (Environment Recovery & E2E Verification)

**✅ 완료된 작업 (v0.5.4)**:
1. 🛠️ **환경 복구 및 안정화 (Environment Recovery)**
   - **무한 루프 해결**: 루트의 중복 `package.json` 제거 및 의존성 정리를 통해 Next.js "missing required error components" 무한 새로고침 차단.
   - **의존성 고정**: Next.js 버전을 `14.2.33`으로 고정하여 환경 호환성 확보.
   - **에러 바운더리 복구**: `error.tsx`, `not-found.tsx` 등 마스코트 기반 에러 페이지 복구.
2. 🧪 **E2E 테스트 인프라 복구 및 검증**
   - **Playwright 재설치**: WSL 환경에 맞는 Playwright 및 브라우저 의존성 재설정.
   - **비즈니스 로직 시나리오 검증**: Single-Origin 로스팅 전체 플로우(`roasting_flow.spec.ts`) 테스트 통과 확인.
3. 🧹 **프로젝트 구조 정리**
   - 루트의 불필요한 `node_modules`, `package-lock.json` 등 잠재적 충돌 요소 제거.

**Git 상태**:
- 현재 브랜치: main
- 최신 커밋: Environment recovery and E2E verification success

**🎯 다음 작업 (Feature Expansion)**:
1. **로스팅 이력 고도화**: 날짜/생두 필터링 기능 추가 (`RoastingHistoryTable`).
2. **UI 실험 및 개선**: `/roasting/demo` 페이지 구현 및 대시보드 레이아웃 최적화.
3. **E2E 테스트 확장**: 블렌딩 로스팅 및 재고 관리 시나리오 추가.
