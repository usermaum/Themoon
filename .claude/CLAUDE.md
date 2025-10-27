# CLAUDE.md - 프로젝트 가이드 네비게이터

> **The Moon Drip BAR - 로스팅 비용 계산기**
> 버전: 1.2.0 · 스택: Streamlit + SQLite · 환경: ./venv/

---

## 🎯 필수 규칙 (CRITICAL)

✅ **항상 프로젝트 venv 사용** (절대 `python3` 금지)
```bash
./venv/bin/python script.py
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true
./venv/bin/pip install package_name
```

✅ **모든 응답은 한글로 작성** (코드/오류는 원본 유지)

---

## 📁 핵심 문서 위치

| 문서 | 위치 | 용도 |
|------|------|------|
| **파일 구조** | `Documents/Architecture/FILE_STRUCTURE.md` | 프로젝트 파일 맵 |
| **개발 가이드** | `Documents/Architecture/DEVELOPMENT_GUIDE.md` | 5단계 개발 프로세스 |
| **시스템 아키텍처** | `Documents/Architecture/SYSTEM_ARCHITECTURE.md` | 3계층 아키텍처 & 데이터 흐름 |
| **문제 해결** | `Documents/Architecture/TROUBLESHOOTING.md` | 16가지 오류 & 해결법 |
| **자주 하는 작업** | `Documents/Architecture/COMMON_TASKS.md` | 25가지 작업 단계 가이드 |
| **진행 현황** | `Documents/Progress/SESSION_SUMMARY_*.md` | 세션별 진행 상황 |

---

## 🚀 빠른 시작

```bash
# 1. 앱 실행
./venv/bin/streamlit run app/app.py --server.port 8501 --server.headless true
# → http://localhost:8501

# 2. 테스트 데이터 생성
./venv/bin/python app/test_data.py

# 3. Git 커밋 (한글 설명)
git add .
git commit -m "feat: 새 기능 설명"

# 4. 포트 충돌 해결
lsof -ti :8501 | xargs kill -9
```

---

## 📌 프로젝트 구조

```
TheMoon_Project/
├── venv/                   # 프로젝트 격리 환경 (Python 3.12.3)
├── app/                    # Streamlit 애플리케이션
│   ├── app.py            # 메인 진입점
│   ├── pages/            # 9개 페이지
│   ├── services/         # 6개 서비스 (비즈니스 로직)
│   ├── models/           # SQLAlchemy 모델
│   └── components/       # 15+ 재사용 컴포넌트
├── Data/                  # SQLite 데이터베이스
├── Documents/            # 28개 분류별 문서
└── logs/                 # 버전 관리 (VERSION, CHANGELOG.md)
```

---

## 🔗 문서 로드 전략

새로운 세션에서는 다음 순서로 확인:
1. **SESSION_SUMMARY_*.md** - 지난 세션 진행 상황
2. **필요한 아키텍처 문서** 로드 (위의 표 참조)
3. **COMMON_TASKS.md** - 자주 하는 작업 참고

**전체 구조:** `Documents/` → Architecture(설계), Guides(가이드), Progress(진행), Planning(계획), Resources(자료)

---

마지막 업데이트: 2025-10-27
