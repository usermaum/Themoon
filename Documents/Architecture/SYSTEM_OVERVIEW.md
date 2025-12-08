# 🌙 TheMoon 시스템 전체 개요 (System Overview)

> **작성일**: 2025-12-07
> **버전**: 0.0.6
> **작성자**: AI Assistant

---

## 📋 목차

1. [프로젝트 소개](#프로젝트-소개)
2. [시스템 목적](#시스템-목적)
3. [핵심 비즈니스 개념](#핵심-비즈니스-개념)
4. [시스템 아키텍처 개요](#시스템-아키텍처-개요)
5. [주요 기능 모듈](#주요-기능-모듈)
6. [사용자 흐름](#사용자-흐름)
7. [기술 스택 요약](#기술-스택-요약)
8. [배포 환경](#배포-환경)

---

## 프로젝트 소개

### 프로젝트명
**TheMoon Drip Bar - 커피 로스팅 원가 계산 시스템**

### 개요
TheMoon은 **커피 로스팅 전문점**을 위한 **재고 관리 및 원가 계산 시스템**입니다.
생두 구매부터 로스팅, 블렌딩, 재고 관리까지 커피 제조 전 과정의 원가를 추적하고 관리합니다.

### 대상 사용자
- **로스터리 카페 운영자**: 생두 재고, 로스팅 원가 관리
- **커피 블렌더**: 블렌드 레시피 개발 및 원가 산출
- **재고 관리자**: 입출고 이력 추적, 재고 현황 모니터링

---

## 시스템 목적

### 핵심 목표
1. **정확한 원가 계산**: 로스팅 손실률, 블렌드 비율을 고려한 정밀한 원가 산출
2. **재고 투명성**: 실시간 재고 현황 및 입출고 이력 추적
3. **운영 효율화**: 수작업 계산 제거, 데이터 기반 의사결정 지원
4. **레시피 관리**: 블렌드 레시피 저장 및 원가 시뮬레이션

### 해결하는 문제
- ❌ **수작업 계산의 비효율**: 엑셀 수작업 → 자동화
- ❌ **재고 불일치**: 실물 재고와 장부 불일치 → 실시간 동기화
- ❌ **원가 불투명**: 로스팅 손실률 미반영 → 정확한 원가 산출
- ❌ **레시피 관리 어려움**: 블렌드 원가 계산 복잡 → 자동 계산

---

## 핵심 비즈니스 개념

### 1. Bean (원두)
- **생두 (GREEN_BEAN)**: 로스팅 전 원료
  - 속성: 원산지, 품종, 등급, 가공 방식, 구매 단가
  - 예: 예가체프 G2 Washed (Ethiopia, 12,000원/kg)

- **원두 (ROASTED_BEAN)**: 로스팅 후 제품
  - 속성: 로스팅 프로필 (Light/Medium/Dark), 생산 원가
  - 로스팅 손실률 반영 (예: 15% 손실)

- **블렌드 (BLEND_BEAN)**: 여러 원두 혼합 제품
  - 블렌드 레시피에 따라 자동 생성
  - 각 원두 비율에 따른 가중 평균 원가

### 2. Blend (블렌드 레시피)
- **정의**: 여러 원두를 특정 비율로 혼합하는 레시피
- **구성 요소**:
  - 레시피명: 예) "Full Moon (풀문)"
  - Recipe: `[{bean_id: 6, ratio: 0.4}, {bean_id: 9, ratio: 0.4}, ...]`
  - 목표 로스팅 레벨: Medium Dark
- **원가 계산**: 각 원두의 (단가 × 비율) 합산

### 3. Inventory Log (재고 이력)
- **목적**: 모든 재고 변동 추적
- **변동 유형**:
  - `PURCHASE`: 구매 입고 (+)
  - `ROASTING_INPUT`: 로스팅 투입 (생두 -)
  - `ROASTING_OUTPUT`: 로스팅 산출 (원두 +)
  - `BLENDING_INPUT`: 블렌딩 투입 (원두 -)
  - `SALES`: 판매 출고 (-)
  - `LOSS`: 손실 (-)
  - `ADJUSTMENT`: 재고 조정 (±)

### 4. Roasting (로스팅 프로세스)
- **Single Origin Roasting**: 단일 품종 로스팅
  - Input: 생두 20kg
  - 손실률: 15%
  - Output: 원두 17kg (20kg × 0.85)
  - 원가: (생두 단가 / 0.85)

- **Blend Roasting**: 블렌드 로스팅
  - Input: 블렌드 레시피
  - 각 원두를 비율대로 혼합 후 로스팅
  - Output: 블렌드 원두

---

## 시스템 아키텍처 개요

### 3-Tier Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │   Next.js 14 Frontend (SSR + Client Components) │   │
│  │   - React 18 + TypeScript                        │   │
│  │   - Tailwind CSS + shadcn/ui                     │   │
│  │   - SWR (Data Fetching)                          │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↕ HTTPS (RESTful API)
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │      FastAPI Backend (Python 3.12)              │   │
│  │   ┌──────────────────────────────────────┐     │   │
│  │   │  API Endpoints (v1)                  │     │   │
│  │   │  - /api/v1/beans                     │     │   │
│  │   │  - /api/v1/blends                    │     │   │
│  │   │  - /api/v1/roasting                  │     │   │
│  │   │  - /api/v1/inventory-logs            │     │   │
│  │   └──────────────────────────────────────┘     │   │
│  │   ┌──────────────────────────────────────┐     │   │
│  │   │  Business Logic (Services)           │     │   │
│  │   │  - BeanService                       │     │   │
│  │   │  - BlendService                      │     │   │
│  │   │  - RoastingService                   │     │   │
│  │   │  - InventoryLogService               │     │   │
│  │   └──────────────────────────────────────┘     │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↕ SQLAlchemy ORM
┌─────────────────────────────────────────────────────────┐
│                      Data Layer                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │      PostgreSQL Database (Render.com)           │   │
│  │   ┌──────────────────────────────────────┐     │   │
│  │   │  Tables                              │     │   │
│  │   │  - beans                             │     │   │
│  │   │  - blends                            │     │   │
│  │   │  - inventory_logs                    │     │   │
│  │   └──────────────────────────────────────┘     │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 계층별 책임

| 계층 | 책임 | 기술 |
|------|------|------|
| **Presentation** | UI 렌더링, 사용자 입력 처리, 상태 관리 | Next.js, React, SWR |
| **Application** | 비즈니스 로직, API 제공, 데이터 검증 | FastAPI, Pydantic |
| **Data** | 데이터 영속화, 트랜잭션 관리 | PostgreSQL, SQLAlchemy |

---

## 주요 기능 모듈

### 1. Bean Management (원두 관리)
**목적**: 생두 및 로스팅 원두 마스터 데이터 관리

**주요 기능**:
- ✅ 생두 등록 (원산지, 품종, 등급, 가격 등)
- ✅ 원두 목록 조회 (페이지네이션, 검색)
- ✅ 원두 상세 정보 수정
- ✅ 원두 삭제 (재고 이력 포함)
- ✅ 재고 현황 실시간 조회

**API Endpoints**:
- `GET /api/v1/beans/` - 목록 조회
- `GET /api/v1/beans/{id}` - 상세 조회
- `POST /api/v1/beans/` - 생두 등록
- `PUT /api/v1/beans/{id}` - 수정
- `DELETE /api/v1/beans/{id}` - 삭제

### 2. Blend Management (블렌드 관리)
**목적**: 커피 블렌드 레시피 관리

**주요 기능**:
- ✅ 블렌드 레시피 생성 (원두 조합, 비율 설정)
- ✅ 블렌드 목록 조회
- ✅ 블렌드 레시피 수정
- ✅ 블렌드 원가 자동 계산
- ✅ 블렌드 레시피 시뮬레이션

**API Endpoints**:
- `GET /api/v1/blends/` - 목록 조회
- `GET /api/v1/blends/{id}` - 상세 조회
- `POST /api/v1/blends/` - 레시피 생성
- `PUT /api/v1/blends/{id}` - 수정
- `DELETE /api/v1/blends/{id}` - 삭제

### 3. Roasting Process (로스팅 프로세스)
**목적**: 로스팅 작업 처리 및 원가 계산

**주요 기능**:
- ✅ Single Origin 로스팅
  - 생두 투입 → 로스팅 → 원두 산출
  - 손실률 자동 반영
  - 재고 자동 업데이트 (생두 감소, 원두 증가)
  - 원가 자동 계산

- ✅ Blend 로스팅
  - 블렌드 레시피 기반 로스팅
  - 각 원두 비율대로 재고 차감
  - 블렌드 원두 생성 및 재고 증가

**API Endpoints**:
- `POST /api/v1/roasting/single-origin` - 싱글 오리진 로스팅
- `POST /api/v1/roasting/blend` - 블렌드 로스팅

### 4. Inventory Management (재고 관리)
**목적**: 원두 재고 추적 및 이력 관리

**주요 기능**:
- ✅ 재고 이력 전체 조회
- ✅ 원두별 재고 이력 조회
- ✅ 수동 재고 조정
- ✅ 재고 통계 (총 재고량, 재고 부족 알림 등)

**API Endpoints**:
- `GET /api/v1/inventory-logs/` - 이력 조회
- `POST /api/v1/inventory-logs/` - 수동 이력 생성
- `PUT /api/v1/inventory-logs/{id}` - 이력 수정
- `DELETE /api/v1/inventory-logs/{id}` - 이력 삭제

---

## 사용자 흐름

### 시나리오 1: 생두 구매 및 로스팅

```
1. 생두 구매 등록
   └→ Bean Management: "예가체프 G2 생두" 등록
      (20kg, 12,000원/kg, 손실률 15%)

2. 로스팅 작업 실행
   └→ Roasting Process: "Single Origin Roasting"
      Input: 예가체프 생두 20kg
      Output: 예가체프 원두 17kg (20 × 0.85)
      원가: 14,118원/kg (12,000 / 0.85)

3. 재고 확인
   └→ Inventory Management: 재고 자동 업데이트
      - 생두 재고: 20kg → 0kg
      - 원두 재고: 0kg → 17kg
```

### 시나리오 2: 블렌드 레시피 생성 및 로스팅

```
1. 블렌드 레시피 생성
   └→ Blend Management: "Full Moon" 레시피 등록
      - 마사이 (Kenya) 40%
      - 안티구아 (Guatemala) 40%
      - 모모라 (Ethiopia) 10%
      - 시다모 (Ethiopia) 10%

2. 블렌드 로스팅 실행
   └→ Roasting Process: "Blend Roasting"
      Input: Full Moon 레시피 (10kg 목표)
      각 원두 비율대로 투입:
        - 마사이 4kg
        - 안티구아 4kg
        - 모모라 1kg
        - 시다모 1kg
      Output: Full Moon 블렌드 원두 10kg

3. 원가 자동 계산
   └→ 가중 평균 원가:
      (마사이 단가 × 0.4) + (안티구아 × 0.4) +
      (모모라 × 0.1) + (시다모 × 0.1)
```

### 시나리오 3: 재고 모니터링 및 알림

```
1. 대시보드 접속
   └→ 실시간 재고 현황 확인
      - 전체 원두: 21종
      - 총 재고량: 347.5kg
      - 재고 부족: 3종 (⚠️ 5kg 이하)

2. 재고 부족 알림 확인
   └→ 재고 부족 원두 목록:
      - 코케허니 (Ethiopia): 3.2kg
      - 게이샤 (Panama): 1.5kg
      - 디카페 SM (Colombia): 4.8kg

3. 재구매 계획 수립
   └→ 재고 이력 분석 → 적정 재구매 시점 결정
```

---

## 기술 스택 요약

### Frontend
- **프레임워크**: Next.js 14.2 (App Router)
- **언어**: TypeScript 5.x
- **UI 라이브러리**: React 18
- **스타일링**: Tailwind CSS + shadcn/ui
- **데이터 페칭**: SWR (Stale-While-Revalidate)
- **차트**: Recharts
- **애니메이션**: Framer Motion

### Backend
- **프레임워크**: FastAPI 0.104+
- **언어**: Python 3.12
- **ORM**: SQLAlchemy 2.0
- **검증**: Pydantic V2
- **CORS**: FastAPI Middleware

### Database
- **DBMS**: PostgreSQL 15+ (Production)
- **로컬**: SQLite 3 (Development)
- **마이그레이션**: SQLAlchemy Alembic (예정)

### DevOps
- **배포**: Render.com
  - Frontend: Static Site
  - Backend: Web Service
  - Database: PostgreSQL Service
- **버전 관리**: Git + GitHub
- **CI/CD**: Render Auto-Deploy

---

## 배포 환경

### Production (Render.com)

```
┌──────────────────────────────────────────────┐
│   Frontend (Next.js)                         │
│   URL: https://themoon-xxx.onrender.com     │
│   - SSR + Static Generation                 │
│   - Auto-deploy from GitHub                 │
└──────────────────────────────────────────────┘
                    ↓ API Calls
┌──────────────────────────────────────────────┐
│   Backend (FastAPI)                          │
│   URL: https://themoon-api-gv1u.onrender.com│
│   - RESTful API                              │
│   - Auto-deploy from GitHub                 │
└──────────────────────────────────────────────┘
                    ↓ PostgreSQL Driver
┌──────────────────────────────────────────────┐
│   Database (PostgreSQL)                      │
│   Host: dpg-xxx.oregon-postgres.render.com  │
│   - Persistent Volume                        │
│   - Auto Backup                              │
└──────────────────────────────────────────────┘
```

### Development (Local)

```
┌──────────────────────────────────────────────┐
│   Frontend                                   │
│   http://localhost:3000                     │
│   npm run dev                                │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   Backend                                    │
│   http://localhost:8000                     │
│   uvicorn app.main:app --reload             │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│   Database (SQLite)                          │
│   backend/themoon.db                         │
└──────────────────────────────────────────────┘
```

---

---

## 🔗 관련 문서

**← 상위**: [Documents README](../README.md) | [프로젝트 루트](../../README.md)

**아키텍처 문서**:
- [데이터 흐름도](DATA_FLOW.md) - 시스템 내 데이터 흐름 상세 분석
- [데이터베이스 스키마](DATABASE_SCHEMA.md) - 테이블 구조 및 관계도
- [API 명세](API_SPECIFICATION.md) ⭐ - 모든 API 엔드포인트 상세 문서
- [기술 스택](TECHNOLOGY_STACK.md) ⭐ - 사용 기술 상세 설명
- [배포 아키텍처](DEPLOYMENT_ARCHITECTURE.md) ⭐ - 배포 환경 상세 구조

**개발 가이드**:
- [개발 가이드](DEVELOPMENT_GUIDE.md) - 5단계 개발 프로세스
- [문제 해결](TROUBLESHOOTING.md) - 16가지 오류 & 해결법

---

**작성**: AI Assistant
**최종 업데이트**: 2025-12-08
**버전**: 0.0.6
