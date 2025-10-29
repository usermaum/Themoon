# 🛑 세션 종료 체크리스트

> 세션을 종료하기 전에 이 체크리스트를 완료하세요!
> 이렇게 하면 다음 세션에서 완벽한 연속성을 유지할 수 있습니다.

---

## ✅ 체크리스트

### 1️⃣ 작업 내용 정리

#### Step 1-1: 오늘 한 일 정리
다음 항목들을 정리하세요:

- [ ] **주요 작업**: 오늘 무엇을 했는가?
- [ ] **완료된 작업**: 구체적으로 뭘 완료했는가?
- [ ] **발견된 문제**: 해결되지 않은 문제가 있는가?
- [ ] **다음 할 일**: 내일 뭘 할 건가?

**예시**:
```
주요 작업: 문서 정리 및 세션 관리 시스템 구축
완료된 작업:
  - Documents/ 폴더를 5개 분류로 정리 (20개 파일)
  - SESSION_SUMMARY_2025-10-27.md 작성
  - SESSION_START_CHECKLIST.md 작성
  - 프로젝트 문서 업데이트

발견된 문제: 없음

다음 할 일:
  1. 컴포넌트 시스템 실제 페이지 적용
  2. 웹페이지 구현
  3. UI 개선
```

#### Step 1-2: SESSION_SUMMARY 파일 작성 또는 업데이트
```bash
# 오늘 날짜로 새 SESSION_SUMMARY 파일 생성
# 파일 이름: Documents/Progress/SESSION_SUMMARY_YYYY-MM-DD.md

# 필수 포함 항목:
# 1. 🎯 오늘 한 일
# 2. ✅ 완료된 작업
# 3. 🔧 기술 세부사항
# 4. ⏳ 다음 세션에서 할 일
# 5. 🛠️ 현재 설정 & 규칙
```

**참고**: `Documents/Progress/SESSION_SUMMARY_2025-10-27.md` 형식 참고

---

### 2️⃣ 코드 변경사항 확인

#### Step 2-1: 변경된 파일 확인
```bash
# 추적되지 않은 파일 확인
git status

# 변경사항 확인
git diff --stat
```

**확인 항목**:
- [ ] 의도하지 않은 변경이 있는가?
- [ ] 중요한 파일이 빠졌는가?
- [ ] 삭제되면 안 되는 파일이 삭제되었는가?

#### Step 2-2: 코드 품질 확인
```bash
# Python 구문 오류 확인 (선택)
./venv/bin/python -m py_compile app/app.py

# 앱 실행 테스트 (선택)
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true &
sleep 5
curl -s http://localhost:8501 | head -10
pkill -f streamlit
```

**확인 항목**:
- [ ] 앱이 정상 실행되는가?
- [ ] 에러가 발생하지 않는가?

---

### 3️⃣ 버전 관리

#### Step 3-1: 버전 업데이트 (필요시)
```bash
# 현재 버전 확인
cat logs/VERSION

# 버전 업데이트 (필요시)
./venv/bin/python logs/update_version.py \
  --type patch \
  --summary "오늘의 작업 요약"

# 또는 CHANGELOG.md 직접 수정
```

**버전 업데이트 기준**:
- **PATCH** (0.1.0 → 0.1.1): 버그 수정
- **MINOR** (0.1.0 → 0.2.0): 새 기능 추가
- **MAJOR** (0.1.0 → 1.0.0): 호환성 깨지는 변경

#### Step 3-2: CHANGELOG 확인
```bash
# 최근 변경사항 확인
head -50 logs/CHANGELOG.md
```

**확인 항목**:
- [ ] CHANGELOG.md가 최신인가?
- [ ] 오늘의 작업이 기록되어 있는가?

---

### 4️⃣ Git 커밋

#### Step 4-1: 모든 변경사항 스테이징
```bash
# 변경사항 확인
git status

# 모든 변경사항 스테이징
git add .

# 다시 한 번 확인
git diff --cached --stat
```

**확인 항목**:
- [ ] 커밋하려는 파일들이 맞는가?
- [ ] 실수로 커밋할 파일이 없는가?
- [ ] 민감한 파일은 제외되었는가?

#### Step 4-2: 적절한 커밋 메시지 작성
```bash
# 커밋 메시지 형식
# type: 한글 설명

# 예시:
git commit -m "docs: 세션 관리 시스템 완성
- SESSION_SUMMARY_2025-10-27.md 작성
- SESSION_START_CHECKLIST.md 작성
- SESSION_END_CHECKLIST.md 작성

이를 통해 다음 세션에서 완벽한 연속성 유지 가능"
```

**커밋 타입**:
- **feat**: 새로운 기능
- **fix**: 버그 수정
- **refactor**: 코드 정리/리팩토링
- **docs**: 문서 작성/수정
- **chore**: 설정 변경, 패키지 업데이트

#### Step 4-3: 커밋 확인
```bash
# 커밋 후 상태 확인
git status

# 최근 커밋 확인
git log --oneline -3
```

**확인 항목**:
- [ ] `git status`가 "nothing to commit"인가?
- [ ] 최근 커밋이 올바른가?
- [ ] 커밋 메시지가 명확한가?

---

### 5️⃣ 최종 확인

#### Step 5-1: 모든 문서의 버전 동기화 (⚠️ 매우 중요)
```bash
# 1️⃣ 현재 버전 확인
CURRENT_VERSION=$(cat logs/VERSION)
echo "📦 현재 버전: $CURRENT_VERSION"

# 2️⃣ README.md의 모든 버전 정보를 현재 버전으로 업데이트
# 다음 위치들을 모두 확인하고 수정:
# - Line 3: v1.2.0 → v$CURRENT_VERSION
# - Line 7: v1.2.0 → v$CURRENT_VERSION
# - Line 11, 67, 492, 503, 537 등 모든 버전 표기
# - Line 501: 마지막 커밋 해시 업데이트

# 3️⃣ .claude/CLAUDE.md의 버전도 동기화
# - Line 4: 버전: 1.2.0 → 버전: $CURRENT_VERSION

# 4️⃣ 최근 커밋 확인
git log --oneline -1

# 5️⃣ git status로 변경사항 확인
git status
```

**⚠️ 필수 업데이트 항목** (모두 확인!):

📄 **README.md**:
- [ ] **버전 번호**: `v1.2.0` → `v$(cat logs/VERSION)` (모든 위치)
- [ ] **라인 3**: 타이틀의 버전
- [ ] **라인 7**: 프로젝트 상태 라인의 버전
- [ ] **라인 492-502**: "프로젝트 정보" 섹션의 버전
- [ ] **라인 501**: "최종 커밋" 해시값 업데이트
- [ ] **라인 637-645**: 마지막 요약 라인들

📄 **.claude/CLAUDE.md**:
- [ ] **라인 4**: `버전: 1.2.0` → `버전: $(cat logs/VERSION)`

**💡 팁**: 에디터의 "모두 바꾸기" 기능(Ctrl+H)으로 `1.2.0` → `[최신버전]` 일괄 변경 가능

#### Step 5-2: 문서 정리 확인
```bash
# 모든 문서가 Documents/ 폴더에 있는지 확인
ls -la | grep -E "\.md$|\.docx$|\.xlsx$" || echo "✅ 루트에 문서 없음"

# Documents/ 구조 확인
find Documents -type f | wc -l
```

**확인 항목**:
- [ ] 프로젝트 루트에 문서 파일이 없는가?
- [ ] 모든 문서가 Documents/ 폴더에 있는가?
- [ ] 각 문서가 올바른 분류 폴더에 있는가?

#### Step 5-3: 최종 Git 상태 확인
```bash
# 마지막 확인
git status
git log --oneline -5

# 원격 저장소와 비교 (선택)
git status -u
```

**확인 항목**:
- [ ] 워킹 트리가 깨끗한가?
- [ ] 모든 변경사항이 커밋되었는가?
- [ ] 원격 저장소와 동기화되었는가?

---

## 🚀 체크리스트 완료 확인표

모든 항목을 완료했으면 아래 체크를 하세요:

```
작업 내용 정리
  [✅] 오늘 한 일 정리
  [✅] SESSION_SUMMARY 파일 작성

코드 변경사항 확인
  [✅] 변경된 파일 확인
  [✅] 코드 품질 확인

버전 관리
  [✅] 버전 업데이트 (필요시)
  [✅] CHANGELOG 확인

Git 커밋
  [✅] 변경사항 스테이징
  [✅] 적절한 메시지로 커밋
  [✅] 커밋 확인

최종 확인
  [✅] README 업데이트
  [✅] 문서 정리 확인
  [✅] Git 상태 최종 확인

모든 항목 완료! 🎉
```

---

## 📋 빠른 종료 (5분)

시간이 없으면 최소한 이것만 해세요:

```bash
# 1. 변경사항 확인
git status

# 2. SESSION_SUMMARY 작성 여부 확인
ls -lt Documents/Progress/SESSION_SUMMARY_*.md | head -1

# 3. 모든 것 커밋
git add .
git commit -m "docs: 세션 종료 - $(date +%Y-%m-%d)"

# 4. 최종 확인
git status
git log --oneline -1
```

---

## 💡 팁

### 커밋 메시지 예시

**좋은 예**:
```
feat: 새로운 분석 기능 추가

- 월별 비용 분석 차트 추가
- 원두별 사용량 분석 구현
- ROI 분석 기능 추가

테스트 완료: 모든 기능 정상 작동
```

**나쁜 예**:
```
update
fix bug
작업 완료
```

### 자주 하는 실수

❌ **피해야 할 것**:
1. 변경사항을 커밋하지 않고 종료
2. SESSION_SUMMARY 파일을 만들지 않음
3. Git에 추적되지 않은 중요 파일이 있는 상태
4. 문서를 프로젝트 루트에 저장

✅ **해야 할 것**:
1. 모든 변경사항을 명확하게 커밋
2. SESSION_SUMMARY로 진행 상황 기록
3. 정기적으로 버전 업데이트
4. 모든 문서는 Documents/ 폴더에만 저장

---

## 🎉 모든 항목을 완료했으면

다음 세션에서는:
1. `Documents/Progress/SESSION_START_CHECKLIST.md` 읽기
2. 이전 세션 요약 확인
3. 완벽한 연속성으로 작업 시작!

**좋은 세션 종료! 다음 세션에서 만나요! 👋**
