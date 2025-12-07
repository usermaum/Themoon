"""
로컬 SQLite 데이터를 PostgreSQL로 마이그레이션

실행 방법:
cd backend
export DATABASE_URL="postgresql://user:password@host:port/dbname"
python scripts/migrate_to_postgres.py

또는 Render.com DATABASE_URL 사용:
DATABASE_URL="<Render.com DATABASE_URL>" python scripts/migrate_to_postgres.py
"""
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# backend 디렉토리를 sys.path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)

# 환경 변수 로드
env_path = os.path.join(backend_dir, ".env")
load_dotenv(env_path)

# DATABASE_URL 확인
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("❌ DATABASE_URL 환경변수가 설정되지 않았습니다.")
    print("사용법: DATABASE_URL='postgresql://...' python scripts/migrate_to_postgres.py")
    sys.exit(1)

# PostgreSQL URL 변환
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

print(f"🔗 연결 대상: {database_url[:30]}...")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.bean import Bean, BeanType, RoastProfile
from app.models.blend import Blend
from app.models.inventory_log import InventoryLog, InventoryChangeType

def migrate_data():
    """JSON 파일에서 데이터를 읽어 PostgreSQL로 마이그레이션"""

    # PostgreSQL 엔진 생성
    engine = create_engine(database_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # 기존 테이블 삭제 및 재생성
    print("🗑️  기존 테이블 삭제 중...")
    Base.metadata.drop_all(bind=engine)
    print("✅ 기존 테이블 삭제 완료")

    print("🔨 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✅ 테이블 생성 완료")

    # JSON 파일에서 데이터 로드
    data_file = os.path.join(backend_dir, "data_export.json")
    if not os.path.exists(data_file):
        print(f"❌ {data_file} 파일을 찾을 수 없습니다.")
        print("먼저 데이터를 추출해주세요:")
        print("  python -c \"[데이터 추출 스크립트]\"")
        sys.exit(1)

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📁 데이터 로드:")
    print(f"  - Beans: {len(data['beans'])}개")
    print(f"  - Blends: {len(data['blends'])}개")
    print(f"  - Inventory Logs: {len(data['inventory_logs'])}개")

    db = SessionLocal()

    try:
        # 1. Beans 마이그레이션
        print("🌱 Beans 마이그레이션 중...")
        bean_id_map = {}  # 로컬 ID → PostgreSQL ID 매핑

        for bean_data in data['beans']:
            old_id = bean_data['id']

            # BeanType enum 변환
            bean_type = bean_data['type']
            if isinstance(bean_type, str):
                bean_type = BeanType[bean_type] if hasattr(BeanType, bean_type) else BeanType.GREEN_BEAN

            # RoastProfile enum 변환 (있는 경우)
            roast_profile = bean_data.get('roast_profile')
            if roast_profile and isinstance(roast_profile, str):
                roast_profile = RoastProfile[roast_profile] if hasattr(RoastProfile, roast_profile) else None

            bean = Bean(
                name=bean_data['name'],
                type=bean_type,
                sku=bean_data.get('sku'),
                origin=bean_data.get('origin'),
                variety=bean_data.get('variety'),
                grade=bean_data.get('grade'),
                processing_method=bean_data.get('processing_method'),
                roast_profile=roast_profile,
                parent_bean_id=bean_data.get('parent_bean_id'),
                quantity_kg=bean_data['quantity_kg'],
                avg_price=bean_data['avg_price'],
                purchase_price_per_kg=bean_data.get('purchase_price_per_kg'),
                cost_price=bean_data.get('cost_price'),
                expected_loss_rate=bean_data.get('expected_loss_rate', 0.15),
                description=bean_data.get('description')
            )
            db.add(bean)
            db.flush()  # ID 생성
            bean_id_map[old_id] = bean.id

        print(f"✅ {len(data['beans'])}개 Bean 마이그레이션 완료")

        # 2. Blends 마이그레이션
        print("🌱 Blends 마이그레이션 중...")
        blend_id_map = {}  # 로컬 ID → PostgreSQL ID 매핑

        for blend_data in data['blends']:
            old_id = blend_data['id']

            # recipe의 bean_id 업데이트
            recipe = blend_data.get('recipe')
            if isinstance(recipe, str):
                recipe = json.loads(recipe)

            if recipe:
                for item in recipe:
                    old_bean_id = item['bean_id']
                    if old_bean_id in bean_id_map:
                        item['bean_id'] = bean_id_map[old_bean_id]

            blend = Blend(
                name=blend_data['name'],
                description=blend_data.get('description'),
                recipe=recipe,
                target_roast_level=blend_data.get('target_roast_level'),
                notes=blend_data.get('notes')
            )
            db.add(blend)
            db.flush()  # ID 생성
            blend_id_map[old_id] = blend.id

        print(f"✅ {len(data['blends'])}개 Blend 마이그레이션 완료")

        # 3. Inventory Logs 마이그레이션
        print("🌱 Inventory Logs 마이그레이션 중...")

        for log_data in data['inventory_logs']:
            old_bean_id = log_data['bean_id']

            # Bean ID 매핑
            new_bean_id = bean_id_map.get(old_bean_id)
            if not new_bean_id:
                print(f"⚠️  경고: Bean ID {old_bean_id}를 찾을 수 없습니다. 로그 건너뜀.")
                continue

            # InventoryChangeType enum 변환
            change_type = log_data['change_type']
            if isinstance(change_type, str):
                change_type = InventoryChangeType[change_type] if hasattr(InventoryChangeType, change_type) else InventoryChangeType.ADJUSTMENT

            log = InventoryLog(
                bean_id=new_bean_id,
                change_type=change_type,
                change_amount=log_data['change_amount'],
                current_quantity=log_data['current_quantity'],
                notes=log_data.get('notes')
            )
            db.add(log)

        print(f"✅ {len(data['inventory_logs'])}개 Inventory Log 마이그레이션 완료")

        # 커밋
        db.commit()
        print("🎉 모든 데이터 마이그레이션 완료!")

        # 최종 확인
        print("\n📊 마이그레이션 결과:")
        print(f"  - Beans: {db.query(Bean).count()}개")
        print(f"  - Blends: {db.query(Blend).count()}개")
        print(f"  - Inventory Logs: {db.query(InventoryLog).count()}개")

    except Exception as e:
        print(f"❌ 마이그레이션 오류: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("📦 SQLite → PostgreSQL 데이터 마이그레이션")
    print("=" * 60)
    migrate_data()
