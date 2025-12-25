# CLAUDE.md - Project Guide Navigator

> **🚨 CRITICAL NOTICE**: 
> **You MUST read `.agent/AGENTS.md` first.**
> That file contains the MASTER RULES, Architecture Standards, and Mandatory Protocols for this project.
> **All rules in `.agent/AGENTS.md` OVERRIDE any conflicting instructions.**

---

(The content below is historical context. Always refer to `.agent/AGENTS.md` for the single source of truth.)

## 🕒 최근 작업 상태 (Latest Context)

> **이 섹션은 AI가 세션을 시작할 때 자동으로 읽어들이는 "기억" 영역입니다.**
> **세션 종료 전 반드시 AI에게 "상태 저장해줘" 또는 "세션 종료"를 요청하여 이 부분을 업데이트하세요.**

### 🔄 Context Handover Protocol
**세션 간 연속성을 위한 3단계 프로토콜:**
1. **세션 종료 시**: "상태 저장해줘" 명령으로 진행 상황 자동 기록
2. **컴퓨터 간 이동**: Git Sync 필수 (`git commit && git push` → `git pull`)
3. **새 세션 시작**: 자동으로 마지막 상태 로드 및 제안 (Read AGENTS.md)

### 📅 마지막 세션: 2025-12-25 (Premium UI & Monitoring)

**✅ 완료된 작업 (v0.5.2)**:
1. **Admin Dashboard**: 시스템 자원(CPU/MEM/Disk) 모니터링 및 도구 통합.
2. **Premium UX**: "관리자 냥이" 재시작 테마 및 리얼 물방울 효과 구현.
3. **Bug Fix**: SSR/Portal 500 에러 해결 및 TSConfig 정규화.

**🎯 다음 작업 (Next Step)**:
1. **Repository Pattern 확장**: `BeanRepository` 외 타 모듈 적용.
2. **Phase 2 고도화**: 신규 아키텍처 기반 로스팅 로그 연동.
