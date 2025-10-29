"""
테스트 데이터 생성 스크립트
Generate sample transaction data for testing
"""

import sys
import os
from datetime import datetime, timedelta

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import SessionLocal, Bean, Transaction
from sqlalchemy import func

def create_test_data():
    """Create sample transaction data for testing"""
    db = SessionLocal()

    try:
        # Get some beans for testing
        beans = db.query(Bean).filter(Bean.status == "active").limit(5).all()

        if not beans:
            print("❌ 활성 원두가 없습니다. 먼저 init_data.py를 실행하세요.")
            return

        # Generate sample transactions (last 30 days)
        base_date = datetime.now() - timedelta(days=30)

        print("\n📝 테스트 거래 데이터 생성 중...\n")

        transaction_count = 0

        for i in range(6):  # 6 weeks of data
            for bean in beans:
                # 입고 거래
                inflow = Transaction(
                    bean_id=bean.id,
                    transaction_type="입고",
                    quantity_kg=5.0 + (i * 0.5),  # 점진적으로 증가
                    price_per_unit=bean.price_per_kg,
                    total_amount=(5.0 + (i * 0.5)) * bean.price_per_kg,
                    description=f"{bean.name} 입고 (샘플)",
                    created_at=base_date + timedelta(days=i*5)
                )
                db.add(inflow)
                transaction_count += 1

                # 출고 거래 (입고 후 3일 뒤)
                outflow = Transaction(
                    bean_id=bean.id,
                    transaction_type="출고",
                    quantity_kg=3.0 + (i * 0.3),
                    price_per_unit=bean.price_per_kg,
                    total_amount=(3.0 + (i * 0.3)) * bean.price_per_kg,
                    description=f"{bean.name} 출고 (샘플)",
                    created_at=base_date + timedelta(days=i*5+3)
                )
                db.add(outflow)
                transaction_count += 1

        db.commit()

        # 통계 출력
        print(f"✅ {transaction_count}개의 테스트 거래 데이터 생성 완료!\n")

        # 요약 정보
        print("📊 생성된 데이터 요약:")
        print(f"  - 입고 거래: {db.query(func.count(Transaction.id)).filter(Transaction.transaction_type == '입고').scalar()}")
        print(f"  - 출고 거래: {db.query(func.count(Transaction.id)).filter(Transaction.transaction_type == '출고').scalar()}")
        print(f"  - 총 거래: {db.query(func.count(Transaction.id)).scalar()}")

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    create_test_data()
