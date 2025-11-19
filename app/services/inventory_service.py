"""
재고 관리 서비스
원가계산기 고도화 - Phase 1: 재고 관리 시스템

기능:
- 생두/원두 재고 조회
- 입고 처리
- 출고 처리
- 로스팅 시 재고 자동 연동
"""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List, Dict, Tuple
from models.database import Inventory, Transaction, Bean, RoastingLog


class InventoryType:
    """재고 유형 상수"""
    RAW_BEAN = "RAW_BEAN"  # 생두
    ROASTED_BEAN = "ROASTED_BEAN"  # 원두


class TransactionType:
    """거래 유형 상수"""
    PURCHASE = "입고"  # 입고 (생두 구매)
    ROASTING = "로스팅"  # 로스팅 (생두 → 원두)
    PRODUCTION = "생산"  # 생산 (로스팅 완료, 원두 증가)
    SALES = "판매출고"  # 판매출고
    GIFT = "증정출고"  # 증정출고
    WASTE = "폐기"  # 폐기
    ADJUSTMENT = "재고조정"  # 재고조정


class InventoryService:
    """재고 관리 서비스"""

    def __init__(self, db: Session):
        self.db = db

    # ═══════════════════════════════════════════════════════════════
    # 재고 조회
    # ═══════════════════════════════════════════════════════════════

    def get_inventory(
        self,
        bean_id: int,
        inventory_type: str = InventoryType.RAW_BEAN
    ) -> Optional[Inventory]:
        """
        특정 원두의 재고 조회

        Args:
            bean_id: 원두 ID
            inventory_type: 재고 유형 (RAW_BEAN or ROASTED_BEAN)

        Returns:
            Inventory 객체 또는 None
        """
        return self.db.query(Inventory).filter(
            Inventory.bean_id == bean_id,
            Inventory.inventory_type == inventory_type
        ).first()

    def get_all_inventory(self) -> List[Dict]:
        """
        모든 재고 조회 (원두별 생두/원두 재고)

        Returns:
            재고 정보 리스트
            [
                {
                    'bean_id': 1,
                    'bean_name': '예가체프',
                    'raw_bean_qty': 20.0,
                    'roasted_bean_qty': 10.5,
                    'total_qty': 30.5,
                    'raw_inventory': Inventory 객체,
                    'roasted_inventory': Inventory 객체
                },
                ...
            ]
        """
        beans = self.db.query(Bean).filter(Bean.status == "active").all()
        result = []

        for bean in beans:
            raw_inv = self.get_inventory(bean.id, InventoryType.RAW_BEAN)
            roasted_inv = self.get_inventory(bean.id, InventoryType.ROASTED_BEAN)

            raw_qty = raw_inv.quantity_kg if raw_inv else 0.0
            roasted_qty = roasted_inv.quantity_kg if roasted_inv else 0.0

            result.append({
                'bean_id': bean.id,
                'bean_name': bean.name,
                'bean_country': bean.country_name,
                'raw_bean_qty': raw_qty,
                'roasted_bean_qty': roasted_qty,
                'total_qty': raw_qty + roasted_qty,
                'raw_inventory': raw_inv,
                'roasted_inventory': roasted_inv,
                'bean': bean
            })

        return result

    def get_low_stock_items(self) -> List[Dict]:
        """
        저재고 항목 조회 (현재 재고 < 최소 재고)

        Returns:
            저재고 항목 리스트
        """
        inventories = self.db.query(Inventory).all()
        low_stock = []

        for inv in inventories:
            if inv.min_quantity_kg > 0 and inv.quantity_kg < inv.min_quantity_kg:
                bean = self.db.query(Bean).filter(Bean.id == inv.bean_id).first()
                low_stock.append({
                    'bean_name': bean.name if bean else "알 수 없음",
                    'inventory_type': inv.inventory_type,
                    'current_qty': inv.quantity_kg,
                    'min_qty': inv.min_quantity_kg,
                    'shortage': inv.min_quantity_kg - inv.quantity_kg,
                    'inventory': inv
                })

        return low_stock

    # ═══════════════════════════════════════════════════════════════
    # 재고 변경
    # ═══════════════════════════════════════════════════════════════

    def add_stock(
        self,
        bean_id: int,
        quantity_kg: float,
        inventory_type: str = InventoryType.RAW_BEAN,
        transaction_type: str = TransactionType.PURCHASE,
        price_per_kg: float = 0.0,
        notes: str = None,
        roasting_log_id: int = None
    ) -> Tuple[bool, str, Optional[Transaction]]:
        """
        재고 추가 (입고, 생산 등)

        Args:
            bean_id: 원두 ID
            quantity_kg: 수량 (kg)
            inventory_type: 재고 유형
            transaction_type: 거래 유형
            price_per_kg: kg당 가격
            notes: 비고
            roasting_log_id: 로스팅 기록 ID (있으면)

        Returns:
            (성공 여부, 메시지, Transaction 객체)
        """
        try:
            # 재고 조회 또는 생성
            inventory = self.get_inventory(bean_id, inventory_type)
            if not inventory:
                # 재고 항목이 없으면 생성
                inventory = Inventory(
                    bean_id=bean_id,
                    inventory_type=inventory_type,
                    quantity_kg=0.0,
                    min_quantity_kg=5.0,
                    max_quantity_kg=50.0
                )
                self.db.add(inventory)
                self.db.flush()

            # 재고 증가
            inventory.quantity_kg += quantity_kg
            inventory.last_updated = datetime.utcnow()

            # 거래 기록 생성
            transaction = Transaction(
                bean_id=bean_id,
                transaction_type=transaction_type,
                inventory_type=inventory_type,
                quantity_kg=quantity_kg,
                price_per_unit=price_per_kg,
                total_amount=quantity_kg * price_per_kg,
                roasting_log_id=roasting_log_id,
                notes=notes,
                created_at=datetime.utcnow()
            )
            self.db.add(transaction)

            self.db.commit()

            bean = self.db.query(Bean).filter(Bean.id == bean_id).first()
            bean_name = bean.name if bean else "알 수 없음"

            return True, f"✅ {bean_name} {inventory_type} 재고 {quantity_kg}kg 추가 완료", transaction

        except Exception as e:
            self.db.rollback()
            return False, f"❌ 재고 추가 실패: {str(e)}", None

    def reduce_stock(
        self,
        bean_id: int,
        quantity_kg: float,
        inventory_type: str = InventoryType.RAW_BEAN,
        transaction_type: str = TransactionType.SALES,
        notes: str = None,
        roasting_log_id: int = None,
        allow_negative: bool = False
    ) -> Tuple[bool, str, Optional[Transaction]]:
        """
        재고 차감 (출고, 로스팅 사용 등)

        Args:
            bean_id: 원두 ID
            quantity_kg: 수량 (kg)
            inventory_type: 재고 유형
            transaction_type: 거래 유형
            notes: 비고
            roasting_log_id: 로스팅 기록 ID (있으면)
            allow_negative: 마이너스 재고 허용 여부

        Returns:
            (성공 여부, 메시지, Transaction 객체)
        """
        try:
            # 재고 조회
            inventory = self.get_inventory(bean_id, inventory_type)
            if not inventory:
                return False, f"❌ 재고를 찾을 수 없습니다 (bean_id={bean_id}, type={inventory_type})", None

            # 재고 부족 확인
            if not allow_negative and inventory.quantity_kg < quantity_kg:
                return False, f"❌ 재고 부족: 현재 {inventory.quantity_kg}kg, 필요 {quantity_kg}kg", None

            # 재고 차감
            inventory.quantity_kg -= quantity_kg
            inventory.last_updated = datetime.utcnow()

            # 거래 기록 생성 (음수로 저장)
            transaction = Transaction(
                bean_id=bean_id,
                transaction_type=transaction_type,
                inventory_type=inventory_type,
                quantity_kg=-quantity_kg,  # 차감은 음수
                price_per_unit=0.0,
                total_amount=0.0,
                roasting_log_id=roasting_log_id,
                notes=notes,
                created_at=datetime.utcnow()
            )
            self.db.add(transaction)

            self.db.commit()

            bean = self.db.query(Bean).filter(Bean.id == bean_id).first()
            bean_name = bean.name if bean else "알 수 없음"

            return True, f"✅ {bean_name} {inventory_type} 재고 {quantity_kg}kg 차감 완료", transaction

        except Exception as e:
            self.db.rollback()
            return False, f"❌ 재고 차감 실패: {str(e)}", None

    # ═══════════════════════════════════════════════════════════════
    # 로스팅 시 재고 자동 연동
    # ═══════════════════════════════════════════════════════════════

    def process_roasting_transaction(
        self,
        bean_id: int,
        raw_weight_kg: float,
        roasted_weight_kg: float,
        roasting_log_id: int
    ) -> Tuple[bool, str]:
        """
        로스팅 시 재고 자동 연동
        - 생두 재고 차감
        - 원두 재고 증가

        Args:
            bean_id: 원두 ID
            raw_weight_kg: 생두 투입량 (kg)
            roasted_weight_kg: 원두 산출량 (kg)
            roasting_log_id: 로스팅 기록 ID

        Returns:
            (성공 여부, 메시지)
        """
        try:
            bean = self.db.query(Bean).filter(Bean.id == bean_id).first()
            if not bean:
                return False, "❌ 원두를 찾을 수 없습니다"

            bean_name = bean.name

            # 1. 생두 재고 차감
            success_raw, msg_raw, trans_raw = self.reduce_stock(
                bean_id=bean_id,
                quantity_kg=raw_weight_kg,
                inventory_type=InventoryType.RAW_BEAN,
                transaction_type=TransactionType.ROASTING,
                notes=f"로스팅 사용 (log_id: {roasting_log_id})",
                roasting_log_id=roasting_log_id,
                allow_negative=False  # 생두 부족 시 로스팅 불가
            )

            if not success_raw:
                return False, f"❌ 생두 재고 부족: {msg_raw}"

            # 2. 원두 재고 증가
            success_roasted, msg_roasted, trans_roasted = self.add_stock(
                bean_id=bean_id,
                quantity_kg=roasted_weight_kg,
                inventory_type=InventoryType.ROASTED_BEAN,
                transaction_type=TransactionType.PRODUCTION,
                notes=f"로스팅 생산 (log_id: {roasting_log_id})",
                roasting_log_id=roasting_log_id
            )

            if not success_roasted:
                # 원두 재고 증가 실패 시 롤백
                self.db.rollback()
                return False, f"❌ 원두 재고 증가 실패: {msg_roasted}"

            loss_rate = ((raw_weight_kg - roasted_weight_kg) / raw_weight_kg) * 100

            return True, f"✅ {bean_name} 로스팅 재고 처리 완료\n" \
                         f"  생두: -{raw_weight_kg}kg\n" \
                         f"  원두: +{roasted_weight_kg}kg\n" \
                         f"  손실률: {loss_rate:.2f}%"

        except Exception as e:
            self.db.rollback()
            return False, f"❌ 로스팅 재고 처리 실패: {str(e)}"

    # ═══════════════════════════════════════════════════════════════
    # 재고 조정
    # ═══════════════════════════════════════════════════════════════

    def adjust_inventory(
        self,
        bean_id: int,
        new_quantity_kg: float,
        inventory_type: str = InventoryType.RAW_BEAN,
        reason: str = None
    ) -> Tuple[bool, str]:
        """
        재고 실사 후 조정

        Args:
            bean_id: 원두 ID
            new_quantity_kg: 새로운 재고량 (kg)
            inventory_type: 재고 유형
            reason: 조정 사유

        Returns:
            (성공 여부, 메시지)
        """
        try:
            inventory = self.get_inventory(bean_id, inventory_type)
            if not inventory:
                return False, "❌ 재고를 찾을 수 없습니다"

            old_quantity = inventory.quantity_kg
            diff = new_quantity_kg - old_quantity

            # 재고 조정
            inventory.quantity_kg = new_quantity_kg
            inventory.last_updated = datetime.utcnow()

            # 거래 기록
            transaction = Transaction(
                bean_id=bean_id,
                transaction_type=TransactionType.ADJUSTMENT,
                inventory_type=inventory_type,
                quantity_kg=diff,
                notes=f"재고 조정: {old_quantity}kg → {new_quantity_kg}kg. 사유: {reason or '없음'}",
                created_at=datetime.utcnow()
            )
            self.db.add(transaction)

            self.db.commit()

            bean = self.db.query(Bean).filter(Bean.id == bean_id).first()
            bean_name = bean.name if bean else "알 수 없음"

            return True, f"✅ {bean_name} {inventory_type} 재고 조정 완료\n" \
                         f"  변경: {old_quantity}kg → {new_quantity_kg}kg ({diff:+.2f}kg)"

        except Exception as e:
            self.db.rollback()
            return False, f"❌ 재고 조정 실패: {str(e)}"

    # ═══════════════════════════════════════════════════════════════
    # 거래 기록 조회
    # ═══════════════════════════════════════════════════════════════

    def get_transactions(
        self,
        bean_id: Optional[int] = None,
        inventory_type: Optional[str] = None,
        transaction_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Transaction]:
        """
        거래 기록 조회

        Args:
            bean_id: 원두 ID (선택)
            inventory_type: 재고 유형 (선택)
            transaction_type: 거래 유형 (선택)
            limit: 최대 개수

        Returns:
            Transaction 리스트
        """
        query = self.db.query(Transaction)

        if bean_id:
            query = query.filter(Transaction.bean_id == bean_id)
        if inventory_type:
            query = query.filter(Transaction.inventory_type == inventory_type)
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)

        return query.order_by(Transaction.created_at.desc()).limit(limit).all()

    def predict_stock_depletion(self, bean_id: int, inventory_type: str, days: int = 30) -> dict:
        """재고 소진 예측

        최근 N일간의 소비량을 기반으로 재고 소진 시점을 예측합니다.

        Args:
            bean_id: 원두 ID
            inventory_type: 재고 유형
            days: 분석 기간 (기본값: 30일)

        Returns:
            {
                'current_qty': 현재 재고량,
                'daily_consumption': 일평균 소비량,
                'days_remaining': 남은 일수,
                'depletion_date': 소진 예상 날짜,
                'consumption_trend': 소비 추이 (increasing/stable/decreasing),
                'sample_days': 실제 분석 일수
            }
        """
        from datetime import datetime, timedelta

        # 현재 재고 조회
        inventory = self.get_inventory(bean_id, inventory_type)
        if not inventory:
            return {'error': '재고 정보를 찾을 수 없습니다'}

        current_qty = inventory.quantity_kg

        # 최근 N일간의 출고 거래 조회
        start_date = datetime.now() - timedelta(days=days)

        outbound_transactions = self.db.query(Transaction).filter(
            Transaction.bean_id == bean_id,
            Transaction.inventory_type == inventory_type,
            Transaction.transaction_type.in_([TransactionType.SALES, TransactionType.ROASTING, TransactionType.WASTE]),
            Transaction.created_at >= start_date
        ).all()

        if not outbound_transactions:
            return {
                'current_qty': current_qty,
                'daily_consumption': 0,
                'days_remaining': float('inf'),
                'depletion_date': None,
                'consumption_trend': 'no_data',
                'sample_days': 0
            }

        # 총 소비량 계산
        total_consumption = sum(abs(t.quantity_kg) for t in outbound_transactions)

        # 실제 거래가 있는 일수 계산
        transaction_dates = set(t.created_at.date() for t in outbound_transactions)
        sample_days = len(transaction_dates)

        # 일평균 소비량 (실제 거래 일수 기준)
        daily_consumption = total_consumption / sample_days if sample_days > 0 else 0

        # 남은 일수 계산
        if daily_consumption > 0:
            days_remaining = current_qty / daily_consumption
            depletion_date = datetime.now() + timedelta(days=days_remaining)
        else:
            days_remaining = float('inf')
            depletion_date = None

        # 소비 추이 분석 (최근 절반 vs 이전 절반)
        consumption_trend = 'stable'
        if len(outbound_transactions) >= 4:
            mid_point = len(outbound_transactions) // 2
            recent_half = outbound_transactions[:mid_point]
            older_half = outbound_transactions[mid_point:]

            recent_consumption = sum(abs(t.quantity_kg) for t in recent_half)
            older_consumption = sum(abs(t.quantity_kg) for t in older_half)

            if recent_consumption > older_consumption * 1.2:
                consumption_trend = 'increasing'
            elif recent_consumption < older_consumption * 0.8:
                consumption_trend = 'decreasing'

        return {
            'current_qty': current_qty,
            'daily_consumption': daily_consumption,
            'days_remaining': days_remaining,
            'depletion_date': depletion_date,
            'consumption_trend': consumption_trend,
            'sample_days': sample_days
        }
