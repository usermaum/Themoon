import logging
from typing import Tuple

from app.repositories.inbound_repository import InboundRepository
from app.repositories.inventory_log_repository import InventoryLogRepository

logger = logging.getLogger(__name__)


class InventoryService:
    def __init__(
        self,
        inbound_repo: InboundRepository,
        inventory_log_repo: InventoryLogRepository,
    ):
        self.inbound_repo = inbound_repo
        self.inventory_log_repo = inventory_log_repo

    def calculate_fifo_cost(self, bean_id: int, quantity: float) -> Tuple[float, float]:
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
        items = self.inbound_repo.get_fifo_candidates(bean_id)

        total_cost = 0.0
        remaining_to_deduct = quantity

        # 가상 차감 시뮬레이션
        for item in items:
            if remaining_to_deduct <= 0:
                break

            # 이번 항목에서 차감할 수량
            deduct_amount = min(item.remaining_quantity, remaining_to_deduct)

            # 원가 누적 (단가 * 수량)
            unit_price = item.unit_price or 0.0
            total_cost += unit_price * deduct_amount

            remaining_to_deduct -= deduct_amount

        # 재고 부족 시 로직
        if remaining_to_deduct > 0:
            logger.warning(
                f"Inventory shortage simulation for bean {bean_id}: requested {quantity}, missing {remaining_to_deduct}"
            )

        avg_cost = total_cost / quantity if quantity > 0 else 0.0

        return avg_cost, total_cost

    def deduct_inventory(
        self, bean_id: int, quantity: float, ref_type: str = "ROASTING", ref_id: int = None
    ) -> None:
        """
        실제 재고 차감 (FIFO) 수행
        """
        if quantity <= 0:
            return

        # 잔여 재고가 있는 입고 항목 조회
        items = self.inbound_repo.get_fifo_candidates(bean_id)

        remaining_to_deduct = quantity

        for item in items:
            if remaining_to_deduct <= 0:
                break

            deduct_amount = min(item.remaining_quantity, remaining_to_deduct)

            # DB 업데이트 (Repo 사용)
            new_remaining = item.remaining_quantity - deduct_amount
            self.inbound_repo.update_item_remaining_quantity(item.id, new_remaining)
            
            remaining_to_deduct -= deduct_amount

        if remaining_to_deduct > 0:
            logger.warning(
                f"Inventory shortage deduction for bean {bean_id}: requested {quantity}, missing {remaining_to_deduct}"
            )
