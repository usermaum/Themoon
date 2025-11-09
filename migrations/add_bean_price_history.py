"""
원두 가격 변경 이력 테이블 추가 마이그레이션

실행 방법:
    ./venv/bin/python migrations/add_bean_price_history.py
"""

import sys
import os

# 프로젝트 루트를 sys.path에 추가
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'app'))

from models.database import Base, engine, SessionLocal
from models.database import BeanPriceHistory  # 새 모델 import
from sqlalchemy import text

def migrate():
    """bean_price_history 테이블 생성"""
    print("=" * 60)
    print("마이그레이션: BeanPriceHistory 테이블 추가")
    print("=" * 60)

    try:
        # 새 테이블만 생성 (기존 테이블은 그대로 유지)
        BeanPriceHistory.__table__.create(bind=engine, checkfirst=True)
        print("✅ bean_price_history 테이블 생성 완료")

        # 테이블 확인
        db = SessionLocal()
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='bean_price_history'"))
        table_exists = result.fetchone() is not None
        db.close()

        if table_exists:
            print("✅ 테이블 존재 확인: bean_price_history")
        else:
            print("❌ 테이블 생성 실패")
            return False

        print("=" * 60)
        print("마이그레이션 완료!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"❌ 마이그레이션 실패: {str(e)}")
        return False

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)
