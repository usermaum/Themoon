# n8n 하이브리드 OCR 통합 시스템 플랜

> **프로젝트**: The Moon Drip BAR - Roasting Cost Calculator
> **목적**: n8n + Claude Vision API를 활용한 자동화된 명세서 처리 시스템 구축
> **버전**: 1.0.0
> **작성일**: 2025-11-17
> **방법론**: 7단계 체계적 개발 방법론

---

## 📋 목차

1. [Constitution (원칙)](#1-constitution-원칙)
2. [Specify (명세)](#2-specify-명세)
3. [Clarify (명확화)](#3-clarify-명확화)
4. [Plan (계획)](#4-plan-계획)
5. [Tasks (작업 분해)](#5-tasks-작업-분해)
6. [Technical Specifications (기술 사양)](#6-technical-specifications-기술-사양)
7. [Next Steps (다음 단계)](#7-next-steps-다음-단계)

---

## 1. Constitution (원칙)

### 1.1 프로젝트 기본 원칙

**목표:**
- 명세서 처리를 수동 → 자동으로 전환하여 업무 효율 극대화
- n8n 워크플로우 자동화 + Streamlit 수동 검증의 하이브리드 시스템 구축
- 기존 Streamlit 애플리케이션과 완벽한 통합

**핵심 가치:**
1. **자동화 우선**: 반복 작업은 n8n이 자동 처리
2. **검증 중심**: Streamlit은 검증 및 분석 도구로 활용
3. **무중단 전환**: 기존 시스템과 병행 운영 후 점진적 전환
4. **확장 가능**: 향후 다른 문서 유형(견적서, 발주서) 처리 확장 가능

### 1.2 제약사항

**기술적 제약:**
- n8n Cloud 또는 Self-hosted 선택 필요
- Claude API 크레딧 관리 (월 예산 설정)
- SQLite DB 동시 접근 제어 (n8n + Streamlit)
- WSL 환경에서 n8n Self-hosted 실행 시 네트워크 설정

**비즈니스 제약:**
- 초기 설정 시간: 4-6시간
- 월 운영 비용: $20-50 (n8n Cloud 기준)
- 데이터 보안: API 키, 명세서 이미지 관리
- 학습 곡선: n8n 워크플로우 작성 능력 필요

**운영 제약:**
- 이메일 첨부파일 형식: PNG, JPG, PDF
- 명세서 형식: GSC, HACIELO (확장 가능)
- 처리 시간: 이미지당 2-5초 (Claude API 호출)

### 1.3 기술 스택 결정 원칙

**선택 기준:**
1. 기존 시스템과의 호환성 (SQLite, Streamlit)
2. 확장성 (다른 데이터 소스 연결 용이)
3. 유지보수 편의성 (GUI 워크플로우 편집)
4. 비용 효율성 (무료 티어 활용 가능)

**채택 기술:**
- **n8n**: 워크플로우 자동화 플랫폼
- **Claude Vision API**: 고정밀 OCR 엔진
- **SQLite**: 기존 데이터베이스 유지
- **Streamlit**: 기존 UI 유지 (검증/분석용)

---

## 2. Specify (명세)

### 2.1 시스템 아키텍처 명세

#### 전체 시스템 구조

```
┌──────────────────────────────────────────────────────────────┐
│                    데이터 소스 (다중)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Gmail   │  │ Webhook  │  │  Drive   │  │   FTP    │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
└───────┼─────────────┼─────────────┼─────────────┼────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                      n8n 워크플로우                           │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Phase 1: 데이터 수집                                 │    │
│  │  - 트리거 감지 (이메일/Webhook/폴더 변경)            │    │
│  │  - 첨부파일 추출                                     │    │
│  │  - 이미지 포맷 검증 (PNG/JPG/PDF)                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Phase 2: Claude Vision API 호출                     │    │
│  │  - 이미지 → Base64 변환                              │    │
│  │  - HTTP Request (Claude API)                        │    │
│  │  - 응답 JSON 파싱                                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Phase 3: 데이터 검증 및 변환                         │    │
│  │  - JSON 스키마 검증                                  │    │
│  │  - 데이터 정규화 (날짜, 금액, 원두명)                │    │
│  │  - 신뢰도 평가 (confidence check)                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Phase 4: 데이터베이스 저장                           │    │
│  │  - SQLite INSERT (invoices 테이블)                  │    │
│  │  - 이미지 파일 저장 (data/invoices/)                │    │
│  │  - 메타데이터 기록 (timestamp, source)              │    │
│  └─────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Phase 5: 알림 및 로깅                                │    │
│  │  - Slack/Email 알림 (선택)                          │    │
│  │  - 에러 로깅 (실패 시 재시도)                        │    │
│  │  - 통계 업데이트 (일일 처리 건수)                   │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   SQLite Database                            │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                 │
│  │ invoices 테이블   │  │ invoice_items    │                 │
│  │ - id             │  │ - invoice_id     │                 │
│  │ - supplier       │  │ - bean_name      │                 │
│  │ - invoice_date   │  │ - weight         │                 │
│  │ - total_amount   │  │ - unit_price     │                 │
│  │ - source         │  │ - amount         │                 │
│  │ - confidence     │  └──────────────────┘                 │
│  │ - processed_at   │                                        │
│  │ - image_path     │                                        │
│  └──────────────────┘                                        │
└──────────────────────────────────────────────────────────────┘
                            ↑
                            │ (Read Only - 검증/분석)
┌──────────────────────────────────────────────────────────────┐
│               Streamlit 웹 애플리케이션                       │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 자동 처리된 데이터 검증                              │    │
│  │  - 명세서 목록 보기                                  │    │
│  │  - OCR 결과 확인/수정                                │    │
│  │  - 신뢰도 낮은 항목 플래그                           │    │
│  └─────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 수동 업로드 (기존 기능 유지)                         │    │
│  │  - 긴급/특수 케이스 처리                             │    │
│  │  - n8n 미연동 명세서 처리                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                            ↓                                 │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ 데이터 분석 및 보고서 (기존 기능)                    │    │
│  │  - 월간/연간 비용 분석                               │    │
│  │  - 원두별 사용량 추이                                │    │
│  │  - Excel/PDF 보고서 생성                             │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

### 2.2 기능 요구사항 (Functional Requirements)

#### FR-1: n8n 워크플로우 자동화

**FR-1.1: 이메일 트리거**
- **입력**: Gmail/Outlook 계정
- **조건**: 특정 발신자 또는 제목 필터링 (예: "거래명세서")
- **출력**: 첨부파일 이미지 추출
- **우선순위**: 높음

**FR-1.2: Webhook 트리거**
- **입력**: HTTP POST 요청 (이미지 파일)
- **출력**: 워크플로우 시작
- **사용 사례**: 외부 시스템 연동, 모바일 앱
- **우선순위**: 중간

**FR-1.3: Google Drive 폴더 감시**
- **입력**: Google Drive 특정 폴더
- **조건**: 새 파일 추가 시 자동 트리거
- **출력**: 이미지 다운로드 및 처리
- **우선순위**: 낮음

#### FR-2: Claude Vision API 통합

**FR-2.1: 이미지 → JSON 변환**
- **입력**: PNG/JPG 이미지 (최대 5MB)
- **처리**: Claude 3.5 Haiku Vision API 호출
- **출력**: 구조화된 JSON (명세서 데이터)
- **품질**: 95%+ 정확도
- **우선순위**: 높음

**FR-2.2: 프롬프트 커스터마이징**
- **입력**: 명세서 유형 (GSC, HACIELO, 기타)
- **처리**: 유형별 최적화된 프롬프트 사용
- **출력**: JSON 스키마 준수
- **우선순위**: 중간

**FR-2.3: 에러 핸들링**
- **조건**: API 호출 실패, 타임아웃, 크레딧 부족
- **처리**: 최대 3회 재시도 (지수 백오프)
- **알림**: Slack/Email 에러 알림
- **우선순위**: 높음

#### FR-3: 데이터베이스 통합

**FR-3.1: 명세서 테이블 생성**
- **테이블명**: `invoices`
- **컬럼**:
  - `id` (INTEGER PRIMARY KEY)
  - `supplier` (TEXT)
  - `invoice_date` (TEXT)
  - `total_amount` (REAL)
  - `total_weight` (REAL)
  - `source` (TEXT: 'email', 'webhook', 'manual')
  - `confidence` (REAL: 0-100)
  - `processed_at` (TEXT: ISO timestamp)
  - `image_path` (TEXT)
  - `raw_json` (TEXT: Claude 응답 전체)
- **우선순위**: 높음

**FR-3.2: 항목 테이블 생성**
- **테이블명**: `invoice_items`
- **컬럼**:
  - `id` (INTEGER PRIMARY KEY)
  - `invoice_id` (INTEGER FOREIGN KEY)
  - `bean_name` (TEXT)
  - `spec` (TEXT)
  - `quantity` (INTEGER)
  - `weight` (REAL)
  - `unit_price` (REAL)
  - `amount` (REAL)
- **우선순위**: 높음

**FR-3.3: 동시 접근 제어**
- **문제**: n8n과 Streamlit이 동시에 DB 접근
- **해결**: SQLite WAL 모드 활성화
- **백업**: 일일 자동 백업
- **우선순위**: 중간

#### FR-4: Streamlit 검증 인터페이스

**FR-4.1: 자동 처리 대시보드**
- **기능**: 최근 자동 처리된 명세서 목록 표시
- **정보**: 처리 시간, 신뢰도, 소스, 상태
- **필터**: 날짜, 공급자, 신뢰도 범위
- **우선순위**: 높음

**FR-4.2: OCR 결과 검증**
- **기능**: 자동 추출된 데이터 수동 검토/수정
- **UI**: 원본 이미지 | 추출 데이터 병렬 표시
- **수정**: 인라인 편집 (항목별 수정 가능)
- **승인**: "확인" 버튼 클릭 시 승인 플래그 설정
- **우선순위**: 높음

**FR-4.3: 수동 업로드 (기존 기능 유지)**
- **사용 사례**: n8n 미연동 명세서, 긴급 처리
- **기능**: 기존 CostCalculation.py 페이지 유지
- **통합**: 수동 업로드도 invoices 테이블에 저장
- **우선순위**: 중간

#### FR-5: 알림 및 모니터링

**FR-5.1: 처리 완료 알림**
- **채널**: Slack/Email (설정 가능)
- **내용**: 공급자, 총액, 항목 수, 처리 시간
- **빈도**: 실시간 또는 일일 요약
- **우선순위**: 낮음

**FR-5.2: 에러 알림**
- **조건**: API 실패, 파싱 오류, DB 오류
- **채널**: Slack/Email (긴급)
- **내용**: 에러 메시지, 스택 트레이스, 재시도 여부
- **우선순위**: 중간

**FR-5.3: 통계 대시보드**
- **지표**: 일일 처리 건수, 평균 신뢰도, 에러율
- **시각화**: Streamlit 차트
- **갱신**: 실시간 또는 1시간마다
- **우선순위**: 낮음

---

### 2.3 비기능 요구사항 (Non-Functional Requirements)

#### NFR-1: 성능

| 지표 | 목표 | 측정 방법 |
|------|------|-----------|
| **처리 시간** | < 10초/이미지 | n8n 워크플로우 실행 시간 |
| **동시 처리** | 최대 5개 동시 | n8n 워크플로우 병렬 실행 |
| **API 응답 시간** | < 5초 | Claude API 호출 시간 |
| **DB 쓰기 시간** | < 1초 | SQLite INSERT 시간 |

#### NFR-2: 안정성

| 지표 | 목표 | 측정 방법 |
|------|------|-----------|
| **성공률** | > 95% | (성공 건수 / 전체 건수) * 100 |
| **재시도 성공률** | > 80% | 재시도 후 성공 비율 |
| **데이터 정합성** | 100% | 수동 검증 샘플링 |

#### NFR-3: 확장성

- n8n 워크플로우로 새 문서 유형 추가 용이 (견적서, 발주서)
- 다른 OCR 엔진으로 교체 가능 (Google Vision, AWS Textract)
- 추가 데이터 소스 연결 용이 (Dropbox, OneDrive, FTP)

#### NFR-4: 보안

- API 키 암호화 저장 (n8n Credentials)
- 이미지 파일 로컬 저장 (외부 유출 방지)
- DB 접근 제어 (읽기 전용 권한 분리)
- HTTPS 통신 (Webhook)

#### NFR-5: 유지보수성

- n8n 워크플로우 GUI 편집 (코드 수정 불필요)
- 로그 자동 기록 (n8n 내장 로깅)
- 버전 관리 (워크플로우 백업)

---

### 2.4 데이터 모델 명세

#### 데이터베이스 스키마

```sql
-- 명세서 메인 테이블
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier TEXT NOT NULL,                    -- 공급자명 (GSC, HACIELO 등)
    invoice_date TEXT NOT NULL,                -- 거래일자 (YYYY-MM-DD)
    total_amount REAL NOT NULL DEFAULT 0,      -- 총액 (원)
    total_weight REAL NOT NULL DEFAULT 0,      -- 총중량 (kg)
    source TEXT NOT NULL DEFAULT 'manual',     -- 데이터 소스 (email, webhook, manual)
    confidence REAL DEFAULT 0,                 -- 신뢰도 (0-100)
    processed_at TEXT NOT NULL,                -- 처리 시간 (ISO 8601)
    image_path TEXT,                           -- 이미지 파일 경로
    raw_json TEXT,                             -- Claude 응답 원본 (디버깅용)
    verified BOOLEAN DEFAULT 0,                -- 검증 완료 여부
    verified_at TEXT,                          -- 검증 시간
    verified_by TEXT,                          -- 검증자 (향후 다중 사용자 대비)
    notes TEXT,                                -- 메모
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 명세서 항목 테이블
CREATE TABLE invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,               -- 명세서 ID (FK)
    bean_name TEXT NOT NULL,                   -- 원두명
    spec TEXT,                                 -- 규격 (1kg, 5kg 등)
    quantity INTEGER DEFAULT 0,                -- 수량
    weight REAL NOT NULL,                      -- 중량 (kg)
    unit_price REAL NOT NULL,                  -- 단가 (원/kg)
    amount REAL NOT NULL,                      -- 공급가액 (원)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
);

-- 인덱스 생성 (검색 성능 향상)
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_supplier ON invoices(supplier);
CREATE INDEX idx_invoices_source ON invoices(source);
CREATE INDEX idx_invoices_verified ON invoices(verified);
CREATE INDEX idx_invoice_items_invoice_id ON invoice_items(invoice_id);
CREATE INDEX idx_invoice_items_bean_name ON invoice_items(bean_name);

-- 트리거: updated_at 자동 갱신
CREATE TRIGGER update_invoices_timestamp
AFTER UPDATE ON invoices
BEGIN
    UPDATE invoices SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

#### Claude API 응답 스키마

```json
{
  "invoice_type": "GSC",
  "invoice_data": {
    "supplier": "글로벌 스페셜티 커피",
    "invoice_date": "2025-11-15",
    "total_amount": 1250000,
    "total_weight": 50.0
  },
  "items": [
    {
      "bean_name": "에티오피아 예가체프 G1",
      "spec": "1kg",
      "quantity": 20,
      "weight": 20.0,
      "unit_price": 25000,
      "amount": 500000
    },
    {
      "bean_name": "브라질 산토스 NY2",
      "spec": "5kg",
      "quantity": 6,
      "weight": 30.0,
      "unit_price": 25000,
      "amount": 750000
    }
  ],
  "confidence": 95.5,
  "warnings": [
    "단가 계산이 정확하지 않을 수 있음 (항목 2)"
  ]
}
```

---

## 3. Clarify (명확화)

### 3.1 사용자 요구사항 명확화

#### Q1: n8n은 Cloud와 Self-hosted 중 어느 것을 사용하시겠습니까?

**옵션 A: n8n Cloud (추천)**
- 장점: 설치 불필요, 자동 업데이트, 안정적 운영
- 단점: 월 $20 (Starter 플랜)
- 적합: 빠른 시작, 운영 부담 최소화

**옵션 B: n8n Self-hosted (WSL)**
- 장점: 무료, 완전한 제어
- 단점: 설치/관리 필요, WSL 네트워크 설정
- 적합: 비용 절감, 기술적 자유도

**결정 기준:**
- 월 예산이 $20 이상이면 → Cloud
- 기술적 역량이 있고 비용 절감 원하면 → Self-hosted

**질문**: 어느 것을 선택하시겠습니까?

---

#### Q2: 이메일 트리거의 필터링 조건은 무엇입니까?

**필터링 옵션:**
1. **발신자 기준**: 특정 이메일 주소 (예: gsc@coffee.com, hacielo@coffee.com)
2. **제목 기준**: "거래명세서", "명세서", "invoice" 포함
3. **첨부파일 기준**: 이미지 파일만 (PNG, JPG, PDF)

**다중 조건 AND/OR:**
- AND: 발신자가 X이고 제목에 "명세서" 포함
- OR: 발신자가 X 또는 Y

**질문**: 어떤 필터링 규칙을 사용하시겠습니까?

---

#### Q3: 신뢰도가 낮은 OCR 결과는 어떻게 처리하시겠습니까?

**옵션 A: 자동 저장 + 검증 플래그**
- 신뢰도 < 80%인 경우 `verified = 0`으로 저장
- Streamlit에서 "미검증" 목록 별도 표시
- 사용자가 수동 검증 필요

**옵션 B: 수동 승인 대기**
- 신뢰도 < 80%인 경우 Slack/Email 알림
- 사용자가 Streamlit에서 승인/거부 결정
- 승인 후 DB 저장

**옵션 C: 재처리**
- 신뢰도 < 80%인 경우 다른 OCR 엔진 시도 (Google Vision)
- 두 결과를 비교하여 더 높은 신뢰도 선택

**질문**: 어느 방식을 선호하시겠습니까?

---

#### Q4: 이미지 파일은 어떻게 저장하시겠습니까?

**옵션 A: 로컬 파일 시스템**
- 경로: `data/invoices/YYYY-MM-DD_supplier_id.png`
- 백업: 주기적으로 외부 저장소에 백업
- 장점: 빠른 접근, 비용 없음
- 단점: 디스크 공간 관리 필요

**옵션 B: 클라우드 스토리지**
- AWS S3, Google Cloud Storage
- 경로: `s3://bucket-name/invoices/...`
- 장점: 무제한 용량, 자동 백업
- 단점: 월 비용 발생

**옵션 C: 저장 안 함**
- DB에 base64 인코딩하여 저장 (비추천)
- 장점: 단순함
- 단점: DB 크기 증가, 성능 저하

**질문**: 어느 방식을 사용하시겠습니까?

---

#### Q5: Streamlit의 수동 업로드 기능을 어떻게 처리하시겠습니까?

**옵션 A: 기존 기능 유지 (추천)**
- CostCalculation.py 페이지 그대로 유지
- 수동 업로드도 `invoices` 테이블에 저장 (`source='manual'`)
- 자동/수동 구분 없이 동일한 검증 워크플로우

**옵션 B: n8n Webhook 경유**
- Streamlit에서 업로드 시 n8n Webhook 호출
- 모든 처리를 n8n으로 통일
- 장점: 중앙화된 처리, 로깅 일관성
- 단점: 네트워크 오버헤드

**옵션 C: 기능 제거**
- 모든 명세서는 이메일/Drive로만 처리
- Streamlit은 검증/분석 전용
- 단점: 긴급 상황 대응 불가

**질문**: 어느 방식을 선호하시겠습니까?

---

### 3.2 기술적 결정사항

| 항목 | 질문 | 옵션 | 기본 추천 |
|------|------|------|-----------|
| **n8n 환경** | Cloud vs Self-hosted | Cloud / Self-hosted | Cloud (간편함) |
| **이메일 제공자** | Gmail vs Outlook | Gmail / Outlook / 기타 | Gmail (n8n 연동 쉬움) |
| **알림 채널** | Slack vs Email | Slack / Email / 둘 다 | Slack (실시간) |
| **재시도 정책** | 최대 재시도 횟수 | 1회 / 3회 / 5회 | 3회 (적정) |
| **신뢰도 임계값** | 자동 승인 기준 | 70% / 80% / 90% | 80% (균형) |
| **처리 빈도** | 실시간 vs 배치 | 실시간 / 1시간마다 / 일 1회 | 실시간 (효율) |

---

## 4. Plan (계획)

### 4.1 시스템 아키텍처

#### 4.1.1 컴포넌트 다이어그램

```
┌─────────────────────────────────────────────────────────────────┐
│                          외부 시스템                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Gmail   │  │  Slack   │  │  Drive   │  │ Webhook  │        │
│  │  IMAP    │  │  API     │  │  API     │  │  HTTP    │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
└───────┼─────────────┼─────────────┼─────────────┼───────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      n8n 워크플로우 엔진                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Workflow 1: Email Invoice Processor                      │  │
│  │                                                          │  │
│  │  [Gmail Trigger]                                         │  │
│  │       ↓                                                  │  │
│  │  [Filter: Attachment + Sender]                           │  │
│  │       ↓                                                  │  │
│  │  [Extract Image]                                         │  │
│  │       ↓                                                  │  │
│  │  [Convert to Base64]                                     │  │
│  │       ↓                                                  │  │
│  │  [HTTP Request: Claude API]                              │  │
│  │       ↓                                                  │  │
│  │  [IF: API Success]                                       │  │
│  │    ├─ Yes → [Parse JSON]                                 │  │
│  │    │           ↓                                         │  │
│  │    │        [Validate Schema]                            │  │
│  │    │           ↓                                         │  │
│  │    │        [Save to SQLite]                             │  │
│  │    │           ↓                                         │  │
│  │    │        [Save Image File]                            │  │
│  │    │           ↓                                         │  │
│  │    │        [Slack Notification]                         │  │
│  │    │                                                     │  │
│  │    └─ No  → [Retry (3x)]                                 │  │
│  │                ↓                                         │  │
│  │             [Error Log]                                  │  │
│  │                ↓                                         │  │
│  │             [Slack Alert]                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Workflow 2: Webhook Invoice Processor (동일 구조)        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Workflow 3: Daily Statistics (일일 통계 생성)            │  │
│  │  [Cron: 23:59] → [Query DB] → [Generate Report] →       │  │
│  │  [Send Email Summary]                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ (Write)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SQLite Database                              │
│                 data/roasting_data.db                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  invoices    │  │ invoice_items│  │  logs        │          │
│  │  (메인 테이블)│  │  (항목)      │  │  (n8n 로그)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          │ (Read + Write)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Streamlit 웹 애플리케이션                       │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 신규 페이지: AutoProcessedInvoices.py                    │  │
│  │                                                          │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │ Section 1: 최근 자동 처리 목록                   │    │  │
│  │  │  - 날짜, 공급자, 총액, 신뢰도, 상태             │    │  │
│  │  │  - 필터: 날짜/공급자/검증 여부                  │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  │                    ↓ (행 클릭)                           │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │ Section 2: 상세 정보 (2 컬럼)                    │    │  │
│  │  │  Left: 원본 이미지                               │    │  │
│  │  │  Right: OCR 결과 (편집 가능)                     │    │  │
│  │  │    - 공급자, 날짜, 총액 (텍스트 인풋)           │    │  │
│  │  │    - 항목 테이블 (원두명, 중량, 단가, 금액)     │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  │                    ↓                                     │  │
│  │  ┌─────────────────────────────────────────────────┐    │  │
│  │  │ Section 3: 액션 버튼                             │    │  │
│  │  │  [확인 및 승인] [수정 후 저장] [삭제]           │    │  │
│  │  └─────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 기존 페이지: CostCalculation.py (수동 업로드)            │  │
│  │  - 기존 기능 유지                                        │  │
│  │  - 수동 업로드도 invoices 테이블에 저장                  │  │
│  │  - source='manual' 플래그                                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 기존 페이지들 (Dashboard, Analysis 등)                   │  │
│  │  - invoices 테이블 데이터 활용                           │  │
│  │  - 자동/수동 구분 없이 통합 분석                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4.2 기술 스택 상세

| 레이어 | 기술 | 버전 | 용도 |
|--------|------|------|------|
| **워크플로우 자동화** | n8n | Latest | 이메일 트리거, API 호출, DB 저장 |
| **OCR 엔진** | Claude Vision API | 3.5 Haiku | 이미지 → JSON 변환 |
| **데이터베이스** | SQLite | 3.x | 명세서 데이터 저장 (WAL 모드) |
| **백엔드** | Python | 3.12.3 | Streamlit 서비스 로직 |
| **프론트엔드** | Streamlit | 1.38.0 | 웹 UI (검증/분석) |
| **알림** | Slack API | v1 | 처리 완료/에러 알림 |
| **이미지 저장** | 로컬 파일시스템 | - | data/invoices/ |

---

### 4.3 데이터 흐름 (Data Flow)

#### 시나리오 1: 이메일 자동 처리

```
1. 공급자가 거래명세서 이메일 발송
   └─ 발신: gsc@coffee.com
   └─ 제목: "거래명세서 - 2025-11-17"
   └─ 첨부: invoice_20251117.png

2. Gmail이 이메일 수신
   └─ n8n Gmail Trigger 활성화 (1분마다 폴링)

3. n8n 워크플로우 시작
   └─ 필터링: 발신자 = gsc@coffee.com AND 첨부파일 존재
   └─ 첨부파일 추출: invoice_20251117.png
   └─ Base64 인코딩

4. Claude Vision API 호출
   └─ Request:
        {
          "model": "claude-3-5-haiku-20241022",
          "messages": [{
            "role": "user",
            "content": [
              { "type": "image", "source": { "data": "base64..." } },
              { "type": "text", "text": "명세서 분석 프롬프트..." }
            ]
          }]
        }
   └─ Response:
        {
          "invoice_type": "GSC",
          "invoice_data": { ... },
          "items": [ ... ],
          "confidence": 95.5
        }

5. JSON 파싱 및 검증
   └─ 스키마 검증: 필수 필드 존재 확인
   └─ 데이터 정규화: 날짜 형식, 숫자 변환

6. SQLite 저장 (2개 쿼리)
   └─ Query 1: INSERT INTO invoices (...) VALUES (...)
        └─ 반환: invoice_id = 42
   └─ Query 2: INSERT INTO invoice_items (invoice_id, ...) VALUES (42, ...)
        └─ 항목별로 반복 (N개)

7. 이미지 파일 저장
   └─ 경로: data/invoices/20251117_GSC_42.png
   └─ DB 업데이트: UPDATE invoices SET image_path = '...' WHERE id = 42

8. Slack 알림 전송
   └─ 메시지:
        "✅ 명세서 자동 처리 완료
         - 공급자: 글로벌 스페셜티 커피
         - 총액: 1,250,000원
         - 항목: 2개
         - 신뢰도: 95.5%
         - 검증 필요: 아니오"

9. Streamlit 자동 갱신
   └─ 사용자가 "AutoProcessedInvoices" 페이지 접속
   └─ DB 쿼리: SELECT * FROM invoices ORDER BY processed_at DESC
   └─ 최신 명세서 (id=42) 목록에 표시
```

#### 시나리오 2: 신뢰도 낮은 경우

```
4. Claude Vision API 호출
   └─ Response:
        {
          "confidence": 65.0,  ← 임계값(80%) 미만
          "warnings": ["날짜 인식 불확실", "항목 1의 단가 확인 필요"]
        }

5. 조건부 처리
   └─ IF confidence < 80:
        ├─ DB 저장 시 verified = 0 플래그
        ├─ Slack 알림:
        │    "⚠️ 명세서 처리 완료 (검증 필요)
        │     - 신뢰도: 65%
        │     - 경고: 날짜 인식 불확실, 항목 1의 단가 확인 필요
        │     - 액션: Streamlit에서 수동 검증 필요"
        └─ 워크플로우 종료

6. 사용자 액션
   └─ Streamlit "AutoProcessedInvoices" 페이지 접속
   └─ "미검증" 필터 활성화
   └─ 명세서 id=42 선택
   └─ 원본 이미지 vs OCR 결과 비교
   └─ 날짜 수정: 2025-11-17 (OCR: 2025-11-77 ← 오인식)
   └─ 항목 1 단가 수정: 25,000원 (OCR: 2,500원 ← 오인식)
   └─ [확인 및 승인] 버튼 클릭
   └─ DB 업데이트: UPDATE invoices SET verified = 1, verified_at = NOW()
```

---

### 4.4 보안 설계

#### 4.4.1 API 키 관리

**n8n Credentials (암호화 저장):**
```
Claude API:
  - Type: Header Auth
  - Name: x-api-key
  - Value: sk-ant-api03-xxxxx (암호화)

Gmail:
  - Type: OAuth2
  - Client ID: xxxxx.apps.googleusercontent.com
  - Client Secret: xxxxx (암호화)

Slack:
  - Type: Webhook URL
  - URL: https://hooks.slack.com/services/xxxxx (암호화)
```

#### 4.4.2 데이터 보안

**이미지 파일:**
- 로컬 파일 시스템에만 저장 (data/invoices/)
- 파일 권한: 600 (소유자만 읽기/쓰기)
- 주기적 백업: 주 1회 외부 저장소 (암호화)

**데이터베이스:**
- SQLite WAL 모드 (동시 접근 제어)
- 일일 백업: data/backups/roasting_data_YYYYMMDD.db
- 접근 제어: Streamlit은 읽기 전용 (향후 권한 분리)

**네트워크:**
- n8n Webhook: HTTPS 필수 (Let's Encrypt 인증서)
- Claude API: HTTPS (기본)
- Slack Webhook: HTTPS (기본)

---

### 4.5 에러 처리 전략

| 에러 유형 | 감지 방법 | 처리 방법 | 알림 |
|-----------|-----------|-----------|------|
| **Claude API 실패** | HTTP 5xx | 지수 백오프 재시도 (3회) | Slack 에러 알림 |
| **크레딧 부족** | HTTP 402 | 재시도 중단, 관리자 알림 | Slack 긴급 알림 |
| **JSON 파싱 오류** | JSON.parse 예외 | 원본 응답 로깅 후 재시도 | Slack 에러 알림 |
| **DB 쓰기 실패** | SQLite 예외 | 트랜잭션 롤백, 재시도 | Slack 에러 알림 |
| **이미지 저장 실패** | 파일시스템 예외 | DB 데이터는 유지, 경로 NULL | 로그만 기록 |
| **신뢰도 낮음** | confidence < 80 | verified=0 플래그, 정상 저장 | Slack 경고 알림 |

**재시도 정책 (지수 백오프):**
```
1차 시도: 즉시
2차 시도: 5초 후
3차 시도: 25초 후 (5² = 25)
실패: 에러 로그 + Slack 알림
```

---

## 5. Tasks (작업 분해)

### Phase 1: 환경 준비 (예상: 1-2시간)

#### Task 1.1: n8n 환경 구축

**목표**: n8n 실행 환경 준비

**옵션 A: n8n Cloud (추천)**
```bash
# 1. https://n8n.io 회원가입
# 2. Starter 플랜 선택 ($20/월)
# 3. 워크스페이스 생성
```

**옵션 B: n8n Self-hosted (Docker)**
```bash
# 1. Docker 설치 확인
docker --version

# 2. n8n 컨테이너 실행
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# 3. 브라우저 접속
# http://localhost:5678
```

**완료 조건**: n8n 웹 인터페이스 접속 가능

**의존성**: 없음

---

#### Task 1.2: SQLite 데이터베이스 스키마 생성

**목표**: invoices 및 invoice_items 테이블 생성

```bash
# 1. 프로젝트 디렉토리 이동
cd /mnt/d/Ai/WslProject/TheMoon_Project

# 2. SQL 스크립트 실행
./venv/bin/python << 'EOF'
import sqlite3

conn = sqlite3.connect('data/roasting_data.db')
cursor = conn.cursor()

# invoices 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier TEXT NOT NULL,
    invoice_date TEXT NOT NULL,
    total_amount REAL NOT NULL DEFAULT 0,
    total_weight REAL NOT NULL DEFAULT 0,
    source TEXT NOT NULL DEFAULT 'manual',
    confidence REAL DEFAULT 0,
    processed_at TEXT NOT NULL,
    image_path TEXT,
    raw_json TEXT,
    verified BOOLEAN DEFAULT 0,
    verified_at TEXT,
    verified_by TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
''')

# invoice_items 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,
    bean_name TEXT NOT NULL,
    spec TEXT,
    quantity INTEGER DEFAULT 0,
    weight REAL NOT NULL,
    unit_price REAL NOT NULL,
    amount REAL NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
)
''')

# 인덱스 생성
cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoices_date ON invoices(invoice_date)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoices_supplier ON invoices(supplier)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoices_source ON invoices(source)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoice_items_invoice_id ON invoice_items(invoice_id)')

# WAL 모드 활성화 (동시 접근 제어)
cursor.execute('PRAGMA journal_mode=WAL')

conn.commit()
conn.close()
print("✅ 데이터베이스 스키마 생성 완료")
EOF
```

**완료 조건**: 테이블 및 인덱스 생성 확인

**의존성**: 없음

---

#### Task 1.3: n8n Credentials 설정

**목표**: Claude API, Gmail, Slack 인증 정보 등록

**n8n 설정:**
```
1. n8n 웹 인터페이스 → Settings → Credentials

2. Claude API (Header Auth):
   - Name: Claude API
   - Type: Header Auth
   - Header Name: x-api-key
   - Header Value: sk-ant-api03-xxxxx

3. Gmail (OAuth2):
   - Name: Gmail Account
   - Type: Gmail OAuth2
   - [Connect My Account] 클릭
   - Google 계정 로그인 및 권한 승인

4. Slack (Webhook):
   - Name: Slack Webhook
   - Type: Webhook
   - URL: https://hooks.slack.com/services/xxxxx
```

**완료 조건**: 모든 Credentials 연결 성공

**의존성**: Task 1.1 완료

---

### Phase 2: n8n 워크플로우 구축 (예상: 2-3시간)

#### Task 2.1: 워크플로우 1 - 이메일 트리거 생성

**목표**: Gmail에서 명세서 이메일 감지

**n8n 노드 설정:**

```
1. Gmail Trigger 노드
   - Trigger: On New Email
   - Credentials: Gmail Account (Task 1.3에서 생성)
   - Filters:
     - From: gsc@coffee.com, hacielo@coffee.com
     - Subject: "명세서" OR "거래명세서"
     - Has Attachment: Yes
   - Poll Interval: 1 minute

2. Filter 노드 (첨부파일 검증)
   - Condition: {{ $json.attachments.length > 0 }}
   - IF True: Continue
   - IF False: Stop Workflow

3. Extract Attachment 노드 (Code)
   JavaScript:
   ---
   const attachments = $input.item.json.attachments;
   const imageAttachment = attachments.find(att =>
     att.mimeType.startsWith('image/')
   );

   if (!imageAttachment) {
     throw new Error('No image attachment found');
   }

   return {
     json: {
       filename: imageAttachment.filename,
       mimeType: imageAttachment.mimeType,
       data: imageAttachment.data
     }
   };
   ---
```

**완료 조건**: 테스트 이메일 발송 시 노드 정상 작동

**의존성**: Task 1.3 완료

---

#### Task 2.2: Claude Vision API 호출 노드

**목표**: 이미지를 Claude API로 전송하여 JSON 응답 받기

**HTTP Request 노드 설정:**

```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "claudeApi",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "anthropic-version",
        "value": "2023-06-01"
      }
    ]
  },
  "sendBody": true,
  "contentType": "application/json",
  "bodyParameters": {
    "parameters": [
      {
        "name": "model",
        "value": "claude-3-5-haiku-20241022"
      },
      {
        "name": "max_tokens",
        "value": 2048
      },
      {
        "name": "messages",
        "value": "={{ [{\"role\":\"user\",\"content\":[{\"type\":\"image\",\"source\":{\"type\":\"base64\",\"media_type\":\"{{ $json.mimeType }}\",\"data\":\"{{ $json.data }}\"}},{\"type\":\"text\",\"text\":\"당신은 거래 명세서 분석 전문가입니다...\" }]}] }}"
      }
    ]
  }
}
```

**프롬프트 (상세):**
```
당신은 거래 명세서 분석 전문가입니다.
첨부된 이미지는 커피 원두 거래 명세서입니다.

다음 정보를 정확하게 추출하여 JSON 형식으로 반환하세요:

{
    "invoice_type": "GSC 또는 HACIELO (공급자명 기준)",
    "invoice_data": {
        "supplier": "공급자명",
        "invoice_date": "거래일자 (YYYY-MM-DD)",
        "total_amount": 총금액 (숫자),
        "total_weight": 총중량 (kg, 소수점)
    },
    "items": [
        {
            "bean_name": "원두명",
            "spec": "규격 (1kg, 5kg 등)",
            "quantity": 수량,
            "weight": 중량 (kg),
            "unit_price": 단가 (원/kg),
            "amount": 공급가액 (원)
        }
    ],
    "confidence": 신뢰도 (0-100),
    "warnings": ["경고 메시지 배열"]
}

주의사항:
1. 숫자는 쉼표 제거
2. 날짜는 YYYY-MM-DD 형식
3. JSON만 반환 (설명 불필요)
```

**완료 조건**: 샘플 이미지로 JSON 응답 확인

**의존성**: Task 2.1 완료

---

#### Task 2.3: JSON 파싱 및 검증 노드

**목표**: Claude 응답에서 JSON 추출 및 스키마 검증

**Code 노드 (JavaScript):**

```javascript
const response = $input.item.json;

// 1. Claude 응답에서 텍스트 추출
const content = response.content[0].text;

// 2. JSON 추출 (```json ... ``` 형태 처리)
let jsonText = content;
if (content.includes('```json')) {
  const start = content.indexOf('```json') + 7;
  const end = content.indexOf('```', start);
  jsonText = content.substring(start, end).trim();
} else if (content.includes('```')) {
  const start = content.indexOf('```') + 3;
  const end = content.indexOf('```', start);
  jsonText = content.substring(start, end).trim();
}

// 3. JSON 파싱
let result;
try {
  result = JSON.parse(jsonText);
} catch (e) {
  throw new Error(`JSON 파싱 실패: ${e.message}\n원본: ${jsonText}`);
}

// 4. 스키마 검증 (필수 필드 확인)
const requiredFields = ['invoice_type', 'invoice_data', 'items'];
for (const field of requiredFields) {
  if (!result[field]) {
    throw new Error(`필수 필드 누락: ${field}`);
  }
}

// 5. 데이터 정규화
result.invoice_data.total_amount = parseFloat(result.invoice_data.total_amount) || 0;
result.invoice_data.total_weight = parseFloat(result.invoice_data.total_weight) || 0;
result.confidence = parseFloat(result.confidence) || 0;

// 6. 타임스탬프 추가
result.processed_at = new Date().toISOString();

return { json: result };
```

**완료 조건**: 유효한 JSON 객체 출력

**의존성**: Task 2.2 완료

---

#### Task 2.4: SQLite INSERT 노드

**목표**: invoices 및 invoice_items 테이블에 데이터 저장

**Execute Command 노드 (2개 필요):**

**노드 1: invoices 테이블 INSERT**
```bash
sqlite3 /mnt/d/Ai/WslProject/TheMoon_Project/data/roasting_data.db << 'EOF'
INSERT INTO invoices (
    supplier,
    invoice_date,
    total_amount,
    total_weight,
    source,
    confidence,
    processed_at,
    raw_json
) VALUES (
    '{{ $json.invoice_data.supplier }}',
    '{{ $json.invoice_data.invoice_date }}',
    {{ $json.invoice_data.total_amount }},
    {{ $json.invoice_data.total_weight }},
    'email',
    {{ $json.confidence }},
    '{{ $json.processed_at }}',
    '{{ JSON.stringify($json) }}'
);
SELECT last_insert_rowid() AS invoice_id;
EOF
```

**노드 2: invoice_items 테이블 INSERT (Loop)**
```bash
# n8n Loop 노드 사용
# 입력: {{ $json.items }}
# 각 항목마다 실행:

sqlite3 /mnt/d/Ai/WslProject/TheMoon_Project/data/roasting_data.db << 'EOF'
INSERT INTO invoice_items (
    invoice_id,
    bean_name,
    spec,
    quantity,
    weight,
    unit_price,
    amount
) VALUES (
    {{ $('노드1').item.json.invoice_id }},
    '{{ $json.bean_name }}',
    '{{ $json.spec }}',
    {{ $json.quantity }},
    {{ $json.weight }},
    {{ $json.unit_price }},
    {{ $json.amount }}
);
EOF
```

**완료 조건**: DB에 데이터 저장 확인

**의존성**: Task 2.3 완료

---

#### Task 2.5: 이미지 파일 저장 노드

**목표**: 원본 이미지를 로컬 파일시스템에 저장

**Execute Command 노드:**

```bash
# 1. 디렉토리 생성 (없으면)
mkdir -p /mnt/d/Ai/WslProject/TheMoon_Project/data/invoices

# 2. 파일명 생성 (날짜_공급자_ID.png)
FILENAME="{{ $json.invoice_data.invoice_date }}_{{ $json.invoice_data.supplier }}_{{ $('노드1').item.json.invoice_id }}.png"
FILEPATH="/mnt/d/Ai/WslProject/TheMoon_Project/data/invoices/${FILENAME}"

# 3. Base64 → 이미지 파일 저장
echo "{{ $('Extract Attachment').item.json.data }}" | base64 -d > "${FILEPATH}"

# 4. DB 업데이트 (image_path 설정)
sqlite3 /mnt/d/Ai/WslProject/TheMoon_Project/data/roasting_data.db << EOF
UPDATE invoices
SET image_path = '${FILEPATH}'
WHERE id = {{ $('노드1').item.json.invoice_id }};
EOF

echo "✅ 이미지 저장 완료: ${FILEPATH}"
```

**완료 조건**: 파일 생성 및 DB 업데이트 확인

**의존성**: Task 2.4 완료

---

#### Task 2.6: Slack 알림 노드

**목표**: 처리 완료 또는 에러 알림 전송

**Slack 노드 설정:**

```json
{
  "channel": "#invoices",
  "text": "",
  "attachments": [
    {
      "color": "{{ $json.confidence >= 80 ? 'good' : 'warning' }}",
      "title": "{{ $json.confidence >= 80 ? '✅ 명세서 자동 처리 완료' : '⚠️ 명세서 처리 완료 (검증 필요)' }}",
      "fields": [
        {
          "title": "공급자",
          "value": "{{ $json.invoice_data.supplier }}",
          "short": true
        },
        {
          "title": "거래일자",
          "value": "{{ $json.invoice_data.invoice_date }}",
          "short": true
        },
        {
          "title": "총액",
          "value": "{{ Number($json.invoice_data.total_amount).toLocaleString() }}원",
          "short": true
        },
        {
          "title": "항목 수",
          "value": "{{ $json.items.length }}개",
          "short": true
        },
        {
          "title": "신뢰도",
          "value": "{{ $json.confidence }}%",
          "short": true
        },
        {
          "title": "검증 필요",
          "value": "{{ $json.confidence < 80 ? '예' : '아니오' }}",
          "short": true
        }
      ],
      "footer": "n8n Invoice Processor",
      "ts": "{{ Math.floor(Date.now() / 1000) }}"
    }
  ]
}
```

**완료 조건**: Slack 채널에 알림 수신 확인

**의존성**: Task 2.5 완료

---

#### Task 2.7: 에러 핸들링 노드

**목표**: API 실패 시 재시도 및 에러 로깅

**IF 노드 (조건 분기):**

```
조건: {{ $json.error }}

True (에러 발생):
  ├─ Wait 노드 (5초 대기)
  ├─ Increment Retry 노드 (재시도 카운터 +1)
  ├─ IF retry_count < 3:
  │    └─ Claude API 노드로 돌아가기 (루프)
  └─ ELSE (3회 재시도 실패):
       ├─ SQLite INSERT (에러 로그 테이블)
       └─ Slack 에러 알림

False (정상 처리):
  └─ 다음 노드 진행
```

**에러 로그 테이블:**
```sql
CREATE TABLE IF NOT EXISTS error_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id TEXT,
    error_message TEXT,
    error_stack TEXT,
    retry_count INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**완료 조건**: 강제 에러 시 재시도 및 알림 확인

**의존성**: Task 2.6 완료

---

### Phase 3: Streamlit 검증 인터페이스 구축 (예상: 2-3시간)

#### Task 3.1: AutoProcessedInvoices.py 페이지 생성

**목표**: 자동 처리된 명세서 목록 및 상세 보기 페이지

**파일 위치**: `app/pages/AutoProcessedInvoices.py`

**구현 내용** (450줄 예상):

```python
"""
자동 처리된 명세서 검증 페이지
"""

import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
from datetime import datetime, timedelta

st.set_page_config(page_title="자동 처리 명세서", page_icon="🤖", layout="wide")

# ===== 데이터베이스 연결 =====
@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect('data/roasting_data.db', check_same_thread=False)
    return conn

conn = get_db_connection()

# ===== Section 1: 필터 및 목록 =====
st.title("🤖 자동 처리된 명세서")

col1, col2, col3, col4 = st.columns(4)

with col1:
    date_filter = st.date_input(
        "기간",
        value=(datetime.now() - timedelta(days=7), datetime.now())
    )

with col2:
    supplier_filter = st.selectbox(
        "공급자",
        ["전체", "GSC", "HACIELO", "기타"]
    )

with col3:
    verified_filter = st.selectbox(
        "검증 상태",
        ["전체", "미검증", "검증 완료"]
    )

with col4:
    confidence_filter = st.slider(
        "최소 신뢰도",
        0, 100, 0
    )

# 쿼리 작성
query = """
SELECT
    id,
    supplier,
    invoice_date,
    total_amount,
    total_weight,
    source,
    confidence,
    verified,
    processed_at,
    image_path
FROM invoices
WHERE 1=1
"""

params = []

if date_filter:
    query += " AND invoice_date BETWEEN ? AND ?"
    params.extend([date_filter[0].strftime('%Y-%m-%d'), date_filter[1].strftime('%Y-%m-%d')])

if supplier_filter != "전체":
    query += " AND supplier LIKE ?"
    params.append(f"%{supplier_filter}%")

if verified_filter == "미검증":
    query += " AND verified = 0"
elif verified_filter == "검증 완료":
    query += " AND verified = 1"

query += " AND confidence >= ?"
params.append(confidence_filter)

query += " ORDER BY processed_at DESC"

# 데이터 조회
df = pd.read_sql_query(query, conn, params=params)

if df.empty:
    st.info("조건에 맞는 명세서가 없습니다.")
    st.stop()

# 데이터프레임 표시
st.write(f"**총 {len(df)}건**")

# 상태 컬럼 추가
df['상태'] = df.apply(
    lambda row: "✅ 검증 완료" if row['verified'] == 1
    else ("⚠️ 검증 필요" if row['confidence'] < 80 else "🟢 자동 승인"),
    axis=1
)

# 테이블 표시
selected_row = st.dataframe(
    df[['id', 'supplier', 'invoice_date', 'total_amount', 'confidence', '상태']],
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row"
)

# ===== Section 2: 상세 정보 =====
if selected_row['selection']['rows']:
    selected_id = df.iloc[selected_row['selection']['rows'][0]]['id']

    st.divider()
    st.subheader(f"명세서 상세 (ID: {selected_id})")

    # 명세서 데이터 조회
    invoice = df[df['id'] == selected_id].iloc[0]

    # 항목 데이터 조회
    items_df = pd.read_sql_query(
        "SELECT * FROM invoice_items WHERE invoice_id = ?",
        conn,
        params=(selected_id,)
    )

    # 2컬럼 레이아웃
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.write("**원본 이미지**")
        if invoice['image_path'] and os.path.exists(invoice['image_path']):
            img = Image.open(invoice['image_path'])
            st.image(img, use_column_width=True)
        else:
            st.warning("이미지 파일을 찾을 수 없습니다.")

    with col_right:
        st.write("**OCR 결과 (편집 가능)**")

        with st.form(f"edit_form_{selected_id}"):
            # 메인 정보
            supplier_edit = st.text_input("공급자", value=invoice['supplier'])
            date_edit = st.date_input("거래일자", value=pd.to_datetime(invoice['invoice_date']))
            total_amount_edit = st.number_input("총액", value=float(invoice['total_amount']))

            st.write("**항목 정보**")

            # 항목 편집 (데이터 에디터)
            items_edit = st.data_editor(
                items_df[['bean_name', 'spec', 'quantity', 'weight', 'unit_price', 'amount']],
                use_container_width=True,
                num_rows="dynamic"
            )

            # 버튼
            col1, col2, col3 = st.columns(3)
            with col1:
                submit_verify = st.form_submit_button("✅ 확인 및 승인", use_container_width=True)
            with col2:
                submit_save = st.form_submit_button("💾 수정 후 저장", use_container_width=True)
            with col3:
                submit_delete = st.form_submit_button("🗑️ 삭제", use_container_width=True, type="secondary")

            # 처리
            if submit_verify:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE invoices SET verified = 1, verified_at = ? WHERE id = ?",
                    (datetime.now().isoformat(), selected_id)
                )
                conn.commit()
                st.success("✅ 명세서가 승인되었습니다!")
                st.rerun()

            elif submit_save:
                # 업데이트 쿼리 실행
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE invoices
                    SET supplier = ?, invoice_date = ?, total_amount = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (supplier_edit, date_edit.strftime('%Y-%m-%d'), total_amount_edit,
                     datetime.now().isoformat(), selected_id)
                )

                # 항목 삭제 후 재삽입
                cursor.execute("DELETE FROM invoice_items WHERE invoice_id = ?", (selected_id,))
                for _, item in items_edit.iterrows():
                    cursor.execute(
                        """
                        INSERT INTO invoice_items (invoice_id, bean_name, spec, quantity, weight, unit_price, amount)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (selected_id, item['bean_name'], item['spec'], item['quantity'],
                         item['weight'], item['unit_price'], item['amount'])
                    )

                conn.commit()
                st.success("💾 수정사항이 저장되었습니다!")
                st.rerun()

            elif submit_delete:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM invoices WHERE id = ?", (selected_id,))
                conn.commit()
                st.success("🗑️ 명세서가 삭제되었습니다!")
                st.rerun()

# ===== Section 3: 통계 =====
st.divider()
st.subheader("📊 처리 통계")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_count = len(df)
    st.metric("총 처리 건수", f"{total_count}건")

with col2:
    verified_count = len(df[df['verified'] == 1])
    st.metric("검증 완료", f"{verified_count}건")

with col3:
    avg_confidence = df['confidence'].mean()
    st.metric("평균 신뢰도", f"{avg_confidence:.1f}%")

with col4:
    low_confidence_count = len(df[df['confidence'] < 80])
    st.metric("검증 필요", f"{low_confidence_count}건", delta=None if low_confidence_count == 0 else "주의")
```

**완료 조건**:
- 페이지 정상 로드
- 목록 필터링 작동
- 상세 보기 및 편집 기능 작동
- 승인/삭제 기능 작동

**의존성**: Task 1.2 (DB 스키마) 완료

---

#### Task 3.2: 기존 CostCalculation.py 수정

**목표**: 수동 업로드도 invoices 테이블에 저장

**수정 위치**: `app/pages/CostCalculation.py`

**변경 내용**:

```python
# 기존 코드 (OCR 처리 후):
if ocr_result:
    # ===== 신규: invoices 테이블에 저장 =====
    conn = sqlite3.connect('data/roasting_data.db')
    cursor = conn.cursor()

    # 메인 테이블
    cursor.execute("""
        INSERT INTO invoices (
            supplier, invoice_date, total_amount, total_weight,
            source, confidence, processed_at, image_path, raw_json
        ) VALUES (?, ?, ?, ?, 'manual', 100, ?, ?, ?)
    """, (
        ocr_result['invoice_data']['supplier'],
        ocr_result['invoice_data']['invoice_date'],
        ocr_result['invoice_data']['total_amount'],
        ocr_result['invoice_data']['total_weight'],
        datetime.now().isoformat(),
        image_path,  # 이미지 임시 저장 경로
        json.dumps(ocr_result)
    ))

    invoice_id = cursor.lastrowid

    # 항목 테이블
    for item in ocr_result['items']:
        cursor.execute("""
            INSERT INTO invoice_items (invoice_id, bean_name, spec, quantity, weight, unit_price, amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            invoice_id,
            item['bean_name'],
            item['spec'],
            item['quantity'],
            item['weight'],
            item['unit_price'],
            item['amount']
        ))

    conn.commit()
    conn.close()

    st.success(f"✅ 명세서가 저장되었습니다! (ID: {invoice_id})")
    # ===== 신규 끝 =====

    # 기존 로직 계속...
```

**완료 조건**: 수동 업로드 후 invoices 테이블에 데이터 확인

**의존성**: Task 3.1 완료

---

#### Task 3.3: app.py에 페이지 추가

**목표**: 사이드바에 "자동 처리 명세서" 메뉴 추가

**수정 위치**: `app/app.py`

**변경 내용**:

```python
# 페이지 설정
pages = {
    "홈": [
        st.Page("pages/Dashboard.py", title="📊 대시보드"),
    ],
    "데이터 관리": [
        st.Page("pages/BeanManagement.py", title="☕ 원두 관리"),
        st.Page("pages/BlendManagement.py", title="🎨 블렌드 관리"),
        st.Page("pages/InventoryManagement.py", title="📦 재고 관리"),
    ],
    "명세서 처리": [  # ← 신규 섹션
        st.Page("pages/AutoProcessedInvoices.py", title="🤖 자동 처리 명세서"),  # ← 신규
        st.Page("pages/CostCalculation.py", title="💰 원가 계산 (수동)"),
    ],
    "분석 및 보고서": [
        st.Page("pages/Analysis.py", title="📈 상세 분석"),
        st.Page("pages/AdvancedAnalysis.py", title="🔬 고급 분석"),
        st.Page("pages/Report.py", title="📄 보고서"),
    ],
    "시스템": [
        st.Page("pages/ExcelSync.py", title="📊 Excel 동기화"),
        st.Page("pages/Settings.py", title="⚙️ 설정"),
    ],
}
```

**완료 조건**: 사이드바에 메뉴 표시 및 클릭 시 페이지 로드

**의존성**: Task 3.1 완료

---

### Phase 4: 테스트 및 검증 (예상: 1-2시간)

#### Task 4.1: End-to-End 테스트 (이메일 → Streamlit)

**시나리오**:
```
1. 테스트 이메일 발송
   - 발신: 본인 Gmail
   - 수신: n8n 연결된 Gmail
   - 제목: "거래명세서 테스트"
   - 첨부: 샘플 명세서 이미지

2. n8n 워크플로우 모니터링
   - 각 노드 실행 확인
   - 에러 여부 체크
   - 최종 Slack 알림 수신

3. Streamlit 확인
   - "자동 처리 명세서" 페이지 접속
   - 목록에 새 명세서 표시 확인
   - 상세 보기에서 OCR 결과 확인
   - 신뢰도 점수 확인

4. 검증 및 승인
   - OCR 결과와 원본 이미지 비교
   - 필요 시 수정
   - "확인 및 승인" 클릭
   - verified=1 플래그 확인
```

**예상 결과**:
- 이메일 수신 → 2분 이내 처리 완료
- Slack 알림 수신
- Streamlit에 데이터 표시
- 전체 소요 시간: < 5분

**완료 조건**: 전체 흐름 정상 작동

**의존성**: Phase 1-3 완료

---

#### Task 4.2: 에러 케이스 테스트

**테스트 케이스**:

**TC-1: Claude API 크레딧 부족**
```
조건: API 키를 잘못된 키로 변경
예상:
  - HTTP 401 에러
  - 3회 재시도
  - Slack 에러 알림
  - 워크플로우 중단
```

**TC-2: 신뢰도 낮은 OCR 결과**
```
조건: 품질 낮은 이미지 업로드 (흐릿함, 회전)
예상:
  - confidence < 80
  - verified=0 플래그
  - Slack 경고 알림
  - Streamlit "검증 필요" 목록에 표시
```

**TC-3: DB 동시 접근**
```
조건: n8n 저장 중 Streamlit에서 동일 데이터 조회
예상:
  - WAL 모드로 정상 처리
  - 데이터 무결성 유지
```

**TC-4: 이미지 저장 실패**
```
조건: 디스크 공간 부족 시뮬레이션 (권한 제거)
예상:
  - DB 데이터는 저장
  - image_path = NULL
  - 로그 기록
```

**완료 조건**: 모든 TC 통과

**의존성**: Task 4.1 완료

---

#### Task 4.3: 성능 테스트

**목표**: 동시 처리 및 응답 시간 측정

**테스트 방법**:
```bash
# 5개 이메일 동시 발송 (다른 첨부파일)
for i in {1..5}; do
  # 이메일 발송 스크립트
  python send_test_email.py --attachment "test_invoice_${i}.png" &
done

# n8n 워크플로우 실행 시간 측정
# 각 워크플로우의 시작/종료 타임스탬프 비교
```

**성능 목표**:
- 단일 처리: < 10초
- 동시 5개: < 30초 (병렬 처리)
- DB 쓰기: < 1초

**완료 조건**: 목표 성능 달성

**의존성**: Task 4.2 완료

---

### Phase 5: 문서화 및 배포 (예상: 1시간)

#### Task 5.1: 사용자 가이드 작성

**파일 위치**: `Documents/Guides/N8N_OCR_USER_GUIDE.md`

**내용**:
- n8n 워크플로우 설명
- Streamlit 검증 인터페이스 사용법
- 트러블슈팅 (FAQ)
- 에러 메시지 해석

**완료 조건**: 가이드 문서 작성

**의존성**: Task 4.3 완료

---

#### Task 5.2: README.md 업데이트

**수정 내용**:

```markdown
## 🤖 n8n 하이브리드 OCR 시스템

### 자동화 워크플로우
- ✅ 이메일 자동 감지 (Gmail)
- ✅ Claude Vision API 기반 OCR
- ✅ SQLite DB 자동 저장
- ✅ Slack 알림

### 사용 방법
1. 명세서를 이메일로 발송 (gsc@coffee.com 등)
2. n8n이 자동 처리 (2-5분 소요)
3. Slack 알림 수신
4. Streamlit에서 검증 ("🤖 자동 처리 명세서" 페이지)

### 설정
- n8n: `http://localhost:5678` (Self-hosted) 또는 Cloud
- Streamlit: `http://localhost:8501`
```

**완료 조건**: README.md 업데이트 및 커밋

**의존성**: Task 5.1 완료

---

#### Task 5.3: Git 커밋 및 배포

**커밋 메시지**:
```bash
git add .
git commit -m "feat: n8n 하이브리드 OCR 시스템 통합

- n8n 워크플로우 구축 (이메일 트리거 + Claude API)
- invoices 및 invoice_items 테이블 생성
- AutoProcessedInvoices.py 검증 페이지 추가
- CostCalculation.py 수동 업로드 통합
- Slack 알림 및 에러 핸들링
- End-to-End 테스트 완료

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**배포**:
```bash
# n8n 워크플로우 백업
n8n export:workflow --all --output=./n8n_workflows/

# Streamlit 재시작
./venv/bin/streamlit run app/app.py --server.port 8501
```

**완료 조건**: Git 푸시 및 시스템 운영 시작

**의존성**: Task 5.2 완료

---

## 6. Technical Specifications (기술 사양)

### 6.1 시스템 요구사항

| 항목 | 최소 사양 | 권장 사양 |
|------|-----------|-----------|
| **OS** | Ubuntu 20.04 (WSL2) | Ubuntu 22.04 (WSL2) |
| **Python** | 3.10+ | 3.12.3 |
| **Node.js** | 18+ (n8n Self-hosted) | 20+ |
| **RAM** | 4GB | 8GB |
| **디스크** | 10GB 여유 | 50GB 여유 (이미지 저장) |
| **네트워크** | 10Mbps | 100Mbps |

### 6.2 외부 서비스

| 서비스 | 용도 | 비용 |
|--------|------|------|
| **n8n Cloud** | 워크플로우 실행 (선택) | $20/월 (Starter) |
| **Claude API** | Vision OCR | $0.002/이미지 (Haiku) |
| **Gmail** | 이메일 트리거 | 무료 |
| **Slack** | 알림 | 무료 |

### 6.3 API 사용량 예측

**월 처리량**: 100건 명세서 기준

| 항목 | 사용량 | 비용 |
|------|--------|------|
| Claude API | 100 이미지 | $0.20 |
| n8n Cloud | 100 워크플로우 실행 | $20 (포함) |
| 저장 공간 | 100 이미지 (평균 500KB) | 50MB |
| **총 비용** | - | **$20.20/월** |

### 6.4 성능 벤치마크

| 지표 | 목표 | 실제 측정 (예상) |
|------|------|------------------|
| 이메일 감지 시간 | < 2분 | 1분 (폴링 간격) |
| Claude API 응답 | < 5초 | 3-4초 |
| DB 저장 시간 | < 1초 | 0.5초 |
| 전체 처리 시간 | < 10초 | 6-8초 |
| 동시 처리 능력 | 5개 | 5개 (병렬) |

---

## 7. Next Steps (다음 단계)

### 7.1 즉시 실행 가능한 작업 (Quick Start)

**Step 1: n8n 환경 선택 (5분)**
```
질문: n8n Cloud vs Self-hosted?
├─ Cloud ($20/월): https://n8n.io 가입 → Starter 플랜 선택
└─ Self-hosted (무료): docker run -d --name n8n -p 5678:5678 n8nio/n8n
```

**Step 2: 데이터베이스 준비 (5분)**
```bash
cd /mnt/d/Ai/WslProject/TheMoon_Project
./venv/bin/python << EOF
import sqlite3
conn = sqlite3.connect('data/roasting_data.db')
# (Task 1.2의 SQL 실행)
EOF
```

**Step 3: 첫 워크플로우 생성 (30분)**
```
1. n8n 접속: http://localhost:5678 또는 Cloud URL
2. New Workflow 클릭
3. Gmail Trigger 노드 추가
4. Claude API 노드 추가 (Task 2.2 참조)
5. 테스트 실행
```

---

### 7.2 구현 진행 순서 (타임라인)

```
Day 1 (4시간):
  ├─ Phase 1: 환경 준비 (1-2시간)
  │    ├─ Task 1.1: n8n 설치
  │    ├─ Task 1.2: DB 스키마 생성
  │    └─ Task 1.3: Credentials 설정
  └─ Phase 2 (시작): 워크플로우 구축 (2시간)
       ├─ Task 2.1: Gmail Trigger
       └─ Task 2.2: Claude API 호출

Day 2 (4시간):
  ├─ Phase 2 (완료): 워크플로우 구축
  │    ├─ Task 2.3: JSON 파싱
  │    ├─ Task 2.4: SQLite 저장
  │    ├─ Task 2.5: 이미지 저장
  │    ├─ Task 2.6: Slack 알림
  │    └─ Task 2.7: 에러 핸들링
  └─ Phase 3 (시작): Streamlit 인터페이스 (1시간)
       └─ Task 3.1: AutoProcessedInvoices.py

Day 3 (4시간):
  ├─ Phase 3 (완료): Streamlit 인터페이스 (2시간)
  │    ├─ Task 3.2: CostCalculation.py 수정
  │    └─ Task 3.3: app.py 업데이트
  ├─ Phase 4: 테스트 (1.5시간)
  │    ├─ Task 4.1: E2E 테스트
  │    ├─ Task 4.2: 에러 케이스
  │    └─ Task 4.3: 성능 테스트
  └─ Phase 5: 문서화 및 배포 (0.5시간)
       ├─ Task 5.1: 사용자 가이드
       ├─ Task 5.2: README 업데이트
       └─ Task 5.3: Git 커밋

총 소요 시간: 12시간 (3일 * 4시간)
```

---

### 7.3 체크리스트

**시작 전:**
- [ ] n8n 환경 결정 (Cloud vs Self-hosted)
- [ ] Claude API 키 준비 (크레딧 충전)
- [ ] Gmail 계정 준비 (OAuth 동의)
- [ ] Slack Webhook URL 생성 (선택)

**Phase 1:**
- [ ] n8n 설치 및 접속 확인
- [ ] invoices 테이블 생성 확인
- [ ] invoice_items 테이블 생성 확인
- [ ] Credentials 3개 등록 (Claude, Gmail, Slack)

**Phase 2:**
- [ ] Gmail Trigger 정상 작동
- [ ] Claude API 응답 확인 (JSON)
- [ ] JSON 파싱 성공
- [ ] SQLite INSERT 성공
- [ ] 이미지 파일 저장 확인
- [ ] Slack 알림 수신
- [ ] 에러 재시도 작동

**Phase 3:**
- [ ] AutoProcessedInvoices.py 페이지 로드
- [ ] 목록 필터링 작동
- [ ] 상세 보기 표시
- [ ] 편집 기능 작동
- [ ] 승인/삭제 기능 작동
- [ ] CostCalculation.py 수동 업로드 통합

**Phase 4:**
- [ ] E2E 테스트 통과
- [ ] 에러 케이스 4개 통과
- [ ] 성능 목표 달성

**Phase 5:**
- [ ] 사용자 가이드 작성
- [ ] README.md 업데이트
- [ ] Git 커밋 및 푸시

---

### 7.4 향후 개선 방향

**1차 릴리스 (이 플랜):**
- ✅ 이메일 트리거 자동 처리
- ✅ Claude Vision API OCR
- ✅ Streamlit 검증 인터페이스

**2차 개선 (추후):**
- 🔄 Webhook 트리거 추가 (모바일 앱 연동)
- 🔄 Google Drive 폴더 감시
- 🔄 다중 OCR 엔진 (Google Vision, Textract) 비교
- 🔄 자동 원가 계산 (명세서 → 원가 테이블 직접 저장)

**3차 개선 (장기):**
- 🔄 AI 기반 이상치 감지 (가격 급등, 중량 오류)
- 🔄 공급자별 명세서 템플릿 학습
- 🔄 월말 자동 정산 보고서
- 🔄 다중 사용자 권한 관리

---

### 7.5 문의 및 지원

**문제 발생 시:**
1. n8n 워크플로우 Execution 로그 확인
2. Streamlit 디버그 모드 실행: `streamlit run app.py --logger.level=debug`
3. SQLite DB 무결성 검사: `sqlite3 data/roasting_data.db "PRAGMA integrity_check;"`
4. 이 플랜 문서의 "6.7 에러 처리" 섹션 참조

**피드백:**
- n8n 워크플로우 개선 제안
- Streamlit UI/UX 개선
- 추가 데이터 소스 요청

---

## 📌 부록

### A. n8n 워크플로우 JSON 백업 예시

```json
{
  "name": "Email Invoice Processor",
  "nodes": [
    {
      "id": "gmail-trigger",
      "type": "n8n-nodes-base.gmailTrigger",
      "parameters": {
        "pollTimes": {"item": [{"mode": "everyMinute"}]},
        "filters": {
          "from": "gsc@coffee.com,hacielo@coffee.com",
          "subject": "명세서"
        }
      }
    },
    {
      "id": "claude-api",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.anthropic.com/v1/messages",
        "method": "POST",
        "body": "..."
      }
    }
  ],
  "connections": {
    "gmail-trigger": {"main": [[{"node": "claude-api"}]]}
  }
}
```

### B. 샘플 테스트 데이터

**테스트 이미지**: `Documents/Resources/test_invoice_gsc.png`

**예상 JSON 응답**:
```json
{
  "invoice_type": "GSC",
  "invoice_data": {
    "supplier": "글로벌 스페셜티 커피",
    "invoice_date": "2025-11-17",
    "total_amount": 1250000,
    "total_weight": 50.0
  },
  "items": [
    {
      "bean_name": "에티오피아 예가체프 G1",
      "spec": "1kg",
      "quantity": 20,
      "weight": 20.0,
      "unit_price": 25000,
      "amount": 500000
    }
  ],
  "confidence": 95.5,
  "warnings": []
}
```

### C. 참고 자료

- [n8n 공식 문서](https://docs.n8n.io/)
- [Claude Vision API 가이드](https://docs.anthropic.com/claude/docs/vision)
- [SQLite WAL 모드](https://www.sqlite.org/wal.html)
- [Streamlit 데이터 에디터](https://docs.streamlit.io/library/api-reference/data/st.data_editor)

---

**문서 끝**

마지막 업데이트: 2025-11-17
작성자: Claude (Sonnet 4.5)
버전: 1.0.0
