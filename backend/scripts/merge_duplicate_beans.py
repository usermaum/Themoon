#!/usr/bin/env python3
"""
중복 생두 통합 스크립트

통합 대상:
- ID=18 (Colombia Supremo Huila) → ID=8 (후일라)
- ID=19 (Colombia Supremo Popayan sugarcane decaf) → ID=14 (디카페 SM)

처리 사항:
1. InventoryLog의 bean_id 업데이트
2. InboundItem의 bean_name 업데이트 (필요시)
3. Bean 재고 통합
4. 중복 Bean 레코드 삭제
"""

import sys
import os

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models.bean import Bean
from app.models.inventory_log import InventoryLog
from app.models.inbound_item import InboundItem


def merge_duplicate_beans():
    db = SessionLocal()

    try:
        # 중복 쌍 정의 (old_id, new_id, description)
        duplicate_pairs = [
            (18, 8, "Colombia Supremo Huila"),
            (19, 14, "Popayan Sugarcane Decaf"),
        ]

        print("=" * 60)
        print("중복 생두 통합 시작")
        print("=" * 60)
        print()

        for old_id, new_id, desc in duplicate_pairs:
            print(f"📦 {desc}: ID={old_id} → ID={new_id}")

            # 1. Bean 레코드 가져오기
            old_bean = db.query(Bean).filter(Bean.id == old_id).first()
            new_bean = db.query(Bean).filter(Bean.id == new_id).first()

            if not old_bean:
                print(f"   ⚠️  경고: ID={old_id} 생두를 찾을 수 없습니다.")
                continue

            if not new_bean:
                print(f"   ⚠️  경고: ID={new_id} 생두를 찾을 수 없습니다.")
                continue

            print(f"   삭제 대상: {old_bean.name} ({old_bean.quantity_kg}kg)")
            print(f"   통합 대상: {new_bean.name} ({new_bean.quantity_kg}kg)")

            # 2. InventoryLog 업데이트
            logs = db.query(InventoryLog).filter(InventoryLog.bean_id == old_id).all()
            for log in logs:
                log.bean_id = new_id
                print(f"   ✅ InventoryLog ID={log.id} 업데이트 (bean_id: {old_id} → {new_id})")

            # 3. InboundItem 업데이트 (bean_name으로 저장되어 있는 경우)
            # InboundItem은 bean_name을 사용하므로 name_en으로 업데이트 필요
            items = db.query(InboundItem).filter(InboundItem.bean_name == old_bean.name).all()
            for item in items:
                # new_bean의 name_en이 있으면 사용, 없으면 name 사용
                new_name = new_bean.name_en if new_bean.name_en else new_bean.name
                item.bean_name = new_name
                print(f"   ✅ InboundItem ID={item.id} 업데이트 (bean_name: '{old_bean.name}' → '{new_name}')")

            # 4. 재고 통합
            old_qty = old_bean.quantity_kg
            new_bean.quantity_kg += old_qty
            print(f"   ✅ 재고 통합: {new_bean.quantity_kg - old_qty}kg + {old_qty}kg = {new_bean.quantity_kg}kg")

            # 5. 중복 Bean 삭제
            db.delete(old_bean)
            print(f"   ✅ Bean ID={old_id} 삭제")
            print()

        # 커밋
        db.commit()
        print("=" * 60)
        print("✅ 중복 생두 통합 완료!")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"❌ 오류 발생: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    merge_duplicate_beans()
