# 🚀 세션 시작 체크리스트

> 새로운 세션을 시작할 때마다 이 체크리스트를 확인하세요!
> 이렇게 하면 이전 진행 상황을 완벽하게 이어갈 수 있습니다.

---

## ✅ 체크리스트

### 1️⃣ 이전 세션 정보 확인

#### Step 1-1: 마지막 세션 요약 읽기
```bash
# 가장 최신 SESSION_SUMMARY 파일 확인
ls -lt Documents/Progress/SESSION_SUMMARY_*.md | head -1

# 파일 읽기
cat Documents/Progress/SESSION_SUMMARY_2025-10-27.md
```

**확인 항목**:
- [ ] 지난 세션에서 한 일이 뭐였는가?
- [ ] 완료된 작업은 뭐였는가?
- [ ] 다음 할 일이 뭐였는가?
- [ ] 주의사항은 뭐였는가?

#### Step 1-2: 변경 로그 확인
```bash
# 최근 버전 변경사항 확인
head -30 logs/CHANGELOG.md

# 현재 버전 확인
cat logs/VERSION
```

**확인 항목**:
- [ ] 현재 버전은?
- [ ] 마지막 업데이트는 언제?
- [ ] 마지막 변경사항은 뭐?

---

### 2️⃣ 프로젝트 상태 확인

#### Step 2-1: Git 상태 확인
```bash
# 깨끗한 상태 확인
git status

# 최근 커밋 확인
git log --oneline -5

# 현재 브랜치 확인
git branch
```

**확인 항목**:
- [ ] `git status`가 "nothing to commit"인가?
- [ ] 마지막 커밋이 뭐였는가?
- [ ] 현재 브랜치가 main인가?

#### Step 2-2: venv 상태 확인
```bash
# venv 존재 확인
ls -la venv/bin/ | grep -E "python|streamlit"

# Python 버전 확인
./venv/bin/python --version

# Streamlit 버전 확인
./venv/bin/streamlit --version
```

**확인 항목**:
- [ ] venv가 존재하는가?
- [ ] Python 3.12.3인가?
- [ ] Streamlit 1.38.0인가?

#### Step 2-3: 데이터베이스 상태 확인
```bash
# DB 파일 존재 확인
ls -lh Data/roasting_data.db

# DB 테이블 확인
./venv/bin/python -c "
import sqlite3
conn = sqlite3.connect('Data/roasting_data.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
tables = cursor.fetchall()
print('Database Tables:', [t[0] for t in tables])
conn.close()
"
```

**확인 항목**:
- [ ] DB 파일이 존재하는가?
- [ ] 필요한 테이블들이 있는가?

---

### 3️⃣ 문서 구조 확인

#### Step 3-1: Documents 폴더 구조 확인
```bash
# 문서 폴더 구조 확인
find Documents -type d

# 각 폴더의 파일 개수 확인
echo "Architecture: $(ls Documents/Architecture/ | wc -l) 파일"
echo "Guides: $(ls Documents/Guides/ | wc -l) 파일"
echo "Progress: $(ls Documents/Progress/ | wc -l) 파일"
echo "Planning: $(ls Documents/Planning/ | wc -l) 파일"
echo "Resources: $(ls Documents/Resources/ | wc -l) 파일"
```

**확인 항목**:
- [ ] Documents/Architecture/ 폴더가 있는가?
- [ ] Documents/Guides/ 폴더가 있는가?
- [ ] Documents/Progress/ 폴더가 있는가?
- [ ] Documents/Planning/ 폴더가 있는가?
- [ ] Documents/Resources/ 폴더가 있는가?

#### Step 3-2: 프로젝트 규칙 확인
```bash
# 핵심 규칙 파일 확인
cat .claude/CLAUDE.md | head -50
```

**확인 항목**:
- [ ] `.claude/CLAUDE.md`가 있는가?
- [ ] 프로젝트 규칙이 설정되어 있는가?
- [ ] venv 사용 규칙이 명시되어 있는가?

---

### 4️⃣ 개발 환경 준비

#### Step 4-1: 필요한 패키지 확인
```bash
# 설치된 패키지 확인
./venv/bin/pip list | grep -E "streamlit|pandas|plotly|numpy|openpyxl"
```

**필수 패키지**:
- [ ] streamlit 1.38.0
- [ ] pandas 2.2.3
- [ ] numpy 2.1.3
- [ ] plotly 5.24.1
- [ ] openpyxl 3.1.5

#### Step 4-2: README 확인
```bash
# 현재 상태 섹션 확인
cat README.md | grep -A 20 "프로젝트 정보"
```

**확인 항목**:
- [ ] README.md가 최신인가?
- [ ] 프로젝트 정보가 맞는가?
- [ ] 버전이 맞는가?

---

### 5️⃣ 작업 시작 준비

#### Step 5-1: 작업 목표 정하기
```bash
# 다음 할 일 목록 확인
cat Documents/Progress/SESSION_SUMMARY_2025-10-27.md | grep -A 15 "다음 세션에서 할 일"
```

**준비 항목**:
- [ ] 오늘 할 작업이 뭔지 확인했는가?
- [ ] 우선순위를 정했는가?
- [ ] 예상 시간을 추정했는가?

#### Step 5-2: 작업 환경 준비
```bash
# 현재 디렉토리 확인
pwd

# 아무것도 실행 중이지 않은지 확인
lsof -ti :8501 2>/dev/null || echo "포트 8501 사용 가능"
```

**준비 항목**:
- [ ] 프로젝트 루트 디렉토리에 있는가?
- [ ] 포트 8501이 사용 가능한가?

---

## 🎯 체크리스트 완료 후

모든 항목을 확인했으면 이렇게 진행하세요:

```bash
# 1. 현재 상태 최종 확인
git status

# 2. 작업 시작
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true

# 3. 브라우저 접속
# http://localhost:8501
```

---

## 📋 빠른 확인 (1분)

시간이 없으면 최소한 이것만 확인하세요:

```bash
# 모든 것 한 번에 확인
echo "=== 현재 버전 ===" && cat logs/VERSION && \
echo "=== 최근 세션 ===" && ls -lt Documents/Progress/SESSION_SUMMARY_*.md | head -1 && \
echo "=== Git 상태 ===" && git status --short && \
echo "=== venv ===" && ./venv/bin/python --version
```

---

## 🚀 이제 시작하세요!

이 체크리스트를 완료하면 이전 세션과 완벽한 연속성을 유지하면서 작업을 시작할 수 있습니다!

**행운을 빕니다! 🎉**
