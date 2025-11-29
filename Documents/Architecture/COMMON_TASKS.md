# 자주 하는 작업 가이드 (Common Tasks)

> 프로젝트에서 자주 수행하는 25가지 작업의 단계별 가이드입니다.
> **Next.js (Frontend) + FastAPI (Backend) + PostgreSQL**

---

## 📋 빠른 참조 목록

| # | 작업 | 예상 시간 | 난이도 |
|---|------|---------|--------|
| 1 | [앱 실행하기](#1-앱-실행하기) | 10초 | ⭐ |
| 2 | [앱 중지하기](#2-앱-중지하기) | 5초 | ⭐ |
| 3 | [원두 추가하기](#3-원두-추가하기) | 1분 | ⭐ |
| 4 | [블렌드 레시피 만들기](#4-블렌드-레시피-만들기) | 3분 | ⭐ |
| 5 | [로스팅 로그 기록하기](#5-로스팅-로그-기록하기) | 2분 | ⭐ |
| 6 | [비용 설정 변경하기](#6-비용-설정-변경하기) | 2분 | ⭐ |
| 7 | [분석 보고서 생성하기](#7-분석-보고서-생성하기) | 5분 | ⭐⭐ |
| 8 | [Excel로 내보내기](#8-excel로-내보내기) | 2분 | ⭐ |
| 9 | [Excel에서 임포트하기](#9-excel에서-임포트하기) | 3분 | ⭐⭐ |
| 10 | [재고 현황 확인하기](#10-재고-현황-확인하기) | 1분 | ⭐ |
| 11 | [새 패키지 설치하기](#11-새-패키지-설치하기) | 2분 | ⭐⭐ |
| 12 | [의존성 업데이트하기](#12-의존성-업데이트하기) | 3분 | ⭐⭐ |
| 13 | [데이터베이스 초기화하기](#13-데이터베이스-초기화하기) | 1분 | ⭐⭐ |
| 14 | [테스트 데이터 생성하기](#14-테스트-데이터-생성하기) | 2분 | ⭐ |
| 15 | [Git 커밋하기](#15-git-커밋하기) | 3분 | ⭐⭐ |
| 16 | [버전 업데이트하기](#16-버전-업데이트하기) | 2분 | ⭐⭐ |
| 17 | [포트 충돌 해결하기](#17-포트-충돌-해결하기) | 1분 | ⭐ |
| 18 | [데이터베이스 백업하기](#18-데이터베이스-백업하기) | 1분 | ⭐ |
| 19 | [새 페이지 추가하기](#19-새-페이지-추가하기) | 10분 | ⭐⭐⭐ |
| 20 | [새 API 엔드포인트 추가하기](#20-새-api-엔드포인트-추가하기) | 10분 | ⭐⭐⭐ |
| 21 | [새 모델 추가하기](#21-새-모델-추가하기) | 10분 | ⭐⭐⭐ |
| 22 | [새 컴포넌트 만들기](#22-새-컴포넌트-만들기) | 5분 | ⭐⭐⭐ |
| 23 | [디버깅 모드 실행하기](#23-디버깅-모드-실행하기) | 1분 | ⭐⭐ |
| 24 | [성능 최적화하기](#24-성능-최적화하기) | 15분 | ⭐⭐⭐ |
| 25 | [문서 작성하기](#25-문서-작성하기) | 10분 | ⭐⭐ |

---

## 🚀 기본 작업 (Basic Tasks)

### 1. 앱 실행하기

**목적:** Backend (FastAPI) + Frontend (Next.js) 애플리케이션 시작하기

**단계:**

```bash
# 1단계: Backend 실행 (터미널 1)
cd backend
../venv/bin/uvicorn app.main:app --reload --port 8000

# 2단계: Frontend 실행 (터미널 2)
cd frontend
npm run dev

# 또는 한 번에 실행 (터미널 1개)
cd /path/to/Themoon
./start_all.sh
```

**확인:**

- Backend 확인:

<http://localhost:8000/docs>

- Frontend 확인:

<http://localhost:3000>

**팁:**

```bash
# 포트 변경하려면
# Backend
cd backend
../venv/bin/uvicorn app.main:app --reload --port 8001

# Frontend (package.json 수정 필요 또는)
cd frontend
PORT=3001 npm run dev

# 로그를 파일에 저장
../venv/bin/uvicorn app.main:app --reload --port 8000 > backend.log 2>&1 &
npm run dev > frontend.log 2>&1 &
```

---

### 2. 앱 중지하기

**목적:** 실행 중인 애플리케이션 종료하기

**단계:**

```bash
# 방법 1: 터미널에서 Ctrl+C 누르기
# (각각의 실행한 터미널에서)
Ctrl+C

# 방법 2: 포트로 프로세스 종료
# Backend 종료
lsof -ti :8000 | xargs kill -9

# Frontend 종료
lsof -ti :3000 | xargs kill -9

# 방법 3: 프로세스명으로 종료
pkill -f uvicorn  # Backend
pkill -f "next dev"  # Frontend
```

**확인:**

```bash
# 포트가 해제되었는지 확인
lsof -i :8000  # Backend - 아무것도 나오지 않아야 함
lsof -i :3000  # Frontend - 아무것도 나오지 않아야 함
```

---

### 3. 원두 추가하기

**목적:** 새로운 원두 등록하기

**단계:**

1. **웹 UI에서:**
   - 앱 실행 후 `http://localhost:3000`
   - Sidebar > "Beans" 클릭
   - "Add New Bean" 버튼 클릭
   - 원두명 입력 (예: "Ethiopia Yirgacheffe")
   - kg당 가격 입력 (예: 28000)
   - "Submit" 버튼 클릭

2. **API로 직접:**

```bash
curl -X POST "http://localhost:8000/api/v1/beans" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ethiopia Yirgacheffe",
    "price_per_kg": 28000,
    "description": "Floral, citrus notes"
  }'
```

3. **데이터베이스 확인:**

```bash
psql -h localhost -U postgres -d themoon_db \
  -c "SELECT * FROM beans WHERE name = 'Ethiopia Yirgacheffe';"
```

**팁:**

- 원두명은 고유해야 함 (중복 불가)
- 가격은 양수만 가능
- API 문서: `http://localhost:8000/docs#/beans`

---

### 4. 블렌드 레시피 만들기

**목적:** 여러 원두를 섞어 새 블렌드 만들기

**단계:**

1. **사전 준비:**
   - 사용할 원두들이 먼저 등록되어 있어야 함
   - 각 원두의 가격이 설정되어 있어야 함

2. **웹 UI에서:**
   - "Blends" 페이지 이동
   - "Create Blend" 탭
   - 블렌드 이름 입력 (예: "Signature Blend")
   - "Add Bean" 버튼 클릭
   - 원두 선택 & 비율(%) 입력
   - 여러 원두를 반복하여 추가 (총합 100%)
   - "Create Blend" 버튼 클릭

3. **API로 직접:**

```bash
curl -X POST "http://localhost:8000/api/v1/blends" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Signature Blend",
    "components": [
      {"bean_id": 1, "percentage": 40},
      {"bean_id": 2, "percentage": 35},
      {"bean_id": 3, "percentage": 25}
    ]
  }'
```

**예시:**

```
블렌드명: Signature Blend
- Ethiopia Yirgacheffe (ID: 1): 40%
- Kenya AA FAQ (ID: 2): 35%
- Colombia Huila (ID: 3): 25%
(총합: 100%)
```

---

### 5. 로스팅 로그 기록하기

**목적:** 매일의 로스팅 기록 저장하기

**단계:**

1. **웹 UI에서:**
   - "Dashboard" 또는 "Roasting Logs" 페이지
   - "Add New Log" 버튼 클릭
   - 날짜 선택
   - 원두 선택 (또는 블렌드)
   - 생두 무게(kg) 입력 (예: 1.5)
   - 로스팅 후 무게(kg) 입력 (예: 1.25)
   - 비용 정보 입력
   - "Save" 버튼 클릭

2. **API로 직접:**

```bash
curl -X POST "http://localhost:8000/api/v1/roasting-logs" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-11-29",
    "bean_id": 1,
    "green_weight_kg": 1.5,
    "roasted_weight_kg": 1.25,
    "roasting_cost": 3000
  }'
```

**팁:**

- 로스팅 손실율은 자동 계산됨 (약 16.7%)
- 모든 필드는 필수입력
- 같은 날짜에 여러 로그 기록 가능

---

### 6. 비용 설정 변경하기

**목적:** 로스팅 비용 파라미터 업데이트하기

**단계:**

1. **웹 UI에서:**
   - "Settings" 페이지 이동
   - "Cost Settings" 섹션
   - 각 항목 수정:
     - 로스팅 비용/kg (예: 2000)
     - 인건비/시간 (예: 15000)
     - 로스팅 시간 (예: 2시간)
     - 전기료 (예: 5000)
     - 기타 비용 (예: 3000)
   - "Save" 버튼 클릭

2. **API로 직접:**

```bash
curl -X PUT "http://localhost:8000/api/v1/cost-settings/1" \
  -H "Content-Type: application/json" \
  -d '{
    "roasting_cost_per_kg": 2000,
    "labor_cost_per_hour": 15000,
    "roasting_time_hours": 2,
    "electricity_cost": 5000,
    "other_costs": 3000
  }'
```

**팁:**

- 설정 변경은 즉시 반영됨
- 과거 로그의 비용은 자동 재계산되지 않음 (필요시 별도 업데이트)

---

## 📊 분석 & 리포트 (Analytics & Reports)

### 7. 분석 보고서 생성하기

**목적:** 종합 비용 분석 및 차트 생성하기

**단계:**

1. **웹 UI에서:**
   - "Analytics" 페이지 이동
   - 분석 기간 선택 (시작일 ~ 종료일)
   - "분석 유형" 선택:
     - 월별 비용 추이
     - 원두별 비용 분석
     - 블렌드별 수익성
     - 로스팅 효율 분석
   - "Generate Report" 버튼 클릭

2. **결과 확인:**
   - 차트와 통계 표 표시 (Recharts 사용)
   - KPI 메트릭 표시:
     - 총 원두 무게
     - 총 로스팅 비용
     - 평균 kg당 비용
     - 총 수익

3. **API로 조회:**

```bash
curl "http://localhost:8000/api/v1/analytics/summary?start_date=2025-01-01&end_date=2025-12-31"
```

**팁:**

- 차트는 인터랙티브 (확대, 축소, 필터링)
- 기간 미지정 시 전체 데이터 분석
- 데이터 많을 경우 페이지네이션 활용

---

### 8. Excel로 내보내기

**목적:** 모든 데이터를 Excel 파일로 저장하기

**단계:**

1. **웹 UI에서:**
   - "Reports" 페이지 이동
   - "Export Data" 섹션
   - "Export Type" 선택:
     - Beans List
     - Blends Recipes
     - Roasting Logs
     - Full Report
   - "Download Excel" 버튼 클릭

2. **API로 직접:**

```bash
curl "http://localhost:8000/api/v1/export/beans" -o beans.xlsx
curl "http://localhost:8000/api/v1/export/blends" -o blends.xlsx
curl "http://localhost:8000/api/v1/export/logs" -o logs.xlsx
```

3. **파일 확인:**
   - 브라우저 다운로드 폴더에서 파일 확인
   - Excel 또는 Google Sheets에서 열기

---

### 9. Excel에서 임포트하기

**목적:** Excel 파일에서 데이터 가져오기

**단계:**

1. **Excel 파일 준비:**
   - 다음 형식으로 파일 준비:

     ```
     | 원두명 | 가격(원/kg) | 설명 |
     |--------|-------------|------|
     | Ethiopia | 28000 | Floral notes |
     | Kenya | 26000 | Bright acidity |
     ```

2. **웹 UI에서:**
   - "Import" 페이지 이동
   - "Choose File" 버튼으로 Excel 파일 선택
   - "Upload" 버튼 클릭
   - 미리보기 확인
   - "Import" 버튼 클릭

3. **API로 직접:**

```bash
curl -X POST "http://localhost:8000/api/v1/import/beans" \
  -F "file=@beans.xlsx"
```

**팁:**

- Excel 파일은 .xlsx 형식이어야 함
- 첫 행은 헤더(열 이름)여야 함
- 중복 원두는 자동 건너뜀 또는 업데이트 옵션 선택 가능

---

### 10. 재고 현황 확인하기

**목적:** 현재 원두 재고량 확인하기

**단계:**

1. **웹 UI에서:**
   - "Inventory" 페이지 이동
   - "Current Stock" 탭 클릭
   - 각 원두별 현재 재고 표시

2. **상세 정보:**
   - 원두명
   - 현재 보유량 (kg)
   - 최근 입고 날짜
   - 최근 출고 날짜
   - 사용 추이 그래프

3. **API로 조회:**

```bash
curl "http://localhost:8000/api/v1/inventory"
```

**팁:**

- 재고는 로스팅 로그에서 자동 계산
- 부족한 원두는 경고 표시 (threshold 설정 가능)

---

## ⚙️ 개발 환경 (Development)

### 11. 새 패키지 설치하기

**목적:** 프로젝트에 새 패키지 추가하기

**Backend (Python):**

```bash
cd backend

# 패키지 설치
../venv/bin/pip install package_name

# 또는 버전 지정
../venv/bin/pip install package_name==1.2.3

# 의존성 저장
../venv/bin/pip freeze > requirements.txt

# 설치 확인
../venv/bin/pip show package_name
```

**Frontend (Node.js):**

```bash
cd frontend

# 프로덕션 의존성
npm install package-name

# 개발 의존성
npm install --save-dev package-name

# 버전 지정
npm install package-name@1.2.3

# 설치 확인
npm list package-name
```

**예시:**

```bash
# Backend: 새 데이터 분석 라이브러리
cd backend
../venv/bin/pip install pandas==2.0.0
../venv/bin/pip freeze > requirements.txt

# Frontend: UI 라이브러리
cd frontend
npm install @radix-ui/react-dialog
```

---

### 12. 의존성 업데이트하기

**목적:** 설치된 패키지 버전 업그레이드하기

**Backend:**

```bash
cd backend

# 단일 패키지 업그레이드
../venv/bin/pip install --upgrade package_name

# 전체 패키지 업그레이드
../venv/bin/pip install --upgrade -r requirements.txt

# 의존성 저장
../venv/bin/pip freeze > requirements.txt

# 테스트
../venv/bin/pytest
```

**Frontend:**

```bash
cd frontend

# 특정 패키지 업데이트
npm update package-name

# 모든 패키지 업데이트
npm update

# 또는 최신 버전으로
npm install package-name@latest

# 테스트
npm run build
npm run test
```

**경고:**

- 주요 버전 업그레이드 전에 항상 테스트
- `package.json` / `requirements.txt` 변경사항은 Git에 커밋

---

### 13. 데이터베이스 초기화하기

**목적:** 데이터베이스를 초기 상태로 리셋하기

**단계:**

1. **데이터베이스 백업 (권장):**

```bash
# PostgreSQL 백업
pg_dump -h localhost -U postgres themoon_db > backup_$(date +%Y%m%d).sql
```

2. **데이터베이스 초기화:**

```bash
# 방법 1: 테이블만 삭제
psql -h localhost -U postgres -d themoon_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# 방법 2: 데이터베이스 재생성
dropdb -h localhost -U postgres themoon_db
createdb -h localhost -U postgres themoon_db
```

3. **마이그레이션 실행:**

```bash
cd backend
../venv/bin/alembic upgrade head
```

4. **확인:**

```bash
psql -h localhost -U postgres -d themoon_db -c "\dt"
```

**⚠️ 주의:** 모든 데이터가 삭제됩니다!

---

### 14. 테스트 데이터 생성하기

**목적:** 개발/테스트용 샘플 데이터 만들기

**단계:**

1. **스크립트 실행:**

```bash
cd backend
../venv/bin/python -m scripts.seed_data
```

2. **생성되는 데이터:**
   - 13종 원두
   - 7개 블렌드 레시피
   - 30개 로스팅 로그
   - 비용 설정

3. **API로 생성:**

```bash
curl -X POST "http://localhost:8000/api/v1/dev/seed-data"
```

4. **확인:**

```bash
curl "http://localhost:8000/api/v1/beans"
curl "http://localhost:8000/api/v1/blends"
```

**팁:**

- `seed_data.py` 스크립트는 idempotent (여러 번 실행 가능)
- 기존 데이터 유지하면서 추가 데이터 생성
- 리셋하려면 DB 초기화 후 실행

---

## 🔄 버전 관리 (Version Control)

### 15. Git 커밋하기

**목적:** 변경사항을 Git에 커밋하기

**단계:**

1. **변경사항 확인:**

```bash
git status
git diff
```

2. **파일 추가:**

```bash
# 특정 파일만
git add backend/app/services/new_service.py

# 모든 변경사항
git add .
```

3. **커밋 메시지 작성:**

```bash
git commit -m "feat: 새로운 API 엔드포인트 추가

- /api/v1/beans CRUD 구현
- Pydantic 스키마 정의
- 단위 테스트 추가"
```

4. **푸시 (선택):**

```bash
git push origin main
```

5. **확인:**

```bash
git log --oneline | head -5
```

**커밋 타입:**

- `feat:` - 새로운 기능
- `fix:` - 버그 수정
- `docs:` - 문서 업데이트
- `refactor:` - 코드 리팩토링
- `test:` - 테스트 추가
- `chore:` - 빌드, 패키지 관리

**`.agent/instructions.md` 규칙 참조!**

---

### 16. 버전 업데이트하기

**목적:** 프로젝트 버전 번호 업데이트하기

**단계:**

1. **현재 버전 확인:**

```bash
cat logs/VERSION
# 출력: 0.0.3
```

2. **새 버전으로 업데이트:**

```bash
# Semantic Versioning 규칙:
# MAJOR.MINOR.PATCH
# - PATCH: 버그 수정 (0.0.3 → 0.0.4)
# - MINOR: 새 기능 (0.0.0 → 0.1.0)
# - MAJOR: 호환성 깨짐 (0.0.0 → 1.0.0)

# 스크립트로 자동 업데이트
./venv/bin/python logs/update_version.py --type patch --summary "버그 수정"
```

3. **CHANGELOG 업데이트:**

```bash
# logs/CHANGELOG.md 편집
cat logs/CHANGELOG.md
```

4. **모든 문서 버전 동기화:**

```bash
# README.md, .claude/CLAUDE.md 버전 일치시키기
# .agent/instructions.md 참조
```

5. **커밋:**

```bash
git add logs/VERSION logs/CHANGELOG.md README.md .claude/CLAUDE.md
git commit -m "chore: v0.0.4 버전 업데이트"
```

**📌 버전 관리 규칙: `logs/VERSION_MANAGEMENT.md` 참조**

---

### 17. 포트 충돌 해결하기

**목적:** 포트 3000, 8000이 이미 사용 중일 때 해결하기

**단계:**

1. **포트 점유 프로세스 확인:**

```bash
# Backend (8000)
lsof -i :8000

# Frontend (3000)
lsof -i :3000
```

2. **프로세스 종료:**

```bash
# Backend 종료
lsof -ti :8000 | xargs kill -9

# Frontend 종료
lsof -ti :3000 | xargs kill -9

# 또는 특정 프로세스 종료
pkill -f uvicorn
pkill -f "next dev"
```

3. **다른 포트로 실행:**

```bash
# Backend
cd backend
../venv/bin/uvicorn app.main:app --reload --port 8001

# Frontend
cd frontend
PORT=3001 npm run dev
```

4. **확인:**

```bash
lsof -i :8000  # 비어있어야 함
lsof -i :3000  # 비어있어야 함
curl http://localhost:8001/docs  # 새 포트 확인
```

---

### 18. 데이터베이스 백업하기

**목적:** 데이터베이스 정기적으로 백업하기

**단계:**

1. **PostgreSQL 백업:**

```bash
# SQL 덤프 백업 (권장)
pg_dump -h localhost -U postgres themoon_db > backup_$(date +%Y%m%d_%H%M%S).sql

# 압축 백업
pg_dump -h localhost -U postgres themoon_db | gzip > backup_$(date +%Y%m%d).sql.gz

# 특정 테이블만 백업
pg_dump -h localhost -U postgres -t beans -t blends themoon_db > tables_backup.sql
```

2. **복원하기:**

```bash
# SQL 덤프에서 복원
psql -h localhost -U postgres themoon_db < backup_20251129.sql

# 압축 파일 복원
gunzip -c backup_20251129.sql.gz | psql -h localhost -U postgres themoon_db
```

3. **자동 백업 설정 (선택):**

```bash
# cron 작업으로 매일 백업
crontab -e
# 다음 추가:
# 0 2 * * * pg_dump -h localhost -U postgres themoon_db > /path/to/backup/themoon_db_$(date +\%Y\%m\%d).sql
```

4. **백업 확인:**

```bash
ls -lh backup_*.sql
```

---

## 🛠️ 고급 개발 (Advanced Development)

### 19. 새 페이지 추가하기

**목적:** Next.js에서 새로운 UI 페이지 추가하기

**단계:**

1. **페이지 파일 생성:**

```bash
cd frontend
touch app/new-feature/page.tsx
```

2. **기본 구조 작성:**

```typescript
// app/new-feature/page.tsx
"use client"

import { useState, useEffect } from 'react'
import PageHero from '@/components/ui/PageHero'
import Card from '@/components/ui/Card'

export default function NewFeaturePage() {
  const [data, setData] = useState([])

  useEffect(() => {
    // API 호출
    fetch('/api/data')
      .then(res => res.json())
      .then(setData)
  }, [])

  return (
    <div className="container mx-auto p-6">
      <PageHero 
        title="New Feature" 
        subtitle="Description" 
      />

      <div className="grid grid-cols-3 gap-4 mt-6">
        {data.map(item => (
          <Card key={item.id} title={item.name}>
            {item.description}
          </Card>
        ))}
      </div>
    </div>
  )
}
```

3. **Sidebar에 링크 추가:**

```typescript
// components/layout/Sidebar.tsx
const navItems = [
  // ... existing
  { name: 'New Feature', href: '/new-feature', icon: Star }
]
```

4. **테스트:**

```bash
npm run dev
# http://localhost:3000/new-feature 접속 확인
```

**Linear Design System 가이드 참조**

---

### 20. 새 API 엔드포인트 추가하기

**목적:** FastAPI에서 새 REST API 엔드포인트 추가하기

**단계:**

1. **스키마 정의 (Pydantic):**

```bash
cd backend
touch app/schemas/feature_schema.py
```

```python
# app/schemas/feature_schema.py
from pydantic import BaseModel
from typing import Optional

class FeatureBase(BaseModel):
    name: str
    description: Optional[str] = None

class FeatureCreate(FeatureBase):
    pass

class FeatureUpdate(FeatureBase):
    pass

class FeatureResponse(FeatureBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

2. **서비스 로직 (CRUD):**

```bash
touch app/services/feature_service.py
```

```python
# app/services/feature_service.py
from sqlalchemy.orm import Session
from app.models.feature import Feature
from app.schemas.feature_schema import FeatureCreate

class FeatureService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: FeatureCreate):
        feature = Feature(**data.dict())
        self.db.add(feature)
        self.db.commit()
        self.db.refresh(feature)
        return feature

    def get_all(self):
        return self.db.query(Feature).all()

    def get_by_id(self, feature_id: int):
        return self.db.query(Feature).filter(
            Feature.id == feature_id
        ).first()
```

3. **라우터 정의:**

```bash
touch app/api/v1/feature.py
```

```python
# app/api/v1/feature.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.feature_service import FeatureService
from app.schemas.feature_schema import FeatureCreate, FeatureResponse

router = APIRouter(prefix="/features", tags=["features"])

@router.post("/", response_model=FeatureResponse)
def create_feature(data: FeatureCreate, db: Session = Depends(get_db)):
    service = FeatureService(db)
    return service.create(data)

@router.get("/", response_model=list[FeatureResponse])
def get_features(db: Session = Depends(get_db)):
    service = FeatureService(db)
    return service.get_all()

@router.get("/{feature_id}", response_model=FeatureResponse)
def get_feature(feature_id: int, db: Session = Depends(get_db)):
    service = FeatureService(db)
    feature = service.get_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Not found")
    return feature
```

4. **라우터 등록:**

```python
# app/api/v1/__init__.py
from app.api.v1 import bean, blend, feature

def register_routers(app):
    app.include_router(bean.router)
    app.include_router(blend.router)
    app.include_router(feature.router)  # 추가
```

5. **테스트:**

```bash
# 앱 실행
cd backend
../venv/bin/uvicorn app.main:app --reload

# API 문서 확인
http://localhost:8000/docs

# 테스트
curl -X POST "http://localhost:8000/api/v1/features" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Feature", "description": "Description"}'
```

---

### 21. 새 모델 추가하기

**목적:** SQLAlchemy 모델을 통해 새 데이터베이스 테이블 정의하기

**단계:**

1. **모델 파일 생성:**

```bash
cd backend
touch app/models/feature.py
```

2. **SQLAlchemy 모델 정의:**

```python
# app/models/feature.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Feature {self.name}>"
```

3. **모델 등록:**

```python
# app/models/__init__.py
from app.models.bean import Bean
from app.models.blend import Blend
from app.models.feature import Feature  # 추가
```

4. **마이그레이션 생성:**

```bash
# Alembic 마이그레이션 생성
cd backend
../venv/bin/alembic revision --autogenerate -m "Add Feature table"

# 마이그레이션 적용
../venv/bin/alembic upgrade head
```

5. **데이터베이스 확인:**

```bash
psql -h localhost -U postgres -d themoon_db -c "\d features"
```

---

### 22. 새 컴포넌트 만들기

**목적:** React에서 재사용 가능한 UI 컴포넌트 만들기

**단계:**

1. **컴포넌트 파일 생성:**

```bash
cd frontend
touch components/ui/Badge.tsx
```

2. **컴포넌트 정의:**

```typescript
// components/ui/Badge.tsx
interface BadgeProps {
  children: React.ReactNode
  variant?: 'success' | 'warning' | 'error' | 'info'
  size?: 'sm' | 'md' | 'lg'
}

export default function Badge({ 
  children, 
  variant = 'info',
  size = 'md'
}: BadgeProps) {
  const variantStyles = {
    success: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
    info: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
  }

  const sizeStyles = {
    sm: 'text-xs px-2 py-1',
    md: 'text-sm px-3 py-1',
    lg: 'text-base px-4 py-2'
  }

  return (
    <span className={`
      inline-flex items-center rounded-full font-medium
      ${variantStyles[variant]}
      ${sizeStyles[size]}
    `}>
      {children}
    </span>
  )
}
```

3. **Export 추가:**

```typescript
// components/ui/index.ts
export { default as Card } from './Card'
export { default as Badge } from './Badge'  // 추가
```

4. **사용 예시:**

```typescript
import { Badge } from '@/components/ui'

<Badge variant="success">완료</Badge>
<Badge variant="warning" size="sm">대기중</Badge>
```

5. **테스트:**

```bash
npm run dev
# 페이지에서 컴포넌트 확인
```

---

### 23. 디버깅 모드 실행하기

**목적:** 개발 중 디버깅 정보를 자세히 확인하기

**Backend (FastAPI):**

```bash
# 로그 레벨 설정
cd backend
../venv/bin/uvicorn app.main:app --reload --log-level debug

# 로그를 파일에 저장
../venv/bin/uvicorn app.main:app --reload 2>&1 | tee debug.log

# 로그 확인
grep -i "error" debug.log
grep -i "warning" debug.log
```

**Frontend (Next.js):**

```bash
cd frontend

# 개발 모드 (기본적으로 디버그 정보 포함)
npm run dev

# Chrome DevTools 사용
# F12 > Console, Network, Sources 탭 활용
```

**디버깅 팁:**

```typescript
// Frontend 디버깅
console.log('Data:', data)
console.error('Error occurred:', error)

// Network 요청 확인
fetch('/api/endpoint')
  .then(res => {
    console.log('Response:', res)
    return res.json()
  })
  .catch(err => console.error('Fetch error:', err))
```

```python
# Backend 디버깅
import logging
logger = logging.getLogger(__name__)

@router.get("/debug")
def debug_endpoint():
    logger.debug("Debug info")
    logger.info("Info message")
    logger.warning("Warning")
    logger.error("Error")
    return {"status": "ok"}
```

---

### 24. 성능 최적화하기

**목적:** 느린 부분을 찾아 성능 개선하기

**Frontend 최적화:**

```typescript
// 1. React.memo로 불필요한 리렌더링 방지
import { memo } from 'react'

const BeanCard = memo(({ bean }) => {
  return <div>{bean.name}</div>
})

// 2. useMemo로 연산 캐싱
const expensiveValue = useMemo(() => {
  return calculateExpensiveValue(data)
}, [data])

// 3. useCallback으로 함수 메모이제이션
const handleClick = useCallback(() => {
  doSomething(id)
}, [id])

// 4. Dynamic Import로 코드 스플리팅
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <p>Loading...</p>
})

// 5. Image 최적화
import Image from 'next/image'
<Image src="/bean.jpg" width={300} height={300} alt="Bean" />
```

**Backend 최적화:**

```python
# 1. N+1 쿼리 해결
# ❌ 느림
beans = db.query(Bean).all()
for bean in beans:
    price = bean.price  # 각 bean마다 쿼리

# ✅ 빠름
beans = db.query(Bean).options(
    joinedload(Bean.prices)
).all()

# 2. 인덱스 추가
class Bean(Base):
    name = Column(String, index=True)  # 인덱스 추가
    price = Column(Float, index=True)

# 3. 페이지네이션
@router.get("/beans")
def get_beans(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Bean).offset(skip).limit(limit).all()

# 4. 캐싱 (Redis)
from fastapi_cache import cache

@router.get("/expensive")
@cache(expire=60)  # 60초 캐시
def expensive_endpoint():
    return expensive_calculation()
```

---

### 25. 문서 작성하기

**목적:** 새 기능에 대한 문서 작성하기

**단계:**

1. **문서 파일 생성:**

```bash
# 기능 가이드
touch Documents/Guides/새기능_가이드.md

# 또는 아키텍처 문서
touch Documents/Architecture/새기능_설계.md
```

2. **문서 작성:**

```markdown
# 새 기능 가이드

## 목적

기능의 목적 설명

## 사용 방법

### 1단계

첫 번째 단계

### 2단계

두 번째 단계

## API 명세

\`\`\`
POST /api/v1/feature
Request: { "name": "Feature" }
Response: { "id": 1, "name": "Feature" }
\`\`\`

## 예시

코드 예시 또는 스크린샷

## FAQ

자주 묻는 질문
```

3. **문서 구조:**

```
Documents/
├── Architecture/     # 기술 설계 문서
│   ├── SYSTEM_ARCHITECTURE.md
│   └── 새기능_설계.md
├── Guides/          # 사용 가이드
│   ├── PROGRAMMING_RULES.md
│   └── 새기능_사용법.md
└── Progress/        # 진행 상황
    └── SESSION_SUMMARY_*.md
```

4. **문서 커밋:**

```bash
git add Documents/
git commit -m "docs: 새 기능 가이드 추가

- 기능 설명
- 사용 방법
- API 명세
- 예시 코드"
```

**`.agent/instructions.md` 규칙 참조**

---

## 📌 빠른 단축키

| 작업 | 명령어 |
|------|--------|
| Backend 시작 | `cd backend && ../venv/bin/uvicorn app.main:app --reload` |
| Frontend 시작 | `cd frontend && npm run dev` |
| 모두 시작 | `./start_all.sh` |
| Backend 중지 | `lsof -ti :8000 \| xargs kill -9` |
| Frontend 중지 | `lsof -ti :3000 \| xargs kill -9` |
| DB 백업 | `pg_dump themoon_db > backup.sql` |
| 마이그레이션 | `cd backend && ../venv/bin/alembic upgrade head` |
| 테스트 데이터 | `cd backend && ../venv/bin/python -m scripts.seed_data` |
| Git 커밋 | `git add . && git commit -m "메시지"` |
| 버전 확인 | `cat logs/VERSION` |
| API 문서 | `http://localhost:8000/docs` |
| 패키지 설치 (BE) | `cd backend && ../venv/bin/pip install package` |
| 패키지 설치 (FE) | `cd frontend && npm install package` |

---

## 🔗 참고 문서

| 문서 | 위치 | 용도 |
|------|------|------|
| **프로그래밍 규칙** | `Documents/Guides/PROGRAMMING_RULES.md` | 개발 규칙 및 컨벤션 |
| **개발 가이드** | `Documents/Architecture/DEVELOPMENT_GUIDE.md` | 5단계 개발 프로세스 |
| **시스템 아키텍처** | `Documents/Architecture/SYSTEM_ARCHITECTURE.md` | 시스템 구조 및 데이터 흐름 |
| **문제 해결** | `Documents/Architecture/TROUBLESHOOTING.md` | 오류 및 해결법 |
| **버전 관리** | `logs/VERSION_MANAGEMENT.md` | 버전 관리 가이드 |
| **AI 규칙** | `.agent/instructions.md` | AI Assistant 규칙 |

---

**마지막 업데이트: 2025-11-29**

**프로젝트:** TheMoon v0.0.3 (Next.js + FastAPI + PostgreSQL)
