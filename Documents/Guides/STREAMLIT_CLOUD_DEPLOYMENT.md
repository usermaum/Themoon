# Streamlit Cloud 배포 가이드

> **The Moon Drip BAR - Roasting Cost Calculator**
> Streamlit Cloud에 배포하는 방법

---

## 📋 목차

1. [배포 준비](#배포-준비)
2. [Streamlit Cloud 설정](#streamlit-cloud-설정)
3. [API 키 설정 (Secrets)](#api-키-설정-secrets)
4. [배포 및 확인](#배포-및-확인)
5. [트러블슈팅](#트러블슈팅)

---

## 🚀 배포 준비

### 1. GitHub 저장소 확인

배포할 코드가 GitHub에 푸시되어 있어야 합니다.

```bash
# 현재 상태 확인
git status

# 변경사항 커밋
git add .
git commit -m "feat: Streamlit Cloud 배포 준비"

# GitHub에 푸시
git push origin main
```

### 2. 필수 파일 확인

다음 파일들이 저장소에 포함되어 있는지 확인:

- ✅ `requirements.txt` - 의존성 패키지
- ✅ `app/app.py` - 메인 애플리케이션
- ✅ `.streamlit/config.toml` - Streamlit 설정
- ✅ `.streamlit/secrets.toml.example` - Secrets 예시 (참고용)

**⚠️ 주의**: `.env` 파일과 `.streamlit/secrets.toml`은 Git에 절대 커밋하지 마세요!

---

## 🌐 Streamlit Cloud 설정

### 1. Streamlit Cloud 가입

1. https://share.streamlit.io/ 접속
2. GitHub 계정으로 로그인
3. "New app" 버튼 클릭

### 2. 앱 배포 설정

**Repository 설정:**
- **GitHub repository**: `usermaum/Project` (본인의 저장소)
- **Branch**: `main`
- **Main file path**: `app/app.py`

**Advanced settings (선택):**
- **Python version**: `3.12` (권장)
- **App URL**: 원하는 URL 입력 (예: `themoon-roasting-calculator`)

### 3. Deploy 클릭

초기 배포 시 패키지 설치로 2-3분 소요됩니다.

---

## 🔐 API 키 설정 (Secrets)

### ⚠️ 중요: 배포 후 반드시 설정해야 합니다!

Claude API를 사용하려면 Streamlit Cloud Secrets에 API 키를 설정해야 합니다.

### 1. Secrets 메뉴 접속

1. Streamlit Cloud 대시보드에서 앱 선택
2. 우측 상단 **⋮** (점 3개) → **Settings** 클릭
3. 좌측 메뉴에서 **Secrets** 클릭

### 2. API 키 입력

**TOML 형식으로 입력:**

```toml
# Anthropic Claude API Key (필수)
ANTHROPIC_API_KEY = "sk-ant-api03-여기에-실제-API-키-입력"
```

**참고**: `.streamlit/secrets.toml.example` 파일 내용을 복사하여 사용 가능

### 3. Save 버튼 클릭

저장 후 앱이 자동으로 재시작됩니다 (~30초).

### 4. API 키 발급 방법

Anthropic API 키가 없다면:

1. https://console.anthropic.com 접속
2. **API Keys** 메뉴 클릭
3. **Create Key** 버튼 클릭
4. 생성된 키 복사 (한 번만 표시됨!)
5. Streamlit Cloud Secrets에 붙여넣기

---

## ✅ 배포 및 확인

### 1. 앱 접속

배포 완료 후 제공되는 URL로 접속:

```
https://your-app-name.streamlit.app
```

### 2. 기능 테스트

**필수 체크리스트:**

- [ ] 대시보드 페이지 정상 로드
- [ ] 데이터베이스 연결 확인
- [ ] "이미지 명세서 업로드" 페이지 접속
- [ ] Claude API 초기화 성공 (에러 없음)
- [ ] 테스트 이미지 업로드 및 OCR 처리

### 3. 로그 확인

**Manage app** → **Logs** 메뉴에서 에러 확인:

```
✅ 정상:
   - "You can now view your Streamlit app in your browser."
   - "ClaudeOCRService initialized successfully"

❌ 에러:
   - "ANTHROPIC_API_KEY not found" → Secrets 설정 확인
   - "ModuleNotFoundError" → requirements.txt 확인
```

---

## 🛠️ 트러블슈팅

### 문제 1: API 키 에러

**증상:**
```
ValueError: ANTHROPIC_API_KEY not found.
```

**해결:**
1. Settings → Secrets 메뉴 확인
2. TOML 형식 정확한지 확인:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."  # 따옴표 필수!
   ```
3. Save 후 앱 재시작 확인

### 문제 2: 패키지 설치 실패

**증상:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**해결:**
1. `requirements.txt` 확인
2. 버전 범위 조정:
   ```txt
   anthropic>=0.73.0  # ✅ 권장
   anthropic==0.73.0  # ❌ 너무 엄격
   ```
3. Python 버전 확인 (Settings → Python version: 3.12)

### 문제 3: 데이터베이스 초기화 실패

**증상:**
```
sqlite3.OperationalError: unable to open database file
```

**해결:**
1. `data/` 디렉토리가 Git에 포함되어 있는지 확인
2. `.gitkeep` 파일 추가:
   ```bash
   touch data/.gitkeep
   git add data/.gitkeep
   git commit -m "chore: Add data directory"
   ```

### 문제 4: 이미지 업로드 실패

**증상:**
```
FileNotFoundError: data/invoices/ directory not found
```

**해결:**
1. `data/invoices/` 디렉토리 생성:
   ```bash
   mkdir -p data/invoices
   touch data/invoices/.gitkeep
   git add data/invoices/.gitkeep
   ```

### 문제 5: 앱이 느리게 로드됨

**원인:**
- Streamlit Cloud 무료 플랜은 리소스 제한이 있습니다.

**해결:**
1. 불필요한 패키지 제거 (`requirements.txt` 최적화)
2. 데이터베이스 쿼리 최적화
3. `@st.cache_data` 데코레이터 활용

---

## 📊 배포 체크리스트

배포 전 최종 확인:

- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는가?
- [ ] `.streamlit/secrets.toml`이 `.gitignore`에 포함되어 있는가?
- [ ] `requirements.txt`에 모든 의존성이 포함되어 있는가?
- [ ] `app/app.py`가 정상 실행되는가? (로컬 테스트)
- [ ] GitHub에 최신 코드가 푸시되어 있는가?
- [ ] Anthropic API 키를 발급받았는가?
- [ ] `data/` 및 `data/invoices/` 디렉토리가 존재하는가?

---

## 🔄 업데이트 배포

코드 수정 후 재배포:

```bash
# 1. 로컬에서 테스트
./venv/bin/streamlit run app/app.py

# 2. Git 커밋 및 푸시
git add .
git commit -m "feat: 새로운 기능 추가"
git push origin main

# 3. Streamlit Cloud 자동 재배포
# GitHub push 감지 시 자동으로 재배포됩니다 (~2분)
```

---

## 📚 참고 문서

- **Streamlit Cloud 공식 문서**: https://docs.streamlit.io/deploy/streamlit-community-cloud
- **Secrets 관리**: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
- **Anthropic API 문서**: https://docs.anthropic.com/

---

## 💡 추가 팁

### 무료 플랜 제한

Streamlit Cloud 무료 플랜:
- **리소스**: 1GB RAM, 공유 CPU
- **앱 개수**: 무제한 (public)
- **사용량**: 무제한

### 비용 절감

Claude API 비용 절감 방법:
- Claude 3.5 Haiku 사용 (가장 저렴)
- 이미지 크기 최적화 (1000px 이하)
- API 호출 캐싱 (`@st.cache_data`)

### 보안

- **절대 하지 말 것**: API 키를 코드에 하드코딩
- **권장**: Streamlit Secrets 사용
- **백업**: API 키를 안전한 곳에 별도 저장 (1Password, LastPass 등)

---

마지막 업데이트: 2025-11-16
버전: 0.49.0
