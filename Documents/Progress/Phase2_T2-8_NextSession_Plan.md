# 🚀 Phase 2 - T2-8: 다음 세션 상세 플랜

> **작성일:** 2025-10-30
> **현재 진행:** T2-8 10% 완료 (환경 구축 완료)
> **목표:** T2-8 완료 → 커버리지 90% 달성
> **예상 시간:** 6~8시간 (2~3 세션)

---

## 📊 현재 상태 점검

### ✅ 완료된 작업
```
✅ pytest 환경 구축 (pytest 8.4.2)
✅ conftest.py 작성 (9개 픽스처)
✅ test_cost_service.py 작성 (15개 테스트)
✅ 버전 0.9.0 업데이트
✅ Git 커밋 & 푸시
```

### ⏳ 남은 작업
```
🔄 CostService 테스트 수정 (메서드 시그니처 맞추기)
⏳ RoastingService 테스트 작성 (8개 메서드)
⏳ AuthService 테스트 작성 (11개 메서드)
⏳ LossRateAnalyzer 테스트 작성 (7개 메서드)
⏳ ExcelService 테스트 작성 (3개 메서드)
⏳ 통합 테스트 작성
⏳ 커버리지 90% 달성
```

### 📈 커버리지 현황
```
현재: 8% (전체 서비스)
목표: 90%
필요: 82% 증가
```

---

## 🎯 실제 서비스 메서드 분석 (Phase 2)

### **CostService** (6개 메서드)
```python
1. get_blend_cost(db, blend_id, unit='kg', use_current_recipes=True)
   → 블렌드 원가 계산 (핵심)

2. update_bean_price(db, bean_id, new_price)
   → 원두 가격 업데이트

3. batch_calculate_all_blends(db)
   → 모든 블렌드 일괄 계산

4. get_cost_setting(db, parameter_name)  ⚠️ 수정 필요
   → 비용 설정 조회 (파라미터 필요)

5. update_cost_setting(db, parameter_name, value, description=None)  ⚠️ 수정 필요
   → 비용 설정 업데이트 (파라미터 필요)

6. calculate_blend_cost_with_components(db, blend_id)
   → 상세 원가 분석
```

### **RoastingService** (8개 메서드)
```python
1. create_roasting_log(db, raw_weight_kg, roasted_weight_kg, roasting_date, ...)
   → 로스팅 기록 생성

2. get_roasting_logs_by_month(db, month)
   → 월별 로스팅 기록 조회

3. get_monthly_statistics(db, month)
   → 월별 통계

4. update_roasting_log(db, log_id, **kwargs)
   → 로스팅 기록 수정

5. delete_roasting_log(db, log_id)
   → 로스팅 기록 삭제

6. _check_loss_rate_anomaly(db, roasting_log)  [Private]
   → 손실률 이상 탐지 (자동 호출)

7. get_all_logs(db, limit=100)
   → 모든 로스팅 기록 조회

8. get_roasting_log_by_id(db, log_id)
   → ID로 로스팅 기록 조회
```

### **AuthService** (11개 메서드)
```python
1. create_user(db, username, password, email=None, full_name=None, role='viewer', department=None)
   → 사용자 생성

2. authenticate(db, username, password)
   → 사용자 인증

3. grant_permission(db, user_id, resource, action, granted_by)  ⚠️ 4개 파라미터
   → 권한 부여

4. revoke_permission(db, user_id, resource, action)
   → 권한 취소

5. has_permission(db, user_id, resource, action)
   → 권한 확인

6. get_user_permissions(db, user_id)
   → 사용자 권한 조회

7. change_password(db, user_id, old_password, new_password)
   → 비밀번호 변경

8. deactivate_user(db, user_id)
   → 사용자 비활성화

9. get_user_by_username(db, username)
   → 사용자명으로 조회

10. get_user_by_id(db, user_id)
    → ID로 조회

11. list_all_users(db, active_only=True)
    → 모든 사용자 조회
```

### **LossRateAnalyzer** (7개 메서드)
```python
1. analyze_loss_rate_trend(db, days=30)
   → 손실률 트렌드 분석

2. get_recent_warnings(db, limit=10)
   → 최근 미해결 경고 조회

3. resolve_warning(db, warning_id, notes=None)
   → 경고 해결 처리

4. get_loss_rate_by_bean(db, days=30)
   → 원두별 손실률 분석

5. get_monthly_summary(db, month)
   → 월별 요약

6. detect_continuous_anomalies(db, threshold=3)
   → 연속 이상 탐지

7. get_severity_distribution(db, days=30)
   → 심각도별 분포
```

---

## 📋 다음 세션 실행 계획 (6단계)

### **STEP 1: CostService 테스트 수정** ⏱️ 1시간

#### 1-1. conftest.py 수정 (15분)
**문제:** `sample_cost_setting` 픽스처가 CostSetting 모델 구조와 맞지 않음

```python
# 현재 (잘못됨):
cost_setting = CostSetting(
    loss_rate=17.0,
    margin_multiplier=2.5,
    roasting_cost_per_kg=500,
    ...
)

# 수정 필요:
# CostSetting은 parameter_name, value 구조로 작동
cost_settings = [
    CostSetting(parameter_name='loss_rate', value=17.0),
    CostSetting(parameter_name='margin_multiplier', value=2.5),
]
```

#### 1-2. test_cost_service.py 수정 (45분)
**수정할 테스트:**

1. `test_get_cost_setting()` 수정
```python
# 현재:
setting = CostService.get_cost_setting(db=db_session)

# 수정:
value = CostService.get_cost_setting(db=db_session, parameter_name='loss_rate')
assert value == 17.0
```

2. `test_update_cost_setting()` 수정
```python
# 수정:
setting = CostService.update_cost_setting(
    db=db_session,
    parameter_name='loss_rate',
    value=18.0,
    description='Updated loss rate'
)
```

3. 테스트 실행 및 검증
```bash
./venv/bin/pytest app/tests/test_cost_service.py -v
```

**목표:** CostService 테스트 15개 모두 통과

---

### **STEP 2: RoastingService 테스트 작성** ⏱️ 2시간

#### 파일 생성: `app/tests/test_roasting_service.py`

**테스트 케이스 (12개):**

```python
class TestRoastingService:
    """RoastingService 테스트"""

    # 1. 로스팅 기록 생성 테스트
    def test_create_roasting_log_basic(db_session):
        """기본 로스팅 기록 생성"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today()
        )
        assert log.raw_weight_kg == 10.0
        assert log.roasted_weight_kg == 8.3
        assert abs(log.loss_rate_percent - 17.0) < 0.1

    # 2. 손실률 계산 검증
    def test_loss_rate_calculation(db_session):
        """손실률 자동 계산 검증"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.0,  # 20% 손실
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )
        assert abs(log.loss_rate_percent - 20.0) < 0.1
        assert abs(log.loss_variance_percent - 3.0) < 0.1  # 20 - 17 = 3%

    # 3. 월별 조회 테스트
    def test_get_roasting_logs_by_month(db_session):
        """월별 로스팅 기록 조회"""
        # 여러 기록 생성
        for i in range(5):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                roasting_date=date.today()
            )

        month = date.today().strftime('%Y-%m')
        logs = RoastingService.get_roasting_logs_by_month(db_session, month)
        assert len(logs) == 5

    # 4. 월별 통계 테스트
    def test_get_monthly_statistics(db_session):
        """월별 통계 계산"""
        # 기록 생성
        RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today()
        )

        month = date.today().strftime('%Y-%m')
        stats = RoastingService.get_monthly_statistics(db_session, month)

        assert stats['total_logs'] == 1
        assert stats['total_raw_weight_kg'] == 10.0
        assert abs(stats['avg_loss_rate_percent'] - 17.0) < 0.1

    # 5. 로스팅 기록 수정
    def test_update_roasting_log(db_session):
        """로스팅 기록 수정"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today()
        )

        updated = RoastingService.update_roasting_log(
            db=db_session,
            log_id=log.id,
            notes='Updated notes'
        )

        assert updated.notes == 'Updated notes'

    # 6. 로스팅 기록 삭제
    def test_delete_roasting_log(db_session):
        """로스팅 기록 삭제"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today()
        )

        result = RoastingService.delete_roasting_log(db_session, log.id)
        assert result is True

        # 삭제 확인
        deleted = RoastingService.get_roasting_log_by_id(db_session, log.id)
        assert deleted is None

    # 7. 전체 조회
    def test_get_all_logs(db_session):
        """모든 로스팅 기록 조회"""
        # 3개 생성
        for i in range(3):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=8.3,
                roasting_date=date.today()
            )

        logs = RoastingService.get_all_logs(db_session, limit=10)
        assert len(logs) == 3

    # 8. ID로 조회
    def test_get_roasting_log_by_id(db_session):
        """ID로 로스팅 기록 조회"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=8.3,
            roasting_date=date.today()
        )

        found = RoastingService.get_roasting_log_by_id(db_session, log.id)
        assert found is not None
        assert found.id == log.id

    # 9. 이상치 자동 탐지
    def test_anomaly_detection(db_session):
        """손실률 이상치 자동 탐지"""
        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=10.0,
            roasted_weight_kg=7.0,  # 30% 손실 (이상치)
            roasting_date=date.today(),
            expected_loss_rate=17.0
        )

        # 경고 생성 확인
        warnings = db_session.query(LossRateWarning).filter(
            LossRateWarning.roasting_log_id == log.id
        ).all()

        assert len(warnings) > 0
        assert warnings[0].severity == 'CRITICAL'  # 13% 편차 → CRITICAL

    # 10. 예외 처리: 존재하지 않는 ID 수정
    def test_update_nonexistent_log(db_session):
        """존재하지 않는 로스팅 기록 수정 - 예외"""
        with pytest.raises(ValueError):
            RoastingService.update_roasting_log(db_session, log_id=999, notes='test')

    # 11. 예외 처리: 음수 무게
    def test_negative_weight(db_session):
        """음수 무게 - 예외 또는 정상 처리"""
        # 서비스가 음수를 받아들이는지 확인
        # 필요시 예외 처리 추가
        pass

    # 12. 빈 데이터 월별 통계
    def test_empty_monthly_statistics(db_session):
        """데이터 없는 월의 통계"""
        stats = RoastingService.get_monthly_statistics(db_session, '2020-01')
        assert stats['count'] == 0
        assert stats['status'] == '데이터 없음'
```

**예상 커버리지:** RoastingService 95%

---

### **STEP 3: AuthService 테스트 작성** ⏱️ 1.5시간

#### 파일 생성: `app/tests/test_auth_service.py`

**테스트 케이스 (15개):**

```python
class TestAuthService:
    """AuthService 테스트"""

    # 1. 사용자 생성
    def test_create_user_basic(db_session):
        """기본 사용자 생성"""
        user = AuthService.create_user(
            db=db_session,
            username='testuser',
            password='password123',
            role='editor'
        )
        assert user.username == 'testuser'
        assert user.role == 'editor'
        assert user.is_active is True
        # 비밀번호는 해시되어야 함
        assert user.password_hash != 'password123'

    # 2. 중복 사용자명 예외
    def test_create_duplicate_user(db_session):
        """중복 사용자명 - 예외"""
        AuthService.create_user(db_session, 'testuser', 'password123')

        with pytest.raises(ValueError) as exc:
            AuthService.create_user(db_session, 'testuser', 'password123')
        assert '이미 존재하는 사용자명' in str(exc.value)

    # 3. 인증 성공
    def test_authenticate_success(db_session):
        """인증 성공"""
        AuthService.create_user(db_session, 'testuser', 'password123')

        user = AuthService.authenticate(db_session, 'testuser', 'password123')
        assert user is not None
        assert user.username == 'testuser'

    # 4. 인증 실패 - 잘못된 비밀번호
    def test_authenticate_wrong_password(db_session):
        """인증 실패 - 잘못된 비밀번호"""
        AuthService.create_user(db_session, 'testuser', 'password123')

        user = AuthService.authenticate(db_session, 'testuser', 'wrongpass')
        assert user is None

    # 5. 인증 실패 - 존재하지 않는 사용자
    def test_authenticate_nonexistent_user(db_session):
        """인증 실패 - 존재하지 않는 사용자"""
        user = AuthService.authenticate(db_session, 'nonexistent', 'password')
        assert user is None

    # 6. 권한 부여
    def test_grant_permission(db_session):
        """권한 부여"""
        user = AuthService.create_user(db_session, 'testuser', 'password123')

        perm = AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='write',
            granted_by=user.id
        )

        assert perm.resource == 'blends'
        assert perm.action == 'write'

    # 7. 권한 확인
    def test_has_permission(db_session):
        """권한 확인"""
        user = AuthService.create_user(db_session, 'testuser', 'password123')

        AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete',
            granted_by=user.id
        )

        has_perm = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete'
        )

        assert has_perm is True

    # 8. 권한 취소
    def test_revoke_permission(db_session):
        """권한 취소"""
        user = AuthService.create_user(db_session, 'testuser', 'password123')

        AuthService.grant_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete',
            granted_by=user.id
        )

        AuthService.revoke_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete'
        )

        has_perm = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='delete'
        )

        assert has_perm is False

    # 9. 사용자 권한 조회
    def test_get_user_permissions(db_session):
        """사용자 권한 조회"""
        user = AuthService.create_user(db_session, 'testuser', 'password123')

        perms = AuthService.get_user_permissions(db_session, user.id)
        # 기본 권한 3개 (blends:read, beans:read, roasting_logs:read)
        assert len(perms) >= 3

    # 10. 비밀번호 변경
    def test_change_password(db_session):
        """비밀번호 변경"""
        user = AuthService.create_user(db_session, 'testuser', 'oldpass')

        result = AuthService.change_password(
            db=db_session,
            user_id=user.id,
            old_password='oldpass',
            new_password='newpass'
        )

        assert result is True

        # 새 비밀번호로 인증 확인
        auth_user = AuthService.authenticate(db_session, 'testuser', 'newpass')
        assert auth_user is not None

    # 11. 사용자 비활성화
    def test_deactivate_user(db_session):
        """사용자 비활성화"""
        user = AuthService.create_user(db_session, 'testuser', 'password123')

        result = AuthService.deactivate_user(db_session, user.id)
        assert result is True

        # 비활성화된 사용자는 인증 불가
        auth_user = AuthService.authenticate(db_session, 'testuser', 'password123')
        assert auth_user is None

    # 12. 사용자명으로 조회
    def test_get_user_by_username(db_session):
        """사용자명으로 조회"""
        AuthService.create_user(db_session, 'testuser', 'password123')

        user = AuthService.get_user_by_username(db_session, 'testuser')
        assert user is not None
        assert user.username == 'testuser'

    # 13. ID로 조회
    def test_get_user_by_id(db_session):
        """ID로 조회"""
        created = AuthService.create_user(db_session, 'testuser', 'password123')

        user = AuthService.get_user_by_id(db_session, created.id)
        assert user is not None
        assert user.id == created.id

    # 14. 모든 사용자 조회
    def test_list_all_users(db_session):
        """모든 사용자 조회"""
        for i in range(3):
            AuthService.create_user(db_session, f'user{i}', 'password123')

        users = AuthService.list_all_users(db_session)
        assert len(users) == 3

    # 15. 기본 권한 자동 설정 확인
    def test_default_permissions(db_session):
        """기본 권한 자동 설정 확인"""
        user = AuthService.create_user(db_session, 'testuser', 'password123')

        # 기본 읽기 권한 확인
        has_blend_read = AuthService.has_permission(
            db=db_session,
            user_id=user.id,
            resource='blends',
            action='read'
        )
        assert has_blend_read is True
```

**예상 커버리지:** AuthService 90%

---

### **STEP 4: LossRateAnalyzer 테스트 작성** ⏱️ 1시간

#### 파일 생성: `app/tests/test_loss_rate_analyzer.py`

**테스트 케이스 (10개):**

```python
class TestLossRateAnalyzer:
    """LossRateAnalyzer 테스트"""

    # 1. 트렌드 분석 - 정상
    def test_analyze_loss_rate_trend_normal(db_session, multiple_roasting_logs):
        """트렌드 분석 - 정상 상태"""
        trend = LossRateAnalyzer.analyze_loss_rate_trend(db_session, days=30)

        assert trend['data_count'] > 0
        assert 'avg_loss_rate' in trend
        assert trend['status'] in ['NORMAL', 'ATTENTION', 'CRITICAL']

    # 2. 트렌드 분석 - 데이터 없음
    def test_analyze_loss_rate_trend_no_data(db_session):
        """트렌드 분석 - 데이터 없음"""
        trend = LossRateAnalyzer.analyze_loss_rate_trend(db_session, days=30)

        assert trend['data_count'] == 0
        assert trend['status'] == 'NO_DATA'

    # 3. 최근 경고 조회
    def test_get_recent_warnings(db_session, sample_loss_rate_warning):
        """최근 미해결 경고 조회"""
        warnings = LossRateAnalyzer.get_recent_warnings(db_session, limit=10)

        assert len(warnings) > 0
        assert 'severity' in warnings[0]

    # 4. 경고 해결
    def test_resolve_warning(db_session, sample_loss_rate_warning):
        """경고 해결 처리"""
        resolved = LossRateAnalyzer.resolve_warning(
            db=db_session,
            warning_id=sample_loss_rate_warning.id,
            notes='Resolved by admin'
        )

        assert resolved.is_resolved is True
        assert resolved.resolved_notes == 'Resolved by admin'

    # 5. 월별 요약
    def test_get_monthly_summary(db_session, multiple_roasting_logs):
        """월별 요약"""
        month = date.today().strftime('%Y-%m')
        summary = LossRateAnalyzer.get_monthly_summary(db_session, month)

        assert 'total_logs' in summary
        assert 'avg_loss_rate' in summary

    # 6. 연속 이상 탐지
    def test_detect_continuous_anomalies(db_session):
        """연속 이상 탐지"""
        # 연속 이상 기록 생성
        from app.services.roasting_service import RoastingService

        for i in range(4):
            RoastingService.create_roasting_log(
                db=db_session,
                raw_weight_kg=10.0,
                roasted_weight_kg=7.0,  # 30% 손실 (이상)
                roasting_date=date.today() - timedelta(days=i),
                expected_loss_rate=17.0
            )

        anomalies = LossRateAnalyzer.detect_continuous_anomalies(
            db=db_session,
            threshold=3
        )

        assert len(anomalies) > 0

    # 7. 심각도별 분포
    def test_get_severity_distribution(db_session, multiple_roasting_logs):
        """심각도별 분포"""
        dist = LossRateAnalyzer.get_severity_distribution(db_session, days=30)

        assert 'NORMAL' in dist or 'WARNING' in dist or 'CRITICAL' in dist

    # ... (추가 테스트)
```

**예상 커버리지:** LossRateAnalyzer 85%

---

### **STEP 5: 통합 테스트 작성** ⏱️ 30분

#### 파일: `app/tests/test_integration.py`

```python
@pytest.mark.integration
class TestIntegration:
    """통합 테스트"""

    def test_full_roasting_workflow(db_session, sample_beans, sample_blend):
        """전체 로스팅 워크플로우"""
        # 1. 로스팅 기록 생성
        log = RoastingService.create_roasting_log(...)

        # 2. 원가 계산
        cost = CostService.get_blend_cost(...)

        # 3. 손실률 분석
        trend = LossRateAnalyzer.analyze_loss_rate_trend(...)

        assert log is not None
        assert cost['final_cost_per_kg'] > 0
        assert trend['data_count'] > 0
```

---

### **STEP 6: 커버리지 확인 및 보완** ⏱️ 1시간

```bash
# 전체 테스트 실행
./venv/bin/pytest app/tests/ -v --cov=app/services --cov-report=html

# 커버리지 확인
open htmlcov/index.html

# 목표 확인
# Phase 2 서비스: 90% 이상
# 전체 평균: 80% 이상
```

---

## 📅 일정 타임라인

### **세션 1 (3시간)**
```
09:00 - 10:00  STEP 1: CostService 수정
10:00 - 12:00  STEP 2: RoastingService 테스트
```

### **세션 2 (3시간)**
```
09:00 - 10:30  STEP 3: AuthService 테스트
10:30 - 11:30  STEP 4: LossRateAnalyzer 테스트
11:30 - 12:00  STEP 5: 통합 테스트
```

### **세션 3 (2시간)**
```
09:00 - 10:00  STEP 6: 커버리지 확인 및 보완
10:00 - 11:00  T2-9: 코드 리뷰 시작
11:00 - 12:00  문서화 및 최종 커밋
```

**총 예상 시간:** 8시간

---

## 🎯 성공 기준

### 필수 (MUST)
- ✅ CostService 커버리지 95%
- ✅ RoastingService 커버리지 95%
- ✅ AuthService 커버리지 90%
- ✅ LossRateAnalyzer 커버리지 85%
- ✅ 전체 Phase 2 서비스 평균 90%
- ✅ 모든 테스트 통과 (0 failures)

### 권장 (SHOULD)
- ✅ ExcelService 커버리지 80%
- ✅ 통합 테스트 5개 이상
- ✅ Edge case 테스트 포함
- ✅ HTML 커버리지 리포트 생성

### 선택 (COULD)
- ⭕ Phase 1 서비스 테스트 70%
- ⭕ 성능 테스트 추가
- ⭕ CI/CD 설정

---

## 🚀 빠른 시작 (다음 세션)

```bash
# 1. 세션 시작 체크리스트
cat Documents/Progress/SESSION_START_CHECKLIST.md

# 2. 이 플랜 확인
cat Documents/Progress/Phase2_T2-8_NextSession_Plan.md

# 3. STEP 1 시작: conftest.py 수정
vim app/tests/conftest.py

# 4. CostService 테스트 수정
vim app/tests/test_cost_service.py

# 5. 테스트 실행
./venv/bin/pytest app/tests/test_cost_service.py -v
```

---

## 📝 주의사항

### 🔧 수정 필요한 항목

**1. conftest.py**
- `sample_cost_setting`: CostSetting 모델 구조 확인 후 수정

**2. test_cost_service.py**
- `test_get_cost_setting()`: parameter_name 추가
- `test_update_cost_setting()`: parameter_name 추가

**3. conftest.py - sample_user**
- AuthService.grant_permission() 호출 시 granted_by 파라미터 추가

### ⚠️ 테스트 작성 시 유의사항

1. **실제 메서드 시그니처 확인**: 각 서비스 파일 먼저 읽기
2. **픽스처 활용**: conftest.py의 픽스처 최대한 활용
3. **예외 처리 테스트**: ValueError, TypeError 등 검증
4. **경계값 테스트**: 음수, 0, 매우 큰 값 등
5. **통합 테스트**: 여러 서비스 연계 동작 검증

---

**작성:** 2025-10-30
**현재 버전:** v0.9.0
**목표 버전:** v1.0.0 (T2-8 완료 시)
**예상 완료:** 2~3 세션 후
