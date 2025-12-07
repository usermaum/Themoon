# TheMoon 프로젝트 현대화 (Modernization) 전략 기획서

> **문서 개요**
>
> 본 문서는 TheMoon 프로젝트의 기존 Streamlit 기반 프로토타입을 엔터프라이즈급 성능과 확장성을 갖춘 Next.js + FastAPI 기반의 모던 웹 애플리케이션으로 전환하기 위한 포괄적인 기술 전략 및 실행 계획을 기술합니다.

---

## 1. Executive Summary (개요)

현재 TheMoon 프로젝트는 Streamlit을 통해 성공적으로 초기 요구사항을 검증하고 MVP(Minimum Viable Product)를 구축했습니다. 그러나 단일 사용자 환경, 제한적인 UI/UX 커스터마이징, 그리고 동기식 처리로 인한 성능 병목 현상은 서비스의 확장과 고도화에 걸림돌이 되고 있습니다.

본 마이그레이션 프로젝트의 핵심 목표는 **"확장 가능한 클라우드 네이티브 아키텍처로의 전환"**입니다. 이를 통해 다중 사용자 지원, 실시간 데이터 처리, 모바일 최적화, 그리고 타 시스템과의 연동성을 확보하여 단순한 도구를 넘어선 **SaaS(Software as a Service) 플랫폼**으로 도약하고자 합니다.

---

## 2. 현황 분석 및 문제 정의 (As-Is Analysis)

### 2.1 현재 시스템 (Streamlit)

* **장점**: 빠른 개발 속도, 데이터 과학 라이브러리와의 높은 호환성, 직관적인 코드 구조.
* **성과**: 14개 핵심 페이지 구현 완료, 96%의 높은 테스트 커버리지 달성.

### 2.2 주요 한계점 (Pain Points)

| 구분 | 문제점 | 비즈니스 영향 |
| :--- | :--- | :--- |
| **UX/UI** | 제한적인 컴포넌트 및 레이아웃, 페이지 전환 시 깜빡임 (Reload) | 사용자 경험 저하, 브랜드 아이덴티티 구현 불가 |
| **성능** | 상호작용 시 전체 스크립트 재실행, 클라이언트 캐싱 부족 | 대량 데이터 처리 시 응답 지연, 서버 리소스 비효율 |
| **확장성** | 단일 서버/단일 인스턴스 구조, 상태 관리의 어려움 | 동시 접속자 증가 시 서비스 불능 위험 |
| **기능** | 모바일 네이티브 기능(카메라 등) 접근 제한, PWA 미지원 | 현장(로스팅 룸, 창고)에서의 활용성 저하 |

---

## 3. 목표 아키텍처 및 기술 스택 (To-Be Architecture)

### 3.1 아키텍처 설계 원칙

1. **관심사의 분리 (Separation of Concerns)**: 프론트엔드(UI/UX)와 백엔드(비즈니스 로직/데이터)의 완벽한 분리.
2. **API First**: 모든 기능은 RESTful API로 노출하여 다양한 클라이언트(Web, Mobile, 3rd Party) 지원.
3. **클라우드 네이티브**: 컨테이너 기반 배포, 마이크로서비스 지향, 오토스케일링 고려.

### 3.2 기술 스택 선정 (Tech Stack)

#### Frontend: Next.js (React Framework)

* **선정 이유**:
  * **Hybrid Rendering (SSR/SSG/ISR)**: 초기 로딩 속도 획기적 개선 및 SEO 최적화.
  * **Server Components**: 클라이언트 번들 사이즈 감소 및 서버 리소스 활용.
  * **API Routes**: BFF(Backend for Frontend) 패턴 구현 용이.
  * **Ecosystem**: TailwindCSS, shadcn/ui 등 풍부한 모던 UI 생태계 활용.

#### Backend: FastAPI (Python)

* **선정 이유**:
  * **High Performance**: 비동기(Async I/O) 처리를 통한 높은 처리량 (Node.js/Go와 대등).
  * **Python Ecosystem**: 기존 데이터 처리 로직 및 AI/OCR 라이브러리(Gemini 등) 재사용 용이.
  * **Auto Documentation**: Swagger/OpenAPI 문서 자동 생성으로 협업 효율 증대.

#### Database & Infrastructure

* **Main DB**: **PostgreSQL** (안정성, 복잡한 쿼리, JSON 지원)
* **Cache/Queue**: **Redis** (세션 관리, 캐싱, Celery 메시지 브로커)
* **Async Task**: **Celery** (OCR 등 장시간 소요 작업의 비동기 백그라운드 처리)

### 3.3 시스템 아키텍처 다이어그램

```mermaid
graph TD
    Client[Client Devices] -->|HTTPS| CDN[CloudFront/CDN]
    CDN --> LB[Load Balancer]
    
    subgraph Frontend_Layer [Frontend (Next.js)]
        LB -->|Page Req| NextServer[Next.js Server]
        NextServer -->|API Req| Backend_Layer
        Client -->|Client-side API| Backend_Layer
    end
    
    subgraph Backend_Layer [Backend (FastAPI)]
        API[API Gateway / Server]
        Auth[Auth Service]
        Core[Business Logic]
        API --> Auth
        API --> Core
    end
    
    subgraph Data_Layer
        Core -->|Read/Write| DB[(PostgreSQL)]
        Core -->|Cache| Redis[(Redis)]
        Core -->|Async Task| Queue[RabbitMQ/Redis]
    end
    
    subgraph Worker_Layer
        Queue --> Worker[Celery Workers]
        Worker -->|OCR Processing| AI_Service[Gemini/AI Model]
        Worker -->|Update| DB
    end
```

---

## 4. 단계별 마이그레이션 로드맵 (Migration Roadmap)

리스크를 최소화하고 서비스 연속성을 보장하기 위해 **"Strangler Fig Pattern"**(기존 시스템을 유지하면서 새로운 시스템으로 점진적 대체)을 적용합니다.

### Phase 1: 기반 구축 및 백엔드 API화 (개월 1-3)
>
> **목표**: 데이터 레이어 분리 및 핵심 비즈니스 로직의 API화

1. **데이터베이스 마이그레이션**: SQLite → PostgreSQL 이관 (스키마 최적화 포함).
2. **FastAPI 백엔드 구축**:
    * 인증/인가 (JWT, OAuth2) 시스템 구현.
    * 핵심 도메인(원두, 블렌드, 재고)에 대한 RESTful API 개발.
    * 기존 비즈니스 로직의 Service Layer 리팩토링 및 이식.
3. **API 테스트**: Pytest를 활용한 단위/통합 테스트 확보.

### Phase 2: 프론트엔드 전환 및 하이브리드 운영 (개월 4-6)
>
> **목표**: 사용자 접점(UI)의 현대화 및 병행 운영 시작

1. **Next.js 프로젝트 셋업**: 디자인 시스템(shadcn/ui + Tailwind) 구축.
2. **핵심 페이지 구현**: 대시보드, 원두 관리 등 주요 기능을 React 컴포넌트로 재구현.
3. **하이브리드 운영**: 기존 Streamlit 앱과 신규 Next.js 앱을 병행 운영하며 기능 검증.
    * *전략*: 신규 기능은 Next.js에만 추가, 기존 기능은 점진적 이관.

### Phase 3: 고도화 및 최적화 (개월 7-9)
>
> **목표**: 차별화된 사용자 경험 제공 및 성능 극대화

1. **실시간 기능**: WebSocket을 이용한 실시간 알림 및 OCR 처리 상태 공유.
2. **모바일 최적화**: PWA(Progressive Web App) 적용으로 앱 수준의 경험 제공 (카메라 연동 등).
3. **성능 튜닝**:
    * React Query(TanStack Query)를 활용한 서버 상태 관리 및 캐싱.
    * 이미지 최적화 및 Lazy Loading 적용.
    * Lighthouse 점수 95+ 달성 목표.

### Phase 4: 완전 전환 및 레거시 청산 (개월 10-12)
>
> **목표**: Streamlit 제거 및 운영 안정화

1. **기능 동등성(Feature Parity) 검증**: 모든 기능이 이관되었는지 최종 확인.
2. **데이터 완전 이관**: 프로덕션 데이터의 최종 동기화.
3. **Streamlit 종료**: 레거시 시스템 아카이빙 및 서비스 종료.
4. **운영 모니터링**: Sentry, Grafana 등을 통한 에러 추적 및 리소스 모니터링 체계 확립.

---

## 5. 리스크 관리 및 대응 전략 (Risk Management)

| 리스크 항목 | 발생 가능성 | 영향도 | 대응 전략 (Mitigation Plan) |
| :--- | :---: | :---: | :--- |
| **기술 복잡도 증가** | 높음 | 높음 | • 단계적 도입 및 팀원 기술 교육 병행<br>• 철저한 코드 리뷰 및 문서화<br>• 초기에는 복잡한 상태 관리 라이브러리(Redux 등) 배제 |
| **데이터 정합성 깨짐** | 중간 | 치명적 | • 마이그레이션 스크립트의 반복 테스트 (Dry Run)<br>• 이관 전후 데이터 검증 툴 개발<br>• 롤백(Rollback) 시나리오 사전 준비 |
| **일정 지연** | 높음 | 중간 | • MVP(최소 기능 제품) 범위 명확화<br>• 핵심 기능(Core)과 부가 기능(Nice-to-have)의 우선순위 분리<br>• 2주 단위 스프린트로 진행 상황 지속 점검 |
| **운영 비용 증가** | 확실 | 낮음 | • Serverless(Vercel) 및 Free Tier(Neon, Supabase 등) 적극 활용<br>• 클라우드 비용 모니터링 및 알림 설정 |

---

## 6. 기대 효과 (Expected Outcomes)

1. **사용자 경험(UX) 혁신**:
    * 네이티브 앱에 준하는 부드러운 인터랙션과 반응 속도.
    * 모바일 환경에서의 완벽한 사용성 보장.
2. **비즈니스 민첩성 확보**:
    * API 기반 구조로 타 서비스 연동 및 기능 확장이 용이.
    * 프론트/백엔드 병렬 개발로 기능 출시 속도(Time-to-Market) 단축.
3. **운영 안정성**:
    * 타입 안정성(TypeScript, Pydantic) 확보로 런타임 에러 감소.
    * 체계적인 테스트 및 배포 파이프라인(CI/CD) 구축.

---

> **결론**
>
> 본 마이그레이션은 단순한 기술 스택 교체가 아닌, TheMoon 프로젝트가 **'개인용 도구'에서 '엔터프라이즈급 플랫폼'으로 진화**하는 과정입니다. 초기 투자 비용과 학습 곡선이 존재하지만, 장기적인 유지보수성, 확장성, 그리고 사용자 가치 측면에서 필수적인 투자입니다.
