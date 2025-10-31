# 📚 Phase 2-5 통합 구현 가이드

**작성일:** 2025-10-29
**기반:** 실제 프로젝트 상태 진단 + 마스터플랜 v2.1
**대상:** Phase 1 완료 후, Phase 2~5 순차 실행

---

## 📊 현재 상태 vs 목표 상태

### A. 데이터베이스 상태

**현재 (2025-10-29):**
```
✓ beans (13 레코드)
✓ blends (7 레코드) - 구조 문제 있음
✓ blend_recipes (14 레코드)
✓ inventory (13 레코드)
✓ transactions (60 레코드)
✓ cost_settings (7 레코드) - 예상 외 존재!
✗ roasting_logs - 없음 (Phase 1에서 추가)
✗ blend_recipes_history, users, audit_logs, loss_rate_warnings - 없음
```

**목표 (v2.1):**
```
10개 테이블 완성
✓ beans, blends, blend_recipes, inventory, transactions
✓ cost_settings (이미 있음!)
+ roasting_logs, blend_recipes_history, users, user_permissions, audit_logs, loss_rate_warnings
```

**주요 이슈:**
| 테이블 | 현재 문제 | 해결 방법 |
|--------|---------|---------|
| **blends** | "마사이", "안티구아" 같은 개별 원두가 blend으로 등록됨 | Phase 1에서 데이터 정리 |
| **blend_recipes** | portion_count(포션개수)와 ratio(%)가 혼재 | v2.1에서 blending_ratio_percent로 통일 |
| **beans** | price_per_kg이 모두 0.0으로 설정됨 | Phase 1 T1-4에서 입력 필요 |
| **cost_settings** | 존재하지만 활용 구조 미정 | Phase 2-5에서 CostService에 통합 |

---

## 🏗️ Phase 2: 백엔드 서비스 (2.5주)

### Phase 2 개요
- **목표:** 5개 추가 테이블 생성 + 10개 서비스 완성
- **기간:** 10일 (2.5주)
- **산출물:** 프로덕션 레디 백엔드 API

---

## 📋 T2-1: DB 스키마 설계 및 마이그레이션 (1일)

### T2-1-1: 새 테이블 정의서 작성

**1. roasting_logs 테이블** (Phase 1과 동시 진행)

```sql
CREATE TABLE roasting_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 핵심 데이터
    raw_weight_kg REAL NOT NULL,           -- 생두 투입량
    roasted_weight_kg REAL NOT NULL,       -- 로스팅 후 무게
    loss_rate_percent REAL NOT NULL,       -- 실제 손실률 (자동 계산)
    expected_loss_rate_percent REAL,       -- 예상 손실률 (기본값 17%)
    loss_variance_percent REAL,             -- 손실률 편차 (실제 vs 예상)

    -- 식별정보
    roasting_date DATE NOT NULL,           -- 로스팅 날짜
    roasting_month TEXT,                    -- 로스팅 월 (YYYY-MM)
    blend_recipe_version_id INTEGER,        -- BlendRecipesHistory 참조

    -- 메타데이터
    notes TEXT,                             -- 로스팅 노트
    operator_id INTEGER,                    -- 담당자 (추후 users 연결)

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (blend_recipe_version_id) REFERENCES blend_recipes_history(id),
    FOREIGN KEY (operator_id) REFERENCES users(id)
);

-- 인덱스
CREATE INDEX idx_roasting_date ON roasting_logs(roasting_date);
CREATE INDEX idx_roasting_month ON roasting_logs(roasting_month);
```

**2. blend_recipes_history 테이블** (레시피 버전 관리)

```sql
CREATE TABLE blend_recipes_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 원본 레시피 참조
    blend_id INTEGER NOT NULL,

    -- 레시피 정보
    version INTEGER NOT NULL,               -- 버전 번호 (1, 2, 3...)
    blending_ratio_percent REAL NOT NULL,  -- 혼합률 (0-100%)
    effective_date DATE NOT NULL,           -- 적용 시작일
    obsolete_date DATE,                     -- 적용 종료일
    is_current BOOLEAN DEFAULT TRUE,        -- 현재 활성 버전?

    -- 원두 정보
    bean_id INTEGER NOT NULL,
    bean_name TEXT,                         -- 스냅샷 (원두명 변경 시 추적용)

    -- 메타데이터
    change_reason TEXT,                     -- 변경 사유
    changed_by INTEGER,                     -- 변경자

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (blend_id) REFERENCES blends(id),
    FOREIGN KEY (bean_id) REFERENCES beans(id),
    FOREIGN KEY (changed_by) REFERENCES users(id),

    UNIQUE(blend_id, bean_id, version)
);

CREATE INDEX idx_blend_current ON blend_recipes_history(blend_id, is_current);
CREATE INDEX idx_effective_date ON blend_recipes_history(effective_date);
```

**3. users 테이블** (사용자 관리)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,            -- bcrypt 해시
    email TEXT UNIQUE,

    -- 사용자 정보
    full_name TEXT,
    role TEXT DEFAULT 'viewer',             -- viewer, editor, admin
    department TEXT,                        -- 로스팅부, 영업 등

    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_username ON users(username);
```

**4. user_permissions 테이블** (세분화된 권한)

```sql
CREATE TABLE user_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,
    resource TEXT NOT NULL,                 -- 'blends', 'beans', 'roasting_logs', etc.
    action TEXT NOT NULL,                   -- 'read', 'create', 'update', 'delete'

    granted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_by INTEGER,                     -- 권한 부여자

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (granted_by) REFERENCES users(id),

    UNIQUE(user_id, resource, action)
);
```

**5. audit_logs 테이블** (감사/추적용)

```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 작업 정보
    action_type TEXT NOT NULL,              -- 'CREATE', 'UPDATE', 'DELETE', 'EXPORT'
    resource_type TEXT NOT NULL,            -- 'Blend', 'Bean', 'RoastingLog', etc.
    resource_id INTEGER,                    -- 대상 ID

    -- 변경 내용
    old_values TEXT,                        -- JSON: 변경 전 값
    new_values TEXT,                        -- JSON: 변경 후 값
    description TEXT,

    -- 메타데이터
    user_id INTEGER,                        -- 작업자
    ip_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_user_action ON audit_logs(user_id, action_type);
CREATE INDEX idx_created_at ON audit_logs(created_at);
```

**6. loss_rate_warnings 테이블** (이상 탐지)

```sql
CREATE TABLE loss_rate_warnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- 경고 정보
    roasting_log_id INTEGER NOT NULL,
    warning_type TEXT,                      -- 'HIGH', 'LOW', 'TREND'
    severity TEXT,                          -- 'INFO', 'WARNING', 'CRITICAL'

    -- 분석 결과
    variance_from_expected REAL,             -- 예상치와의 편차
    consecutive_occurrences INTEGER,        -- 연속 발생 횟수

    -- 상태
    is_resolved BOOLEAN DEFAULT FALSE,
    resolution_notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,

    FOREIGN KEY (roasting_log_id) REFERENCES roasting_logs(id)
);

CREATE INDEX idx_warning_date ON loss_rate_warnings(created_at);
CREATE INDEX idx_unresolved ON loss_rate_warnings(is_resolved, severity);
```

### T2-1-2: 마이그레이션 전략 결정

**기존 테이블 수정 방향:**

```python
# blend_recipes 수정 계획
# 현재: portion_count(정의 불명) + ratio(%)
# 변경: blending_ratio_percent + version + effective_date

# ALTER TABLE blend_recipes
# RENAME COLUMN ratio TO blending_ratio_percent;
# ADD COLUMN recipe_version INTEGER DEFAULT 1;
# ADD COLUMN effective_date DATE DEFAULT CURRENT_DATE;
# ADD COLUMN is_current BOOLEAN DEFAULT TRUE;
# DROP COLUMN portion_count;  # 마이그레이션 후
```

**기존 데이터 정리:**
- blends 테이블: "마사이", "안티구아" 같은 개별 원두는 주 테이블에서 제거 (이미 beans에 있음)
- beans 테이블: price_per_kg 값 입력 (현재 모두 0.0)
- cost_settings: 현재 용도 파악 및 CostService와의 통합 방식 결정

---

## 💼 T2-2: SQLAlchemy 모델 확장 (1.5일)

### T2-2-1: 새 모델 정의

**파일:** `app/models/database.py` (기존에 추가)

```python
# roasting_logs.py
from sqlalchemy import Column, Integer, Float, Date, String, Text, ForeignKey, DateTime, Boolean
from datetime import datetime

class RoastingLog(Base):
    __tablename__ = 'roasting_logs'

    id = Column(Integer, primary_key=True)
    raw_weight_kg = Column(Float, nullable=False)
    roasted_weight_kg = Column(Float, nullable=False)
    loss_rate_percent = Column(Float, nullable=False)
    expected_loss_rate_percent = Column(Float, default=17.0)
    loss_variance_percent = Column(Float)

    roasting_date = Column(Date, nullable=False)
    roasting_month = Column(String(7))  # YYYY-MM
    blend_recipe_version_id = Column(Integer, ForeignKey('blend_recipes_history.id'))

    notes = Column(Text)
    operator_id = Column(Integer, ForeignKey('users.id'))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    operator = relationship("User", back_populates="roasting_logs")
    recipe_version = relationship("BlendRecipesHistory")


class BlendRecipesHistory(Base):
    __tablename__ = 'blend_recipes_history'

    id = Column(Integer, primary_key=True)
    blend_id = Column(Integer, ForeignKey('blends.id'), nullable=False)
    version = Column(Integer, nullable=False)
    blending_ratio_percent = Column(Float, nullable=False)  # 0-100
    effective_date = Column(Date, nullable=False)
    obsolete_date = Column(Date)
    is_current = Column(Boolean, default=True)

    bean_id = Column(Integer, ForeignKey('beans.id'), nullable=False)
    bean_name = Column(String(255))
    change_reason = Column(Text)
    changed_by = Column(Integer, ForeignKey('users.id'))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    blend = relationship("Blend", back_populates="recipe_history")
    bean = relationship("Bean")
    changer = relationship("User")

    __table_args__ = (
        UniqueConstraint('blend_id', 'bean_id', 'version'),
    )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)

    full_name = Column(String(255))
    role = Column(String(50), default='viewer')  # viewer, editor, admin
    department = Column(String(255))

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    permissions = relationship("UserPermission", back_populates="user")
    roasting_logs = relationship("RoastingLog", back_populates="operator")
    audit_logs = relationship("AuditLog", back_populates="user")


class UserPermission(Base):
    __tablename__ = 'user_permissions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    resource = Column(String(255), nullable=False)  # 'blends', 'roasting_logs', etc.
    action = Column(String(50), nullable=False)     # 'read', 'create', 'update', 'delete'

    granted_date = Column(DateTime, default=datetime.utcnow)
    granted_by = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="permissions", foreign_keys=[user_id])
    grantor = relationship("User", foreign_keys=[granted_by])

    __table_args__ = (
        UniqueConstraint('user_id', 'resource', 'action'),
    )


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    action_type = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, EXPORT
    resource_type = Column(String(255), nullable=False)
    resource_id = Column(Integer)

    old_values = Column(Text)  # JSON
    new_values = Column(Text)  # JSON
    description = Column(Text)

    user_id = Column(Integer, ForeignKey('users.id'))
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")


class LossRateWarning(Base):
    __tablename__ = 'loss_rate_warnings'

    id = Column(Integer, primary_key=True)
    roasting_log_id = Column(Integer, ForeignKey('roasting_logs.id'), nullable=False)
    warning_type = Column(String(50))  # HIGH, LOW, TREND
    severity = Column(String(50))      # INFO, WARNING, CRITICAL

    variance_from_expected = Column(Float)
    consecutive_occurrences = Column(Integer, default=1)

    is_resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)

    roasting_log = relationship("RoastingLog")
```

### T2-2-2: 기존 모델 수정

**BlendRecipe 모델 업데이트:**

```python
class BlendRecipe(Base):
    __tablename__ = 'blend_recipes'

    id = Column(Integer, primary_key=True)
    blend_id = Column(Integer, ForeignKey('blends.id'), nullable=False)
    bean_id = Column(Integer, ForeignKey('beans.id'), nullable=False)

    # 이전: portion_count + ratio
    # 변경: blending_ratio_percent (%) + version + effective_date
    blending_ratio_percent = Column(Float, nullable=False)  # 0~100, 합=100%
    recipe_version = Column(Integer, default=1)
    effective_date = Column(Date, default=datetime.now)
    is_current = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    blend = relationship("Blend", back_populates="recipes")
    bean = relationship("Bean", back_populates="blend_recipes")


class Blend(Base):
    __tablename__ = 'blends'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    blend_type = Column(String(50))  # '풀문', '뉴문'
    description = Column(Text)

    # 이전: total_portion (포션 개수, 정의 불명)
    # 변경: 혼합률 기반이므로 제거
    loss_rate_percent = Column(Float, default=17.0)        # 손실률
    standard_selling_price = Column(Float)                 # 판매가

    status = Column(String(50), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recipes = relationship("BlendRecipe", back_populates="blend")
    recipe_history = relationship("BlendRecipesHistory", back_populates="blend")
    transactions = relationship("Transaction", back_populates="blend")
```

---

## 🔧 T2-3: RoastingService 개발 (1.5일)

**파일:** `app/services/roasting_service.py`

```python
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, between
from app.models.database import RoastingLog, LossRateWarning
from datetime import datetime, date
import json

class RoastingService:
    """로스팅 기록 관리 서비스"""

    @staticmethod
    def create_roasting_log(
        db: Session,
        raw_weight_kg: float,
        roasted_weight_kg: float,
        roasting_date: date,
        blend_recipe_version_id: int = None,
        notes: str = None,
        operator_id: int = None,
        expected_loss_rate: float = 17.0
    ) -> RoastingLog:
        """로스팅 기록 생성"""

        # 손실률 계산
        loss_rate = ((raw_weight_kg - roasted_weight_kg) / raw_weight_kg) * 100
        loss_variance = loss_rate - expected_loss_rate

        roasting_log = RoastingLog(
            raw_weight_kg=raw_weight_kg,
            roasted_weight_kg=roasted_weight_kg,
            loss_rate_percent=round(loss_rate, 2),
            expected_loss_rate_percent=expected_loss_rate,
            loss_variance_percent=round(loss_variance, 2),
            roasting_date=roasting_date,
            roasting_month=roasting_date.strftime('%Y-%m'),
            blend_recipe_version_id=blend_recipe_version_id,
            notes=notes,
            operator_id=operator_id
        )

        db.add(roasting_log)
        db.commit()
        db.refresh(roasting_log)

        # 이상 탐지
        RoastingService._check_loss_rate_anomaly(db, roasting_log)

        return roasting_log

    @staticmethod
    def get_roasting_logs_by_month(db: Session, month: str) -> list:
        """월별 로스팅 기록 조회 (YYYY-MM)"""
        logs = db.query(RoastingLog).filter(
            RoastingLog.roasting_month == month
        ).order_by(RoastingLog.roasting_date).all()
        return logs

    @staticmethod
    def get_monthly_statistics(db: Session, month: str) -> dict:
        """월별 통계"""
        logs = RoastingService.get_roasting_logs_by_month(db, month)

        if not logs:
            return {"month": month, "count": 0}

        total_raw = sum(log.raw_weight_kg for log in logs)
        total_roasted = sum(log.roasted_weight_kg for log in logs)
        avg_loss_rate = sum(log.loss_rate_percent for log in logs) / len(logs)

        return {
            "month": month,
            "total_logs": len(logs),
            "total_raw_weight_kg": round(total_raw, 2),
            "total_roasted_weight_kg": round(total_roasted, 2),
            "avg_loss_rate_percent": round(avg_loss_rate, 2),
            "total_loss_kg": round(total_raw - total_roasted, 2),
            "variance_from_expected": round(avg_loss_rate - 17.0, 2)
        }

    @staticmethod
    def _check_loss_rate_anomaly(db: Session, roasting_log: RoastingLog):
        """손실률 이상 탐지"""
        variance = roasting_log.loss_variance_percent

        if abs(variance) > 3.0:  # 3% 이상 편차
            warning_type = 'HIGH' if variance > 3.0 else 'LOW'
            severity = 'CRITICAL' if abs(variance) > 5.0 else 'WARNING'

            # 연속 발생 확인 (지난 3회)
            recent_logs = db.query(RoastingLog).filter(
                RoastingLog.roasting_date < roasting_log.roasting_date
            ).order_by(RoastingLog.roasting_date.desc()).limit(3).all()

            consecutive = 0
            for log in recent_logs:
                if abs(log.loss_variance_percent) > 3.0:
                    consecutive += 1
                else:
                    break

            warning = LossRateWarning(
                roasting_log_id=roasting_log.id,
                warning_type=warning_type,
                severity=severity,
                variance_from_expected=round(variance, 2),
                consecutive_occurrences=consecutive + 1
            )

            db.add(warning)
            db.commit()

    @staticmethod
    def export_to_excel(db: Session, month: str) -> bytes:
        """월별 로스팅 기록을 Excel로 내보내기"""
        # Phase 3에서 구현 (ExcelService와 통합)
        pass
```

---

## 💰 T2-4: CostService 개발 (1.5일)

**파일:** `app/services/cost_service.py`

```python
from sqlalchemy.orm import Session
from app.models.database import Bean, Blend, BlendRecipe, CostSettings

class CostService:
    """원가 계산 서비스 (핵심 비즈니스 로직)"""

    # 손실률 상수
    STANDARD_LOSS_RATE = 0.17  # 17%

    @staticmethod
    def get_blend_cost(
        db: Session,
        blend_id: int,
        unit: str = 'kg',
        use_current_recipes: bool = True
    ) -> dict:
        """
        블렌드의 최종 원가 계산

        공식: Final Cost = (Σ(Bean Cost × Ratio%)) / (1 - Loss Rate)

        예시 (풀문):
        - 마사이 40% @ 5,000원/kg = 2,000원
        - 안티구아 40% @ 6,000원/kg = 2,400원
        - 모모라 10% @ 4,500원/kg = 450원
        - g4 10% @ 5,500원/kg = 550원
        ------------------------------------------
        - 혼합 원가 = 5,400원
        - 손실률 17% 반영 = 5,400 / 0.83 = 6,506원/kg

        Args:
            blend_id: 블렌드 ID
            unit: 'kg' 또는 'cup' (1cup = 200g)
            use_current_recipes: True면 현재 레시피, False면 모든 버전 포함

        Returns:
            {
                'blend_id': int,
                'blend_name': str,
                'component_costs': [
                    {'bean_name': str, 'ratio': float, 'price_per_kg': float, 'component_cost': float}
                ],
                'blend_cost_before_loss': float,  # 혼합 원가
                'loss_rate': float,               # 손실률
                'final_cost_per_kg': float,       # 최종 원가
                'final_cost_per_unit': float,     # 단위당 원가
                'margin_with_selling_price': float # 판매가 대비 마진율
            }
        """

        blend = db.query(Blend).filter(Blend.id == blend_id).first()
        if not blend:
            raise ValueError(f"블렌드를 찾을 수 없습니다: {blend_id}")

        # 현재 레시피 조회
        if use_current_recipes:
            recipes = db.query(BlendRecipe).filter(
                and_(
                    BlendRecipe.blend_id == blend_id,
                    BlendRecipe.is_current == True
                )
            ).all()
        else:
            recipes = db.query(BlendRecipe).filter(
                BlendRecipe.blend_id == blend_id
            ).all()

        # 혼합 원가 계산
        component_costs = []
        total_blend_cost = 0

        for recipe in recipes:
            bean = db.query(Bean).filter(Bean.id == recipe.bean_id).first()
            bean_price = bean.price_per_kg if bean.price_per_kg > 0 else 5000  # 기본값

            component_cost = bean_price * (recipe.blending_ratio_percent / 100)
            total_blend_cost += component_cost

            component_costs.append({
                'bean_name': bean.name,
                'ratio': recipe.blending_ratio_percent,
                'price_per_kg': bean_price,
                'component_cost': round(component_cost, 0)
            })

        # 손실률 반영한 최종 원가
        loss_rate = blend.loss_rate_percent / 100
        final_cost_per_kg = total_blend_cost / (1 - loss_rate)

        # 단위별 계산
        final_cost_per_unit = final_cost_per_kg
        if unit == 'cup':
            final_cost_per_unit = (final_cost_per_kg * 0.2)  # 1cup = 200g = 0.2kg

        # 마진율 계산
        margin = 0
        if blend.standard_selling_price and blend.standard_selling_price > 0:
            margin = ((blend.standard_selling_price - final_cost_per_kg)
                     / blend.standard_selling_price * 100)

        return {
            'blend_id': blend.id,
            'blend_name': blend.name,
            'component_costs': component_costs,
            'blend_cost_before_loss': round(total_blend_cost, 0),
            'loss_rate': blend.loss_rate_percent,
            'final_cost_per_kg': round(final_cost_per_kg, 0),
            'final_cost_per_unit': round(final_cost_per_unit, 0),
            'selling_price': blend.standard_selling_price,
            'margin_percent': round(margin, 1) if margin else None
        }

    @staticmethod
    def update_bean_price(db: Session, bean_id: int, new_price: float):
        """원두 가격 업데이트"""
        bean = db.query(Bean).filter(Bean.id == bean_id).first()
        if not bean:
            raise ValueError(f"원두를 찾을 수 없습니다: {bean_id}")

        bean.price_per_kg = new_price
        bean.updated_at = datetime.utcnow()
        db.commit()

        return bean

    @staticmethod
    def batch_calculate_all_blends(db: Session) -> list:
        """모든 블렌드의 원가 계산 (일괄)"""
        blends = db.query(Blend).filter(Blend.status == 'active').all()
        results = []

        for blend in blends:
            try:
                cost_data = CostService.get_blend_cost(db, blend.id)
                results.append(cost_data)
            except Exception as e:
                results.append({
                    'blend_id': blend.id,
                    'blend_name': blend.name,
                    'error': str(e)
                })

        return results
```

---

## 🔐 T2-5: AuthService 개발 (1일)

**파일:** `app/services/auth_service.py`

```python
from sqlalchemy.orm import Session
from app.models.database import User, UserPermission
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """인증 및 권한 관리 서비스"""

    @staticmethod
    def create_user(
        db: Session,
        username: str,
        password: str,
        email: str = None,
        full_name: str = None,
        role: str = 'viewer',
        department: str = None
    ) -> User:
        """사용자 생성"""

        # 중복 확인
        if db.query(User).filter(User.username == username).first():
            raise ValueError(f"이미 존재하는 사용자명: {username}")

        password_hash = pwd_context.hash(password)

        user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            full_name=full_name,
            role=role,
            department=department
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # 기본 권한 설정
        default_permissions = [
            ('blends', 'read'),
            ('beans', 'read'),
            ('roasting_logs', 'read'),
        ]

        for resource, action in default_permissions:
            AuthService.grant_permission(db, user.id, resource, action, user.id)

        return user

    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> User:
        """사용자 인증"""
        user = db.query(User).filter(
            and_(User.username == username, User.is_active == True)
        ).first()

        if not user or not pwd_context.verify(password, user.password_hash):
            return None

        user.last_login = datetime.utcnow()
        db.commit()

        return user

    @staticmethod
    def grant_permission(
        db: Session,
        user_id: int,
        resource: str,
        action: str,
        granted_by: int
    ):
        """사용자에게 권한 부여"""

        permission = UserPermission(
            user_id=user_id,
            resource=resource,
            action=action,
            granted_by=granted_by
        )

        db.add(permission)
        db.commit()

    @staticmethod
    def has_permission(
        db: Session,
        user_id: int,
        resource: str,
        action: str
    ) -> bool:
        """권한 확인"""

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Admin은 모든 권한 보유
        if user.role == 'admin':
            return True

        # 특정 권한 확인
        permission = db.query(UserPermission).filter(
            and_(
                UserPermission.user_id == user_id,
                UserPermission.resource == resource,
                UserPermission.action == action
            )
        ).first()

        return permission is not None
```

---

## 📊 T2-6: LossRateAnalyzer 개발 (1일)

**파일:** `app/services/loss_rate_analyzer.py`

```python
from sqlalchemy.orm import Session
from app.models.database import RoastingLog, LossRateWarning
from datetime import datetime, timedelta
import statistics

class LossRateAnalyzer:
    """손실률 이상 탐지 및 분석 서비스"""

    # 설정
    NORMAL_LOSS_RATE = 17.0
    WARNING_THRESHOLD = 3.0      # 3% 편차
    CRITICAL_THRESHOLD = 5.0     # 5% 편차
    TREND_WINDOW = 5              # 최근 5회 로그 분석

    @staticmethod
    def analyze_loss_rate_trend(db: Session, days: int = 30) -> dict:
        """지정된 기간의 손실률 트렌드 분석"""

        start_date = datetime.now().date() - timedelta(days=days)
        logs = db.query(RoastingLog).filter(
            RoastingLog.roasting_date >= start_date
        ).order_by(RoastingLog.roasting_date).all()

        if not logs:
            return {"period_days": days, "data_count": 0, "status": "NO_DATA"}

        loss_rates = [log.loss_rate_percent for log in logs]
        variances = [log.loss_variance_percent for log in logs]

        # 통계 계산
        avg_loss = statistics.mean(loss_rates)
        median_loss = statistics.median(loss_rates)
        stdev_loss = statistics.stdev(loss_rates) if len(loss_rates) > 1 else 0

        # 이상치 개수
        anomalies = sum(1 for v in variances if abs(v) > LossRateAnalyzer.WARNING_THRESHOLD)

        return {
            "period_days": days,
            "data_count": len(logs),
            "avg_loss_rate": round(avg_loss, 2),
            "median_loss_rate": round(median_loss, 2),
            "std_deviation": round(stdev_loss, 2),
            "min_loss_rate": round(min(loss_rates), 2),
            "max_loss_rate": round(max(loss_rates), 2),
            "anomalies_count": anomalies,
            "anomaly_rate_percent": round((anomalies / len(logs) * 100), 1),
            "status": "NORMAL" if anomalies < 2 else "ATTENTION" if anomalies < 5 else "CRITICAL"
        }

    @staticmethod
    def get_recent_warnings(db: Session, limit: int = 10) -> list:
        """최근 경고 조회 (미해결)"""
        warnings = db.query(LossRateWarning).filter(
            LossRateWarning.is_resolved == False
        ).order_by(LossRateWarning.created_at.desc()).limit(limit).all()

        return [{
            'id': w.id,
            'roasting_date': w.roasting_log.roasting_date,
            'severity': w.severity,
            'variance': w.variance_from_expected,
            'consecutive': w.consecutive_occurrences,
            'created_at': w.created_at
        } for w in warnings]

    @staticmethod
    def resolve_warning(db: Session, warning_id: int, notes: str = None):
        """경고 해결"""
        warning = db.query(LossRateWarning).filter(LossRateWarning.id == warning_id).first()
        if not warning:
            raise ValueError(f"경고를 찾을 수 없습니다: {warning_id}")

        warning.is_resolved = True
        warning.resolution_notes = notes
        warning.resolved_at = datetime.utcnow()
        db.commit()
```

---

## 🔄 T2-7: ExcelSyncService 확장 (1.5일)

**파일:** `app/services/excel_service.py` (기존 + 확장)

```python
class ExcelSyncService:
    """Excel 동기화 및 마이그레이션 서비스"""

    @staticmethod
    def export_roasting_logs_to_excel(
        db: Session,
        month: str,
        output_path: str
    ):
        """월별 로스팅 기록을 Excel로 내보내기 (담당자용 영수증 형식)"""

        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

        logs = db.query(RoastingLog).filter(
            RoastingLog.roasting_month == month
        ).order_by(RoastingLog.roasting_date).all()

        wb = Workbook()
        ws = wb.active
        ws.title = f"{month}_로스팅"

        # 헤더
        headers = ['날짜', '생두투입(kg)', '로스팅량(kg)', '손실률(%)', '예상손실률(%)', '편차(%)', '담당자', '비고']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")

        # 데이터
        for row, log in enumerate(logs, 2):
            ws.cell(row=row, column=1, value=log.roasting_date.strftime('%Y-%m-%d'))
            ws.cell(row=row, column=2, value=round(log.raw_weight_kg, 1))
            ws.cell(row=row, column=3, value=round(log.roasted_weight_kg, 1))
            ws.cell(row=row, column=4, value=round(log.loss_rate_percent, 2))
            ws.cell(row=row, column=5, value=round(log.expected_loss_rate_percent, 2))
            ws.cell(row=row, column=6, value=round(log.loss_variance_percent, 2))
            ws.cell(row=row, column=7, value=log.operator.full_name if log.operator else '')
            ws.cell(row=row, column=8, value=log.notes or '')

        # 컬럼 너비 조정
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 14
        ws.column_dimensions['F'].width = 12

        wb.save(output_path)
        return output_path

    @staticmethod
    def validate_phase1_migration(db: Session) -> dict:
        """Phase 1 마이그레이션 검증"""

        # RoastingLog 데이터 검증
        logs = db.query(RoastingLog).all()

        validations = {
            'total_logs': len(logs),
            'checks': {
                'raw_weight_valid': 0,
                'roasted_weight_valid': 0,
                'loss_rate_valid': 0,
                'no_null_dates': 0,
                'no_duplicates': 0
            },
            'errors': []
        }

        # 1. 무게 유효성 확인
        for log in logs:
            if log.raw_weight_kg > 0 and log.roasted_weight_kg > 0:
                validations['checks']['raw_weight_valid'] += 1

            if log.roasted_weight_kg <= log.raw_weight_kg:
                validations['checks']['roasted_weight_valid'] += 1
            else:
                validations['errors'].append(f"로그 {log.id}: 로스팅량 > 생두투입량")

            # 2. 손실률 검증 (0~50%)
            if 0 <= log.loss_rate_percent <= 50:
                validations['checks']['loss_rate_valid'] += 1
            else:
                validations['errors'].append(f"로그 {log.id}: 손실률 이상 {log.loss_rate_percent}%")

            # 3. 날짜 검증
            if log.roasting_date:
                validations['checks']['no_null_dates'] += 1

        # 4. 중복 검증
        from sqlalchemy import func
        duplicates = db.query(
            RoastingLog.roasting_date,
            func.count().label('count')
        ).group_by(RoastingLog.roasting_date).having(
            func.count() > 1
        ).all()

        if not duplicates:
            validations['checks']['no_duplicates'] = len(logs)

        validations['validation_passed'] = len(validations['errors']) == 0

        return validations
```

---

## 🧪 T2-8: Unit Tests 작성 (2일)

**기본 구조:** `app/tests/` 디렉토리 생성

```
app/tests/
├── __init__.py
├── conftest.py                    # Pytest 설정
├── test_services.py               # 서비스 단위 테스트
├── test_models.py                 # ORM 모델 테스트
└── test_integration.py            # 통합 테스트
```

**샘플:** `app/tests/test_services.py`

```python
import pytest
from app.services.cost_service import CostService
from app.services.roasting_service import RoastingService
from datetime import date

@pytest.fixture
def setup_test_data(db):
    """테스트 데이터 생성"""
    # Bean 생성
    bean1 = Bean(name="마사이", price_per_kg=5000)
    bean2 = Bean(name="안티구아", price_per_kg=6000)
    db.add_all([bean1, bean2])
    db.commit()

    # Blend 생성
    blend = Blend(name="풀문", loss_rate_percent=17.0, standard_selling_price=22000)
    db.add(blend)
    db.commit()

    # Recipe 생성
    recipe1 = BlendRecipe(blend_id=blend.id, bean_id=bean1.id, blending_ratio_percent=40)
    recipe2 = BlendRecipe(blend_id=blend.id, bean_id=bean2.id, blending_ratio_percent=40)
    db.add_all([recipe1, recipe2])
    db.commit()

    return {'blend': blend, 'beans': [bean1, bean2]}

def test_cost_calculation(db, setup_test_data):
    """원가 계산 테스트"""
    blend = setup_test_data['blend']

    result = CostService.get_blend_cost(db, blend.id)

    # 예상: (5000*0.4 + 6000*0.4) / (1-0.17) = 4400 / 0.83 ≈ 5,300
    assert result['final_cost_per_kg'] > 0
    assert result['blend_cost_before_loss'] == 4400

def test_roasting_log_creation(db):
    """로스팅 기록 생성 테스트"""
    log = RoastingService.create_roasting_log(
        db,
        raw_weight_kg=100,
        roasted_weight_kg=83,
        roasting_date=date(2025, 10, 29)
    )

    assert log.loss_rate_percent == 17.0
    assert log.roasting_month == "2025-10"
```

---

## 🔍 T2-9: 코드 리뷰 및 리팩토링 (0.5일)

**체크리스트:**
- [ ] 모든 서비스에 에러 핸들링 추가
- [ ] 데이터베이스 트랜잭션 처리 확인
- [ ] 로깅 구현 (INFO, WARNING, ERROR)
- [ ] 타입 힌트 완성
- [ ] 문서화 (Docstring) 작성
- [ ] SQL 쿼리 최적화 (N+1 문제 확인)

---

## 🎨 Phase 3: 프론트엔드 (3주) - 개요

### Phase 3 목표
- 11개 페이지 구현
- 반응형 UI/UX
- 사용자 권한 기반 접근 제어

### T3 페이지 목록

| Task | 페이지 | 우선순위 | 난이도 |
|------|--------|---------|--------|
| **T3-1** | 로그인 | P0 | Medium |
| **T3-2** | 대시보드 | P0 | High |
| **T3-3** | 원두 관리 | P1 | Low |
| **T3-4** | 블렌드 관리 | P1 | Medium |
| **T3-5** | 로스팅 기록 | P0 | High |
| **T3-6** | 월별 로스팅 그리드 | P0 | High |
| **T3-7** | 원가 계산 | P0 | High |
| **T3-8** | 손실률 분석 | P1 | Medium |
| **T3-9** | 판매 거래 | P1 | Low |
| **T3-10** | 보고서 | P1 | Medium |
| **T3-11** | 사용자 관리 | P2 | Low |

(각 페이지의 상세 구현 방법은 별도 문서에서 제공)

---

## 🧪 Phase 4: 테스트 (2주) - 개요

### T4 테스트 계획

- **Unit Tests:** 모든 서비스 및 모델 (90% 커버리지)
- **Integration Tests:** 엔드투엔드 시나리오
- **Performance Tests:** 대량 데이터 (10,000+ 로스팅 레코드)
- **Security Tests:** SQL Injection, XSS, CSRF 방어

---

## 🚀 Phase 5: 배포 (1.5주) - 개요

### T5 배포 계획

- **환경 설정:** Production/Staging 환경
- **DB 마이그레이션:** 기존 데이터 보존
- **배포 자동화:** CI/CD 파이프라인
- **모니터링:** 에러 추적, 성능 메트릭

---

## 📊 Phase 2-5 일정 요약

```
Phase 2 (2.5주): T2-1 ~ T2-9
├─ T2-1: DB 스키마 설계 (1일)
├─ T2-2: SQLAlchemy 모델 (1.5일)
├─ T2-3: RoastingService (1.5일)
├─ T2-4: CostService (1.5일)
├─ T2-5: AuthService (1일)
├─ T2-6: LossRateAnalyzer (1일)
├─ T2-7: ExcelSyncService (1.5일)
├─ T2-8: Unit Tests (2일)
└─ T2-9: 코드 리뷰 (0.5일)
    → 총 11일 (2.5주 with buffer)

Phase 3 (3주): T3-1 ~ T3-11
├─ T3-1 ~ T3-6: 핵심 페이지 (2주)
└─ T3-7 ~ T3-11: 추가 페이지 (1주)

Phase 4 (2주): 테스트
├─ Unit Test: 90% 커버리지
├─ Integration Test: E2E 시나리오
└─ Performance Test: 대량 데이터

Phase 5 (1.5주): 배포
├─ 환경 준비
├─ DB 마이그레이션
└─ 배포 및 모니터링

전체: 9주
```

---

## ✅ Phase 2 실행 후 검증 체크리스트

```
□ 10개 테이블 모두 생성 확인
□ 모든 SQLAlchemy 모델 정의 확인
□ 5개 서비스 모두 구현 및 테스트
□ 단위 테스트 90% 이상 통과
□ 문서화 (Docstring) 완성
□ 코드 리뷰 완료
□ 프로덕션 레디 상태 확인
```

---

## 📝 Phase 2 완료 후 다음 단계

**Phase 2 완료 후:**
1. ✅ Phase 2-5 가이드 검토 및 피드백
2. ➡️ Phase 3 시작 전, 실제 DB에서 Phase 2 작업 결과 검증
3. ➡️ Phase 3 프론트엔드 페이지별 상세 가이드 작성 필요

---

**작성 완료: 2025-10-29**
**검토 필수: Phase 2 시작 전에 모든 설계가 타당한지 확인**
**다음 단계: Phase 2 T2-1 (DB 스키마) 착수
