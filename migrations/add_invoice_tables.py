"""
거래 명세서 이미지 자동 입고 기능 - 데이터베이스 마이그레이션

추가되는 테이블:
- invoices: 거래 명세서 메타데이터
- invoice_items: 명세서 항목 (다중 원두)
- invoice_learning: 학습 데이터 (사용자 수정 내역)

실행 방법:
    ./venv/bin/python migrations/add_invoice_tables.py
"""

import sys
import os
import shutil
from datetime import datetime

# 프로젝트 루트를 sys.path에 추가
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'app'))

from models.database import Base, engine, SessionLocal, DATABASE_PATH
from models.invoice import Invoice, InvoiceItem, InvoiceLearning
from sqlalchemy import text, inspect


def backup_database():
    """데이터베이스 백업"""
    if not os.path.exists(DATABASE_PATH):
        print("⚠️  데이터베이스 파일이 없습니다. 백업 생략.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{DATABASE_PATH}.backup_{timestamp}"

    try:
        shutil.copy2(DATABASE_PATH, backup_path)
        print(f"✅ 데이터베이스 백업 완료: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ 백업 실패: {str(e)}")
        return None


def check_table_exists(table_name):
    """테이블 존재 여부 확인"""
    db = SessionLocal()
    try:
        result = db.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"))
        exists = result.fetchone() is not None
        return exists
    finally:
        db.close()


def add_column_if_not_exists(table_name, column_name, column_type):
    """컬럼이 없으면 추가"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]

    if column_name in columns:
        print(f"ℹ️  {table_name}.{column_name} 컬럼이 이미 존재합니다.")
        return True

    try:
        db = SessionLocal()
        db.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
        db.commit()
        db.close()
        print(f"✅ {table_name}.{column_name} 컬럼 추가 완료")
        return True
    except Exception as e:
        print(f"❌ 컬럼 추가 실패: {str(e)}")
        return False


def migrate():
    """마이그레이션 실행"""
    print("=" * 80)
    print("마이그레이션: 거래 명세서 이미지 자동 입고 기능")
    print("=" * 80)
    print()

    # 1. 데이터베이스 백업
    print("📦 Step 1: 데이터베이스 백업")
    print("-" * 80)
    backup_path = backup_database()
    print()

    # 2. 새 테이블 생성
    print("🔧 Step 2: 새 테이블 생성")
    print("-" * 80)
    try:
        # invoices 테이블 생성
        if not check_table_exists('invoices'):
            Invoice.__table__.create(bind=engine, checkfirst=True)
            print("✅ invoices 테이블 생성 완료")
        else:
            print("ℹ️  invoices 테이블이 이미 존재합니다.")

        # invoice_items 테이블 생성
        if not check_table_exists('invoice_items'):
            InvoiceItem.__table__.create(bind=engine, checkfirst=True)
            print("✅ invoice_items 테이블 생성 완료")
        else:
            print("ℹ️  invoice_items 테이블이 이미 존재합니다.")

        # invoice_learning 테이블 생성
        if not check_table_exists('invoice_learning'):
            InvoiceLearning.__table__.create(bind=engine, checkfirst=True)
            print("✅ invoice_learning 테이블 생성 완료")
        else:
            print("ℹ️  invoice_learning 테이블이 이미 존재합니다.")

    except Exception as e:
        print(f"❌ 테이블 생성 실패: {str(e)}")
        if backup_path:
            print(f"💡 백업 파일로 복구 가능: {backup_path}")
        return False

    print()

    # 3. Transaction 테이블에 invoice_item_id 컬럼 추가
    print("🔧 Step 3: Transaction 테이블 확장")
    print("-" * 80)
    if check_table_exists('transactions'):
        add_column_if_not_exists('transactions', 'invoice_item_id', 'INTEGER')
    else:
        print("⚠️  transactions 테이블이 없습니다. 컬럼 추가 생략.")

    print()

    # 4. 테이블 확인
    print("🔍 Step 4: 테이블 확인")
    print("-" * 80)
    tables = ['invoices', 'invoice_items', 'invoice_learning']
    all_ok = True

    for table_name in tables:
        exists = check_table_exists(table_name)
        if exists:
            print(f"✅ {table_name} - 존재")
        else:
            print(f"❌ {table_name} - 없음")
            all_ok = False

    print()

    # 5. 마이그레이션 완료
    print("=" * 80)
    if all_ok:
        print("✅ 마이그레이션 성공!")
        print()
        print("생성된 테이블:")
        print("  - invoices (거래 명세서)")
        print("  - invoice_items (명세서 항목)")
        print("  - invoice_learning (학습 데이터)")
        print()
        if backup_path:
            print(f"백업 파일: {backup_path}")
    else:
        print("❌ 마이그레이션 실패!")
        if backup_path:
            print(f"💡 백업 파일로 복구 가능: {backup_path}")

    print("=" * 80)

    return all_ok


if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)
