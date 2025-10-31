# 📋 Phase 1: 데이터 기초 구축 상세 구현 가이드

**기간:** 2주 (10일)
**목표:** 로스팅 데이터 마이그레이션 완료 및 기본 데이터 설정
**선행 조건:** DB 스냅샷 생성, Excel 파일 백업

---

## 📅 Phase 1 타임라인

```
Day 1~3:   T1-1 마이그레이션 (3일) ████░░░░░░
Day 4:     T1-2 원두 마스터 (1일) ░░░░████░░
Day 5:     T1-3 블렌드 설정 (1일) ░░░░░████░
Day 6~7:   T1-4 원가 입력 (2일) ░░░░░░████░
Day 8~9:   T1-5 데이터 검증 (2일) ░░░░░░░░████
Day 10:    T1-6 손실률 설정 (1일) ░░░░░░░░░░█

예상 버퍼: 1-2일
```

---

## T1-1: 기존 로스팅 기록 마이그레이션 (3일)

### 목표
Excel Sheet1의 월별 로스팅 기록 (2개월분, 60개 레코드) → SQLite DB로 이전

### 사전 작업 (Day 0 - 준비)

#### Step 1: 백업 및 스냅샷 생성

```bash
# 1. Excel 백업
mkdir -p backups/migration_backup
cp 분석결과.xlsx backups/migration_backup/분석결과_$(date +%Y%m%d_%H%M%S).xlsx
cp 분석결과.xlsx backups/migration_backup/분석결과_v1.xlsx
cp 분석결과.xlsx backups/migration_backup/분석결과_v2.xlsx

# 2. DB 스냅샷 생성
cp Data/roasting_data.db Data/backups/roasting_data_before_migration_$(date +%Y%m%d_%H%M%S).db
```

#### Step 2: 환경 준비

```bash
# Python 스크립트 디렉토리 확인
ls -la app/services/

# 필요 패키지 확인
./venv/bin/pip list | grep -E "openpyxl|pandas|sqlalchemy"
```

#### Step 3: 테스트 환경 구축

```bash
# 테스트 DB 생성
cp Data/roasting_data.db Data/test_roasting_data.db

# 테스트용 Excel 파일 (샘플 몇 행만)
# → 분석결과.xlsx에서 Sheet1의 첫 5행만 복사해서 test_분석결과.xlsx 생성
```

---

### Day 1: 마이그레이션 함수 작성

#### Step 1: app/services/excel_sync.py 생성

```python
# app/services/excel_sync.py

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ExcelSyncService:
    """Excel ↔ DB 동기화 서비스"""

    @staticmethod
    def migrate_roasting_logs(excel_file_path: str, db_session: Session):
        """
        Excel Sheet1 → roasting_logs 마이그레이션

        Args:
            excel_file_path: Excel 파일 경로
            db_session: SQLAlchemy 세션

        Returns:
            {
                'success': bool,
                'inserted_count': int,
                'errors': [list],
                'warnings': [list],
                'total_raw_weight': float,
                'total_roasted_weight': float,
                'validation_report': dict
            }
        """

        result = {
            'success': False,
            'inserted_count': 0,
            'errors': [],
            'warnings': [],
            'total_raw_weight': 0,
            'total_roasted_weight': 0,
            'validation_report': {}
        }

        try:
            # Step 1: Excel 읽기
            logger.info(f"Excel 파일 읽기: {excel_file_path}")
            df = pd.read_excel(excel_file_path, sheet_name='Sheet1')

            logger.info(f"읽은 행 수: {len(df)}")

            # Step 2: 데이터 정규화
            df = ExcelSyncService._normalize_data(df)

            # Step 3: 필수 컬럼 검증
            required_columns = ['원두명', '생두량(kg)', '로스팅량(kg)', '월']
            ExcelSyncService._validate_columns(df, required_columns)

            # Step 4: 트랜잭션 시작
            try:
                # Step 5: 데이터 검증
                validation_errors = []
                validation_warnings = []

                for idx, row in df.iterrows():
                    bean_name = row['원두명'].strip()
                    raw_weight = float(row['생두량(kg)'])
                    roasted_weight = float(row['로스팅량(kg)'])
                    month_str = str(row['월'])

                    # 원두명 검증
                    from app.models import Bean
                    bean = db_session.query(Bean).filter_by(name=bean_name).first()
                    if not bean:
                        validation_errors.append(
                            f"행 {idx+2}: 원두 '{bean_name}' 없음"
                        )
                        continue

                    # 생두량 검증
                    if raw_weight <= 0:
                        validation_errors.append(
                            f"행 {idx+2}: 생두량 {raw_weight} (> 0 필수)"
                        )
                        continue

                    # 로스팅량 검증
                    if roasted_weight <= 0 or roasted_weight > raw_weight:
                        validation_errors.append(
                            f"행 {idx+2}: 로스팅량 {roasted_weight} (0 < 값 <= {raw_weight})"
                        )
                        continue

                    # 손실률 검증
                    loss_rate = (raw_weight - roasted_weight) / raw_weight * 100
                    if loss_rate < 10 or loss_rate > 25:
                        validation_warnings.append(
                            f"행 {idx+2}: 손실률 {loss_rate:.1f}% (정상 범위 10~25%)"
                        )

                result['errors'] = validation_errors
                result['warnings'] = validation_warnings

                # 에러 있으면 중단
                if validation_errors:
                    result['success'] = False
                    return result

                # Step 6: 데이터 삽입
                inserted_count = 0
                total_raw = 0
                total_roasted = 0

                from app.models import RoastingLog, Bean

                for idx, row in df.iterrows():
                    bean_name = row['원두명'].strip()
                    raw_weight = float(row['생두량(kg)'])
                    roasted_weight = float(row['로스팅량(kg)'])
                    month_str = str(row['월'])

                    bean = db_session.query(Bean).filter_by(name=bean_name).first()
                    if not bean:
                        continue

                    loss_rate = (raw_weight - roasted_weight) / raw_weight * 100

                    log = RoastingLog(
                        bean_id=bean.id,
                        raw_weight_kg=raw_weight,
                        roasted_weight_kg=roasted_weight,
                        loss_rate_percent=round(loss_rate, 2),
                        expected_loss_rate_percent=17.0,  # 기본값
                        loss_variance_percent=round(loss_rate - 17.0, 2),
                        roasting_month=month_str,
                        roasting_date=datetime.now().date(),
                        notes=f"마이그레이션 완료 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )

                    db_session.add(log)
                    inserted_count += 1
                    total_raw += raw_weight
                    total_roasted += roasted_weight

                    # 10건마다 로깅
                    if inserted_count % 10 == 0:
                        logger.info(f"처리 중: {inserted_count}/{len(df)}")

                # Step 7: 커밋
                db_session.commit()

                result['success'] = True
                result['inserted_count'] = inserted_count
                result['total_raw_weight'] = round(total_raw, 2)
                result['total_roasted_weight'] = round(total_roasted, 2)

                logger.info(f"마이그레이션 완료: {inserted_count}개 행 삽입")

            except Exception as e:
                db_session.rollback()
                result['errors'].append(f"마이그레이션 실패: {str(e)}")
                result['success'] = False
                logger.error(f"마이그레이션 중 오류: {str(e)}")
                raise

        except Exception as e:
            result['errors'].append(f"예외 발생: {str(e)}")
            result['success'] = False
            logger.error(f"예외: {str(e)}")

        return result

    @staticmethod
    def _normalize_data(df):
        """데이터 정규화"""

        # 컬럼명 정규화
        df.columns = df.columns.str.strip()

        # 공백 제거
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        # 천 단위 쉼표 제거
        for col in ['생두량(kg)', '로스팅량(kg)']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '')

        return df

    @staticmethod
    def _validate_columns(df, required_columns):
        """필수 컬럼 검증"""

        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"필수 컬럼 없음: {missing}")


# 사용 예시
if __name__ == "__main__":
    from app.models import create_engine, Base
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///Data/test_roasting_data.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    result = ExcelSyncService.migrate_roasting_logs(
        "분석결과.xlsx",
        session
    )

    print(result)
```

#### Step 2: 모델 정의 확인

```python
# app/models/roasting_log.py 생성/확인

from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

class RoastingLog(Base):
    __tablename__ = 'roasting_logs'

    id = Column(Integer, primary_key=True)
    bean_id = Column(Integer, ForeignKey('beans.id'), nullable=False)
    raw_weight_kg = Column(Numeric(10, 2), nullable=False)
    roasted_weight_kg = Column(Numeric(10, 2), nullable=False)
    loss_rate_percent = Column(Numeric(5, 2))
    expected_loss_rate_percent = Column(Numeric(5, 2), default=17.0)
    loss_variance_percent = Column(Numeric(5, 2))
    roasting_date = Column(Date, nullable=False)
    roasting_month = Column(String(7))  # 2025-10
    blend_recipe_version_id = Column(Integer, ForeignKey('blend_recipes.id'))
    notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계
    bean = relationship('Bean', back_populates='roasting_logs')
    blend_recipe = relationship('BlendRecipe')
```

---

### Day 2: 테스트 및 검증

#### Step 1: 테스트 환경에서 마이그레이션 실행

```bash
# 테스트 DB에서 마이그레이션 실행
./venv/bin/python -c "
from app.services.excel_sync import ExcelSyncService
from app.models import get_session

session = get_session()
result = ExcelSyncService.migrate_roasting_logs('분석결과.xlsx', session)
print('=== 마이그레이션 결과 ===')
print(f'성공: {result[\"success\"]}')
print(f'삽입: {result[\"inserted_count\"]}개')
print(f'생두량: {result[\"total_raw_weight\"]} kg')
print(f'로스팅량: {result[\"total_roasted_weight\"]} kg')
print(f'에러: {result[\"errors\"]}')
print(f'경고: {result[\"warnings\"]}')
"
```

#### Step 2: 검증 쿼리

```sql
-- Data/roasting_data.db에서 실행
-- 테스트 DB 검증

-- 행 수 검증
SELECT COUNT(*) as 행수 FROM roasting_logs;
-- 예상: 60행

-- 생두량 합계
SELECT SUM(raw_weight_kg) as 생두량합계 FROM roasting_logs;
-- 예상: 31,325.3 kg

-- 로스팅량 합계
SELECT SUM(roasted_weight_kg) as 로스팅량합계 FROM roasting_logs;
-- 예상: 26,000 kg

-- 평균 손실률
SELECT AVG(loss_rate_percent) as 평균손실률 FROM roasting_logs;
-- 예상: 17.0%

-- 원두별 행 수
SELECT bean_id, COUNT(*) as 행수 FROM roasting_logs GROUP BY bean_id;

-- 월별 행 수
SELECT roasting_month, COUNT(*) as 행수 FROM roasting_logs GROUP BY roasting_month;
```

#### Step 3: 데이터 정확성 검증

```python
# app/test_migration.py

import pandas as pd
from app.models import get_session, RoastingLog

# Excel과 DB 비교
df = pd.read_excel('분석결과.xlsx', sheet_name='Sheet1')
session = get_session()

excel_sum = df['생두량(kg)'].sum()
db_logs = session.query(RoastingLog).all()
db_sum = sum(log.raw_weight_kg for log in db_logs)

print(f"Excel 생두량: {excel_sum}")
print(f"DB 생두량: {db_sum}")
print(f"일치: {abs(excel_sum - float(db_sum)) < 0.1}")
```

---

### Day 3: 프로덕션 마이그레이션

#### Step 1: 최종 검증

```bash
# 이전 작업 완료 확인
- [ ] 테스트 DB 마이그레이션 성공
- [ ] 모든 검증 쿼리 통과
- [ ] 에러 없음
- [ ] 경고 3개 이내
- [ ] DB 백업 확인
```

#### Step 2: 프로덕션 마이그레이션 실행

```bash
./venv/bin/python -c "
from app.services.excel_sync import ExcelSyncService
from app.models import get_session

session = get_session()
result = ExcelSyncService.migrate_roasting_logs('분석결과.xlsx', session)

# 결과 저장
import json
with open('logs/migration_result_$(date +%Y%m%d_%H%M%S).json', 'w') as f:
    json.dump(result, f, indent=2)

print('마이그레이션 완료')
print(result)
"
```

#### Step 3: 사후 검증

```bash
# 프로덕션 DB 검증
./venv/bin/python -c "
from app.models import get_session, RoastingLog

session = get_session()
logs = session.query(RoastingLog).all()

print(f'총 레코드: {len(logs)}')
print(f'생두량: {sum(log.raw_weight_kg for log in logs):.1f} kg')
print(f'로스팅량: {sum(log.roasted_weight_kg for log in logs):.1f} kg')
print(f'평균 손실률: {sum(log.loss_rate_percent for log in logs) / len(logs):.1f}%')
"
```

#### Step 4: 롤백 계획 문서화

```markdown
# 롤백 절차 (비상 시)

## 방법 1: DB 스냅샷 복원 (권장)
1. 실행: `cp Data/backups/roasting_data_before_migration_*.db Data/roasting_data.db`
2. 시간: 1분 내

## 방법 2: SQL 삭제 (추가 데이터 있을 경우)
1. DELETE FROM roasting_logs WHERE created_at > '2025-10-29';
2. 주의: 다른 로스팅 기록 확인

## 방법 3: Git 복원
1. `git checkout HEAD -- Data/roasting_data.db`
2. 주의: 이전 Git 커밋에 DB가 있어야 함
```

---

## T1-2: 원두 마스터 데이터 설정 (1일)

### 목표
13종 원두 정보를 beans 테이블에 입력

### Day 4: 원두 데이터 입력

#### Step 1: 원두 데이터 정의

```python
# app/utils/bean_data.py

BEANS_MASTER_DATA = [
    {
        'no': 1,
        'name': '마사이',
        'country_code': 'ETH',
        'country_name': '에티오피아',
        'roast_level': 'Normal',
        'description': '화려한 꽃향과 신맛',
        'price_per_kg': 30000,
        'status': 'active'
    },
    {
        'no': 2,
        'name': '안티구아',
        'country_code': 'GUA',
        'country_name': '과테말라',
        'roast_level': 'Normal',
        'description': '초콜릿향과 부드러움',
        'price_per_kg': 25000,
        'status': 'active'
    },
    {
        'no': 3,
        'name': '모모라',
        'country_code': 'ETH',
        'country_name': '에티오피아',
        'roast_level': 'Normal',
        'description': '과일향',
        'price_per_kg': 20000,
        'status': 'active'
    },
    {
        'no': 4,
        'name': 'g4',
        'country_code': 'KEN',
        'country_name': '케냐',
        'roast_level': 'Normal',
        'description': '균형잡힌 맛',
        'price_per_kg': 18000,
        'status': 'active'
    },
    {
        'no': 5,
        'name': '브라질',
        'country_code': 'BRA',
        'country_name': '브라질',
        'roast_level': 'Normal',
        'description': '너트향과 바디감',
        'price_per_kg': 15000,
        'status': 'active'
    },
    {
        'no': 6,
        'name': '콜롬비아',
        'country_code': 'COL',
        'country_name': '콜롬비아',
        'roast_level': 'Normal',
        'description': '밸런스 잡힌 맛',
        'price_per_kg': 17000,
        'status': 'active'
    },
    # 7-13번 추가 예정 (향후 원두)
    {
        'no': 7,
        'name': '예약원두7',
        'country_code': 'TBD',
        'country_name': '미정',
        'roast_level': 'Normal',
        'description': '추후 추가',
        'price_per_kg': 0,
        'status': 'inactive'
    },
    # ... 8~13 유사
]
```

#### Step 2: 원두 데이터 입력 스크립트

```python
# app/scripts/insert_beans.py

from app.models import get_session, Bean
from app.utils.bean_data import BEANS_MASTER_DATA

def insert_beans():
    session = get_session()

    try:
        for bean_data in BEANS_MASTER_DATA:
            # 중복 확인
            existing = session.query(Bean).filter_by(
                name=bean_data['name']
            ).first()

            if existing:
                print(f"이미 존재: {bean_data['name']}")
                continue

            # 새 Bean 생성
            bean = Bean(
                no=bean_data['no'],
                name=bean_data['name'],
                country_code=bean_data['country_code'],
                description=bean_data['description'],
                price_per_kg=bean_data['price_per_kg'],
                status=bean_data['status']
            )

            session.add(bean)
            print(f"추가: {bean_data['name']}")

        session.commit()
        print(f"✓ {len(BEANS_MASTER_DATA)}개 원두 추가 완료")

    except Exception as e:
        session.rollback()
        print(f"✗ 오류: {str(e)}")

if __name__ == "__main__":
    insert_beans()
```

#### Step 3: 실행 및 검증

```bash
# 실행
./venv/bin/python app/scripts/insert_beans.py

# 검증
./venv/bin/python -c "
from app.models import get_session, Bean

session = get_session()
beans = session.query(Bean).all()

print(f'총 원두: {len(beans)}')
for bean in beans:
    print(f'  {bean.no}. {bean.name} - ₩{bean.price_per_kg}/kg')
"
```

---

## T1-3: 블렌드 혼합률 설정 (1일)

### 목표
풀문, 뉴문 블렌드의 혼합률(%) 설정

### Day 5: 블렌드 및 레시피 설정

#### Step 1: 블렌드 데이터 정의

```python
# app/utils/blend_data.py

BLENDS_DATA = [
    {
        'name': 'Full Moon',
        'description': '풀문 블렌드',
        'loss_rate_percent': 17.0,
        'standard_selling_price': 22000,
        'recipes': [
            {'bean_name': '마사이', 'blending_ratio_percent': 40},
            {'bean_name': '안티구아', 'blending_ratio_percent': 40},
            {'bean_name': '모모라', 'blending_ratio_percent': 10},
            {'bean_name': 'g4', 'blending_ratio_percent': 10},
        ]
    },
    {
        'name': 'New Moon',
        'description': '뉴문 블렌드',
        'loss_rate_percent': 17.0,
        'standard_selling_price': 0,  # TBD
        'recipes': [
            {'bean_name': '브라질', 'blending_ratio_percent': 60},
            {'bean_name': '콜롬비아', 'blending_ratio_percent': 30},
            {'bean_name': 'g4', 'blending_ratio_percent': 10},
        ]
    }
]
```

#### Step 2: 블렌드 및 레시피 삽입

```python
# app/scripts/insert_blends.py

from app.models import get_session, Blend, BlendRecipe, Bean
from app.utils.blend_data import BLENDS_DATA
from datetime import datetime

def insert_blends():
    session = get_session()

    try:
        for blend_data in BLENDS_DATA:
            # 블렌드 생성/확인
            blend = session.query(Blend).filter_by(
                name=blend_data['name']
            ).first()

            if not blend:
                blend = Blend(
                    name=blend_data['name'],
                    description=blend_data['description'],
                    loss_rate_percent=blend_data['loss_rate_percent'],
                    standard_selling_price=blend_data['standard_selling_price']
                )
                session.add(blend)
                session.flush()  # ID 할당
                print(f"블렌드 추가: {blend.name}")

            # 기존 레시피 삭제
            session.query(BlendRecipe).filter_by(blend_id=blend.id).delete()

            # 레시피 추가
            sort_order = 1
            for recipe_data in blend_data['recipes']:
                bean = session.query(Bean).filter_by(
                    name=recipe_data['bean_name']
                ).first()

                if not bean:
                    print(f"✗ 원두 없음: {recipe_data['bean_name']}")
                    continue

                recipe = BlendRecipe(
                    blend_id=blend.id,
                    bean_id=bean.id,
                    blending_ratio_percent=recipe_data['blending_ratio_percent'],
                    version=1,
                    effective_date=datetime.now().date(),
                    is_current=True,
                    sort_order=sort_order
                )
                session.add(recipe)
                sort_order += 1

            print(f"레시피 추가: {blend.name}")

        session.commit()
        print(f"✓ 블렌드 설정 완료")

    except Exception as e:
        session.rollback()
        print(f"✗ 오류: {str(e)}")

if __name__ == "__main__":
    insert_blends()
```

#### Step 3: 검증

```bash
./venv/bin/python -c "
from app.models import get_session, Blend, BlendRecipe, Bean

session = get_session()
blends = session.query(Blend).all()

for blend in blends:
    print(f'블렌드: {blend.name}')
    recipes = session.query(BlendRecipe).filter_by(blend_id=blend.id).all()
    total_ratio = 0
    for recipe in recipes:
        bean = session.query(Bean).get(recipe.bean_id)
        print(f'  - {bean.name}: {recipe.blending_ratio_percent}%')
        total_ratio += recipe.blending_ratio_percent
    print(f'  합계: {total_ratio}% (검증: {\"✓\" if total_ratio == 100 else \"✗\"})')
"
```

---

## T1-4: 원가 정보 입력 (2일)

이미 T1-2에서 Bean.price_per_kg를 입력했으므로, 추가로:
- Blend.standard_selling_price 확정
- 필요시 원가 조정

**Day 6~7: 스킵 (이미 진행됨)**

---

## T1-5: 데이터 검증 및 정제 (2일)

### Day 8~9: 전체 검증

#### Step 1: 데이터 완전성 검증

```python
# app/scripts/validate_phase1_data.py

from app.models import get_session, RoastingLog, Bean, Blend, BlendRecipe

def validate_phase1():
    session = get_session()
    errors = []
    warnings = []

    print("=" * 50)
    print("Phase 1 데이터 검증")
    print("=" * 50)

    # 1. 로스팅 기록 검증
    logs = session.query(RoastingLog).all()
    print(f"\n✓ 로스팅 기록: {len(logs)}개")

    if len(logs) != 60:
        warnings.append(f"로스팅 기록: {len(logs)}개 (예상 60개)")

    raw_sum = sum(log.raw_weight_kg for log in logs)
    roasted_sum = sum(log.roasted_weight_kg for log in logs)

    print(f"  생두량: {raw_sum:.1f} kg (예상 31,325.3 kg)")
    print(f"  로스팅량: {roasted_sum:.1f} kg (예상 26,000 kg)")

    if abs(raw_sum - 31325.3) > 0.5:
        errors.append(f"생두량 불일치: {raw_sum}")

    if abs(roasted_sum - 26000) > 0.5:
        errors.append(f"로스팅량 불일치: {roasted_sum}")

    # 2. 원두 검증
    beans = session.query(Bean).all()
    print(f"\n✓ 원두: {len(beans)}개")

    for bean in beans[:6]:  # 활성 원두만
        logs_for_bean = session.query(RoastingLog).filter_by(bean_id=bean.id).all()
        if len(logs_for_bean) == 0:
            warnings.append(f"원두 '{bean.name}'의 로스팅 기록 없음")

    # 3. 블렌드 검증
    blends = session.query(Blend).all()
    print(f"\n✓ 블렌드: {len(blends)}개")

    for blend in blends:
        recipes = session.query(BlendRecipe).filter_by(blend_id=blend.id).all()
        total_ratio = sum(r.blending_ratio_percent for r in recipes)
        print(f"  {blend.name}: {total_ratio}% (검증: {' ✓' if total_ratio == 100 else '✗'})")

        if total_ratio != 100:
            errors.append(f"블렌드 '{blend.name}': 혼합률 {total_ratio}% (100% 필수)")

    # 결과 출력
    print("\n" + "=" * 50)
    print(f"에러: {len(errors)}")
    for error in errors:
        print(f"  ✗ {error}")

    print(f"경고: {len(warnings)}")
    for warning in warnings:
        print(f"  ⚠️  {warning}")

    print("=" * 50)

    return len(errors) == 0

if __name__ == "__main__":
    success = validate_phase1()
    exit(0 if success else 1)
```

#### Step 2: 실행

```bash
./venv/bin/python app/scripts/validate_phase1_data.py
```

---

## T1-6: 손실률 임계값 설정 & 이상 탐지 규칙 (1일)

### Day 10: 손실률 설정

#### Step 1: 손실률 임계값 설정

```python
# app/utils/loss_rate_config.py

LOSS_RATE_CONFIG = {
    'default': {
        'expected': 17.0,
        'min_threshold': 16.0,
        'max_threshold': 18.0,
        'warning_threshold': 15.0,
        'warning_threshold_high': 19.0,
    },
    'by_roast_level': {
        'White': {
            'expected': 12.0,
            'min_threshold': 10.0,
            'max_threshold': 14.0,
        },
        'Normal': {
            'expected': 17.0,
            'min_threshold': 16.0,
            'max_threshold': 18.0,
        },
        'Dark': {
            'expected': 20.0,
            'min_threshold': 18.0,
            'max_threshold': 22.0,
        },
    }
}
```

#### Step 2: 이상 탐지 로직

```python
# app/services/loss_rate_analyzer.py

from app.models import RoastingLog, LossRateWarning
from app.utils.loss_rate_config import LOSS_RATE_CONFIG
from sqlalchemy.orm import Session

class LossRateAnalyzer:
    """손실률 이상 탐지"""

    @staticmethod
    def check_loss_rate(roasting_log: RoastingLog, session: Session):
        """로스팅 기록의 손실률 검증 및 알림 생성"""

        config = LOSS_RATE_CONFIG['default']
        actual = roasting_log.loss_rate_percent
        expected = config['expected']
        variance = actual - expected

        # 임계값 확인
        if actual < config['min_threshold'] or actual > config['max_threshold']:
            # 경고 생성
            warning = LossRateWarning(
                roasting_log_id=roasting_log.id,
                bean_id=roasting_log.bean_id,
                roasting_month=roasting_log.roasting_month,
                actual_loss_rate=actual,
                expected_loss_rate=expected,
                variance_percent=variance,
                status='new',
                notes=f"손실률 이상: {actual:.1f}% ({variance:+.1f}%)"
            )
            session.add(warning)
            session.commit()

            return {
                'warning': True,
                'severity': 'high' if abs(variance) > 2 else 'medium',
                'message': f"손실률 {actual:.1f}% (예상 {expected:.1f}%)"
            }

        return {
            'warning': False,
            'message': f"정상 손실률: {actual:.1f}%"
        }
```

---

## ✅ Phase 1 완료 체크리스트

```
Day 1~3: T1-1 마이그레이션
☐ excel_sync.py 작성
☐ 테스트 DB 마이그레이션 성공
☐ 모든 검증 쿼리 통과
☐ 프로덕션 마이그레이션 실행
☐ 마이그레이션 결과 로그 저장

Day 4: T1-2 원두 설정
☐ bean_data.py 정의
☐ insert_beans.py 실행
☐ 13종 원두 확인

Day 5: T1-3 블렌드 설정
☐ blend_data.py 정의
☐ insert_blends.py 실행
☐ 풀문, 뉴문 혼합률 확인 (각 100%)

Day 6~7: T1-4 원가 입력
☐ 원두별 생두원가 설정 (완료)
☐ 블렌드별 판매가 설정 (완료)

Day 8~9: T1-5 데이터 검증
☐ validate_phase1_data.py 실행
☐ 모든 검증 통과
☐ 에러 0개, 경고 최소화

Day 10: T1-6 손실률 설정
☐ loss_rate_config.py 정의
☐ LossRateAnalyzer 구현
☐ 이상 탐지 규칙 테스트

최종 산출물:
✓ roasting_logs: 60개 레코드
✓ beans: 13종 (6종 활성, 7종 비활성)
✓ blends: 2개 (풀문, 뉴문)
✓ blend_recipes: 7개 (각 블렌드별 구성)
✓ 손실률 임계값 설정 완료
✓ 마이그레이션 로그 저장
```

---

## 📝 주의사항

1. **백업 확인**: Phase 1 시작 전 필수 백업 3개 생성
2. **테스트 우선**: 프로덕션 전 테스트 DB에서 100% 성공 확인
3. **데이터 검증**: 각 Step 후 검증 쿼리 실행
4. **롤백 준비**: 비상 상황 대비 롤백 절차 숙지
5. **로깅**: 모든 마이그레이션 결과 로그 저장

---

**Phase 1 완료 예상일:** 2025-11-08
**다음 Phase:** Phase 2 - 백엔드 서비스 개발
