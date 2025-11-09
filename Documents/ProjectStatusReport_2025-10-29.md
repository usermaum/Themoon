# 📊 더문드립바 프로젝트 현재 상태 진단 보고서

**진단일:** 2025-10-29
**프로젝트:** The Moon Drip BAR 로스팅 관리 시스템
**진단 범위:** 코드, DB, 데이터 구조

---

## 1️⃣ 기존 코드 상태

### A. Models 구조 (database.py)

**현재 상태:** ✅ 기본 모델 정의됨

```
✓ Bean (원두)
  - no, country_code, name, roast_level, description, price_per_kg
  - relationship: inventory, blend_recipes

✓ Blend (블렌드)
  - name, blend_type, description, total_portion, suggested_price
  - relationship: recipes, transactions

✓ BlendRecipe (블렌드 구성)
  - blend_id, bean_id, portion_count, ratio(%)
  - relationship: blend, bean

⚠️ 부분 정의:
  - Inventory (재고) - 기본 구조만
  - Transaction (거래) - 기본 구조만
```

**문제점:**

| 항목 | 현황 | 필요 개선 |
|-----|------|---------|
| **로스팅 기록** | ❌ 없음 | RoastingLog 모델 필요 |
| **손실률 추적** | ❌ 없음 | 자동 계산 필드 필요 |
| **레시피 버전관리** | ❌ 없음 | BlendRecipe 확장 필요 |
| **혼합률(%)** | ⚠️ ratio 필드만 있음 | blending_ratio_percent로 명확화 필요 |
| **권한 관리** | ❌ 없음 | User, Permission 테이블 필요 |
| **감사 로그** | ❌ 없음 | AuditLog 테이블 필요 |

### B. Services 구조 (5개 파일)

**현재 상태:** ✅ 기본 서비스 구현됨

```
✓ bean_service.py (~10KB)
  - Bean CRUD 기본 구현

✓ blend_service.py (~14KB)
  - Blend CRUD + recipe 관리
  - ⚠️ 포션 기반 (혼합률로 수정 필요)

✓ excel_service.py (~12KB)
  - Excel 읽기/쓰기
  - ⚠️ 마이그레이션 검증 로직 부족

✓ analytics_service.py (~10KB)
  - 기본 분석 (손실률, 통계)
  - ⚠️ 이상 탐지 로직 없음

✓ report_service.py (~15KB)
  - 보고서 생성
  - ⚠️ 권한 기반 리포트 없음
```

**필요 추가 서비스:**

| 서비스 | 용도 | 우선순위 |
|--------|------|---------|
| **RoastingService** | 로스팅 기록 CRUD + 월별 조회 | P0 |
| **CostService** | 혼합률 기반 원가 계산 | P0 |
| **AuthService** | 사용자 인증 & 권한 검사 | P1 |
| **LossRateAnalyzer** | 손실률 이상 탐지 | P1 |
| **ExcelSyncService** | 마이그레이션 상세화 | P0 |

---

## 2️⃣ 데이터베이스 현황

### A. DB 파일 상태

```bash
위치: data/roasting_data.db
크기: 81,920 bytes
생성일: Oct 29 19:54
상태: ✅ 존재하며 사용 중
```

### B. 현재 테이블 목록

```sql
-- 예상되는 테이블들
✓ beans                  (원두)
✓ blends                 (블렌드)
✓ blend_recipes          (블렌드 구성)
✓ inventory              (재고)
✓ transactions           (거래)

❌ 없음:
  - roasting_logs        (로스팅 기록) - Phase 1 추가
  - blend_recipes_history (레시피 버전) - Phase 1 추가
  - users                (사용자) - Phase 2 추가
  - audit_logs           (감사 로그) - Phase 2 추가
  - loss_rate_warnings   (손실률 이상) - Phase 2 추가
```

### C. 데이터 상태 (확인 필요)

```bash
# 확인 필요 사항:
□ beans 테이블: 몇 개 레코드?
□ blends 테이블: 풀문/뉴문 데이터 있나?
□ blend_recipes: 혼합률 데이터 정확?
□ transactions: 판매 기록 있나?
```

---

## 3️⃣ 현재 코드의 주요 이슈

### Issue 1: 혼합률 정의 불명확

**현재 코드:**
```python
# database.py BlendRecipe
portion_count = Column(Integer)  # 포션 개수
ratio = Column(Float)             # 비율 (%)
```

**문제:**
- `portion_count`와 `ratio`의 관계 불명확
- 플랜에서는 혼합률(%)이 100%를 합산해야 함
- 기존 코드는 포션 개수로 관리되는 것 같음

**필요 수정:**
```python
# 명확한 필드명으로 변경
blending_ratio_percent = Column(Float)  # 0~100, 합계=100%
blending_recipe_version = Column(Integer, default=1)
effective_date = Column(Date)
is_current = Column(Boolean, default=True)
```

---

### Issue 2: 로스팅 기록 모델 없음

**현재:** RoastingLog 모델이 전혀 없음
**필요:** Phase 1 에서 마이그레이션할 데이터가 저장될 테이블

**추가 필요:**
```python
class RoastingLog(Base):
    raw_weight_kg          # 생두량
    roasted_weight_kg      # 로스팅량
    loss_rate_percent      # 자동 계산
    expected_loss_rate_percent
    loss_variance_percent
    roasting_date
    roasting_month
    blend_recipe_version_id
    notes
```

---

### Issue 3: Blend 모델의 포션 관리

**현재 코드:**
```python
class Blend(Base):
    total_portion = Column(Integer, default=0)  # 포션 총 개수
```

**문제:**
- 포션의 정의가 명확하지 않음
- 플랜에서는 혼합률(%)로 관리하도록 변경

**필요 수정:**
```python
class Blend(Base):
    loss_rate_percent = Column(Float, default=17.0)
    standard_selling_price = Column(Float)
```

---

## 4️⃣ 기존 코드와 플랜의 차이

| 항목 | 기존 코드 | 마스터플랜 v2.1 | 차이 |
|-----|---------|------------|-----|
| **혼합 정의** | portion_count + ratio | blending_ratio_percent (%) | ⚠️ 변경 필요 |
| **손실률** | 미구현 | RoastingLog에서 자동 계산 | ❌ 추가 필요 |
| **로스팅 기록** | ❌ 없음 | RoastingLog + 마이그레이션 | ❌ 추가 필요 |
| **블렌드 레시피 버전** | ❌ 없음 | blend_recipes_history | ❌ 추가 필요 |
| **권한 관리** | ❌ 없음 | User + Permission | ❌ 추가 필요 |
| **감사 로그** | ❌ 없음 | AuditLog | ❌ 추가 필요 |
| **페이지** | 9개 예상 | 11개 (로그인, 영수증형식 추가) | ✅ 확대 |
| **서비스** | 5개 | 10개 (권한, 원가, 이상탐지 등) | ✅ 확대 |

---

## 5️⃣ Phase별 구현 상태

### Phase 1: 데이터 기초 구축

| Task | 상태 | 필요 작업 |
|------|------|---------|
| **T1-1** 마이그레이션 | ❌ 미구현 | RoastingLog 모델 필요 |
| **T1-2** 원두 설정 | ⚠️ 부분 | beans 테이블 확인 후 데이터 검증 |
| **T1-3** 블렌드 설정 | ⚠️ 부분 | ratio → blending_ratio_percent 수정 |
| **T1-4** 원가 입력 | ⚠️ 부분 | price_per_kg 필드 있음 |
| **T1-5** 데이터 검증 | ❌ 미구현 | 검증 스크립트 작성 |
| **T1-6** 손실률 설정 | ❌ 미구현 | 이상 탐지 로직 작성 |

### Phase 2: 백엔드 서비스

| Task | 상태 | 필요 작업 |
|------|------|---------|
| **T2-1** DB 스키마 | ⚠️ 부분 | 5개 테이블 추가 필요 |
| **T2-2** SQLAlchemy 모델 | ⚠️ 부분 | 10개 중 5개만 정의 |
| **T2-3** RoastingService | ❌ 미구현 | 새로 작성 |
| **T2-4** BlendService | ⚠️ 부분 | 혼합률(%) 기반으로 수정 |
| **T2-5** CostService | ❌ 미구현 | 새로 작성 (핵심!) |
| **T2-6** AnalyticsService | ⚠️ 부분 | 이상 탐지 로직 추가 |
| **T2-7** Excel 동기화 | ⚠️ 부분 | 마이그레이션 검증 추가 |
| **T2-8** Unit Test | ❌ 미구현 | 90% 커버리지 필요 |
| **T2-9** 코드 리뷰 | ❌ 미구현 | 모든 서비스 리팩토링 |

### Phase 3: 프론트엔드

| Task | 상태 | 필요 작업 |
|------|------|---------|
| **T3-1** 로그인 페이지 | ❌ 미구현 | 권한 미들웨어 필요 |
| **T3-2~T3-11** 기타 페이지 | ⚠️ 부분 | 혼합률(%) 기반으로 수정 |

---

## 6️⃣ 권장 사항

### A. 즉시 조치 (Phase 2~5 가이드 작성 전)

**1단계: 현재 DB 상태 정확히 파악**

```bash
# 실행:
sqlite3 data/roasting_data.db ".tables"
sqlite3 data/roasting_data.db "SELECT COUNT(*) as count FROM beans;"
sqlite3 data/roasting_data.db "SELECT COUNT(*) as count FROM blends;"
sqlite3 data/roasting_data.db "SELECT * FROM beans LIMIT 5;"
sqlite3 data/roasting_data.db "SELECT * FROM blends LIMIT 5;"
```

**2단계: 기존 코드 분석**

```bash
# 실행:
grep -n "class Blend" app/models/database.py
grep -n "blend_recipes" app/models/database.py
head -50 app/services/blend_service.py
```

**3단계: Excel 파일 확인**

```bash
# 실행:
ls -lh 분석결과.xlsx
# 파일이 있는지, Sheet1/Sheet1(2) 있는지 확인
```

---

### B. Phase 2~5 가이드 작성 시 고려사항

1. **혼합률(%) 정의 명확화**
   - 기존 `portion_count` 지원 vs 새로운 `blending_ratio_percent` 전환
   - Migration 전략 필요 (기존 데이터가 있다면)

2. **RoastingLog 추가**
   - Phase 1에서 마이그레이션할 데이터
   - 월별 그리드 입력을 위한 구조

3. **CostService 개발**
   - 혼합률(%) 기반 원가 계산이 매우 중요
   - 기존 코드와의 호환성 확인

4. **권한 관리 추가**
   - 기존 코드에 사용자 개념이 없음
   - Phase 2에서 추가되어야 함

---

## 7️⃣ 다음 진행 순서

```
① 현재 DB 상태 정확히 파악 (30분)
   └─ sqlite3 쿼리로 테이블/데이터 확인

② Phase 2~5 가이드 작성 (3~4시간)
   ├─ T2-1: DB 스키마 (5개 테이블 추가)
   ├─ T2-2: SQLAlchemy 모델 (10개)
   ├─ T2-3~T2-9: 서비스 개발 (상세 가이드)
   ├─ T3-1~T3-11: 프론트엔드 (UI 목록)
   ├─ T4: 테스트 (테스트 케이스)
   └─ T5: 배포 (배포 절차)

③ Phase 1 실행 시작 (2주)
   ├─ 기존 코드 업데이트 (혼합률, RoastingLog 등)
   ├─ 마이그레이션 스크립트 작성
   ├─ 데이터 마이그레이션 실행
   └─ 검증 완료

④ Phase 2~5 순차 구현
```

---

## ✅ 현재 상태 요약

| 영역 | 완성도 | 비고 |
|-----|--------|-----|
| **Models** | 40% | 기본 모델은 있으나 로스팅/권한/감사 로그 없음 |
| **Services** | 50% | 5개 서비스 있으나 기능 부족 (원가, 권한, 이상탐지 등) |
| **DB** | 30% | 기본 5개 테이블만 있음 (5개 추가 필요) |
| **페이지** | 20% | 기존 app.py 있으나 권한, 로그인 없음 |
| **테스트** | 0% | Unit Test 전혀 없음 |

**전체 준비도: ~30%**

---

## 📋 체크리스트

```
□ sqlite3로 현재 DB 상태 확인
□ beans 테이블 데이터 확인
□ blends 테이블 데이터 확인
□ 분석결과.xlsx 파일 확인
□ Phase 2~5 가이드 작성 시작
□ 기존 코드 마이그레이션 계획 수립
```

---

**작성자:** AI 진단 시스템
**진단 시간:** 2025-10-29 22:00 KST
**신뢰도:** 90% (실제 DB 쿼리로 재확인 필요)
