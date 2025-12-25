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

### 📅 마지막 세션: 2025-12-26 (Roasting UX & Safety Refinement)

**✅ 완료된 작업 (v0.5.3)**:
1. 🛡️ **로스팅 안전장치 강화 (Blocking Validation)**
   - **재고 부족 차단**: Blend/Single Origin 로스팅 시 재고 부족이 감지되면 '확인' 버튼을 비활성화하여 마이너스 재고 발생 원천 차단.
   - **Red Theme Alert**: 기존의 단순한 Dialog를 붉은색 테마의 경고창으로 교체하여 시인성 강화.
2. 📊 **재고 상태 시각화 (Embedded Banner)**
   - **Blend Stock Banner**: 명세서 카드 내부에 재고 상태(충분/부족)를 실시간으로 보여주는 배너 추가.
   - **Responsive Design**: 카드 내부 공간에 맞춰 마진/패딩 최적화 (`p-3`, `text-base`).
3. 🔧 **UI/UX 폴리싱**
   - **숫자 포맷팅**: `formatWeight` 유틸리티 전면 적용 (불필요한 소수점 제거 `30.00` -> `30`).
   - **삭제 UX 개선**: `window.confirm`을 커스텀 `AlertDialog`로 교체하여 일관된 경험 제공.

**Git 상태**:
- 현재 브랜치: main
- 최신 커밋: Roasting UX and Safety Improvements

**🎯 다음 작업 (Feature Expansion)**:
1. `BeanRepository` 구현 및 Service 리팩토링 (Domain Driven Design 적용)
2. Phase 2: 로스팅 로그 시스템 고도화 (신규 아키텍처 연동)
3. 관리자 냥이 마스코트를 활용한 에러 페이지 및 빈 상태 UI 확장
