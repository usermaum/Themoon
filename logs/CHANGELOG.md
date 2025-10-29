# 변경 로그 (Changelog)

모든 주목할 만한 프로젝트 변경사항은 이 파일에 문서화됩니다.

## 버전 관리 규칙 (Semantic Versioning)

- **MAJOR.MINOR.PATCH** 형식 사용
  - MAJOR: 대규모 기능 추가 또는 호환성 깨지는 변경
  - MINOR: 새로운 기능 추가 (하위 호환성 유지)
  - PATCH: 버그 수정 (하위 호환성 유지)

---

## [0.2.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): 3가지 기능 개선 적용

#### 📝 변경사항
1. **BlendManagement.py** - 레시피 편집 UI 추가
   - 기존 블렌드의 레시피 선택 및 수정 기능 추가 (Lines 455-520)
   - 원두와 포션 개수 수정 가능
   - 저장 및 삭제 버튼으로 레시피 관리 개선

2. **InventoryManagement.py** - 재고 범위 설정 커스터마이징
   - 최소/최대 재고량을 원두별로 설정 가능 (Lines 250-270)
   - 기본값 유지 (최소: 5.0kg, 최대: 50.0kg)
   - 입고 시 사용자 정의 범위 적용 (Lines 285-286)

3. **Settings.py** - 데이터 초기화 확인 로직 개선
   - 두 단계 확인 프로세스로 실수 방지 (Lines 467-507)
   - st.session_state를 통한 상태 관리
   - 명확한 경고 메시지와 취소 버튼 제공

## [0.1.0] - 2025-10-29

### 🎯 초기 버전

#### 📝 변경사항
- 프로젝트 시작: 버전 리셋 및 새로운 버전 관리 시스템 도입
- 효율적인 버전관리 전략 수립 (logs/VERSION_STRATEGY.md)
- 세션 관리 시스템 완성 (SESSION_START_CHECKLIST, SESSION_END_CHECKLIST)
- 작업 완료 후 처리 프로세스 명시

#### 🔄 버전 관리 개선
- PATCH/MINOR/MAJOR 누적 기준 명확화
- 모든 문서(README.md, CLAUDE.md) 버전 동기화 규칙 추가
- 버전 올리는 기준: PATCH(버그 3개+), MINOR(기능 3~4개+), MAJOR(호환성 변경)

#### 📚 문서화 완성
- logs/VERSION_STRATEGY.md 생성
- Documents/Progress/SESSION_SUMMARY_2025-10-29.md 생성
- CLAUDE.md에 "⚡ 빠른 버전 관리 참고" 섹션 추가
- SESSION_END_CHECKLIST.md 상세화

---

## 🎯 향후 버전 계획

```
현재: 0.1.0 (초기 버전)
  ↓
2주 후: 0.1.1 (버그 수정 3개)
4주 후: 0.1.2 (문서 개선 5개)
6주 후: 0.2.0 (새 기능 3~4개) ← MINOR
8주 후: 0.2.1 (버그 수정 2개)
12주 후: 1.0.0 (프로덕션 배포) ← MAJOR
```

---

**마지막 업데이트**: 2025-10-29
