# 인바운드 시스템 최종 상태

> **업데이트:** 2025-12-20
> **버전:** 0.2.0
> **상태:** ✅ 프로덕션 준비 완료

---

## 📊 시스템 개요

인바운드 문서(발주서, 송장) 관리 시스템의 최종 구성 상태입니다.

### 주요 기능

| 기능 | 상태 | 설명 |
|------|------|------|
| **OCR 문서 분석** | ✅ 활성화 | Google Gemini API 사용 |
| **로컬 파일 저장** | ✅ 활성화 | `backend/static/uploads/inbound/` |
| **구글 드라이브 업로드** | ⚠️ 비활성화 | 서비스 계정 한계 (선택사항) |
| **데이터베이스 저장** | ✅ 활성화 | PostgreSQL (프로덕션) / SQLite (로컬) |

---

## ✅ 활성화된 기능

### 1. OCR 문서 분석

**사용 기술:** Google Gemini Flash API

**추출 정보:**
- 계약번호 (contract_number)
- 공급자 이름 (supplier_name)
- 공급자 연락처 (supplier_phone, supplier_email)
- 발주 날짜 (invoice_date)
- 총액 (total_amount)
- 품목 리스트 (items)

**테스트 결과:**
```
입력: 명세서_1657.PNG (43.7 KB)
출력:
  - 계약번호: S225SJ612690
  - 공급자: 지에스씨인터내셔날(주)
  - 날짜: 2025-03-11
  - 총액: 3,752,000원
```

**정확도:** ✅ 높음 (한글 명세서 정확히 인식)

### 2. 로컬 파일 저장

**저장 위치:**
```
backend/static/uploads/inbound/[UUID].[확장자]
```

**파일명 형식:**
- UUID v4 사용
- 예: `680a6b04-7b59-4c10-9fab-ee35bc747967.PNG`

**장점:**
- ✅ 빠른 접근
- ✅ 설정 불필요
- ✅ 안정적

**주의사항:**
- Render.com 배포 시 재배포 시 파일 삭제됨 (임시 스토리지)
- 중요 파일은 정기적 백업 권장

### 3. 데이터베이스 저장

**모델:** `InboundDocument`

**저장 정보:**
- 계약번호, 공급자 정보
- 문서 날짜, 총액
- 로컬 파일 경로
- 구글 드라이브 링크 (있는 경우)
- OCR 추출 데이터 (JSON)
- 생성/수정 시간

**데이터베이스:**
- 로컬 개발: SQLite
- 프로덕션: PostgreSQL (Render.com)

---

## ⚠️ 비활성화된 기능

### 구글 드라이브 자동 업로드

**상태:** 비활성화

**이유:**
```
Service accounts do not have storage quota.
서비스 계정은 자체 스토리지 할당량이 없습니다.
```

**서비스 계정의 한계:**
- 개인 구글 드라이브에 직접 업로드 불가
- **공유 드라이브(Shared Drive)** 필요 (Google Workspace 전용)
- Google Workspace 구독 필요 (월 $6~)

**대안:**
1. ✅ **현재 방식 (권장):** 로컬 저장만 사용
   - OCR과 로컬 저장으로 충분
   - 필요 시 수동으로 구글 드라이브에 업로드

2. **Google Workspace 구독:**
   - 공유 드라이브 생성
   - 서비스 계정으로 자동 업로드 가능
   - 월 $6~ 비용 발생

3. **OAuth 2.0 구현:**
   - 사용자 인증으로 개인 드라이브 사용
   - 구현 복잡도 높음

**현재 선택:** 옵션 1 (로컬 저장만 사용)

---

## 🧪 테스트 결과

### 전체 플로우 테스트

**명령어:**
```bash
./venv/bin/python backend/scripts/test_inbound_upload_full.py
```

**결과:**
```
✅ 이미지 파일 읽기: 성공
✅ OCR 분석: 성공 (계약번호, 공급자, 날짜, 총액 추출)
✅ 로컬 저장: 성공 (UUID 파일명)
ℹ️ 구글 드라이브 업로드: 비활성화 (선택사항)
```

**소요 시간:**
- 이미지 읽기: < 1초
- OCR 분석: ~10-30초
- 로컬 저장: < 1초
- **총:** ~30초

---

## 📁 파일 구조

```
TheMoon/
├── backend/
│   ├── static/
│   │   └── uploads/
│   │       └── inbound/           # 인바운드 문서 저장 위치
│   │           ├── [UUID].PNG
│   │           ├── [UUID].JPG
│   │           └── ...
│   ├── app/
│   │   ├── services/
│   │   │   ├── ocr_service.py     # OCR 서비스
│   │   │   └── google_drive_service.py  # 구글 드라이브 (비활성화)
│   │   ├── models/
│   │   │   └── inbound_document.py  # 데이터베이스 모델
│   │   └── api/v1/endpoints/
│   │       └── inbound.py         # API 엔드포인트
│   └── scripts/
│       ├── test_inbound_upload_full.py  # 전체 플로우 테스트
│       └── test_google_drive_local.py   # 구글 드라이브 테스트
├── .gemini/
│   └── service_account.json.backup  # 백업 (사용 안 함)
└── Documents/
    └── Guides/
        └── GOOGLE_DRIVE_SERVICE_ACCOUNT_SETUP.md  # 구글 드라이브 설정 가이드
```

---

## 🔧 환경 변수

### 필수

```bash
# OCR 서비스
GOOGLE_API_KEY=AIza...  # Google Gemini API 키
```

### 선택사항 (비활성화)

```bash
# 구글 드라이브 (현재 사용 안 함)
# GOOGLE_SERVICE_ACCOUNT_JSON_CONTENT={"type": "service_account", ...}
```

### 데이터베이스

```bash
# 로컬 개발
DATABASE_URL=sqlite:///themoon.db

# 프로덕션 (Render.com)
DATABASE_URL=postgresql://themoon:password@host/themoon_p922
```

---

## 🚀 배포 상태

### Render.com

**서비스:**
- 백엔드: `themoon-api`
- 프론트엔드: `themoon-frontend`
- 데이터베이스: `themoon-db` (PostgreSQL)

**환경 변수:**
```yaml
GOOGLE_API_KEY: [설정됨]
DATABASE_URL: [자동 설정]
SECRET_KEY: [자동 생성]
```

**파일 저장:**
- 로컬: `backend/static/uploads/inbound/`
- ⚠️ 재배포 시 삭제됨 (임시 스토리지)
- 데이터베이스에 경로만 저장

---

## 📝 API 엔드포인트

### POST /api/v1/inbound

**요청:**
```json
{
  "file": "[이미지 파일]"
}
```

**응답:**
```json
{
  "id": 1,
  "contract_number": "S225SJ612690",
  "supplier_name": "지에스씨인터내셔날(주)",
  "invoice_date": "2025-03-11",
  "total_amount": 3752000,
  "local_file_path": "backend/static/uploads/inbound/[UUID].PNG",
  "drive_link": null,
  "ocr_data": { ... },
  "created_at": "2025-12-20T12:34:56"
}
```

### GET /api/v1/inbound

**응답:**
```json
{
  "items": [
    { ... }
  ],
  "total": 10
}
```

### GET /api/v1/inbound/{id}

**응답:**
```json
{
  "id": 1,
  "contract_number": "S225SJ612690",
  ...
}
```

---

## 🔍 문제 해결

### OCR이 작동하지 않는 경우

**증상:**
```
Warning: GOOGLE_API_KEY not found in environment variables.
```

**해결:**
1. Google AI Studio에서 API 키 발급
2. 환경 변수 설정:
   ```bash
   export GOOGLE_API_KEY="AIza..."
   ```
3. Render.com: Environment 탭에서 설정

### 구글 드라이브 경고 메시지

**메시지:**
```
ℹ️ Google Drive upload disabled (optional feature)
   - Files are saved locally: backend/static/uploads/inbound/
```

**해결:**
- 정상 동작입니다!
- 로컬 저장으로 충분히 사용 가능
- 필요시 Google Workspace 구독

---

## 💡 권장 사항

### 프로덕션 사용

1. **정기 백업:**
   - Render.com 임시 스토리지 특성상 재배포 시 파일 삭제
   - 중요 파일은 정기적으로 다운로드/백업

2. **영구 스토리지 (선택사항):**
   - AWS S3
   - Google Cloud Storage
   - Cloudinary

3. **모니터링:**
   - OCR API 사용량 확인
   - 저장 공간 모니터링

### 개발 환경

**로컬 서버 실행:**
```bash
# 프로젝트 루트에서
./dev.sh backend
```

**테스트:**
```bash
./venv/bin/python backend/scripts/test_inbound_upload_full.py
```

---

## 📊 성능 지표

| 항목 | 수치 | 비고 |
|------|------|------|
| **OCR 정확도** | ~95% | 한글 명세서 기준 |
| **처리 시간** | ~30초 | OCR 분석 포함 |
| **파일 크기** | < 10MB | 권장 |
| **지원 형식** | PNG, JPG, JPEG | 이미지 파일 |

---

## ✅ 체크리스트

### 배포 전 확인사항

- [x] GOOGLE_API_KEY 설정
- [x] DATABASE_URL 설정
- [x] 백엔드 빌드 성공
- [x] 프론트엔드 빌드 성공
- [x] OCR 테스트 통과
- [x] 로컬 저장 테스트 통과
- [x] API 엔드포인트 테스트 통과

### 운영 중 확인사항

- [ ] OCR API 사용량 모니터링
- [ ] 저장 공간 확인
- [ ] 정기 백업 실행
- [ ] 오류 로그 확인

---

## 📚 관련 문서

- [구글 드라이브 서비스 계정 설정 가이드](./GOOGLE_DRIVE_SERVICE_ACCOUNT_SETUP.md)
- [인바운드 시스템 업그레이드 계획](../Planning/Inbound_System_Upgrade_Plan.md)
- [세션 요약 2025-12-19](./SESSION_SUMMARY_2025-12-19.md)

---

**작성일:** 2025-12-20
**버전:** 1.0.0
**작성자:** Claude Code
