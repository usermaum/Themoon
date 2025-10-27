# 버전 관리 가이드

이 문서는 프로젝트의 버전 관리 시스템 사용 방법을 설명합니다.

## 📚 목차

1. [개요](#개요)
2. [버전 관리 방식](#버전-관리-방식)
3. [사용 방법](#사용-방법)
4. [예제](#예제)
5. [버전 규칙](#버전-규칙)
6. [변경 로그 보기](#변경-로그-보기)

---

## 개요

### 📦 버전 관리 시스템

이 프로젝트는 **Semantic Versioning (SemVer)** 규칙을 따릅니다:

```
MAJOR.MINOR.PATCH
  |      |      |
  |      |      └─ 버그 수정 (0.1.0 → 0.1.1)
  |      └────── 새 기능 (0.1.0 → 0.2.0)
  └──────────── 호환성 깨지는 변경 (0.1.0 → 1.0.0)
```

### 📂 관련 파일

| 파일 | 설명 |
|------|------|
| `VERSION` | 현재 버전 저장 (예: 0.1.0) |
| `CHANGELOG.md` | 모든 버전의 변경사항 기록 |
| `update_version.py` | 자동 버전 관리 스크립트 |

---

## 버전 관리 방식

### 버전 번호 결정

| 변경 유형 | 버전 증가 | 예시 | 사용 사례 |
|---------|---------|------|---------|
| 🐛 버그 수정 | PATCH | 0.1.0 → 0.1.1 | 오류 수정, 하위 호환성 유지 |
| ✨ 새 기능 | MINOR | 0.1.0 → 0.2.0 | 새로운 기능 추가, 하위 호환성 유지 |
| 🚀 호환성 변경 | MAJOR | 0.1.0 → 1.0.0 | API 변경, 구조 재설계 |

### 변경사항 카테고리

변경 로그에 기록할 때 다음 카테고리를 사용합니다:

- **✨ Added** - 새로운 기능
- **🐛 Fixed** - 버그 수정
- **🔧 Improved** - 기존 기능 개선
- **🗑️ Removed** - 제거된 기능
- **⚠️ Deprecated** - 곧 제거될 기능
- **📝 Documentation** - 문서 업데이트
- **🔍 Testing** - 테스트 추가/개선

---

## 사용 방법

### 1️⃣ 현재 버전 확인

```bash
python3 logs/update_version.py --show
```

**출력 예:**
```
📦 현재 버전: 0.1.0
```

### 2️⃣ 버전 업데이트 (패치 - 버그 수정)

```bash
python3 logs/update_version.py \
  --type patch \
  --summary "폼 제출 버튼 오류 수정"
```

**결과:**
- `VERSION` 파일: `0.1.0` → `0.1.1`
- `CHANGELOG.md`: 새 섹션 추가

### 3️⃣ 버전 업데이트 (마이너 - 새 기능)

```bash
python3 logs/update_version.py \
  --type minor \
  --summary "Excel 내보내기 기능 개선"
```

**결과:**
- `VERSION` 파일: `0.1.0` → `0.2.0`
- `CHANGELOG.md`: 새 섹션 추가

### 4️⃣ 버전 업데이트 (메이저 - 구조 변경)

```bash
python3 logs/update_version.py \
  --type major \
  --summary "데이터베이스 스키마 대폭 개선"
```

**결과:**
- `VERSION` 파일: `0.1.0` → `1.0.0`
- `CHANGELOG.md`: 새 섹션 추가

### 5️⃣ 상세한 변경사항 포함

```bash
python3 logs/update_version.py \
  --type patch \
  --summary "성능 최적화" \
  --changes "
- 데이터베이스 쿼리 최적화
- 메모리 사용량 50% 감소
- 로딩 시간 개선
  "
```

---

## 예제

### 예제 1: 버그 수정 후 버전 업데이트

작업 내용: `st.form_submit_button()` key 파라미터 오류 수정

```bash
# 1. 버그 수정 작업 완료
# 파일: app/pages/InventoryManagement.py
# 변경: key="btn_outflow" 파라미터 제거

# 2. 버전 업데이트
python3 logs/update_version.py \
  --type patch \
  --summary "FormMixin.form_submit_button() key 파라미터 제거"
```

### 예제 2: 새 기능 추가 후 버전 업데이트

작업 내용: 새로운 분석 기능 추가

```bash
# 1. 새 기능 구현 완료
# 파일: app/pages/Analysis.py
# 변경: 고급 분석 기능 추가

# 2. 버전 업데이트
python3 logs/update_version.py \
  --type minor \
  --summary "고급 분석 기능 추가" \
  --changes "
- 원두별 판매 추이 분석
- 시즈널 트렌드 분석
- 고객 선호도 분석
  "
```

### 예제 3: 여러 버그 수정

```bash
python3 logs/update_version.py \
  --type patch \
  --summary "여러 UI 오류 수정" \
  --changes "
- Excel 내보내기 'No visible sheet' 오류 수정
- st.number_input() 타입 불일치 오류 수정
- 데이터베이스 연결 오류 수정
  "
```

---

## 버전 규칙

### 언제 어떤 버전을 사용할까?

#### 🐛 PATCH 증가 (0.1.0 → 0.1.1)

```
✓ 버그 수정
✓ 하위 호환성 유지
✓ 사용자에게 영향 최소
```

**사용 예:**
- 오류 메시지 수정
- 성능 최적화
- 보안 버그 수정

#### ✨ MINOR 증가 (0.1.0 → 0.2.0)

```
✓ 새 기능 추가
✓ 기존 기능 개선
✓ 하위 호환성 유지
```

**사용 예:**
- 새로운 분석 도구
- UI 개선
- 새로운 리포트 타입

#### 🚀 MAJOR 증가 (0.1.0 → 1.0.0)

```
✗ 호환성 깨지는 변경
✗ API 변경
✗ 데이터 구조 변경
```

**사용 예:**
- 데이터베이스 마이그레이션
- API 재설계
- 큰 리팩토링

---

## 변경 로그 보기

### CHANGELOG.md 확인

```bash
# 파일 열기
cat CHANGELOG.md

# 또는 편집기에서 열기
code CHANGELOG.md    # VS Code
nano CHANGELOG.md    # Nano
vim CHANGELOG.md     # Vim
```

### 변경 로그 형식

```markdown
## [버전] - 날짜

### 카테고리 (emoji): 요약

#### 상세 설명
- 세부사항 1
- 세부사항 2
```

---

## 📝 작업 흐름

```
1. 기능 개발/버그 수정
        ↓
2. 테스트 및 검증
        ↓
3. 변경 타입 결정
   (patch/minor/major)
        ↓
4. 버전 업데이트 실행
   python3 logs/update_version.py \
     --type [type] \
     --summary "설명"
        ↓
5. VERSION 파일 자동 업데이트
   CHANGELOG.md 자동 추가
        ↓
6. Git 커밋 (선택)
   git add VERSION CHANGELOG.md
   git commit -m "chore: Version 0.x.x"
```

---

## 🚀 Best Practices

### ✅ 권장 사항

1. **정기적인 버전 업데이트**
   - 완료된 작업마다 버전 업데이트
   - 변경 로그를 최신 상태로 유지

2. **명확한 요약 작성**
   - 무엇을 했는지 명확히 기술
   - 사용자 관점에서 설명

3. **상세한 변경사항**
   - 주요 변경사항들을 나열
   - 영향받는 기능들 명시

4. **일관된 카테고리 사용**
   - 정해진 카테고리만 사용
   - emoji와 텍스트를 함께 기록

### ❌ 피해야 할 것

1. ❌ 버전 변경 없이 기능 추가
2. ❌ 불명확한 요약 작성
3. ❌ 변경 로그 미기록
4. ❌ 버전 번호 임의 변경

---

## 🔗 관련 문서

- [CHANGELOG.md](./CHANGELOG.md) - 변경 로그
- [VERSION](./VERSION) - 현재 버전
- [README.md](./README.md) - 프로젝트 개요

---

## 📞 문제 해결

### 문제: 버전 파일이 없습니다

```bash
# 해결: VERSION 파일 생성
echo "0.1.0" > VERSION
```

### 문제: Python 스크립트가 실행되지 않습니다

```bash
# 해결: 실행 권한 추가
chmod +x update_version.py

# 또는 Python으로 직접 실행
python3 logs/update_version.py --show
```

### 문제: CHANGELOG.md 형식 오류

```bash
# 해결: 파일 백업
cp CHANGELOG.md CHANGELOG.md.bak

# 수동으로 수정하거나 기본 CHANGELOG.md 복구
```

---

## 📊 버전 히스토리 예시

```
0.1.0 (2025-10-27) - 초기 버전
  ├─ 데이터베이스 모델 개선
  └─ UI 오류 수정

0.1.1 (2025-10-28) - 버그 수정
  ├─ 성능 최적화
  └─ 보안 업데이트

0.2.0 (2025-11-01) - 새 기능
  ├─ 고급 분석 추가
  ├─ 리포트 기능 개선
  └─ UI 개선

1.0.0 (2025-12-01) - 정식 버전
  ├─ 안정성 개선
  ├─ 성능 최적화
  └─ 문서화 완성
```

---

**이 가이드를 따르면 프로젝트의 버전을 체계적으로 관리할 수 있습니다!** ✅
