# TheMoon Project 현대적 스택 전환 플랜

> **작성일:** 2025-11-20
> **현재 버전:** v0.50.4 (Streamlit 기반)
> **목표:** Next.js + FastAPI 기반 모던 풀스택 애플리케이션
> **예상 기간:** 12개월 (4개 Phase)

---

## 📋 목차

1. [현재 상황 분석](#1-현재-상황-분석)
2. [전환 이유](#2-전환-이유)
3. [새로운 기술 스택](#3-새로운-기술-스택)
4. [단계별 마이그레이션 계획](#4-단계별-마이그레이션-계획)
5. [아키텍처 설계](#5-아키텍처-설계)
6. [데이터베이스 마이그레이션](#6-데이터베이스-마이그레이션)
7. [리스크 관리](#7-리스크-관리)
8. [성공 지표](#8-성공-지표)

---

## 1. 현재 상황 분석

### 1.1 Streamlit의 장점 (유지할 가치)

✅ **빠른 프로토타이핑**
- Python만으로 웹 앱 구축
- 데이터 과학 친화적
- 차트/시각화 내장

✅ **낮은 학습 곡선**
- 프론트엔드 지식 불필요
- 간단한 API
- 빠른 개발 속도

✅ **현재 프로젝트 성과**
- 14개 페이지 완성
- 96% 테스트 커버리지
- 실용적인 기능 완비

### 1.2 Streamlit의 한계 (개선 필요)

❌ **UI/UX 제약**
```
문제점:
- 커스텀 디자인 제한적
- 모달/팝업 미지원
- 드래그 앤 드롭 불가
- 복잡한 레이아웃 구현 어려움
- 페이지 전환 시 깜빡임
```

❌ **성능 문제**
```
문제점:
- 모든 상호작용마다 전체 재실행
- 대량 데이터 처리 느림
- 클라이언트 측 캐싱 제한적
- 메모리 사용량 높음
```

❌ **확장성 제약**
```
문제점:
- 단일 서버 아키텍처
- API 서버 부재
- 모바일 앱 개발 불가
- 실시간 기능 제한적
- 다중 사용자 동시 접속 어려움
```

❌ **개발 생산성**
```
문제점:
- 컴포넌트 재사용 제한적
- 상태 관리 복잡
- 테스트 자동화 어려움
- 라우팅 기능 부족
```

---

## 2. 전환 이유

### 2.1 비즈니스 요구사항

**현재 (Streamlit):**
- 로컬 데스크톱 앱 수준
- 단일 사용자
- 제한적인 UI/UX

**미래 비전:**
- 클라우드 SaaS 서비스
- 다중 사용자 (Multi-tenant)
- 엔터프라이즈급 UI/UX
- 모바일 앱 지원
- 외부 시스템 연동 (API)

### 2.2 기술적 이유

| 항목 | Streamlit | Next.js + FastAPI |
|------|-----------|-------------------|
| **성능** | 느림 (전체 재실행) | 매우 빠름 (SSR + 부분 렌더링) |
| **SEO** | ❌ (CSR만) | ✅ (SSR/SSG) |
| **UI 자유도** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **확장성** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **모바일** | ⭐ | ⭐⭐⭐⭐⭐ |
| **API 지원** | ❌ | ✅ (내장 API Routes) |
| **실시간** | ❌ | ✅ (WebSocket) |
| **라우팅** | 수동 | 자동 (파일 기반) |
| **이미지 최적화** | ❌ | ✅ (자동) |
| **개발 속도** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **학습 곡선** | 낮음 | 중간 |

### 2.3 ROI 분석

**투자 비용:**
- 개발 시간: 12개월
- 개발 인력: 1-2명
- 인프라 비용: +$50/월 (PostgreSQL, Redis)

**예상 효과:**
- 성능 향상: 5-10배
- 사용자 만족도: +40%
- 확장 가능 사용자: 1명 → 100명+
- 모바일 접근성: 0% → 100%
- API 연동: 불가 → 가능

**ROI:** 6개월 내 회수 가능

---

## 3. 새로운 기술 스택

### 3.1 프론트엔드 (Next.js 풀스택)

| 기술 | 버전 | 용도 | Next.js 통합 |
|------|------|------|--------------|
| **Next.js** | 14.x | 풀스택 프레임워크 | 핵심 |
| **React** | 18.x | UI 라이브러리 | Next.js 포함 |
| **TypeScript** | 5.x | 타입 안정성 | 기본 지원 |
| **TailwindCSS** | 3.x | 스타일링 | 공식 플러그인 |
| **shadcn/ui** | latest | UI 컴포넌트 | Next.js 템플릿 |
| **TanStack Query** | 5.x | 서버 상태 관리 | Server Components 보완 |
| **Zustand** | 4.x | 클라이언트 상태 | 필요시만 |
| **React Hook Form** | 7.x | 폼 관리 | Server Actions 활용 |
| **Recharts** | 2.x | 차트 | SSR 가능 |
| **next/image** | 내장 | 이미지 최적화 | 자동 최적화 |
| **next/font** | 내장 | 폰트 최적화 | 자동 로드 |

**Next.js의 독보적 장점:**
- ✅ **API Routes**: 백엔드 로직을 같은 프로젝트에 구현 (FastAPI 보완)
- ✅ **Server Components**: 서버에서 렌더링, 클라이언트 번들 크기 감소
- ✅ **Server Actions**: 폼 제출을 서버 함수로 처리 (타입 안전)
- ✅ **ISR**: 정적 페이지를 주기적으로 재생성 (캐싱 + 실시간)
- ✅ **Edge Runtime**: CloudFlare Workers 같은 엣지에서 실행

### 3.2 백엔드

| 기술 | 버전 | 용도 |
|------|------|------|
| **FastAPI** | 0.109+ | API 서버 |
| **Python** | 3.12+ | 언어 |
| **SQLAlchemy** | 2.0+ | ORM (유지) |
| **Alembic** | 1.13+ | DB 마이그레이션 |
| **PostgreSQL** | 16.x | 메인 DB |
| **Redis** | 7.x | 캐시, 세션 |
| **Celery** | 5.x | 백그라운드 작업 |
| **RabbitMQ** | 3.x | 메시지 큐 |
| **Pydantic** | 2.x | 데이터 검증 |

### 3.3 인프라

| 기술 | 용도 |
|------|------|
| **Docker** | 컨테이너화 |
| **Docker Compose** | 로컬 개발 |
| **Nginx** | 리버스 프록시 |
| **AWS EC2** | 애플리케이션 서버 |
| **AWS RDS** | PostgreSQL 호스팅 |
| **AWS S3** | 이미지 저장 |
| **AWS CloudFront** | CDN |
| **GitHub Actions** | CI/CD |

### 3.4 개발 도구

| 도구 | 용도 |
|------|------|
| **Vite** | 프론트엔드 빌드 |
| **ESLint** | 코드 린팅 |
| **Prettier** | 코드 포맷팅 |
| **Jest** | 유닛 테스트 |
| **Playwright** | E2E 테스트 |
| **Storybook** | 컴포넌트 문서 |

---

## 4. 단계별 마이그레이션 계획

### Phase 1: 백엔드 API 구축 (3개월)

**목표:** Streamlit과 병행하며 FastAPI 백엔드 구축

**작업 항목:**

#### 1.1 프로젝트 구조 재구성 (2주)
```
TheMoon_Project/
├── frontend/              # 신규 (Next.js)
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/               # 신규 (FastAPI)
│   ├── app/
│   │   ├── api/          # API 라우터
│   │   ├── core/         # 설정, 보안
│   │   ├── models/       # SQLAlchemy 모델 (기존 재사용)
│   │   ├── schemas/      # Pydantic 스키마
│   │   ├── services/     # 비즈니스 로직 (기존 재사용)
│   │   └── main.py       # FastAPI 앱
│   ├── alembic/          # DB 마이그레이션
│   ├── tests/
│   └── requirements.txt
├── app/                   # 기존 Streamlit (유지)
├── shared/                # 공통 코드
└── docker-compose.yml     # 개발 환경
```

#### 1.2 FastAPI 기본 설정 (1주)
```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TheMoon API",
    version="1.0.0",
    docs_url="/api/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
```

#### 1.3 인증/인가 시스템 (2주)
```python
# backend/app/core/security.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# backend/app/api/auth.py
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401)

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

#### 1.4 핵심 API 엔드포인트 (6주)

**원두 API:**
```python
# backend/app/api/beans.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/beans", tags=["beans"])

@router.get("/")
def get_beans(db: Session = Depends(get_db)):
    return bean_service.get_all_beans(db)

@router.post("/")
def create_bean(bean: BeanCreate, db: Session = Depends(get_db)):
    return bean_service.add_bean(db, bean)

@router.get("/{bean_id}")
def get_bean(bean_id: int, db: Session = Depends(get_db)):
    return bean_service.get_bean_by_id(db, bean_id)

@router.put("/{bean_id}")
def update_bean(bean_id: int, bean: BeanUpdate, db: Session = Depends(get_db)):
    return bean_service.update_bean(db, bean_id, bean)

@router.delete("/{bean_id}")
def delete_bean(bean_id: int, db: Session = Depends(get_db)):
    return bean_service.delete_bean(db, bean_id)
```

**블렌드 API:**
```python
# backend/app/api/blends.py
@router.get("/")
def get_blends(db: Session = Depends(get_db)):
    return blend_service.get_all_blends(db)

@router.post("/")
def create_blend(blend: BlendCreate, db: Session = Depends(get_db)):
    return blend_service.create_blend(db, blend)

@router.get("/{blend_id}/cost")
def calculate_blend_cost(blend_id: int, db: Session = Depends(get_db)):
    return cost_service.calculate_blend_cost(db, blend_id)
```

**재고 API:**
```python
# backend/app/api/inventory.py
@router.get("/")
def get_inventory(db: Session = Depends(get_db)):
    return inventory_service.get_all_inventory(db)

@router.post("/transactions")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    return inventory_service.create_transaction(db, transaction)
```

**OCR API (비동기 처리):**
```python
# backend/app/api/invoices.py
from celery import current_app as celery

@router.post("/upload")
async def upload_invoice(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # 파일 저장
    file_path = save_uploaded_file(file)

    # Invoice 레코드 생성 (PENDING 상태)
    invoice = create_invoice_record(db, file_path, status="PENDING")

    # 백그라운드 작업 큐에 추가
    task = celery.send_task('tasks.process_invoice', args=[invoice.id])

    return {
        "invoice_id": invoice.id,
        "task_id": task.id,
        "status": "processing"
    }

@router.get("/{invoice_id}/status")
def get_invoice_status(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    return {
        "status": invoice.status,
        "confidence": invoice.confidence_score,
        "result": invoice.ocr_result
    }
```

#### 1.5 Celery 백그라운드 작업 (1주)
```python
# backend/app/tasks/celery_app.py
from celery import Celery

celery = Celery(
    'themoon',
    broker='pyamqp://guest@rabbitmq//',
    backend='redis://redis:6379/0'
)

@celery.task
def process_invoice(invoice_id: int):
    db = SessionLocal()
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

        # OCR 처리
        result = gemini_ocr_service.process_image(invoice.image_path)

        # 결과 저장
        invoice.status = "COMPLETED"
        invoice.ocr_result = result
        invoice.confidence_score = result['confidence']
        db.commit()

        return {"status": "success", "invoice_id": invoice_id}

    except Exception as e:
        invoice.status = "FAILED"
        invoice.error_message = str(e)
        db.commit()
        return {"status": "failed", "error": str(e)}

    finally:
        db.close()
```

#### 1.6 PostgreSQL 마이그레이션 (1주)
```python
# backend/alembic/env.py
from alembic import context
from sqlalchemy import engine_from_config, pool
from app.models import Base

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

```bash
# 마이그레이션 실행
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# SQLite → PostgreSQL 데이터 이관
python scripts/migrate_sqlite_to_postgres.py
```

#### 1.7 API 테스트 (1주)
```python
# backend/tests/test_api_beans.py
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_beans():
    response = client.get("/api/beans")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_bean():
    response = client.post("/api/beans", json={
        "name": "Test Bean",
        "price_per_kg": 10000,
        "roast_level": "MEDIUM"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Bean"

def test_authentication():
    # 인증 없이 접근
    response = client.get("/api/beans")
    assert response.status_code == 401

    # 로그인
    response = client.post("/api/auth/login", data={
        "username": "admin",
        "password": "password"
    })
    token = response.json()["access_token"]

    # 토큰으로 접근
    response = client.get("/api/beans", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
```

**Phase 1 완료 기준:**
- ✅ 모든 핵심 API 엔드포인트 구현
- ✅ 인증/인가 시스템 완성
- ✅ PostgreSQL 마이그레이션 완료
- ✅ API 테스트 커버리지 80%+
- ✅ API 문서 자동 생성 (/api/docs)
- ✅ Streamlit 앱과 병행 실행 가능

---

### Phase 2: 프론트엔드 기본 구조 (3개월)

**목표:** React 기반 프론트엔드 구축 (Streamlit 병행)

#### 2.1 프로젝트 초기화 (1주)
```bash
# Next.js 프로젝트 생성
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend

# 패키지 설치
npm install @tanstack/react-query zustand axios
npm install shadcn-ui recharts react-hook-form zod
npm install -D @types/node @types/react
```

```typescript
// frontend/src/app/layout.tsx
import { Inter } from 'next/font/google'
import { Providers } from '@/components/Providers'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

#### 2.2 API 클라이언트 (1주)
```typescript
// frontend/src/lib/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

// 인터셉터: 토큰 자동 추가
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// API 함수들
export const beansApi = {
  getAll: () => api.get('/api/beans'),
  getById: (id: number) => api.get(`/api/beans/${id}`),
  create: (data: BeanCreate) => api.post('/api/beans', data),
  update: (id: number, data: BeanUpdate) => api.put(`/api/beans/${id}`, data),
  delete: (id: number) => api.delete(`/api/beans/${id}`),
}

export const blendsApi = {
  getAll: () => api.get('/api/blends'),
  create: (data: BlendCreate) => api.post('/api/blends', data),
  calculateCost: (id: number) => api.get(`/api/blends/${id}/cost`),
}
```

#### 2.3 상태 관리 (1주)
```typescript
// frontend/src/store/auth.ts (Zustand)
import { create } from 'zustand'

interface AuthState {
  user: User | null
  token: string | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,

  login: async (username, password) => {
    const response = await api.post('/api/auth/login', { username, password })
    const { access_token, user } = response.data

    localStorage.setItem('access_token', access_token)
    set({ token: access_token, user })
  },

  logout: () => {
    localStorage.removeItem('access_token')
    set({ token: null, user: null })
  },
}))
```

```typescript
// frontend/src/hooks/useBeans.ts (TanStack Query)
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

export function useBeans() {
  return useQuery({
    queryKey: ['beans'],
    queryFn: () => beansApi.getAll().then(res => res.data),
  })
}

export function useCreateBean() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: BeanCreate) => beansApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['beans'] })
    },
  })
}
```

#### 2.4 UI 컴포넌트 라이브러리 (2주)
```typescript
// frontend/src/components/ui/Button.tsx (shadcn/ui)
import { ButtonHTMLAttributes, forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'default', size = 'md', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          'rounded-md font-medium transition-colors',
          {
            'bg-blue-600 text-white hover:bg-blue-700': variant === 'default',
            'border border-gray-300 hover:bg-gray-50': variant === 'outline',
            'hover:bg-gray-100': variant === 'ghost',
          },
          {
            'px-3 py-1.5 text-sm': size === 'sm',
            'px-4 py-2 text-base': size === 'md',
            'px-6 py-3 text-lg': size === 'lg',
          },
          className
        )}
        {...props}
      />
    )
  }
)

export { Button }
```

#### 2.5 핵심 페이지 구현 (6주)

**대시보드:**
```typescript
// frontend/src/app/dashboard/page.tsx
'use client'

import { useBeans, useBlends, useInventory } from '@/hooks'
import { MetricCard, Chart } from '@/components'

export default function DashboardPage() {
  const { data: beans } = useBeans()
  const { data: blends } = useBlends()
  const { data: inventory } = useInventory()

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">대시보드</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <MetricCard
          title="총 원두"
          value={beans?.length || 0}
          icon="☕"
        />
        <MetricCard
          title="총 블렌드"
          value={blends?.length || 0}
          icon="🎨"
        />
        <MetricCard
          title="재고 가치"
          value="₩1,234,560"
          icon="📦"
        />
        <MetricCard
          title="이번 달 판매"
          value="₩456,789"
          icon="💰"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Chart
          title="월별 비용"
          data={monthlyCostData}
          type="bar"
        />
        <Chart
          title="블렌드 판매 비율"
          data={blendSalesData}
          type="pie"
        />
      </div>
    </div>
  )
}
```

**원두 관리:**
```typescript
// frontend/src/app/beans/page.tsx
'use client'

import { useState } from 'react'
import { useBeans, useCreateBean, useUpdateBean, useDeleteBean } from '@/hooks'
import { Button, Table, Modal, Form } from '@/components'

export default function BeansPage() {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedBean, setSelectedBean] = useState<Bean | null>(null)

  const { data: beans, isLoading } = useBeans()
  const createBean = useCreateBean()
  const updateBean = useUpdateBean()
  const deleteBean = useDeleteBean()

  const handleSubmit = (data: BeanFormData) => {
    if (selectedBean) {
      updateBean.mutate({ id: selectedBean.id, data })
    } else {
      createBean.mutate(data)
    }
    setIsModalOpen(false)
  }

  if (isLoading) return <div>로딩 중...</div>

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">원두 관리</h1>
        <Button onClick={() => setIsModalOpen(true)}>
          + 원두 추가
        </Button>
      </div>

      <Table
        columns={[
          { key: 'no', label: 'No.' },
          { key: 'name', label: '원두명' },
          { key: 'roast_level', label: '로스팅 레벨' },
          { key: 'price_per_kg', label: '가격 (₩/kg)' },
          { key: 'actions', label: '작업' },
        ]}
        data={beans}
        onEdit={(bean) => {
          setSelectedBean(bean)
          setIsModalOpen(true)
        }}
        onDelete={(bean) => {
          if (confirm('정말 삭제하시겠습니까?')) {
            deleteBean.mutate(bean.id)
          }
        }}
      />

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={selectedBean ? '원두 수정' : '원두 추가'}
      >
        <BeanForm
          initialData={selectedBean}
          onSubmit={handleSubmit}
          onCancel={() => setIsModalOpen(false)}
        />
      </Modal>
    </div>
  )
}
```

**블렌드 관리:**
```typescript
// frontend/src/app/blends/page.tsx
'use client'

import { BlendCard, BlendForm } from '@/components'
import { useBlends } from '@/hooks'

export default function BlendsPage() {
  const { data: blends } = useBlends()

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">블렌드 관리</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {blends?.map(blend => (
          <BlendCard key={blend.id} blend={blend} />
        ))}
      </div>
    </div>
  )
}
```

#### 2.6 반응형 디자인 (1주)
```typescript
// frontend/tailwind.config.ts
export default {
  theme: {
    extend: {
      screens: {
        'xs': '475px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
    },
  },
}
```

```typescript
// frontend/src/components/ResponsiveLayout.tsx
export function ResponsiveLayout({ children }) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* 모바일 헤더 */}
      <div className="lg:hidden">
        <MobileHeader />
      </div>

      <div className="flex">
        {/* 데스크톱 사이드바 */}
        <aside className="hidden lg:block w-64 bg-white border-r">
          <Sidebar />
        </aside>

        {/* 메인 콘텐츠 */}
        <main className="flex-1 p-4 md:p-6 lg:p-8">
          {children}
        </main>
      </div>

      {/* 모바일 바텀 네비게이션 */}
      <div className="lg:hidden">
        <BottomNav />
      </div>
    </div>
  )
}
```

**Phase 2 완료 기준:**
- ✅ 모든 핵심 페이지 구현 (14개)
- ✅ 반응형 디자인 (모바일, 태블릿, 데스크톱)
- ✅ 다크 모드 지원
- ✅ 컴포넌트 테스트 (Jest)
- ✅ Storybook 문서
- ✅ Lighthouse 점수 90+ (성능, 접근성)

---

### Phase 3: 고급 기능 및 최적화 (3개월)

**목표:** 실시간, 모바일, 성능 최적화

#### 3.1 실시간 기능 (WebSocket) (2주)
```python
# backend/app/api/websocket.py
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({"message": data})
    except WebSocketDisconnect:
        manager.active_connections.remove(websocket)
```

```typescript
// frontend/src/hooks/useWebSocket.ts
export function useWebSocket() {
  const [messages, setMessages] = useState([])

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws')

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setMessages(prev => [...prev, data])
    }

    return () => ws.close()
  }, [])

  return { messages }
}
```

#### 3.2 OCR 실시간 진행 상태 (1주)
```typescript
// frontend/src/components/InvoiceUpload.tsx
'use client'

export function InvoiceUpload() {
  const [uploadProgress, setUploadProgress] = useState(0)
  const [ocrStatus, setOcrStatus] = useState<'idle' | 'uploading' | 'processing' | 'completed'>('idle')
  const { messages } = useWebSocket()

  const handleFileUpload = async (file: File) => {
    setOcrStatus('uploading')

    // 파일 업로드
    const formData = new FormData()
    formData.append('file', file)

    const response = await axios.post('/api/invoices/upload', formData, {
      onUploadProgress: (progressEvent) => {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        setUploadProgress(percentCompleted)
      }
    })

    const { invoice_id, task_id } = response.data
    setOcrStatus('processing')

    // WebSocket으로 진행 상태 수신
    const ws = new WebSocket(`ws://localhost:8000/ws/invoices/${task_id}`)
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)

      if (data.status === 'completed') {
        setOcrStatus('completed')
        ws.close()
      }
    }
  }

  return (
    <div>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => handleFileUpload(e.target.files[0])}
      />

      {ocrStatus === 'uploading' && (
        <ProgressBar value={uploadProgress} />
      )}

      {ocrStatus === 'processing' && (
        <div className="animate-pulse">OCR 처리 중...</div>
      )}

      {ocrStatus === 'completed' && (
        <div className="text-green-600">✓ 처리 완료</div>
      )}
    </div>
  )
}
```

#### 3.3 PWA (Progressive Web App) (1주)
```typescript
// frontend/next.config.js
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
})

module.exports = withPWA({
  // Next.js config
})
```

```json
// frontend/public/manifest.json
{
  "name": "TheMoon Drip BAR",
  "short_name": "TheMoon",
  "description": "Roasting Cost Calculator",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#1F4E78",
  "icons": [
    {
      "src": "/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

#### 3.4 성능 최적화 (3주)

**코드 스플리팅:**
```typescript
// frontend/src/app/beans/page.tsx
import dynamic from 'next/dynamic'

const BeanForm = dynamic(() => import('@/components/BeanForm'), {
  loading: () => <Skeleton />,
  ssr: false,
})
```

**이미지 최적화:**
```typescript
// frontend/src/components/InvoiceImage.tsx
import Image from 'next/image'

export function InvoiceImage({ src, alt }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={800}
      height={600}
      quality={85}
      loading="lazy"
      placeholder="blur"
    />
  )
}
```

**데이터 캐싱:**
```typescript
// frontend/src/hooks/useBeans.ts
export function useBeans() {
  return useQuery({
    queryKey: ['beans'],
    queryFn: () => beansApi.getAll().then(res => res.data),
    staleTime: 5 * 60 * 1000, // 5분
    cacheTime: 10 * 60 * 1000, // 10분
  })
}
```

**가상 스크롤:**
```typescript
// frontend/src/components/BeanTable.tsx
import { useVirtualizer } from '@tanstack/react-virtual'

export function BeanTable({ beans }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: beans.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  })

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            <BeanRow bean={beans[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

#### 3.5 모바일 네이티브 기능 (2주)
```typescript
// frontend/src/hooks/useCamera.ts
export function useCamera() {
  const captureImage = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }
      })

      const video = document.createElement('video')
      video.srcObject = stream
      await video.play()

      const canvas = document.createElement('canvas')
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight

      const ctx = canvas.getContext('2d')
      ctx.drawImage(video, 0, 0)

      stream.getTracks().forEach(track => track.stop())

      return canvas.toBlob((blob) => {
        return new File([blob], 'invoice.jpg', { type: 'image/jpeg' })
      }, 'image/jpeg', 0.9)
    } catch (error) {
      console.error('Camera access denied:', error)
    }
  }

  return { captureImage }
}
```

#### 3.6 E2E 테스트 (2주)
```typescript
// frontend/tests/e2e/beans.spec.ts
import { test, expect } from '@playwright/test'

test.describe('원두 관리', () => {
  test('원두 추가', async ({ page }) => {
    await page.goto('/beans')

    // "원두 추가" 버튼 클릭
    await page.click('text=원두 추가')

    // 폼 입력
    await page.fill('input[name="name"]', 'Test Bean')
    await page.fill('input[name="price_per_kg"]', '10000')
    await page.selectOption('select[name="roast_level"]', 'MEDIUM')

    // 제출
    await page.click('button[type="submit"]')

    // 목록에 추가되었는지 확인
    await expect(page.locator('text=Test Bean')).toBeVisible()
  })

  test('원두 수정', async ({ page }) => {
    await page.goto('/beans')

    // 첫 번째 원두 수정 버튼 클릭
    await page.click('table tbody tr:first-child button:has-text("수정")')

    // 가격 변경
    await page.fill('input[name="price_per_kg"]', '12000')
    await page.click('button[type="submit"]')

    // 변경 확인
    await expect(page.locator('text=₩12,000')).toBeVisible()
  })

  test('원두 삭제', async ({ page }) => {
    await page.goto('/beans')

    const beanName = await page.locator('table tbody tr:first-child td:nth-child(2)').textContent()

    // 삭제 버튼 클릭
    await page.click('table tbody tr:first-child button:has-text("삭제")')

    // 확인 다이얼로그
    page.on('dialog', dialog => dialog.accept())

    // 목록에서 사라졌는지 확인
    await expect(page.locator(`text=${beanName}`)).not.toBeVisible()
  })
})
```

**Phase 3 완료 기준:**
- ✅ 실시간 업데이트 (WebSocket)
- ✅ PWA 지원 (오프라인 모드)
- ✅ Lighthouse 점수 95+ (모든 항목)
- ✅ E2E 테스트 커버리지 70%+
- ✅ 모바일 카메라 연동
- ✅ 로딩 시간 1초 이하 (LCP)

---

### Phase 4: Streamlit 단계적 제거 (3개월)

**목표:** React 앱으로 완전 전환

#### 4.1 기능 비교 검증 (2주)
```
체크리스트:
□ 대시보드
  □ KPI 메트릭
  □ 차트 (월별 비용, 블렌드 판매)
  □ 재고 현황

□ 원두 관리
  □ CRUD 기능
  □ 가격 이력 관리
  □ 검색/필터링

□ 블렌드 관리
  □ CRUD 기능
  □ 레시피 관리
  □ 원가 계산

□ 로스팅 기록
  □ 일지 작성
  □ 손실률 추적
  □ 통계 분석

□ 재고 관리
  □ 입출고 관리
  □ 재고 현황
  □ 알림 설정

□ OCR 처리
  □ 이미지 업로드
  □ 자동 인식
  □ 수동 수정
  □ 학습 기능

□ 분석 및 보고서
  □ 월별 요약
  □ 비용 분석
  □ Excel/CSV 내보내기

□ 설정
  □ 비용 설정
  □ 사용자 관리
  □ 데이터 백업
```

#### 4.2 사용자 테스트 (4주)
```
베타 테스트 계획:
1. 내부 테스트 (1주)
   - 개발팀 전원 사용
   - 버그 리포트 수집

2. 알파 테스트 (1주)
   - 5-10명 사용자
   - 피드백 수집

3. 베타 테스트 (2주)
   - 50-100명 사용자
   - A/B 테스트 (Streamlit vs React)
   - 만족도 조사
```

#### 4.3 데이터 마이그레이션 (2주)
```bash
# 프로덕션 데이터 백업
pg_dump -h localhost -U postgres themoon > backup_20250101.sql

# 새 서버에 복원
psql -h new-server -U postgres themoon < backup_20250101.sql

# S3로 이미지 마이그레이션
aws s3 sync data/invoices/ s3://themoon-invoices/
```

#### 4.4 배포 및 전환 (2주)
```
배포 체크리스트:
□ 프로덕션 환경 설정
  □ Docker 이미지 빌드
  □ Kubernetes 배포 파일 작성
  □ 환경 변수 설정

□ 인프라 준비
  □ AWS RDS (PostgreSQL)
  □ AWS S3 (이미지)
  □ AWS CloudFront (CDN)
  □ AWS ElastiCache (Redis)

□ 모니터링 설정
  □ Sentry (에러 추적)
  □ Grafana (성능 모니터링)
  □ CloudWatch (로그)

□ 보안 설정
  □ HTTPS (SSL 인증서)
  □ CORS 정책
  □ API Rate Limiting
  □ WAF (방화벽)

□ 백업 자동화
  □ DB 일일 백업
  □ S3 버전 관리
  □ 로그 보관 정책
```

#### 4.5 Streamlit 앱 아카이빙 (1주)
```bash
# Streamlit 앱을 legacy 폴더로 이동
mkdir legacy/
mv app/ legacy/streamlit-app/

# README 업데이트
echo "# Legacy Streamlit App (Archived)" > legacy/README.md
echo "This is the original Streamlit version." >> legacy/README.md
echo "Replaced by React + FastAPI on 2025-05-01" >> legacy/README.md

# Git 태그 생성
git tag -a v1.0.0-streamlit -m "Last Streamlit version"
git push --tags
```

**Phase 4 완료 기준:**
- ✅ 모든 기능 React로 전환 완료
- ✅ 사용자 만족도 90%+
- ✅ 버그 0개 (Critical/High)
- ✅ 성능 지표 목표 달성
- ✅ Streamlit 앱 아카이빙
- ✅ 프로덕션 배포 완료

---

## 5. 아키텍처 설계

### 5.1 전체 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                        Client                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Browser   │  │  Mobile App │  │   Desktop   │     │
│  │   (React)   │  │   (React    │  │   (Electron)│     │
│  │             │  │   Native)   │  │             │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
└─────────┼─────────────────┼─────────────────┼───────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │ HTTPS
                  ┌─────────▼─────────┐
                  │   Load Balancer   │
                  │   (Nginx/ALB)     │
                  └─────────┬─────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
┌─────────▼──────┐ ┌────────▼────────┐ ┌─────▼──────┐
│  Frontend      │ │   API Server    │ │  WebSocket │
│  (Next.js)     │ │   (FastAPI)     │ │  Server    │
│  - SSR/SSG     │ │   - REST API    │ │  - Real-   │
│  - Static      │ │   - Auth        │ │    time    │
│    Assets      │ │   - Business    │ │            │
└────────────────┘ └─────────┬───────┘ └────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
┌─────────▼──────┐ ┌─────────▼─────┐ ┌─────────▼──────┐
│   PostgreSQL   │ │     Redis     │ │   RabbitMQ     │
│   - Main DB    │ │   - Cache     │ │   - Message    │
│   - Replicas   │ │   - Session   │ │     Queue      │
└────────────────┘ └───────────────┘ └────────┬───────┘
                                              │
                                    ┌─────────▼─────┐
                                    │    Celery     │
                                    │    Workers    │
                                    │  - OCR        │
                                    │  - Reports    │
                                    └───────────────┘
```

### 5.2 디렉토리 구조 (최종)

```
TheMoon_Project/
├── frontend/                      # React + Next.js
│   ├── src/
│   │   ├── app/                  # App Router
│   │   │   ├── (auth)/
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── dashboard/
│   │   │   ├── beans/
│   │   │   ├── blends/
│   │   │   ├── inventory/
│   │   │   ├── invoices/
│   │   │   ├── analytics/
│   │   │   └── settings/
│   │   ├── components/           # React 컴포넌트
│   │   │   ├── ui/              # shadcn/ui
│   │   │   ├── forms/
│   │   │   ├── charts/
│   │   │   └── layouts/
│   │   ├── hooks/                # Custom Hooks
│   │   ├── lib/                  # 유틸리티
│   │   ├── store/                # Zustand
│   │   └── types/                # TypeScript 타입
│   ├── public/
│   ├── tests/
│   │   ├── unit/
│   │   └── e2e/
│   ├── package.json
│   └── next.config.js
│
├── backend/                       # FastAPI
│   ├── app/
│   │   ├── api/                  # API 라우터
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── beans.py
│   │   │   │   ├── blends.py
│   │   │   │   ├── inventory.py
│   │   │   │   ├── invoices.py
│   │   │   │   └── analytics.py
│   │   │   └── deps.py          # 의존성
│   │   ├── core/                 # 코어 설정
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/               # SQLAlchemy (기존 재사용)
│   │   ├── schemas/              # Pydantic
│   │   ├── services/             # 비즈니스 로직 (기존 재사용)
│   │   ├── tasks/                # Celery 작업
│   │   └── main.py
│   ├── alembic/                  # DB 마이그레이션
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── shared/                        # 공통 코드
│   ├── types/
│   └── utils/
│
├── infrastructure/                # 인프라
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── k8s/                      # Kubernetes
│   │   ├── deployment.yml
│   │   ├── service.yml
│   │   └── ingress.yml
│   └── terraform/                # IaC
│
├── scripts/                       # 스크립트
│   ├── migrate_sqlite_to_postgres.py
│   ├── seed_data.py
│   └── backup.sh
│
├── docs/                          # 문서
│   ├── api/                      # API 문서
│   ├── architecture/
│   └── user-guide/
│
└── legacy/                        # 아카이빙
    └── streamlit-app/            # 기존 Streamlit 앱
```

### 5.3 API 설계 (RESTful)

**엔드포인트 구조:**
```
/api/v1/
├── auth/
│   ├── POST   /login
│   ├── POST   /register
│   ├── POST   /refresh
│   └── POST   /logout
│
├── beans/
│   ├── GET    /                  # 목록 조회
│   ├── POST   /                  # 생성
│   ├── GET    /{id}              # 단일 조회
│   ├── PUT    /{id}              # 수정
│   ├── DELETE /{id}              # 삭제
│   └── GET    /{id}/price-history
│
├── blends/
│   ├── GET    /
│   ├── POST   /
│   ├── GET    /{id}
│   ├── PUT    /{id}
│   ├── DELETE /{id}
│   ├── GET    /{id}/recipes
│   └── GET    /{id}/cost
│
├── inventory/
│   ├── GET    /
│   ├── GET    /beans/{bean_id}
│   ├── POST   /transactions
│   └── GET    /low-stock
│
├── invoices/
│   ├── POST   /upload
│   ├── GET    /{id}
│   ├── GET    /{id}/status
│   ├── PUT    /{id}/confirm
│   └── POST   /{id}/correct
│
├── analytics/
│   ├── GET    /dashboard
│   ├── GET    /cost-trends
│   ├── GET    /blend-performance
│   └── GET    /inventory-forecast
│
└── settings/
    ├── GET    /cost
    ├── PUT    /cost
    └── POST   /backup
```

**응답 형식:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Ethiopia Yirgacheffe",
    "price_per_kg": 18000
  },
  "meta": {
    "timestamp": "2025-01-01T00:00:00Z",
    "version": "1.0.0"
  }
}
```

**에러 형식:**
```json
{
  "success": false,
  "error": {
    "code": "BEAN_NOT_FOUND",
    "message": "원두를 찾을 수 없습니다",
    "details": {
      "bean_id": 999
    }
  }
}
```

---

## 6. 데이터베이스 마이그레이션

### 6.1 SQLite → PostgreSQL 전환

**마이그레이션 스크립트:**
```python
# scripts/migrate_sqlite_to_postgres.py
import sqlite3
import psycopg2
from psycopg2.extras import execute_batch

def migrate_table(sqlite_conn, pg_conn, table_name, columns):
    """테이블 데이터 마이그레이션"""
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()

    # SQLite에서 데이터 조회
    sqlite_cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
    rows = sqlite_cursor.fetchall()

    # PostgreSQL에 삽입
    placeholders = ', '.join(['%s'] * len(columns))
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    execute_batch(pg_cursor, insert_query, rows, page_size=1000)
    pg_conn.commit()

    print(f"✓ {table_name}: {len(rows)} rows migrated")

def main():
    # SQLite 연결
    sqlite_conn = sqlite3.connect('data/roasting_data.db')

    # PostgreSQL 연결
    pg_conn = psycopg2.connect(
        host='localhost',
        database='themoon',
        user='postgres',
        password='password'
    )

    # 테이블 마이그레이션 (순서 중요: FK 의존성)
    tables = [
        ('beans', ['id', 'no', 'name', 'country', 'roast_level', 'price_per_kg', 'created_at']),
        ('blends', ['id', 'name', 'blend_type', 'total_portion', 'created_at']),
        ('blend_recipes', ['id', 'blend_id', 'bean_id', 'portion_count', 'ratio']),
        ('inventory', ['id', 'bean_id', 'raw_bean_qty', 'roasted_bean_qty']),
        ('transactions', ['id', 'bean_id', 'blend_id', 'quantity_kg', 'transaction_type', 'created_at']),
        ('roasting_logs', ['id', 'bean_id', 'raw_weight_kg', 'roasted_weight_kg', 'loss_rate_percent', 'roasting_date']),
        ('invoices', ['id', 'image_path', 'supplier', 'invoice_date', 'total_amount', 'status', 'created_at']),
        ('invoice_items', ['id', 'invoice_id', 'bean_id', 'quantity', 'unit_price', 'amount', 'confidence_score']),
    ]

    for table_name, columns in tables:
        migrate_table(sqlite_conn, pg_conn, table_name, columns)

    sqlite_conn.close()
    pg_conn.close()

    print("\n✅ Migration completed successfully!")

if __name__ == '__main__':
    main()
```

**실행:**
```bash
python scripts/migrate_sqlite_to_postgres.py
```

### 6.2 스키마 개선

**인덱스 추가:**
```sql
-- 검색 성능 향상
CREATE INDEX idx_beans_name ON beans(name);
CREATE INDEX idx_beans_country ON beans(country);
CREATE INDEX idx_blends_type ON blends(blend_type);
CREATE INDEX idx_transactions_date ON transactions(created_at);
CREATE INDEX idx_roasting_logs_date ON roasting_logs(roasting_date);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_status ON invoices(status);

-- Full-text search
CREATE INDEX idx_beans_name_trgm ON beans USING gin(name gin_trgm_ops);
```

**파티셔닝 (대용량 데이터 대비):**
```sql
-- transactions 테이블 월별 파티셔닝
CREATE TABLE transactions_2025_01 PARTITION OF transactions
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE transactions_2025_02 PARTITION OF transactions
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
```

---

## 7. 리스크 관리

### 7.1 주요 리스크

| 리스크 | 영향도 | 발생 확률 | 완화 전략 |
|--------|--------|----------|-----------|
| **학습 곡선** | High | High | - 온라인 강의 수강<br>- 튜토리얼 프로젝트 먼저 구축<br>- 코드 리뷰 |
| **일정 지연** | Medium | Medium | - 버퍼 시간 20% 추가<br>- MVP 우선 개발<br>- 주간 진행 상황 점검 |
| **데이터 손실** | High | Low | - 백업 자동화<br>- 마이그레이션 전 테스트<br>- 롤백 계획 수립 |
| **성능 저하** | Medium | Low | - 부하 테스트<br>- 모니터링 설정<br>- 캐싱 전략 |
| **보안 취약점** | High | Medium | - 보안 스캔 도구 사용<br>- OWASP Top 10 준수<br>- 정기 감사 |
| **사용자 거부감** | Medium | Medium | - 베타 테스트<br>- 피드백 수렴<br>- 점진적 전환 |

### 7.2 롤백 계획

**각 Phase별 롤백 포인트:**
```
Phase 1: FastAPI만 중단, Streamlit 유지
Phase 2: React 중단, Streamlit 유지
Phase 3: 이전 버전으로 롤백
Phase 4: PostgreSQL → SQLite 복원 스크립트
```

**데이터 백업:**
```bash
# 일일 자동 백업
0 2 * * * /scripts/backup.sh

# backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d)
pg_dump themoon > /backups/themoon_$DATE.sql
aws s3 cp /backups/themoon_$DATE.sql s3://themoon-backups/
```

---

## 8. 성공 지표

### 8.1 기술 지표

| 지표 | 현재 (Streamlit) | 목표 (React) |
|------|------------------|--------------|
| **페이지 로딩 시간** | 2-3초 | <1초 |
| **API 응답 시간** | N/A | <200ms (P95) |
| **Lighthouse 점수** | 60 | >95 |
| **테스트 커버리지** | 96% | >90% |
| **번들 크기** | N/A | <300KB (gzip) |
| **동시 사용자** | 1명 | 100명+ |
| **가동률 (Uptime)** | 95% | 99.9% |

### 8.2 비즈니스 지표

| 지표 | 목표 |
|------|------|
| **사용자 만족도** | >90% |
| **이탈률** | <10% |
| **모바일 사용률** | >30% |
| **API 사용률** | >20% |
| **버그 리포트** | <5건/월 |
| **기능 요청** | >10건/월 |

### 8.3 ROI 계산

**투자 비용:**
- 개발 시간: 12개월 × $5,000/월 = $60,000
- 인프라 비용: 12개월 × $100/월 = $1,200
- **총 투자: $61,200**

**예상 절감/수익:**
- 운영 효율성 향상: $2,000/월 × 12 = $24,000/년
- 신규 고객 확보: $3,000/월 × 12 = $36,000/년
- **총 수익: $60,000/년**

**ROI:** 12개월 내 회수 (Break-even)

---

## 9. 결론 및 권장사항

### 9.1 전환 필요성

**Streamlit의 한계:**
- ❌ UI/UX 커스터마이징 제한적
- ❌ 성능 문제 (전체 재실행)
- ❌ 확장성 부족 (단일 서버)
- ❌ 모바일 경험 저하

**React + FastAPI의 장점:**
- ✅ 완전한 UI 제어
- ✅ 뛰어난 성능 (부분 렌더링)
- ✅ 무한 확장 가능 (마이크로서비스)
- ✅ 모바일 네이티브 앱 개발 가능
- ✅ API 퍼스트 아키텍처

### 9.2 실행 권장사항

**즉시 시작 (Phase 1):**
1. FastAPI 백엔드 구축
2. PostgreSQL 마이그레이션
3. 핵심 API 엔드포인트 개발

**병행 개발:**
- Streamlit 앱 유지 (운영 연속성)
- React 앱 점진적 구축
- 단계별 기능 전환

**점진적 전환:**
- Phase 1-2: 백엔드 + 프론트엔드 기본
- Phase 3: 고급 기능 + 최적화
- Phase 4: 완전 전환 + Streamlit 제거

### 9.3 최종 아키텍처 비전

```
현재 (v0.50.4)                    →         미래 (v2.0.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Streamlit (All-in-One)              Next.js (풀스택 프레임워크)
    ↓                                   ├── Frontend (SSR/SSG)
  SQLite                                │   - Server Components
                                        │   - Client Components
                                        │   - Image Optimization
                                        │
                                        ├── API Routes (내장 백엔드)
                                        │   - /api/beans
                                        │   - /api/blends
                                        │   - /api/analytics
                                        │
                                        └── FastAPI (고급 백엔드)
                                            - OCR 처리 (Celery)
                                            - 복잡한 비즈니스 로직
                                            ↓
                                        PostgreSQL + Redis + RabbitMQ
```

**Next.js의 게임 체인저 기능:**
1. **SSR/SSG**: 초기 로딩 0.5초 (현재 2-3초)
2. **파일 기반 라우팅**: 코드 없이 자동 라우팅
3. **Image Component**: 자동 최적화 (2MB → 200KB)
4. **Server Actions**: 타입 안전한 폼 처리
5. **API Routes**: 간단한 백엔드는 Next.js에서 처리

**기대 효과:**
- 🚀 성능: 5-10배 향상 (SSR 덕분)
- 📱 모바일: 완벽 지원 + PWA
- 🎯 SEO: Google 검색 상위 노출 가능
- 🔗 API: Next.js API Routes + FastAPI 조합
- 👥 사용자: 1명 → 100명+
- ⚡ 확장성: Vercel Edge + AWS Lambda
- 💰 비용: Vercel 무료 티어 활용 가능

---

**작성자:** Claude Code Agent
**작성일:** 2025-11-20
**버전:** 1.1 (Next.js 중심으로 수정)
**상태:** 검토 중

---

## 🎯 왜 Next.js인가?

### React vs Next.js 비교

| 기능 | React (CRA/Vite) | Next.js |
|------|------------------|---------|
| **라우팅** | React Router (수동 설정) | 파일 기반 (자동) |
| **SSR** | ❌ | ✅ |
| **SSG** | ❌ | ✅ |
| **ISR** | ❌ | ✅ |
| **SEO** | 제한적 (CSR만) | 완벽 (SSR/SSG) |
| **이미지 최적화** | 수동 | 자동 (next/image) |
| **코드 스플리팅** | 수동 | 자동 |
| **API 구현** | 별도 서버 필요 | API Routes 내장 |
| **배포** | 정적 호스팅만 | 서버리스/Edge |
| **학습 곡선** | 낮음 | 중간 |

### TheMoon Project에 Next.js가 완벽한 이유

#### 1. **하이브리드 렌더링**
```typescript
// 대시보드: SSR (항상 최신 데이터)
export default async function DashboardPage() {
  const data = await fetch('http://localhost:8000/api/dashboard')
  return <Dashboard data={data} />
}

// 원두 목록: ISR (5분마다 재생성)
export const revalidate = 300 // 5분
export default async function BeansPage() {
  const beans = await fetch('http://localhost:8000/api/beans')
  return <BeanList beans={beans} />
}

// 정적 페이지: SSG (빌드 시 생성)
export default function AboutPage() {
  return <About />  // 완전 정적
}
```

#### 2. **간단한 API는 Next.js에서 처리**
```typescript
// app/api/health/route.ts (Next.js API)
export async function GET() {
  return Response.json({ status: 'ok' })
}

// 복잡한 OCR은 FastAPI로
// → 역할 분담 명확!
```

#### 3. **Vercel 무료 배포**
```bash
# Vercel CLI 설치
npm i -g vercel

# 배포 (1분)
vercel --prod

# 결과:
# https://themoon-roasting.vercel.app
# - 자동 HTTPS
# - 글로벌 CDN
# - 무제한 대역폭 (Hobby 플랜)
```

#### 4. **이미지 자동 최적화**
```typescript
// 거래 명세서 이미지 (2MB)
<Image
  src="/invoice.jpg"
  width={800}
  height={600}
  alt="Invoice"
/>

// 결과:
// - WebP 자동 변환
// - 2MB → 200KB
// - Lazy loading 자동
// - 다양한 크기 자동 생성 (srcset)
```

### 최종 권장 스택

```
✅ Next.js 14 (App Router)
   ├── Frontend: Server Components + Client Components
   ├── Backend: API Routes (간단한 CRUD)
   └── 배포: Vercel (무료)

✅ FastAPI
   ├── 고급 백엔드 로직
   ├── OCR 처리 (Celery)
   └── 배포: AWS EC2 또는 Railway

✅ PostgreSQL + Redis
   └── 배포: Neon (무료) + Upstash (무료)
```

**총 비용: $0/월 (무료 티어 활용 시)**
