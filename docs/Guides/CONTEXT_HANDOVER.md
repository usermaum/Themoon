# AI 협업 컨텍스트 핸드오버 규칙 (Context Handover Rules)

Antigravity(Gemini)와 Claude Code 간의 원활한 업무 이관을 위해 다음 규칙을 준수합니다.

## 1. 핸드오버 파일 생성 규칙
사용자가 **"클로드 전달"** 또는 **"Context Save"**라고 요청하거나, Antigravity의 작업 단계(Plan/Execute)가 완료되면 **반드시** 아래 형식의 파일을 생성 또는 업데이트해야 합니다.

- **파일 경로**: `Documents/Handover/TO_CLAUDE.md` (없으면 생성)
- **파일 경로(역방향)**: `Documents/Handover/TO_ANTIGRAVITY.md` (Claude가 작성)

## 2. TO_CLAUDE.md 템플릿

```markdown
# To: Claude Code
**From**: Antigravity (Gemini 3 Pro)
**Date**: YYYY-MM-DD HH:MM

## 1. 완료된 작업 (Done)
- [x] 구현한 기능 요약 1
- [x] 수정한 파일 목록 및 주요 변경점

## 2. 요청 사항 (Request)
> Claude야, 다음 작업을 수행해줘:

1. **[검증/Verify]**: 위에서 작성한 `implementation_plan.md`의 아키텍처가 적절한지 검토.
2. **[테스트/Test]**: `frontend/app/page.tsx` 기능이 정상 동작하는지 테스트 스크립트 작성 및 실행.
3. **[피드백/Feedback]**: 버그나 개선 사항이 있다면 `TO_ANTIGRAVITY.md`에 남겨줘.

## 3. 핵심 컨텍스트 (Context)
- 관련 파일: `path/to/file1.ts`, `path/to/file2.tsx`
- 주의 사항: (예: DB 마이그레이션이 필요함, API 키 설정 필요 등)
```

## 3. 사용자 행동 가이드
사용자는 이 파일이 생성되었다는 알림을 받으면, **파일 내용을 복사(Ctrl+C)하여 Claude Code 터미널에 붙여넣기(Ctrl+V)**만 하면 됩니다.
