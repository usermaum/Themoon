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

### 📅 마지막 세션: 2025-12-28 (Multi-Order Processing System)

**✅ 완료된 작업 (v0.6.3.1 - Production Ready)**:
1. **DB Migration 적용**: `order_number` 컬럼 추가 (SQLite, indexed)
2. **OCR 후처리 검증**: 3개 주문 그룹화 테스트 통과 (Mock 데이터)
3. **Backend API 확인**: 서버 정상 실행, 엔드포인트 검증 완료
4. **최종 검증**: `MULTI_ORDER_SYSTEM_VERIFICATION.md` 리포트 작성
5. **Parallel Agents**: Agent 2 (Frontend), Agent 3 (Backend) 동시 실행 완료

**📋 Multi-Order System 상세**:
- 입고 문서 내 여러 주문번호(YYYYMMDD-XXXXX) 자동 감지 및 그룹화
- User-driven 워크플로우: 모달 UI로 개별 주문 선택 처리
- IMG_1660.JPG 사례: 3개 주문 (20251108-8B7C2, 20250926-8BD28, 20250822-9533C)
- 관련 파일: `backend/migrations/add_order_number_to_inbound_items_sqlite.sql`

**🎯 다음 작업 (Next Step)**:
1. **Production 배포** (Optional): DB Migration → Backend/Frontend 배포
2. **E2E 테스트** (Optional): 실제 IMG_1660.JPG 이미지로 전체 플로우 검증
3. **Repository Pattern 확장**: `BeanRepository` 외 타 모듈 적용
4. **Phase 2 고도화**: 신규 아키텍처 기반 로스팅 로그 연동
