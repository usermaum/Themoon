"""
로스팅 서비스 - 비즈니스 로직 (Class-based for Clean Architecture)
Ref: docs/Planning/Themoon_Rostings_v2.md
"""

from fastapi import HTTPException
from app.models.bean import Bean, BeanType, RoastProfile
from app.models.inventory_log import InventoryChangeType, InventoryLog
from app.models.roasting_log import RoastingLog
from app.services.bean_service import BeanService
from app.services.inventory_service import InventoryService
from app.repositories.blend_repository import BlendRepository
from app.repositories.roasting_log_repository import RoastingLogRepository
from app.utils.timezone import get_kst_now


class RoastingService:
    def __init__(
        self,
        bean_service: BeanService,
        inventory_service: InventoryService,
        blend_repo: BlendRepository,
        roasting_log_repo: RoastingLogRepository,
    ):
        self.bean_service = bean_service
        self.inventory_service = inventory_service
        self.blend_repo = blend_repo
        self.roasting_log_repo = roasting_log_repo

    def generate_batch_no(self) -> str:
        """생산 배치 번호 생성 (예: R251225-001)"""
        now = get_kst_now()
        date_str = now.strftime("%y%m%d")
        prefix = f"R{date_str}"
        
        latest = self.roasting_log_repo.get_latest_batch_no()
        if latest and latest.startswith(prefix):
            try:
                seq = int(latest.split("-")[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1
            
        return f"{prefix}-{seq:03d}"

    def generate_roasted_bean_sku(self, green_bean: Bean, profile: RoastProfile) -> str:
        """원두 SKU 생성 (예: Yirgacheffe-신콩)"""
        profile_kr = (
            "신콩"
            if profile == RoastProfile.LIGHT
            else "탄콩" if profile == RoastProfile.DARK else "미디엄"
        )
        return f"{green_bean.name}-{profile_kr}"

    def create_single_origin_roasting(
        self,
        green_bean_id: int,
        input_weight: float,
        output_weight: float,
        roast_profile: RoastProfile,
        notes: str = None,
    ) -> tuple[Bean, str]:
        """
        싱글 오리진 로스팅 로직
        1. 생두 재고 차감
        2. 원두 재고 증가 (없으면 생성)
        3. 원가 및 손실률 계산
        """
        # 1. 생두 조회 및 검증
        green_bean = self.bean_service.get_bean(green_bean_id)
        if not green_bean:
            raise HTTPException(status_code=404, detail="Green bean not found")

        if green_bean.quantity_kg < input_weight:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough green bean inventory. Current: {green_bean.quantity_kg}kg",
            )

        # 원가 계산 (FIFO 기반)
        fifo_unit_cost, total_input_cost = self.inventory_service.calculate_fifo_cost(
            green_bean.id, input_weight
        )

        # 2. 생두 재고 차감 (투입)
        self.inventory_service.deduct_inventory(green_bean.id, input_weight)

        # Bean 테이블 재고도 차감 (동기화)
        self.bean_service.update_bean_quantity(green_bean.id, -input_weight)

        # 3. 로스팅 로그 (배치) 생성
        batch_no = self.generate_batch_no()
        roasting_log = self.roasting_log_repo.create({
            "batch_no": batch_no,
            "target_bean_id": green_bean.id, # 원두 생성 전이므로 임시 할당 하거나 나중에 업데이트
            "input_weight_total": input_weight,
            "output_weight_total": output_weight,
            "loss_rate": ((input_weight - output_weight) / input_weight * 100) if input_weight > 0 else 0,
            "production_cost": total_input_cost,
            "notes": notes
        })

        # 생두 재고 로그 (FIFO 원가 기록)
        self.inventory_service.inventory_log_repo.create({
            "bean_id": green_bean.id,
            "change_type": InventoryChangeType.ROASTING_INPUT,
            "change_amount": -input_weight,
            "current_quantity": green_bean.quantity_kg,
            "unit_cost": fifo_unit_cost,
            "notes": f"Roasting Input to {roast_profile} (Batch: {batch_no})",
            "roasting_log_id": roasting_log.id
        })

        # 4. 원두(Roasted Bean) 조회 또는 생성
        sku = self.generate_roasted_bean_sku(green_bean, roast_profile)
        roasted_bean = self.bean_service.get_bean_by_sku(sku)

        production_cost_per_kg = total_input_cost / output_weight if output_weight > 0 else 0

        if not roasted_bean:
            # 원두 신규 생성
            profile_kr = (
                "신콩"
                if roast_profile == RoastProfile.LIGHT
                else "탄콩" if roast_profile == RoastProfile.DARK else "미디엄"
            )
            roasted_bean_data = {
                "name": f"{green_bean.name} {profile_kr}",
                "type": BeanType.ROASTED_BEAN,
                "sku": sku,
                "origin": green_bean.origin,
                "variety": green_bean.variety,
                "grade": green_bean.grade,
                "processing_method": green_bean.processing_method,
                "roast_profile": roast_profile,
                "parent_bean_id": green_bean.id,
                "quantity_kg": 0.0,
                "avg_price": production_cost_per_kg,
                "cost_price": production_cost_per_kg,
            }
            roasted_bean = self.bean_service.repository.create(roasted_bean_data)
        else:
            # 기존 원두: FIFO 기반 가중평균으로 avg_price 업데이트
            current_value = roasted_bean.quantity_kg * roasted_bean.avg_price
            new_value = output_weight * production_cost_per_kg
            total_quantity = roasted_bean.quantity_kg + output_weight

            update_data = {"cost_price": production_cost_per_kg}
            if total_quantity > 0:
                update_data["avg_price"] = (current_value + new_value) / total_quantity
            
            self.bean_service.repository.update(roasted_bean, update_data)

        # Batch Log의 target_bean_id 정확한 ID로 업데이트
        self.roasting_log_repo.update(roasting_log, {"target_bean_id": roasted_bean.id})

        # 5. 원두 재고 증가 (생산)
        self.bean_service.update_bean_quantity(roasted_bean.id, output_weight)

        # 원두 재고 로그
        self.inventory_service.inventory_log_repo.create({
            "bean_id": roasted_bean.id,
            "change_type": InventoryChangeType.ROASTING_OUTPUT,
            "change_amount": output_weight,
            "current_quantity": roasted_bean.quantity_kg,
            "unit_cost": production_cost_per_kg,
            "notes": f"Roasting Output from {green_bean.name} (Batch: {batch_no})",
            "roasting_log_id": roasting_log.id
        })
        return roasted_bean, batch_no

    def create_blend_roasting(
        self,
        blend_id: int,
        output_weight: float,
        input_weight: float = None,
        notes: str = None
    ) -> tuple[Bean, str]:
        """
        블렌드 로스팅 로직
        1. 블렌드 레시피 기반 생두 투입량 자동 계산 및 차감
        2. 블렌드 원두(Roasted) 생성 및 입고
        """
        # 1. 블렌드 조회
        blend = self.blend_repo.get(blend_id)
        if not blend:
            raise HTTPException(status_code=404, detail="Blend not found")

        recipe = blend.recipe
        if not recipe:
            raise HTTPException(status_code=400, detail="Blend recipe is empty")

        # 2. 투입량 계산 및 재고 검증
        input_items = []
        total_input_cost = 0.0
        total_input_weight = 0.0

        for item in recipe:
            # item은 dict 또는 BlendRecipeItem pydantic model 일 수 있음
            b_id = item.bean_id if hasattr(item, 'bean_id') else item['bean_id']
            ratio = item.ratio if hasattr(item, 'ratio') else item['ratio']

            bean = self.bean_service.get_bean(b_id)
            if not bean:
                raise HTTPException(status_code=404, detail=f"Bean ID {b_id} in recipe not found")

            # 필요량 계산
            if input_weight:
                required_input = input_weight * ratio
            else:
                loss_rate = bean.expected_loss_rate if bean.expected_loss_rate is not None else 0.15
                target_part_weight = output_weight * ratio
                required_input = target_part_weight / (1 - loss_rate)

            if bean.quantity_kg < required_input:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock for {bean.name}. Required: {required_input:.2f}kg, Available: {bean.quantity_kg:.2f}kg",
                )

            # FIFO 원가 계산
            fifo_unit_cost, item_cost = self.inventory_service.calculate_fifo_cost(bean.id, required_input)

            input_items.append(
                {
                    "bean": bean,
                    "required_input": required_input,
                    "cost": item_cost,
                    "unit_cost": fifo_unit_cost,
                }
            )

            total_input_cost += item_cost
            total_input_weight += required_input

        # 3. 로스팅 로그 (배치) 생성
        batch_no = self.generate_batch_no()
        # 블렌드 원두 생성 전이므로 target_bean_id는 임시로 첫 번째 생두 ID 또는 0
        roasting_log = self.roasting_log_repo.create({
            "batch_no": batch_no,
            "target_bean_id": input_items[0]["bean"].id if input_items else 0,
            "input_weight_total": total_input_weight,
            "output_weight_total": output_weight,
            "loss_rate": ((total_input_weight - output_weight) / total_input_weight * 100) if total_input_weight > 0 else 0,
            "production_cost": total_input_cost,
            "notes": notes
        })

        # 4. 재고 차감 실행 (FIFO 원가 기록)
        for item in input_items:
            bean = item["bean"]
            amount = item["required_input"]
            unit_cost = item["unit_cost"]

            self.inventory_service.deduct_inventory(bean.id, amount)
            self.bean_service.update_bean_quantity(bean.id, -amount)

            self.inventory_service.inventory_log_repo.create({
                "bean_id": bean.id,
                "change_type": InventoryChangeType.ROASTING_INPUT,
                "change_amount": -amount,
                "current_quantity": bean.quantity_kg,
                "unit_cost": unit_cost,
                "notes": f"Used for Blend: {blend.name} (Batch: {batch_no})",
                "roasting_log_id": roasting_log.id
            })

        # 5. 블렌드 원두 생성/업데이트
        production_cost_per_kg = total_input_cost / output_weight if output_weight > 0 else 0
        sku = f"BLEND-{blend.id}-{blend.name.replace(' ', '')}"

        # Check if roasted blend bean exists
        roasted_bean = self.bean_service.get_bean_by_sku(sku)

        if not roasted_bean:
            roasted_bean_data = {
                "name": f"{blend.name}",
                "type": BeanType.BLEND_BEAN,
                "sku": sku,
                "origin": "Blend",
                "roast_profile": RoastProfile.MEDIUM,
                "quantity_kg": 0.0,
                "avg_price": production_cost_per_kg,
                "cost_price": production_cost_per_kg,
                "notes": f"Blend based on {blend.name}",
            }
            roasted_bean = self.bean_service.repository.create(roasted_bean_data)
        else:
            current_val = roasted_bean.quantity_kg * roasted_bean.avg_price
            new_val = output_weight * production_cost_per_kg
            total_qty = roasted_bean.quantity_kg + output_weight

            update_data = {"cost_price": production_cost_per_kg}
            if total_qty > 0:
                update_data["avg_price"] = (current_val + new_val) / total_qty

            self.bean_service.repository.update(roasted_bean, update_data)

        # Batch Log의 target_bean_id를 실제 블렌드 원두 ID로 업데이트
        self.roasting_log_repo.update(roasting_log, {"target_bean_id": roasted_bean.id})

        self.bean_service.update_bean_quantity(roasted_bean.id, output_weight)

        # 생산 로그
        self.inventory_service.inventory_log_repo.create({
            "bean_id": roasted_bean.id,
            "change_type": InventoryChangeType.ROASTING_OUTPUT,
            "change_amount": output_weight,
            "current_quantity": roasted_bean.quantity_kg,
            "unit_cost": production_cost_per_kg,
            "notes": f"Blend Roasting: {blend.name} (Batch: {batch_no})",
            "roasting_log_id": roasting_log.id
        })
        return roasted_bean, batch_no

    def get_analytics_summary(self, start_date=None, end_date=None):
        """로스팅 통계 요약 조회"""
        from app.schemas.analytics import (
            RoastingStatsResponse, DailyProductionStats, BeanUsageStats, LossRateStats
        )
        from datetime import datetime, timedelta

        if not end_date:
            end_date = get_kst_now().date()
        if not start_date:
            # 기본값: 최근 30일
            start_date = end_date - timedelta(days=30)

        # 1. 일별 생산량
        daily_stats = self.roasting_log_repo.get_daily_production_stats(start_date, end_date)
        daily_data = []
        for stat in daily_stats:
            # SAFETY: Defensive date handling
            if not stat.date:
                continue
                
            d_str = str(stat.date)
            if hasattr(stat.date, 'isoformat'):
                d_str = stat.date.isoformat()
            
            daily_data.append(
                DailyProductionStats(
                    date=d_str,
                    total_weight=stat.total_weight or 0.0,
                    batch_count=stat.batch_count
                )
            )

        # 2. 원두별 비중
        bean_usage = self.roasting_log_repo.get_bean_usage_stats(start_date, end_date)
        total_period_output = sum(item.total_output for item in bean_usage)
        
        usage_data = []
        for item in bean_usage:
            percentage = (item.total_output / total_period_output * 100) if total_period_output > 0 else 0
            usage_data.append(
                BeanUsageStats(
                    bean_type="Unknown",
                    bean_name=item.name,
                    total_output=item.total_output or 0.0,
                    percentage=round(percentage, 1)
                )
            )
        usage_data.sort(key=lambda x: x.percentage, reverse=True)

        # 3. 최근 손실률
        loss_data_raw = self.roasting_log_repo.get_recent_loss_rates(limit=30)
        loss_data = []
        for log, bean_name in loss_data_raw:
            # SAFETY: Defensive date handling
            roast_date_str = ""
            if log.roast_date:
                if hasattr(log.roast_date, 'strftime'):
                    roast_date_str = log.roast_date.strftime("%Y-%m-%d")
                else:
                    roast_date_str = str(log.roast_date).split(' ')[0]
            
            loss_data.append(
                LossRateStats(
                    batch_no=log.batch_no,
                    roast_date=roast_date_str,
                    bean_name=bean_name,
                    loss_rate=round(log.loss_rate, 2) if log.loss_rate else 0.0
                )
            )

        # 4. KPI 요약
        total_batches = sum(d.batch_count for d in daily_data)
        avg_loss = sum(l.loss_rate for l in loss_data) / len(loss_data) if loss_data else 0.0

        return RoastingStatsResponse(
            overview={
                "total_production_kg": round(total_period_output, 2),
                "total_batches": total_batches,
                "avg_loss_rate": round(avg_loss, 2)
            },
            daily_production=daily_data,
            bean_usage=usage_data[:5],
            recent_loss_rates=loss_data
        )
