# TheMoon Backend (FastAPI)

커피 로스팅 원가 계산 시스템 백엔드 API

## 📌 원본 참조

이 프로젝트는 Streamlit 기반 원본을 FastAPI로 완전히 재작성한 버전입니다.

**원본 프로젝트:** `/mnt/d/Ai/WslProject/TheMoon_Project/app/`

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일 생성:

```env
DATABASE_URL=postgresql://themoon:password@localhost:5432/themoon_db
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-key
ANTHROPIC_API_KEY=your-claude-key
```

### 3. 데이터베이스 마이그레이션

```bash
# Alembic 초기화 (최초 1회)
alembic init migrations

# 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행
alembic upgrade head
```

### 4. 서버 실행

```bash
uvicorn app.main:app --reload --port 8000
```

**접속:** http://localhost:8000/docs

## 📁 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱
│   ├── config.py            # 설정
│   ├── database.py          # DB 연결
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/   # API 엔드포인트
│   │       └── deps.py      # 의존성
│   ├── core/
│   │   ├── security.py      # JWT, 비밀번호 해싱
│   │   └── config.py        # 핵심 설정
│   ├── models/              # SQLAlchemy 모델
│   ├── schemas/             # Pydantic 스키마
│   └── services/            # 비즈니스 로직
├── tests/                   # 테스트
├── requirements.txt
└── README.md
```

## 🔗 원본 대응표

| 원본 (Streamlit)         | 신규 (FastAPI)                  | 설명                     |
| ------------------------ | ------------------------------- | ------------------------ |
| `app/models/`            | `backend/app/models/`           | SQLAlchemy 모델 (재작성) |
| `app/services/`          | `backend/app/services/`         | 비즈니스 로직 (재작성)   |
| `app/pages/`             | `backend/app/api/v1/endpoints/` | UI → API 엔드포인트      |
| `app/models/database.py` | `backend/app/database.py`       | DB 연결                  |

## 📚 API 문서

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🧪 테스트

```bash
pytest tests/ -v
```

## 📝 개발 가이드

원본 프로젝트의 비즈니스 로직을 참조하되, 완전히 새로 작성합니다:

1. **모델 작성:** 원본 `TheMoon_Project/app/models/` 참조
2. **서비스 작성:** 원본 `TheMoon_Project/app/services/` 참조
3. **API 설계:** RESTful 원칙 준수
4. **테스트 작성:** 모든 엔드포인트에 대한 테스트

---

## 🔗 관련 문서

**← 상위**: [프로젝트 루트](../README.md)

**아키텍처 문서**:
- [시스템 개요](../docs/Architecture/SYSTEM_OVERVIEW.md) - 전체 시스템 개요 및 핵심 기능
- [데이터 흐름도](../docs/Architecture/DATA_FLOW.md) - 시스템 내 데이터 흐름 상세 분석
- [데이터베이스 스키마](../docs/Architecture/DATABASE_SCHEMA.md) - 테이블 구조 및 관계도
- [API 명세](../docs/Architecture/API_SPECIFICATION.md) ⭐ - 모든 API 엔드포인트 상세 문서
- [기술 스택](../docs/Architecture/TECHNOLOGY_STACK.md) ⭐ - 사용 기술 상세 설명
- [배포 아키텍처](../docs/Architecture/DEPLOYMENT_ARCHITECTURE.md) ⭐ - 배포 환경 상세 구조

**개발 가이드**:
- [개발 가이드](../docs/Architecture/DEVELOPMENT_GUIDE.md) - 5단계 개발 프로세스
- [문제 해결](../docs/Architecture/TROUBLESHOOTING.md) - 16가지 오류 & 해결법

**Frontend**:
- [Frontend README](../frontend/README.md) - Frontend 개발 가이드

---

**버전:** 1.0.0
**최종 업데이트:** 2025-12-08
