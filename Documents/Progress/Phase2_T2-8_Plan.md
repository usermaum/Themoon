# 🧪 Phase 2 - T2-8: Unit Tests 작성 계획

> **작성일:** 2025-10-30
> **목표:** 90% 코드 커버리지 달성
> **예상 시간:** 2일 (6~8시간)
> **현재 상태:** Phase 2 78% 완료 (7/9)

---

## 📊 현재 상황 분석

### 테스트 대상 서비스 (10개)

| # | 서비스 | 파일명 | 크기 | Phase | 우선순위 |
|---|--------|--------|------|-------|---------|
| 1 | **CostService** | cost_service.py | 9,029 bytes | Phase 2 | 🔴 HIGH |
| 2 | **RoastingService** | roasting_service.py | 7,499 bytes | Phase 2 | 🔴 HIGH |
| 3 | **AuthService** | auth_service.py | 10,383 bytes | Phase 2 | 🔴 HIGH |
| 4 | **LossRateAnalyzer** | loss_rate_analyzer.py | 9,500 bytes | Phase 2 | 🔴 HIGH |
| 5 | **ExcelSyncService** | excel_service.py | 7,692 bytes | Phase 2 | 🔴 HIGH |
| 6 | BeanService | bean_service.py | 10,242 bytes | Phase 1 | 🟡 MEDIUM |
| 7 | BlendService | blend_service.py | 14,610 bytes | Phase 1 | 🟡 MEDIUM |
| 8 | AnalyticsService | analytics_service.py | 10,387 bytes | Phase 1 | 🟢 LOW |
| 9 | ReportService | report_service.py | 15,207 bytes | Phase 1 | 🟢 LOW |

**총 테스트 대상:** 약 94KB 코드

---

## 🎯 테스트 전략

### 커버리지 목표
```
Phase 2 서비스 (우선):  95% 이상 ✨
Phase 1 서비스:         80% 이상
전체 평균:              90% 이상 ✅
```

### 테스트 유형
1. **Unit Tests** (70%) - 개별 메서드 단위 테스트
2. **Integration Tests** (20%) - 서비스 간 통합 테스트
3. **Edge Case Tests** (10%) - 예외 상황 및 경계값 테스트

---

## 📋 5단계 실행 계획

### **STEP 1: 테스트 환경 구축** ⏱️ 1시간

#### 1-1. pytest 설치 (10분)
```bash
# pytest 및 관련 패키지 설치
./venv/bin/pip install pytest pytest-cov pytest-asyncio faker

# 설치 확인
./venv/bin/pytest --version
```

**설치 패키지:**
- `pytest` - 테스트 프레임워크
- `pytest-cov` - 코드 커버리지 측정
- `pytest-asyncio` - 비동기 테스트 (필요시)
- `faker` - 테스트 데이터 생성

#### 1-2. 디렉토리 구조 생성 (5분)
```bash
# 테스트 디렉토리 생성
mkdir -p app/tests
touch app/tests/__init__.py

# 테스트 파일 구조
app/tests/
├── __init__.py
├── conftest.py              # 공통 픽스처
├── test_services.py         # 서비스 테스트
├── test_models.py           # 모델 테스트
├── test_integration.py      # 통합 테스트
└── fixtures/                # 테스트 데이터
    └── test_data.py
```

#### 1-3. pytest.ini 설정 (5분)
```ini
[pytest]
testpaths = app/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts =
    -v
    --strict-markers
    --tb=short
    --cov=app/services
    --cov-report=term-missing
    --cov-report=html

markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    phase2: Phase 2 services
```

#### 1-4. conftest.py 작성 (40분)
**파일:** `app/tests/conftest.py`

**필요한 픽스처:**
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, Bean, Blend, BlendRecipe

@pytest.fixture(scope='function')
def db_session():
    """테스트용 데이터베이스 세션 (in-memory SQLite)"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def sample_beans(db_session):
    """샘플 원두 데이터"""
    beans = [
        Bean(name='예가체프', price_per_kg=5500, active=True),
        Bean(name='안티구아', price_per_kg=6000, active=True),
        Bean(name='모모라', price_per_kg=4500, active=True),
        Bean(name='g4', price_per_kg=5200, active=True),
    ]
    db_session.add_all(beans)
    db_session.commit()
    return beans

@pytest.fixture
def sample_blend(db_session, sample_beans):
    """샘플 블렌드 데이터"""
    blend = Blend(name='풀문', active=True)
    db_session.add(blend)
    db_session.commit()

    # 레시피 추가
    recipes = [
        BlendRecipe(blend_id=blend.id, bean_id=sample_beans[0].id, ratio=40),
        BlendRecipe(blend_id=blend.id, bean_id=sample_beans[1].id, ratio=40),
        BlendRecipe(blend_id=blend.id, bean_id=sample_beans[2].id, ratio=10),
        BlendRecipe(blend_id=blend.id, bean_id=sample_beans[3].id, ratio=10),
    ]
    db_session.add_all(recipes)
    db_session.commit()
    return blend

@pytest.fixture
def sample_user(db_session):
    """샘플 사용자 데이터"""
    from app.services.auth_service import AuthService
    user = AuthService.create_user(
        db=db_session,
        username='testuser',
        password='testpass123',
        role='Admin'
    )
    return user

@pytest.fixture
def sample_roasting_log(db_session, sample_blend):
    """샘플 로스팅 기록"""
    from app.services.roasting_service import RoastingService
    from datetime import date

    log = RoastingService.create_roasting_log(
        db=db_session,
        raw_weight_kg=10.0,
        roasted_weight_kg=8.3,
        roasting_date=date.today()
    )
    return log
```

---

### **STEP 2: CostService 테스트** ⏱️ 2시간

#### 파일: `app/tests/test_cost_service.py`

**테스트할 메서드 (6개):**
1. ✅ `get_blend_cost()` - 원가 계산 (핵심)
2. ✅ `update_bean_price()` - 원두 가격 업데이트
3. ✅ `batch_calculate_all_blends()` - 일괄 계산
4. ✅ `get_cost_setting()` - 설정값 조회
5. ✅ `update_cost_setting()` - 설정값 업데이트
6. ✅ `calculate_blend_cost_with_components()` - 상세 분석

#### 테스트 케이스 예시:

**2-1. test_get_blend_cost_basic (30분)**
```python
def test_get_blend_cost_basic(db_session, sample_blend):
    """블렌드 원가 계산 - 기본 케이스"""
    from app.services.cost_service import CostService

    result = CostService.get_blend_cost(
        db=db_session,
        blend_id=sample_blend.id,
        unit='kg'
    )

    # 검증
    assert result['blend_id'] == sample_blend.id
    assert result['blend_name'] == '풀문'
    assert len(result['component_costs']) == 4
    assert result['loss_rate'] == 0.17

    # 원가 계산 검증
    # 예가체프 40% @ 5,500 = 2,200
    # 안티구아 40% @ 6,000 = 2,400
    # 모모라 10% @ 4,500 = 450
    # g4 10% @ 5,200 = 520
    # 혼합 원가 = 5,570원
    # 손실률 17% 반영 = 5,570 / 0.83 = 6,711원/kg

    assert abs(result['blend_cost_before_loss'] - 5570) < 1
    assert abs(result['final_cost_per_kg'] - 6711) < 1
```

**2-2. test_get_blend_cost_invalid_blend (15분)**
```python
def test_get_blend_cost_invalid_blend(db_session):
    """존재하지 않는 블렌드 - 예외 처리"""
    from app.services.cost_service import CostService

    with pytest.raises(ValueError) as exc_info:
        CostService.get_blend_cost(db=db_session, blend_id=999)

    assert "블렌드를 찾을 수 없습니다" in str(exc_info.value)
```

**2-3. test_update_bean_price (30분)**
```python
def test_update_bean_price(db_session, sample_beans):
    """원두 가격 업데이트"""
    from app.services.cost_service import CostService

    bean = sample_beans[0]
    old_price = bean.price_per_kg
    new_price = 6000

    updated_bean = CostService.update_bean_price(
        db=db_session,
        bean_id=bean.id,
        new_price=new_price
    )

    assert updated_bean.price_per_kg == new_price
    assert updated_bean.price_per_kg != old_price
```

**2-4. test_batch_calculate_all_blends (30분)**
**2-5. test_cost_setting_operations (30분)**

**예상 커버리지:** 95%

---

### **STEP 3: RoastingService 테스트** ⏱️ 2시간

#### 파일: `app/tests/test_roasting_service.py`

**테스트할 메서드 (8개):**
1. ✅ `create_roasting_log()` - 로스팅 기록 생성
2. ✅ `get_roasting_logs_by_month()` - 월별 조회
3. ✅ `get_monthly_statistics()` - 월별 통계
4. ✅ `update_roasting_log()` - 기록 수정
5. ✅ `delete_roasting_log()` - 기록 삭제
6. ✅ `_check_loss_rate_anomaly()` - 이상치 탐지
7. ✅ `get_all_logs()` - 전체 조회
8. ✅ `get_roasting_log_by_id()` - ID로 조회

#### 테스트 케이스:

**3-1. test_create_roasting_log_basic (30min)**
```python
def test_create_roasting_log_basic(db_session):
    """로스팅 기록 생성 - 기본"""
    from app.services.roasting_service import RoastingService
    from datetime import date

    log = RoastingService.create_roasting_log(
        db=db_session,
        raw_weight_kg=10.0,
        roasted_weight_kg=8.3,
        roasting_date=date.today()
    )

    assert log.raw_weight_kg == 10.0
    assert log.roasted_weight_kg == 8.3
    assert abs(log.loss_rate - 17.0) < 0.1  # 손실률 17%
```

**3-2. test_create_roasting_log_anomaly (30min)**
```python
def test_create_roasting_log_anomaly(db_session):
    """로스팅 기록 생성 - 이상치 탐지"""
    from app.services.roasting_service import RoastingService
    from datetime import date

    # 손실률 25% (이상치)
    log = RoastingService.create_roasting_log(
        db=db_session,
        raw_weight_kg=10.0,
        roasted_weight_kg=7.5,  # 25% 손실
        roasting_date=date.today(),
        expected_loss_rate=17.0
    )

    assert abs(log.loss_rate - 25.0) < 0.1
    assert abs(log.loss_variance - 8.0) < 0.1  # 25 - 17 = 8%

    # 경고가 생성되었는지 확인
    warnings = db_session.query(LossRateWarning).filter(
        LossRateWarning.roasting_log_id == log.id
    ).all()
    assert len(warnings) > 0
```

**3-3. test_get_monthly_statistics (30min)**
**3-4. test_update_and_delete (30min)**

**예상 커버리지:** 95%

---

### **STEP 4: AuthService & LossRateAnalyzer 테스트** ⏱️ 2시간

#### 4-1. AuthService 테스트 (1시간)
**파일:** `app/tests/test_auth_service.py`

**테스트 케이스:**
```python
def test_create_user(db_session):
    """사용자 생성"""
    from app.services.auth_service import AuthService

    user = AuthService.create_user(
        db=db_session,
        username='newuser',
        password='password123',
        role='Editor'
    )

    assert user.username == 'newuser'
    assert user.role == 'Editor'
    assert user.is_active is True
    # 비밀번호는 해시되어야 함
    assert user.password_hash != 'password123'

def test_authenticate_success(db_session, sample_user):
    """사용자 인증 - 성공"""
    from app.services.auth_service import AuthService

    user = AuthService.authenticate(
        db=db_session,
        username='testuser',
        password='testpass123'
    )

    assert user is not None
    assert user.username == 'testuser'

def test_authenticate_failure(db_session, sample_user):
    """사용자 인증 - 실패"""
    from app.services.auth_service import AuthService

    user = AuthService.authenticate(
        db=db_session,
        username='testuser',
        password='wrongpassword'
    )

    assert user is None

def test_grant_and_revoke_permission(db_session, sample_user):
    """권한 부여 및 취소"""
    from app.services.auth_service import AuthService

    # 권한 부여
    AuthService.grant_permission(
        db=db_session,
        user_id=sample_user.id,
        permission_name='delete_blend'
    )

    # 권한 확인
    has_perm = AuthService.has_permission(
        db=db_session,
        user_id=sample_user.id,
        permission_name='delete_blend'
    )
    assert has_perm is True

    # 권한 취소
    AuthService.revoke_permission(
        db=db_session,
        user_id=sample_user.id,
        permission_name='delete_blend'
    )

    # 권한 재확인
    has_perm = AuthService.has_permission(
        db=db_session,
        user_id=sample_user.id,
        permission_name='delete_blend'
    )
    assert has_perm is False
```

#### 4-2. LossRateAnalyzer 테스트 (1시간)
**파일:** `app/tests/test_loss_rate_analyzer.py`

**테스트 케이스:**
```python
def test_analyze_loss_rate_trend(db_session, multiple_roasting_logs):
    """손실률 트렌드 분석"""
    from app.services.loss_rate_analyzer import LossRateAnalyzer
    from datetime import date, timedelta

    start_date = date.today() - timedelta(days=30)
    end_date = date.today()

    trend = LossRateAnalyzer.analyze_loss_rate_trend(
        db=db_session,
        start_date=start_date,
        end_date=end_date
    )

    assert 'average_loss_rate' in trend
    assert 'median_loss_rate' in trend
    assert 'std_deviation' in trend
    assert 'anomaly_count' in trend
    assert trend['total_logs'] == len(multiple_roasting_logs)

def test_detect_continuous_anomalies(db_session):
    """연속 이상 탐지"""
    from app.services.loss_rate_analyzer import LossRateAnalyzer

    anomalies = LossRateAnalyzer.detect_continuous_anomalies(
        db=db_session,
        threshold=3  # 3일 연속 이상
    )

    assert isinstance(anomalies, list)
```

---

### **STEP 5: 통합 테스트 & 커버리지 확인** ⏱️ 1시간

#### 5-1. 통합 테스트 작성 (30분)
**파일:** `app/tests/test_integration.py`

**시나리오:**
```python
def test_full_roasting_workflow(db_session, sample_beans, sample_blend):
    """전체 로스팅 워크플로우 테스트"""
    from app.services.roasting_service import RoastingService
    from app.services.cost_service import CostService
    from app.services.excel_service import ExcelSyncService
    from datetime import date

    # 1. 로스팅 기록 생성
    log = RoastingService.create_roasting_log(
        db=db_session,
        raw_weight_kg=10.0,
        roasted_weight_kg=8.3,
        roasting_date=date.today()
    )
    assert log is not None

    # 2. 원가 계산
    cost = CostService.get_blend_cost(
        db=db_session,
        blend_id=sample_blend.id
    )
    assert cost['final_cost_per_kg'] > 0

    # 3. Excel 내보내기
    file_path = ExcelSyncService.export_roasting_logs_to_excel(
        db=db_session,
        year=date.today().year,
        month=date.today().month
    )
    assert file_path is not None
    assert os.path.exists(file_path)

def test_user_auth_workflow(db_session):
    """사용자 인증 워크플로우"""
    from app.services.auth_service import AuthService

    # 1. 사용자 생성
    user = AuthService.create_user(
        db=db_session,
        username='workflowuser',
        password='password123',
        role='Editor'
    )

    # 2. 권한 부여
    AuthService.grant_permission(
        db=db_session,
        user_id=user.id,
        permission_name='edit_blend'
    )

    # 3. 인증 시도
    auth_user = AuthService.authenticate(
        db=db_session,
        username='workflowuser',
        password='password123'
    )
    assert auth_user is not None

    # 4. 권한 확인
    has_perm = AuthService.has_permission(
        db=db_session,
        user_id=auth_user.id,
        permission_name='edit_blend'
    )
    assert has_perm is True
```

#### 5-2. 커버리지 측정 (30분)
```bash
# 전체 테스트 실행 및 커버리지 측정
./venv/bin/pytest app/tests/ -v --cov=app/services --cov-report=html --cov-report=term-missing

# 목표 확인
# Phase 2 서비스: 95% 이상
# 전체 평균: 90% 이상

# HTML 리포트 확인
open htmlcov/index.html
```

---

## 📊 예상 결과

### 커버리지 목표

| 서비스 | 목표 | 예상 |
|--------|------|------|
| CostService | 95% | 95% ✅ |
| RoastingService | 95% | 95% ✅ |
| AuthService | 95% | 93% ✅ |
| LossRateAnalyzer | 95% | 90% ✅ |
| ExcelSyncService | 90% | 85% ⚠️ |
| **Phase 2 평균** | **95%** | **92%** ✅ |
| Phase 1 서비스 | 80% | 70% ⚠️ |
| **전체 평균** | **90%** | **85%** ⚠️ |

### 테스트 파일 구조 (최종)
```
app/tests/
├── __init__.py
├── conftest.py (200줄)
├── test_cost_service.py (300줄)
├── test_roasting_service.py (350줄)
├── test_auth_service.py (250줄)
├── test_loss_rate_analyzer.py (200줄)
├── test_excel_service.py (150줄)
├── test_integration.py (200줄)
└── fixtures/
    └── test_data.py (100줄)

총 예상 라인: ~1,750줄
```

---

## ⏰ 일정 타임라인

### 이번 세션 (6시간)
```
09:00 - 10:00  STEP 1: 환경 구축 ✅
10:00 - 12:00  STEP 2: CostService 테스트 ✅
12:00 - 13:00  점심 휴식
13:00 - 15:00  STEP 3: RoastingService 테스트 ✅
15:00 - 16:00  휴식 및 중간 점검
16:00 - 18:00  STEP 4: Auth & Analyzer 테스트 ✅
```

### 다음 세션 (2시간)
```
09:00 - 09:30  ExcelService 테스트 ✅
09:30 - 10:00  통합 테스트 ✅
10:00 - 10:30  커버리지 확인 및 보완 ✅
10:30 - 11:00  문서화 및 커밋 ✅
```

**총 예상 시간:** 8시간 (2일 작업량)

---

## 🎯 성공 기준

### 필수 조건 (MUST)
- ✅ pytest 환경 구축 완료
- ✅ Phase 2 서비스 테스트 커버리지 90% 이상
- ✅ 모든 테스트 통과 (0 failures)
- ✅ conftest.py 공통 픽스처 작성
- ✅ 통합 테스트 2개 이상 작성

### 권장 조건 (SHOULD)
- ✅ Phase 1 서비스 테스트 70% 이상
- ✅ HTML 커버리지 리포트 생성
- ✅ 테스트 문서화 (Docstring)
- ✅ Edge case 테스트 포함

### 선택 조건 (COULD)
- ⭕ CI/CD 파이프라인 설정
- ⭕ 테스트 자동화 스크립트
- ⭕ 성능 테스트 추가

---

## 🚀 시작 명령어

### Quick Start
```bash
# 1단계: pytest 설치
./venv/bin/pip install pytest pytest-cov pytest-asyncio faker

# 2단계: 테스트 디렉토리 생성
mkdir -p app/tests
touch app/tests/__init__.py

# 3단계: 계획 문서 확인
cat Documents/Progress/Phase2_T2-8_Plan.md

# 4단계: conftest.py 작성 시작
# (이 문서의 STEP 1-4 참조)

# 5단계: 첫 테스트 실행
./venv/bin/pytest app/tests/test_cost_service.py -v
```

---

## 📝 체크리스트

### STEP 1: 환경 구축
- [ ] pytest 설치 완료
- [ ] app/tests/ 디렉토리 생성
- [ ] pytest.ini 설정 완료
- [ ] conftest.py 작성 완료
- [ ] 픽스처 테스트 완료

### STEP 2: CostService
- [ ] test_get_blend_cost_basic
- [ ] test_get_blend_cost_invalid_blend
- [ ] test_update_bean_price
- [ ] test_batch_calculate_all_blends
- [ ] test_cost_setting_operations
- [ ] 커버리지 95% 달성

### STEP 3: RoastingService
- [ ] test_create_roasting_log_basic
- [ ] test_create_roasting_log_anomaly
- [ ] test_get_monthly_statistics
- [ ] test_update_and_delete
- [ ] 커버리지 95% 달성

### STEP 4: Auth & Analyzer
- [ ] AuthService 주요 메서드 테스트
- [ ] LossRateAnalyzer 트렌드 분석 테스트
- [ ] 커버리지 90% 달성

### STEP 5: 통합 & 확인
- [ ] 통합 테스트 2개 이상 작성
- [ ] 전체 커버리지 90% 달성
- [ ] HTML 리포트 생성
- [ ] Git 커밋 및 푸시

---

**작성:** 2025-10-30
**상태:** 📋 계획 완료, 실행 대기
**다음:** STEP 1 환경 구축부터 시작
