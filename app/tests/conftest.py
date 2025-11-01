"""
conftest.py: pytest 공통 픽스처 정의

테스트용 데이터베이스 세션 및 샘플 데이터를 제공합니다.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime, timedelta
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import (
    Base, Bean, Blend, BlendRecipe, CostSetting,
    User, UserPermission, RoastingLog, LossRateWarning
)


@pytest.fixture(scope='function')
def db_session():
    """
    테스트용 데이터베이스 세션 (in-memory SQLite)

    각 테스트마다 새로운 데이터베이스를 생성하고 테스트 후 삭제합니다.
    """
    # In-memory SQLite 엔진 생성
    engine = create_engine('sqlite:///:memory:', echo=False)

    # 모든 테이블 생성
    Base.metadata.create_all(engine)

    # 세션 생성
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # 테스트 후 세션 종료 및 정리
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_beans(db_session):
    """
    샘플 원두 데이터 (4개)

    - 예가체프: 5,500원/kg
    - 안티구아: 6,000원/kg
    - 모모라: 4,500원/kg
    - g4: 5,200원/kg
    """
    beans = [
        Bean(
            no=1,
            name='예가체프',
            country_code='ET',
            country_name='Ethiopia',
            roast_level='Medium',
            price_per_kg=5500,
            status='active'
        ),
        Bean(
            no=2,
            name='안티구아',
            country_code='GT',
            country_name='Guatemala',
            roast_level='Medium',
            price_per_kg=6000,
            status='active'
        ),
        Bean(
            no=3,
            name='모모라',
            country_code='BR',
            country_name='Brazil',
            roast_level='Medium',
            price_per_kg=4500,
            status='active'
        ),
        Bean(
            no=4,
            name='g4',
            country_code='BR',
            country_name='Brazil',
            roast_level='Medium',
            price_per_kg=5200,
            status='active'
        ),
    ]

    for bean in beans:
        db_session.add(bean)
    db_session.commit()

    # ID를 갱신하기 위해 refresh
    for bean in beans:
        db_session.refresh(bean)

    return beans


@pytest.fixture
def sample_blend(db_session, sample_beans):
    """
    샘플 블렌드 데이터 (풀문)

    - 예가체프 40%
    - 안티구아 40%
    - 모모라 10%
    - g4 10%
    """
    blend = Blend(
        name='풀문',
        blend_type='풀문',
        description='풀문 블렌드',
        status='active',
        total_portion=10  # 4+4+1+1=10
    )
    db_session.add(blend)
    db_session.commit()
    db_session.refresh(blend)

    # 레시피 추가
    recipes = [
        BlendRecipe(
            blend_id=blend.id,
            bean_id=sample_beans[0].id,
            portion_count=4,
            ratio=40
        ),
        BlendRecipe(
            blend_id=blend.id,
            bean_id=sample_beans[1].id,
            portion_count=4,
            ratio=40
        ),
        BlendRecipe(
            blend_id=blend.id,
            bean_id=sample_beans[2].id,
            portion_count=1,
            ratio=10
        ),
        BlendRecipe(
            blend_id=blend.id,
            bean_id=sample_beans[3].id,
            portion_count=1,
            ratio=10
        ),
    ]

    for recipe in recipes:
        db_session.add(recipe)
    db_session.commit()

    return blend


@pytest.fixture
def sample_cost_setting(db_session):
    """
    샘플 비용 설정 데이터

    - 손실률: 17%
    - 마진율: 2.5배
    - 로스팅 비용: 500원/kg
    - 인건비: 15,000원/시간
    - 전기료: 1,000원/시간
    """
    cost_settings = [
        CostSetting(parameter_name='loss_rate', value=17.0, description='표준 손실률 (%)'),
        CostSetting(parameter_name='margin_multiplier', value=2.5, description='마진율 (배수)'),
        CostSetting(parameter_name='roasting_cost_per_kg', value=500, description='로스팅 비용 (원/kg)'),
        CostSetting(parameter_name='labor_cost_per_hour', value=15000, description='인건비 (원/시간)'),
        CostSetting(parameter_name='electricity_cost_per_hour', value=1000, description='전기료 (원/시간)'),
    ]

    for setting in cost_settings:
        db_session.add(setting)
    db_session.commit()

    # 첫 번째 설정 (loss_rate)을 반환
    for setting in cost_settings:
        db_session.refresh(setting)

    return cost_settings


@pytest.fixture
def sample_user(db_session):
    """
    샘플 사용자 데이터

    - Username: testuser
    - Password: testpass123
    - Role: Admin
    """
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
    """
    샘플 로스팅 기록

    - 생두: 10kg
    - 로스팅 후: 8.3kg
    - 손실률: 17%
    """
    from app.services.roasting_service import RoastingService

    log = RoastingService.create_roasting_log(
        db=db_session,
        raw_weight_kg=10.0,
        roasted_weight_kg=8.3,
        roasting_date=date.today(),
        notes='테스트 로스팅 기록'
    )

    return log


@pytest.fixture
def multiple_roasting_logs(db_session):
    """
    여러 개의 로스팅 기록 (통계 테스트용)

    - 30일간의 로스팅 기록 생성
    - 손실률 15~19% 범위
    """
    from app.services.roasting_service import RoastingService

    logs = []
    base_date = date.today() - timedelta(days=30)

    for i in range(30):
        roasting_date = base_date + timedelta(days=i)

        # 손실률 15~19% 범위로 다양하게
        loss_rate = 15.0 + (i % 5)
        raw_weight = 10.0
        roasted_weight = raw_weight * (1 - loss_rate / 100)

        log = RoastingService.create_roasting_log(
            db=db_session,
            raw_weight_kg=raw_weight,
            roasted_weight_kg=round(roasted_weight, 2),
            roasting_date=roasting_date,
            notes=f'로스팅 기록 {i+1}'
        )
        logs.append(log)

    return logs


@pytest.fixture
def sample_loss_rate_warning(db_session, sample_roasting_log):
    """
    샘플 손실률 경고
    """
    warning = LossRateWarning(
        roasting_log_id=sample_roasting_log.id,
        expected_loss_rate=17.0,
        actual_loss_rate=25.0,
        variance=8.0,
        severity='CRITICAL',
        message='손실률이 예상보다 8% 높습니다',
        is_resolved=False
    )
    db_session.add(warning)
    db_session.commit()
    db_session.refresh(warning)

    return warning


# 테스트 데이터 생성 헬퍼 함수들

def create_test_bean(db_session, name='Test Bean', price=5000, no=99):
    """테스트용 원두 생성"""
    bean = Bean(
        no=no,
        name=name,
        country_name='Test Origin',
        roast_level='Medium',
        price_per_kg=price,
        status='active'
    )
    db_session.add(bean)
    db_session.commit()
    db_session.refresh(bean)
    return bean


def create_test_blend(db_session, name='Test Blend'):
    """테스트용 블렌드 생성"""
    blend = Blend(
        name=name,
        blend_type='기타',
        description=f'{name} Description',
        status='active'
    )
    db_session.add(blend)
    db_session.commit()
    db_session.refresh(blend)
    return blend


def create_test_user(db_session, username='testuser', role='Admin'):
    """테스트용 사용자 생성"""
    from app.services.auth_service import AuthService

    user = AuthService.create_user(
        db=db_session,
        username=username,
        password='password123',
        role=role
    )
    return user
