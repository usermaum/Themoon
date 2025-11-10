"""
데이터베이스 마이그레이션 스크립트 v0.23.0
원가계산기 고도화 - Phase 1: 재고 관리 시스템

변경사항:
1. Bean 테이블: 통계 필드 추가 (brand, avg_loss_rate, std_loss_rate, total_roasted_count, last_roasted_date)
2. Inventory 테이블: inventory_type 필드 추가 (생두/원두 구분)
3. Transaction 테이블: inventory_type, roasting_log_id 필드 추가
"""

import sys
import os
from datetime import datetime

# 프로젝트 루트 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.models.database import SessionLocal, Bean, Inventory, Transaction, RoastingLog
import sqlite3


def backup_database():
    """데이터베이스 백업"""
    data_dir = os.path.join(project_root, "data")
    db_path = os.path.join(data_dir, "roasting_data.db")
    backup_path = os.path.join(data_dir, f"roasting_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")

    if os.path.exists(db_path):
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✅ 데이터베이스 백업 완료: {backup_path}")
        return backup_path
    else:
        print("⚠️ 데이터베이스 파일이 존재하지 않습니다.")
        return None


def add_columns_to_tables():
    """테이블에 새 컬럼 추가 및 Inventory 테이블 재생성 (SQLite 제약)"""
    data_dir = os.path.join(project_root, "data")
    db_path = os.path.join(data_dir, "roasting_data.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n📝 Step 1: 테이블 스키마 확장 중...")

    try:
        # Bean 테이블에 새 컬럼 추가
        print("  - Bean 테이블 확장 중...")
        cursor.execute("PRAGMA table_info(beans)")
        existing_columns = [col[1] for col in cursor.fetchall()]

        if 'brand' not in existing_columns:
            cursor.execute("ALTER TABLE beans ADD COLUMN brand VARCHAR(100)")
            print("    ✅ brand 컬럼 추가")

        if 'avg_loss_rate' not in existing_columns:
            cursor.execute("ALTER TABLE beans ADD COLUMN avg_loss_rate FLOAT")
            print("    ✅ avg_loss_rate 컬럼 추가")

        if 'std_loss_rate' not in existing_columns:
            cursor.execute("ALTER TABLE beans ADD COLUMN std_loss_rate FLOAT")
            print("    ✅ std_loss_rate 컬럼 추가")

        if 'total_roasted_count' not in existing_columns:
            cursor.execute("ALTER TABLE beans ADD COLUMN total_roasted_count INTEGER DEFAULT 0")
            print("    ✅ total_roasted_count 컬럼 추가")

        if 'last_roasted_date' not in existing_columns:
            cursor.execute("ALTER TABLE beans ADD COLUMN last_roasted_date DATE")
            print("    ✅ last_roasted_date 컬럼 추가")

        # Inventory 테이블 재생성 (UNIQUE 제약 변경을 위해)
        print("  - Inventory 테이블 재생성 중...")

        # 기존 데이터 백업
        cursor.execute("CREATE TEMPORARY TABLE inventory_backup AS SELECT * FROM inventory")
        print("    ✅ 기존 데이터 백업")

        # 기존 테이블 삭제
        cursor.execute("DROP TABLE inventory")
        print("    ✅ 기존 테이블 삭제")

        # 새 테이블 생성 (unique constraint 변경)
        cursor.execute("""
            CREATE TABLE inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bean_id INTEGER NOT NULL,
                inventory_type VARCHAR(20) NOT NULL DEFAULT 'RAW_BEAN',
                quantity_kg FLOAT DEFAULT 0.0,
                min_quantity_kg FLOAT DEFAULT 5.0,
                max_quantity_kg FLOAT DEFAULT 50.0,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bean_id) REFERENCES beans(id),
                UNIQUE (bean_id, inventory_type)
            )
        """)
        print("    ✅ 새 테이블 생성 (unique constraint: bean_id + inventory_type)")

        # 기존 데이터 복원 (inventory_type = 'RAW_BEAN'으로 설정)
        cursor.execute("""
            INSERT INTO inventory (id, bean_id, inventory_type, quantity_kg, min_quantity_kg, max_quantity_kg, last_updated, created_at)
            SELECT id, bean_id, 'RAW_BEAN', quantity_kg, min_quantity_kg, max_quantity_kg, last_updated, created_at
            FROM inventory_backup
        """)
        print("    ✅ 기존 데이터 복원 (RAW_BEAN으로 설정)")

        # 임시 테이블 삭제
        cursor.execute("DROP TABLE inventory_backup")

        # Transaction 테이블에 새 컬럼 추가
        print("  - Transaction 테이블 확장 중...")
        cursor.execute("PRAGMA table_info(transactions)")
        existing_columns = [col[1] for col in cursor.fetchall()]

        if 'inventory_type' not in existing_columns:
            cursor.execute("ALTER TABLE transactions ADD COLUMN inventory_type VARCHAR(20)")
            print("    ✅ inventory_type 컬럼 추가")

        if 'roasting_log_id' not in existing_columns:
            cursor.execute("ALTER TABLE transactions ADD COLUMN roasting_log_id INTEGER")
            print("    ✅ roasting_log_id 컬럼 추가")

        conn.commit()
        print("✅ Step 1 완료: 테이블 스키마 확장 성공\n")

    except Exception as e:
        conn.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        conn.close()


def migrate_existing_inventory_data():
    """ROASTED_BEAN 재고 항목 추가 (RAW_BEAN은 Step 1에서 이미 처리됨)"""
    db = SessionLocal()

    try:
        print("📝 Step 2: ROASTED_BEAN 재고 항목 추가 중...")

        # 모든 Bean 조회
        beans = db.query(Bean).all()
        print(f"  - 총 {len(beans)}개 원두 발견")

        for bean in beans:
            # ROASTED_BEAN 재고 항목이 있는지 확인
            roasted_inv = db.query(Inventory).filter(
                Inventory.bean_id == bean.id,
                Inventory.inventory_type == "ROASTED_BEAN"
            ).first()

            if not roasted_inv:
                # ROASTED_BEAN 재고 항목 생성
                roasted_inv = Inventory(
                    bean_id=bean.id,
                    inventory_type="ROASTED_BEAN",
                    quantity_kg=0.0,
                    min_quantity_kg=5.0,
                    max_quantity_kg=50.0
                )
                db.add(roasted_inv)
                print(f"    ✅ {bean.name}: ROASTED_BEAN 재고 항목 생성")
            else:
                print(f"    ⚠️ {bean.name}: ROASTED_BEAN 재고 이미 존재")

        db.commit()
        print("✅ Step 2 완료: 재고 데이터 마이그레이션 성공\n")

    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()


def calculate_bean_statistics():
    """기존 로스팅 기록을 기반으로 Bean 통계 계산"""
    db = SessionLocal()

    try:
        print("📝 Step 3: 원두별 손실률 통계 계산 중...")

        beans = db.query(Bean).all()

        for bean in beans:
            # 해당 원두의 로스팅 기록 조회
            roasting_logs = db.query(RoastingLog).filter(
                RoastingLog.bean_id == bean.id
            ).all()

            if roasting_logs:
                # 손실률 리스트
                loss_rates = [log.loss_rate_percent for log in roasting_logs]

                # 평균 계산
                avg_loss = sum(loss_rates) / len(loss_rates)

                # 표준편차 계산
                variance = sum((x - avg_loss) ** 2 for x in loss_rates) / len(loss_rates)
                std_loss = variance ** 0.5

                # 마지막 로스팅 날짜
                last_date = max(log.roasting_date for log in roasting_logs)

                # Bean 통계 업데이트
                bean.avg_loss_rate = round(avg_loss, 2)
                bean.std_loss_rate = round(std_loss, 2)
                bean.total_roasted_count = len(roasting_logs)
                bean.last_roasted_date = last_date

                print(f"    ✅ {bean.name}: 평균 {avg_loss:.2f}%, 표준편차 {std_loss:.2f}%, {len(roasting_logs)}회 로스팅")
            else:
                print(f"    ⚠️ {bean.name}: 로스팅 기록 없음")

        db.commit()
        print("✅ Step 3 완료: 통계 계산 성공\n")

    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise
    finally:
        db.close()


def verify_migration():
    """마이그레이션 결과 검증"""
    db = SessionLocal()

    try:
        print("📝 Step 4: 마이그레이션 결과 검증 중...")

        # Bean 통계 확인
        beans_with_stats = db.query(Bean).filter(Bean.avg_loss_rate.isnot(None)).count()
        total_beans = db.query(Bean).count()
        print(f"  - Bean 통계: {beans_with_stats}/{total_beans}개 원두에 통계 계산됨")

        # Inventory 확인
        raw_count = db.query(Inventory).filter(Inventory.inventory_type == "RAW_BEAN").count()
        roasted_count = db.query(Inventory).filter(Inventory.inventory_type == "ROASTED_BEAN").count()
        print(f"  - Inventory: RAW_BEAN {raw_count}개, ROASTED_BEAN {roasted_count}개")

        # 검증
        if raw_count == total_beans and roasted_count == total_beans:
            print("✅ Step 4 완료: 검증 성공\n")
            return True
        else:
            print("⚠️ Step 4 경고: 재고 항목 수가 예상과 다릅니다.\n")
            return False

    except Exception as e:
        print(f"❌ 검증 오류: {e}")
        return False
    finally:
        db.close()


def main():
    """메인 마이그레이션 실행"""
    print("=" * 70)
    print("  데이터베이스 마이그레이션 v0.23.0")
    print("  원가계산기 고도화 - Phase 1: 재고 관리 시스템")
    print("=" * 70)
    print()

    try:
        # 1. 백업
        backup_path = backup_database()
        if not backup_path:
            print("❌ 백업 실패. 마이그레이션을 중단합니다.")
            return

        # 2. 스키마 확장
        add_columns_to_tables()

        # 3. 데이터 마이그레이션
        migrate_existing_inventory_data()

        # 4. 통계 계산
        calculate_bean_statistics()

        # 5. 검증
        if verify_migration():
            print("=" * 70)
            print("  ✅ 마이그레이션 완료!")
            print("=" * 70)
            print(f"\n백업 파일: {backup_path}")
            print("문제 발생 시 백업 파일로 복원할 수 있습니다.")
        else:
            print("=" * 70)
            print("  ⚠️ 마이그레이션 완료 (경고 있음)")
            print("=" * 70)
            print(f"\n백업 파일: {backup_path}")

    except Exception as e:
        print("\n" + "=" * 70)
        print("  ❌ 마이그레이션 실패")
        print("=" * 70)
        print(f"\n오류: {e}")
        print("\n백업 파일로 복원하려면:")
        print(f"  cp {backup_path} {os.path.join(project_root, 'data', 'roasting_data.db')}")


if __name__ == "__main__":
    main()
