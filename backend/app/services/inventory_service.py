from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.models.inbound_item import InboundItem
from app.models.inventory_log import InventoryLog, InventoryChangeType
from app.models.bean import Bean
import logging

logger = logging.getLogger(__name__)

class InventoryService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_fifo_cost(self, bean_id: int, quantity: float) -> tuple[float, float]:
        """
        FIFO 기준으로 소모될 재고의 원가를 계산 (실제 차감은 하지 않음)
        
        Args:
            bean_id: 원두 ID
            quantity: 소모할 수량 (kg)
            
        Returns:
            (weighted_avg_cost_per_kg, total_cost)
            - weighted_avg_cost_per_kg: kg당 가중평균 원가
            - total_cost: 총 원가
        """
        if quantity <= 0:
            return 0.0, 0.0

        # 잔여 재고가 있는 입고 항목을 오래된 순서대로 조회 (FIFO)
        items = self.db.query(InboundItem).filter(
            InboundItem.bean_id == bean_id,
            InboundItem.remaining_quantity > 0
        ).order_by(asc(InboundItem.created_at)).all()

        total_cost = 0.0
        remaining_to_deduct = quantity
        
        # 가상 차감 시뮬레이션
        for item in items:
            if remaining_to_deduct <= 0:
                break
                
            # 이번 항목에서 차감할 수량
            deduct_amount = min(item.remaining_quantity, remaining_to_deduct)
            
            # 원가 누적 (단가 * 수량)
            # unit_price가 없으면 0 처리 (또는 에러?) -> 일단 0으로 처리하고 로그
            unit_price = item.unit_price or 0.0
            total_cost += unit_price * deduct_amount
            
            remaining_to_deduct -= deduct_amount

        # 재고 부족 시 로직:
        # 1. 에러 발생 (엄격 모드) OR
        # 2. 남은 수량은 가장 최근 단가 or 0원 처리 (유연 모드)
        # 여기서는 유연 모드: 부족분은 0원으로 처리하되 경고 로그
        if remaining_to_deduct > 0:
            logger.warning(f"Inventory shortage simulation for bean {bean_id}: requested {quantity}, missing {remaining_to_deduct}")

        avg_cost = total_cost / quantity if quantity > 0 else 0.0
        
        return avg_cost, total_cost

    def deduct_inventory(self, bean_id: int, quantity: float, ref_type: str = "ROASTING", ref_id: int = None) -> None:
        """
        실제 재고 차감 (FIFO) 및 로그 생성
        """
        if quantity <= 0:
            return

        # 잔여 재고가 있는 입고 항목 조회
        items = self.db.query(InboundItem).filter(
            InboundItem.bean_id == bean_id,
            InboundItem.remaining_quantity > 0
        ).order_by(asc(InboundItem.created_at)).all()

        remaining_to_deduct = quantity
        
        for item in items:
            if remaining_to_deduct <= 0:
                break
                
            deduct_amount = min(item.remaining_quantity, remaining_to_deduct)
            
            # DB 업데이트
            item.remaining_quantity -= deduct_amount
            remaining_to_deduct -= deduct_amount
            
            # NOTE: 여기서 상세 차감 로그를 남길 수도 있음 (e.g., InboundItemUsageLog)
            
        if remaining_to_deduct > 0:
            logger.warning(f"Inventory shortage deduction for bean {bean_id}: requested {quantity}, missing {remaining_to_deduct}")
            # 전체 재고 수량도 강제로 맞춤 (Optional)
            
        # Bean 테이블의 총 재고 차감 (이건 기존 로직에서 이미 하고 있을 수 있으니 중복 주의)
        # 하지만 InventoryService가 책임을 가져가는 것이 깔끔함.
        # 일단은 호출하는 쪽(Roasting Endpoint)에서 Bean 재고 차감을 하고 있으므로
        # 여기서는 InboundItem의 remaining_quantity 관리만 집중.
