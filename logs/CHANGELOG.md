# 변경 로그 (Changelog)

모든 주목할 만한 프로젝트 변경사항은 이 파일에 문서화됩니다.

## 버전 관리 규칙 (Semantic Versioning)

- **MAJOR.MINOR.PATCH** 형식 사용
  - MAJOR: 대규모 기능 추가 또는 호환성 깨지는 변경
  - MINOR: 새로운 기능 추가 (하위 호환성 유지)
  - PATCH: 버그 수정 (하위 호환성 유지)

---

## [0.9.0] - 2025-11-01

### ✨ 테스트: Phase 1 서비스 테스트 추가 - 103개 테스트 작성

#### 📝 변경사항

**전체 테스트 통계**
- 총 103개 테스트 작성 (100% 통과율)
- Phase 1 서비스 평균 커버리지: 90% (목표 88% 초과 달성)
- 테스트 실행 시간: ~11초

**Phase 1 서비스별 테스트 현황**

1. **BeanService 테스트** (35개 테스트, 커버리지 91%)
   - CRUD 작업 (생성, 조회, 수정, 삭제)
   - 조회 메서드 (ID, No, Name, Country, RoastLevel 등)
   - 비즈니스 로직 (재고 자동 생성, 소프트/하드 삭제)
   - 분석 기능 (요약 통계, 자주 사용되는 원두)
   - 초기화 및 내보내기

2. **BlendService 테스트** (39개 테스트, 커버리지 92%)
   - CRUD 작업 (블렌드 생성, 조회, 수정, 삭제)
   - 레시피 관리 (원두 추가/제거, 비율 재계산)
   - 원가 계산 (블렌드 원가, 제안 가격)
   - 분석 기능 (요약 통계)
   - 초기화 및 내보내기

3. **AnalyticsService 테스트** (14개 테스트, 커버리지 99%)
   - 트렌드 분석 (월별 거래 추이)
   - 재고 예측 및 사용량 예측
   - ROI 분석
   - 성능 지표
   - 원두별 효율성 분석
   - 블렌드 간 비교 분석

4. **ReportService 테스트** (15개 테스트, 커버리지 78%)
   - 월별 요약 데이터
   - 비용 분석
   - 원두 사용량 분석
   - 블렌드 성과 분석
   - Excel/CSV 내보내기

**수정된 버그 및 개선사항**

1. **blend_service.py 수정**
   - `add_recipe_to_blend()` 메서드의 `total_portion` 계산 로직 수정

2. **conftest.py 픽스처 개선**
   - `sample_blend`에 `total_portion` 명시적 설정 추가

3. **test_analytics_service.py 수정**
   - `Inventory` 픽스처에서 존재하지 않는 `location` 필드 제거

**생성된 파일**
- `app/tests/test_bean_service.py` (35개 테스트)
- `app/tests/test_blend_service.py` (39개 테스트)
- `app/tests/test_analytics_service.py` (14개 테스트)
- `app/tests/test_report_service.py` (15개 테스트)

**전체 프로젝트 테스트 현황**
- Phase 2 서비스: 85개 테스트 (커버리지 96.5%)
- Phase 1 서비스: 103개 테스트 (커버리지 90%)
- **총 188개 테스트** (100% 통과율)

---

## [0.9.0] - 2025-10-31

### ✨ 마이너 업데이트 (Minor Update): T2-8 Unit Tests 완료 - Phase 2 서비스 전체 테스트 구축

#### 📝 변경사항

**전체 테스트 통계**
- 총 85개 테스트 작성 (100% 통과율)
- Phase 2 서비스 평균 커버리지: 96.5% (목표 90% 초과 달성)
- 테스트 실행 시간: ~20초

**Phase 2 서비스별 테스트 현황**

1. **CostService 테스트** (15개 테스트, 커버리지 90%)
   - 블렌드 원가 계산 (기본, 컵 단위)
   - 원두 가격 업데이트 및 유효성 검증
   - 비용 설정 CRUD 작업
   - 일괄 계산 및 상세 분석
   - 경계값 테스트 (0 비율, 음수 가격)

2. **RoastingService 테스트** (21개 테스트, 커버리지 100%)
   - 로스팅 기록 CRUD 작업
   - 손실률 자동 계산 및 편차 검증
   - 월별 통계 및 조회
   - 이상치 탐지 (WARNING, CRITICAL, 연속 발생)
   - 통합 워크플로우 테스트

3. **AuthService 테스트** (25개 테스트, 커버리지 96%)
   - 사용자 생성 및 비밀번호 해싱 (passlib + bcrypt)
   - 인증 성공/실패 시나리오
   - 권한 부여/취소/확인 워크플로우
   - Admin 역할 특별 권한 검증
   - 비밀번호 변경 및 사용자 비활성화
   - 기본 권한 자동 할당

4. **LossRateAnalyzer 테스트** (16개 테스트, 커버리지 100%)
   - 손실률 트렌드 분석 (정상/주의/심각 상태)
   - 경고 생성/조회/해결 워크플로우
   - 월별 요약 통계
   - 연속 이상 탐지
   - 심각도별 분포 분석

5. **통합 테스트** (8개 테스트)
   - 완전한 로스팅 워크플로우 (기록 생성 → 이상 탐지 → 경고 해결)
   - 사용자 인증 및 권한 생명주기
   - 원가 계산 및 가격 업데이트 전파
   - 다중 사용자 동시 작업 시나리오

**수정된 버그 및 개선사항**

1. **conftest.py 픽스처 수정**
   - `BlendRecipe`에 `portion_count` 추가 (NOT NULL 제약 위반 해결)
   - `CostSetting` 픽스처를 단일 객체에서 리스트로 재구조화

2. **cost_service.py 개선**
   - `update_bean_price()`에 음수 가격 유효성 검증 추가

3. **roasting_service.py 수정**
   - 존재하지 않는 파라미터 제거 (`blend_recipe_version_id`, `operator_id`)

4. **bcrypt 버전 호환성 해결**
   - bcrypt 5.0.0 → 4.3.0 다운그레이드 (passlib 호환성)

**테스트 패턴 및 방법론**

- pytest 8.4.2 + pytest-cov 기반 테스트 프레임워크
- 인메모리 SQLite 데이터베이스를 사용한 격리된 테스트 환경
- Fixture 기반 테스트 데이터 관리
- 단위 테스트 + 통합 테스트 혼합 전략
- 경계값 테스트 및 예외 처리 검증
- @pytest.mark.integration 마커를 통한 테스트 분류

**다음 단계 (Phase 2 완료)**

- T2-8 Unit Tests 완료로 Phase 2 개발 완료
- Phase 2 진행률: 100% (T2-1 ~ T2-8 모두 완료)
- Phase 3 계획 수립 예정

## [0.8.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): T2-7 ExcelSyncService 개발 (Excel 동기화 및 마이그레이션)

#### 📝 변경사항

**ExcelSyncService 리팩토링**
- 정적 메서드 기반 설계로 전환
- 의존성 주입 패턴 적용
- 코드 라인 수: 526줄 → 204줄 (322줄 감소, 61% 최적화)

**주요 기능**

1. **export_roasting_logs_to_excel()**: 월별 로스팅 기록 Excel 내보내기
   - openpyxl을 사용한 프로페셔널 포맷팅
   - 헤더 스타일링 (굵게, 배경색, 정렬)
   - 컬럼 너비 자동 조정
   - 자동 파일 경로 생성

2. **validate_phase1_migration()**: Phase 1 마이그레이션 검증
   - 무게 유효성 확인 (양수값, NULL 체크)
   - 손실률 범위 검증 (0-50%)
   - 날짜 검증 (유효한 날짜)
   - 중복 데이터 탐지
   - 상세한 오류 리포팅 시스템

3. **get_migration_summary()**: 마이그레이션 요약 통계
   - 전체 데이터 통계
   - 총 무게 및 평균 손실률 계산
   - 마이그레이션 상태 보고

**특징**
- 로깅을 통한 상세한 추적
- 견고한 에러 핸들링
- 통계 계산 기능
- 유연한 파일 경로 관리

**파일**
- `app/services/excel_service.py`: 204 삽입(+), 322 삭제(-)

## [0.7.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): T2-6 LossRateAnalyzer 개발 (손실률 이상 탐지)

#### 📝 변경사항

**모델 개선**
- `RoastingLog`에 `warnings` 관계 추가
- `LossRateWarning`에 `roasting_log` 관계 추가
- 경고에서 로스팅 정보 직접 접근 가능

**LossRateAnalyzer 서비스 (310줄 신규 추가)**

1. **손실률 트렌드 분석**
   - `analyze_loss_rate_trend()`: 기간별 통계 분석
   - 평균, 중앙값, 표준편차 계산
   - 이상치 개수 및 비율 산출

2. **경고 관리**
   - `get_recent_warnings()`: 미해결 경고 조회
   - `resolve_warning()`: 경고 해결 처리
   - `detect_continuous_anomalies()`: 연속 이상 탐지

3. **추가 분석 기능**
   - `get_monthly_summary()`: 월별 요약
   - `get_severity_distribution()`: 심각도별 분포

**특징**
- 3% 경고 임계값 (ATTENTION)
- 5% 심각 임계값 (CRITICAL)
- NORMAL/ATTENTION/CRITICAL 상태 자동 판단
- 통계적 이상치 탐지
- 상세 로깅 시스템

**파일**
- `app/models/database.py`: 6 삽입(+)
- `app/services/loss_rate_analyzer.py`: 310 삽입(+) (신규)

## [0.6.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): T2-5 AuthService 개발 (인증 및 권한 관리)

#### 📝 변경사항

**AuthService 구현 (398줄 신규 추가)**

1. **사용자 인증 및 관리**
   - `create_user()`: 새 사용자 생성 + 기본 권한 자동 설정
   - `authenticate()`: 사용자 인증 (bcrypt 해시 검증)
   - `change_password()`: 비밀번호 변경 (보안 검증)
   - `deactivate_user()`: 사용자 비활성화

2. **권한 관리**
   - `grant_permission()`: 사용자에게 권한 부여
   - `revoke_permission()`: 사용자 권한 취소
   - `has_permission()`: 사용자 권한 확인
   - `get_user_permissions()`: 사용자의 모든 권한 조회

3. **사용자 조회**
   - `get_user_by_username()`: 사용자명으로 조회
   - `get_user_by_id()`: ID로 조회
   - `list_all_users()`: 모든 사용자 조회

**특징**
- bcrypt 해시 기반 보안 시스템
- Admin/Editor/Viewer 역할 기반 접근 제어 (RBAC)
- 마지막 로그인 자동 추적
- 기본 권한 자동 설정
- 상세한 감사 로그

**의존성 추가**
- `passlib==1.7.4`: 비밀번호 해싱
- `bcrypt==4.1.2`: 암호화

**파일**
- `app/services/auth_service.py`: 398 삽입(+) (신규)
- `requirements.txt`: 6 삽입(+), 1 삭제(-)

## [0.5.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): T2-4 CostService 개발 (핵심 비즈니스 로직)

#### 📝 변경사항

**CostService 구현 (277줄 신규 추가)**

1. **블렌드 원가 계산**
   - `get_blend_cost()`: 최종 원가 계산 (손실률 17% 반영)
   - 공식: `Final Cost = (Σ(Bean Cost × Ratio%)) / (1 - Loss Rate)`
   - 실제 비즈니스 로직 구현

2. **가격 관리**
   - `update_bean_price()`: 원두 가격 업데이트
   - 가격 이력 자동 저장 (BeanPriceHistory)
   - 타임스탬프 기반 가격 추적

3. **일괄 계산**
   - `batch_calculate_all_blends()`: 모든 블렌드 일괄 계산
   - 대량 처리 최적화
   - 계산 결과 요약 제공

4. **비용 설정 관리**
   - `get_cost_setting()`: 비용 설정값 조회
   - `update_cost_setting()`: 비용 설정값 업데이트
   - 손실률, 마진율 등 설정 관리

5. **상세 분석**
   - `calculate_blend_cost_with_components()`: 상세 원가 분석
   - 원두별 기여도 계산
   - 단위별 원가 (kg, cup)
   - 마진율 자동 계산

**특징**
- 17% 표준 손실률 적용
- 정확한 원가 계산 로직
- 상세 로깅 시스템
- 에러 핸들링

**파일**
- `app/services/cost_service.py`: 277 삽입(+) (신규)

## [0.4.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): Phase 2 T2-1, T2-2 완료 - DB 스키마 확장 및 모델 정의

#### 📝 변경사항

**T2-1: DB 스키마 설계 및 생성 ✅**

5개 새 테이블 생성 (직접 SQL 실행):
- `blend_recipes_history` (13 컬럼) - 레시피 버전 관리
- `users` (11 컬럼) - 사용자 관리
- `user_permissions` (6 컬럼) - 권한 관리
- `audit_logs` (10 컬럼) - 감사 로그
- `loss_rate_warnings` (10 컬럼) - 손실률 이상 경고

**DB 확장**: 8개 테이블 → 13개 테이블

**T2-2: SQLAlchemy 모델 추가 ✅**

6개 새 SQLAlchemy 모델 클래스 추가:
- `RoastingLog` (11 컬럼): 로스팅 기록
- `BlendRecipesHistory` (13 컬럼): 레시피 버전 이력
- `User` (11 컬럼): 사용자
- `UserPermission` (6 컬럼): 사용자 권한
- `AuditLog` (10 컬럼): 감사 로그
- `LossRateWarning` (10 컬럼): 손실률 경고

**모델 확장**: 6개 → 11개

**추가 수정**
- Boolean import 추가 (SQLAlchemy 타입 오류 해결)
- 관계(relationship) 설정
- 백업 생성: `backups/roasting_data_before_migration.db`

**진행율**
- Phase 2: 22% 완료 (2/9 태스크)
- 전체 프로젝트: 48% 완료

**파일**
- `Data/roasting_data.db`: 90KB → 139KB (54% 증가)
- `app/models/database.py`: 107 삽입(+)
- `Documents/Progress/Phase2진행상황_2025-10-29.md`: 339 삽입(+) (신규)
- `backups/`: 백업 파일 및 로스팅 메모 이미지 추가

## [0.3.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): Phase 1 완료 - 데이터 기초 구축 (v1.6.0)

#### 📝 변경사항
- 변경사항 상세 기록 필요

## [0.2.1] - 2025-10-29

### 🐛 패치 (Bug Fix): test_data.py 현재 데이터베이스 스키마에 맞게 수정

#### 📝 변경사항
1. **app/test_data.py** - 데이터베이스 스키마 업데이트
   - 이전 sqlite3 직접 사용 → SQLAlchemy ORM 사용으로 변경
   - bean_prices 테이블 참조 제거 (Bean 모델의 price_per_kg 사용)
   - roasting_logs 테이블 → transactions 테이블로 변경
   - 모델 import 경로 수정 (models.models → models)
   - Bean 상태값 "활성" → "active"로 수정

#### 📊 결과
- ✅ 60개의 테스트 거래 데이터 생성 완료
  - 입고 거래: 30개
  - 출고 거래: 30개
  - 마지막 30일 거래 기록 생성

## [0.2.0] - 2025-10-29

### ✨ 마이너 업데이트 (Minor Update): 3가지 기능 개선 적용

#### 📝 변경사항
1. **BlendManagement.py** - 레시피 편집 UI 추가
   - 기존 블렌드의 레시피 선택 및 수정 기능 추가 (Lines 455-520)
   - 원두와 포션 개수 수정 가능
   - 저장 및 삭제 버튼으로 레시피 관리 개선

2. **InventoryManagement.py** - 재고 범위 설정 커스터마이징
   - 최소/최대 재고량을 원두별로 설정 가능 (Lines 250-270)
   - 기본값 유지 (최소: 5.0kg, 최대: 50.0kg)
   - 입고 시 사용자 정의 범위 적용 (Lines 285-286)

3. **Settings.py** - 데이터 초기화 확인 로직 개선
   - 두 단계 확인 프로세스로 실수 방지 (Lines 467-507)
   - st.session_state를 통한 상태 관리
   - 명확한 경고 메시지와 취소 버튼 제공

## [0.1.0] - 2025-10-29

### 🎯 초기 버전

#### 📝 변경사항
- 프로젝트 시작: 버전 리셋 및 새로운 버전 관리 시스템 도입
- 효율적인 버전관리 전략 수립 (logs/VERSION_STRATEGY.md)
- 세션 관리 시스템 완성 (SESSION_START_CHECKLIST, SESSION_END_CHECKLIST)
- 작업 완료 후 처리 프로세스 명시

#### 🔄 버전 관리 개선
- PATCH/MINOR/MAJOR 누적 기준 명확화
- 모든 문서(README.md, CLAUDE.md) 버전 동기화 규칙 추가
- 버전 올리는 기준: PATCH(버그 3개+), MINOR(기능 3~4개+), MAJOR(호환성 변경)

#### 📚 문서화 완성
- logs/VERSION_STRATEGY.md 생성
- Documents/Progress/SESSION_SUMMARY_2025-10-29.md 생성
- CLAUDE.md에 "⚡ 빠른 버전 관리 참고" 섹션 추가
- SESSION_END_CHECKLIST.md 상세화

---

## 🎯 향후 버전 계획

```
현재: 0.1.0 (초기 버전)
  ↓
2주 후: 0.1.1 (버그 수정 3개)
4주 후: 0.1.2 (문서 개선 5개)
6주 후: 0.2.0 (새 기능 3~4개) ← MINOR
8주 후: 0.2.1 (버그 수정 2개)
12주 후: 1.0.0 (프로덕션 배포) ← MAJOR
```

---

**마지막 업데이트**: 2025-10-29
