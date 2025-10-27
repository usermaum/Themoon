# 🚀 빠른 시작 가이드 - 버전 관리 자동화

## ✅ 완전 자동화되었습니다!

더 이상 수동으로 버전을 업데이트할 필요가 없습니다.
Git 커밋 메시지 규칙을 따르면 **자동으로** 버전과 변경로그가 업데이트됩니다!

---

## 📝 Git 커밋 메시지 규칙

### 1️⃣ 버그 수정 (PATCH: 0.1.0 → 0.1.1)

```bash
git commit -m "fix: 폼 제출 버튼 오류 수정"
# 또는
git commit -m "🐛 폼 제출 버튼 오류 수정"
```

**자동 실행:**
- `VERSION`: 0.1.0 → 0.1.1
- `CHANGELOG.md`: 패치 버전 섹션 추가

---

### 2️⃣ 새 기능 추가 (MINOR: 0.1.0 → 0.2.0)

```bash
git commit -m "feat: 고급 분석 기능 추가"
# 또는
git commit -m "✨ 고급 분석 기능 추가"
```

**자동 실행:**
- `VERSION`: 0.1.0 → 0.2.0
- `CHANGELOG.md`: 마이너 버전 섹션 추가

---

### 3️⃣ 호환성 변경 (MAJOR: 0.1.0 → 1.0.0)

```bash
git commit -m "🚀 데이터베이스 스키마 대폭 개선"
# 또는
git commit -m "BREAKING CHANGE: API 재설계"
```

**자동 실행:**
- `VERSION`: 0.1.0 → 1.0.0
- `CHANGELOG.md`: 메이저 버전 섹션 추가

---

## 🔄 작업 흐름

### Step 1️⃣: 기능 개발 또는 버그 수정

```bash
# 파일 수정...
# 코드 작성...
```

### Step 2️⃣: Git에 추가

```bash
git add .
```

### Step 3️⃣: 커밋 (규칙 따르기)

```bash
# 버그 수정 예시
git commit -m "fix: Excel 내보내기 오류 수정"

# 새 기능 예시
git commit -m "feat: 실시간 데이터 동기화 추가"

# 호환성 변경 예시
git commit -m "🚀 데이터베이스 마이그레이션 완료"
```

### Step 4️⃣: 자동으로 모든 것이 처리됨! ✅

```
커밋 완료!
├─ VERSION 파일 자동 업데이트 ✅
├─ CHANGELOG.md 자동 업데이트 ✅
└─ 버전 정보 콘솔에 출력 ✅
```

---

## 🎯 사용 예제

### 예제 1: 간단한 버그 수정

```bash
# 오류를 수정했음
git add app/pages/InventoryManagement.py
git commit -m "fix: 폼 제출 버튼 key 파라미터 제거"

# 자동으로 실행됨:
# ✅ VERSION: 0.1.0 → 0.1.1
# ✅ CHANGELOG.md 업데이트
```

### 예제 2: 새 기능 추가

```bash
# 새 기능 구현 완료
git add app/pages/Analysis.py
git add app/services/report_service.py
git commit -m "feat: 고급 분석 대시보드 추가"

# 자동으로 실행됨:
# ✅ VERSION: 0.1.1 → 0.2.0
# ✅ CHANGELOG.md 업데이트
```

### 예제 3: 여러 파일 수정

```bash
# 여러 파일 수정
git add .
git commit -m "fix: UI 오류 및 성능 개선"

# 자동으로 실행됨:
# ✅ VERSION: 0.2.0 → 0.2.1
# ✅ CHANGELOG.md 업데이트
```

---

## 💡 커밋 메시지 팁

### ✅ 좋은 커밋 메시지

```bash
git commit -m "fix: st.number_input 타입 불일치 오류"
git commit -m "feat: 사용자 인증 시스템 추가"
git commit -m "🐛 데이터베이스 연결 오류"
git commit -m "✨ 실시간 알림 기능"
```

### ❌ 피해야 할 커밋 메시지

```bash
git commit -m "수정"                    # 너무 모호함
git commit -m "여러 개 수정"              # 어떤 수정인지 불명확
git commit -m "업데이트"                 # 구체성 부족
```

---

## 🔍 버전 확인

### 현재 버전 확인

```bash
cat VERSION
```

### 변경 로그 확인

```bash
cat CHANGELOG.md

# 또는 편집기로 보기
code CHANGELOG.md
nano CHANGELOG.md
```

---

## ⚙️ 수동 버전 관리 (필요시)

자동화가 작동하지 않거나 수동으로 관리하고 싶으면:

```bash
# 패치 버전 업데이트
python3 update_version.py --type patch --summary "버그 수정"

# 마이너 버전 업데이트
python3 update_version.py --type minor --summary "새 기능 추가"

# 메이저 버전 업데이트
python3 update_version.py --type major --summary "구조 변경"

# 현재 버전 확인
python3 update_version.py --show
```

---

## 🎨 Emoji 가이드 (선택사항)

더 시각적인 커밋 메시지를 위해 사용할 수 있습니다:

| Emoji | 의미 | 사용 예 |
|--------|------|--------|
| 🐛 | 버그 수정 | `git commit -m "🐛 오류 수정"` |
| ✨ | 새 기능 | `git commit -m "✨ 기능 추가"` |
| 🚀 | 호환성 변경 | `git commit -m "🚀 구조 변경"` |
| 🔧 | 개선 | `git commit -m "🔧 성능 최적화"` |
| 📚 | 문서화 | `git commit -m "📚 README 작성"` |
| 🧪 | 테스트 | `git commit -m "🧪 테스트 추가"` |
| 🗑️ | 삭제 | `git commit -m "🗑️ 불필요한 파일 제거"` |

---

## 📊 버전 관리 예시

```
0.1.0 (초기 버전)
  ↓
fix: 오류 수정
  ↓
0.1.1 (패치)
  ↓
feat: 새 기능 추가
  ↓
0.2.0 (마이너)
  ↓
🚀 구조 변경
  ↓
1.0.0 (메이저)
```

---

## 🆘 문제 해결

### Git hook이 작동하지 않음

```bash
# 1. hook 파일 확인
ls -la .git/hooks/post-commit

# 2. 실행 권한 확인
chmod +x .git/hooks/post-commit

# 3. Python 경로 확인
which python3

# 4. 수동 실행 테스트
python3 update_version.py --show
```

### 커밋 메시지가 인식되지 않음

```bash
# fix:, feat:, 🐛, ✨, 🚀 중 하나를 사용하세요
git commit -m "fix: 설명" ✅
git commit -m "feat: 설명" ✅
git commit -m "🐛 설명" ✅
git commit -m "수정 설명" ❌
```

---

## 📖 더 알아보기

- [VERSION_MANAGEMENT.md](./VERSION_MANAGEMENT.md) - 상세 가이드
- [CHANGELOG.md](./CHANGELOG.md) - 변경 로그
- [VERSION](./VERSION) - 현재 버전

---

**이제 Git 커밋 메시지만 따르면 모든 버전 관리가 자동으로 됩니다!** 🎉

