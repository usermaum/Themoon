"""
블렌딩 관리 서비스
블렌드 CRUD + 원가 계산
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional, Dict
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import Blend, BlendRecipe, Bean
from utils.constants import BLENDS_DATA, DEFAULT_COST_SETTINGS

class BlendService:
    """블렌드 관리 서비스"""

    def __init__(self, db: Session):
        self.db = db

    # ═══════════════════════════════════════════════════════════════
    # 📖 조회 (READ)
    # ═══════════════════════════════════════════════════════════════

    def get_all_blends(self, skip: int = 0, limit: int = 100) -> List[Blend]:
        """모든 블렌드 조회"""
        return self.db.query(Blend).offset(skip).limit(limit).all()

    def get_blend_by_id(self, blend_id: int) -> Optional[Blend]:
        """ID로 블렌드 조회"""
        return self.db.query(Blend).filter(Blend.id == blend_id).first()

    def get_blend_by_name(self, name: str) -> Optional[Blend]:
        """이름으로 블렌드 조회"""
        return self.db.query(Blend).filter(Blend.name == name).first()

    def get_blends_by_type(self, blend_type: str) -> List[Blend]:
        """타입별 블렌드 조회 (풀문/뉴문/시즈널)"""
        return self.db.query(Blend).filter(Blend.blend_type == blend_type).all()

    def get_active_blends(self) -> List[Blend]:
        """활성 블렌드만 조회"""
        return self.db.query(Blend).filter(Blend.status == "active").all()

    def get_blend_recipes(self, blend_id: int) -> List[BlendRecipe]:
        """블렌드 구성 조회"""
        return self.db.query(BlendRecipe).filter(
            BlendRecipe.blend_id == blend_id
        ).all()

    def get_blend_with_details(self, blend_id: int) -> Optional[dict]:
        """블렌드 상세 정보 (구성 포함)"""
        blend = self.get_blend_by_id(blend_id)
        if not blend:
            return None

        recipes = self.get_blend_recipes(blend_id)
        recipe_details = []

        for recipe in recipes:
            bean = recipe.bean
            recipe_details.append({
                "bean_id": bean.id,
                "bean_no": bean.no,
                "bean_name": bean.name,
                "roast_level": bean.roast_level,
                "portion": recipe.portion_count,
                "ratio": recipe.ratio,
                "price_per_kg": bean.price_per_kg
            })

        return {
            "id": blend.id,
            "name": blend.name,
            "type": blend.blend_type,
            "description": blend.description,
            "status": blend.status,
            "total_portion": blend.total_portion,
            "suggested_price": blend.suggested_price,
            "recipes": recipe_details
        }

    # ═══════════════════════════════════════════════════════════════
    # ➕ 생성 (CREATE)
    # ═══════════════════════════════════════════════════════════════

    def create_blend(
        self,
        name: str,
        blend_type: str,
        description: str = None,
        suggested_price: float = 0.0
    ) -> Blend:
        """새 블렌드 생성"""
        existing = self.get_blend_by_name(name)
        if existing:
            raise ValueError(f"블렌드 '{name}'이 이미 존재합니다")

        blend = Blend(
            name=name,
            blend_type=blend_type,
            description=description,
            suggested_price=suggested_price,
            status="active"
        )
        self.db.add(blend)
        self.db.commit()
        self.db.refresh(blend)

        return blend

    def add_recipe_to_blend(
        self,
        blend_id: int,
        bean_id: int,
        portion_count: int,
        ratio: float = 0.0
    ) -> Optional[BlendRecipe]:
        """블렌드에 원두 추가"""
        blend = self.get_blend_by_id(blend_id)
        bean = self.db.query(Bean).filter(Bean.id == bean_id).first()

        if not blend or not bean:
            return None

        # 중복 확인
        existing = self.db.query(BlendRecipe).filter(
            and_(
                BlendRecipe.blend_id == blend_id,
                BlendRecipe.bean_id == bean_id
            )
        ).first()

        if existing:
            # 기존 항목 업데이트
            existing.portion_count = portion_count
            existing.ratio = ratio
            self.db.commit()
            return existing

        recipe = BlendRecipe(
            blend_id=blend_id,
            bean_id=bean_id,
            portion_count=portion_count,
            ratio=ratio
        )
        self.db.add(recipe)

        # 블렌드 포션 총합 업데이트
        total = self.db.query(BlendRecipe).filter(
            BlendRecipe.blend_id == blend_id
        ).count()
        blend.total_portion = total + 1

        self.db.commit()
        self.db.refresh(recipe)

        return recipe

    # ═══════════════════════════════════════════════════════════════
    # ✏️ 수정 (UPDATE)
    # ═══════════════════════════════════════════════════════════════

    def update_blend(
        self,
        blend_id: int,
        name: str = None,
        description: str = None,
        suggested_price: float = None,
        status: str = None
    ) -> Optional[Blend]:
        """블렌드 정보 수정"""
        blend = self.get_blend_by_id(blend_id)
        if not blend:
            return None

        if name is not None:
            blend.name = name
        if description is not None:
            blend.description = description
        if suggested_price is not None:
            blend.suggested_price = suggested_price
        if status is not None:
            blend.status = status

        blend.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(blend)

        return blend

    def update_recipe_ratio(self, blend_id: int, recalculate: bool = True) -> bool:
        """레시피 비율 재계산"""
        blend = self.get_blend_by_id(blend_id)
        if not blend:
            return False

        recipes = self.get_blend_recipes(blend_id)
        if not recipes:
            return False

        total_portion = sum(r.portion_count for r in recipes)
        if total_portion == 0:
            return False

        for recipe in recipes:
            recipe.ratio = (recipe.portion_count / total_portion) * 100

        self.db.commit()
        return True

    # ═══════════════════════════════════════════════════════════════
    # 🗑️ 삭제 (DELETE)
    # ═══════════════════════════════════════════════════════════════

    def delete_blend(self, blend_id: int) -> bool:
        """블렌드 삭제 (소프트)"""
        blend = self.get_blend_by_id(blend_id)
        if not blend:
            return False

        blend.status = "inactive"
        self.db.commit()
        return True

    def remove_recipe_from_blend(self, blend_id: int, bean_id: int) -> bool:
        """블렌드에서 원두 제거"""
        recipe = self.db.query(BlendRecipe).filter(
            and_(
                BlendRecipe.blend_id == blend_id,
                BlendRecipe.bean_id == bean_id
            )
        ).first()

        if not recipe:
            return False

        self.db.delete(recipe)
        self.db.commit()

        # 비율 재계산
        self.update_recipe_ratio(blend_id)

        return True

    # ═══════════════════════════════════════════════════════════════
    # 💰 원가 계산
    # ═══════════════════════════════════════════════════════════════

    def calculate_blend_cost(self, blend_id: int) -> dict:
        """블렌드 원가 계산"""
        blend = self.get_blend_with_details(blend_id)
        if not blend:
            return {}

        total_cost = 0.0
        recipe_costs = []

        for recipe in blend["recipes"]:
            bean_cost = recipe["price_per_kg"] * (recipe["portion"] / 100)
            # 로스팅 손실율 적용
            roasted_cost = bean_cost / (1 - DEFAULT_COST_SETTINGS["roasting_loss_rate"])
            recipe_costs.append({
                "bean_name": recipe["bean_name"],
                "portion": recipe["portion"],
                "unit_cost": recipe["price_per_kg"],
                "bean_cost": bean_cost,
                "roasted_cost": roasted_cost
            })
            total_cost += roasted_cost

        # 추가 비용
        roasting_cost = total_cost * 0.1  # 로스팅비 10%
        labor_cost = DEFAULT_COST_SETTINGS["labor_cost_per_hour"] * \
            DEFAULT_COST_SETTINGS["roasting_time_hours"] / blend["total_portion"]
        misc_cost = DEFAULT_COST_SETTINGS["misc_cost"] / blend["total_portion"]

        total_cost += roasting_cost + labor_cost + misc_cost

        # 판매가 제안 (마진율 적용)
        margin_rate = DEFAULT_COST_SETTINGS["default_margin_rate"]
        suggested_price = total_cost * margin_rate

        return {
            "blend_name": blend["name"],
            "blend_type": blend["type"],
            "total_portion": blend["total_portion"],
            "recipes": recipe_costs,
            "bean_cost_total": sum(r["bean_cost"] for r in recipe_costs),
            "roasting_cost": roasting_cost,
            "labor_cost": labor_cost,
            "misc_cost": misc_cost,
            "cost_per_portion": total_cost / blend["total_portion"],
            "total_cost": total_cost,
            "margin_rate": margin_rate,
            "suggested_price": suggested_price,
            "profit_margin": suggested_price - total_cost
        }

    # ═══════════════════════════════════════════════════════════════
    # 🔧 초기화 & 데이터 로드
    # ═══════════════════════════════════════════════════════════════

    def init_default_blends(self) -> int:
        """기본 블렌드 로드"""
        from models.database import SessionLocal
        count = 0

        for blend_data in BLENDS_DATA:
            existing = self.get_blend_by_name(blend_data["name"])
            if not existing:
                blend = self.create_blend(
                    name=blend_data["name"],
                    blend_type=blend_data["type"],
                    description=blend_data["description"],
                    suggested_price=blend_data["price_suggested"]
                )

                # 레시피 추가
                for recipe in blend_data["recipes"]:
                    bean = self.db.query(Bean).filter(
                        Bean.no == recipe["bean_no"]
                    ).first()
                    if bean:
                        self.add_recipe_to_blend(
                            blend.id,
                            bean.id,
                            recipe["portion"],
                            recipe["ratio"]
                        )

                count += 1

        return count

    # ═══════════════════════════════════════════════════════════════
    # 📊 분석 & 통계
    # ═══════════════════════════════════════════════════════════════

    def get_blends_summary(self) -> dict:
        """블렌드 전체 요약"""
        all_blends = self.get_active_blends()
        type_summary = {}

        for blend in all_blends:
            blend_type = blend.blend_type
            if blend_type not in type_summary:
                type_summary[blend_type] = 0
            type_summary[blend_type] += 1

        return {
            "total_blends": len(all_blends),
            "by_type": type_summary,
            "blends": all_blends
        }

    def export_as_dict(self) -> List[dict]:
        """딕셔너리로 내보내기"""
        blends = self.get_active_blends()
        result = []

        for blend in blends:
            recipes = self.get_blend_recipes(blend.id)
            recipe_names = ", ".join([r.bean.name for r in recipes])

            result.append({
                "이름": blend.name,
                "타입": blend.blend_type,
                "포션": blend.total_portion,
                "구성": recipe_names,
                "제안가격": blend.suggested_price
            })

        return result


if __name__ == "__main__":
    from models.database import SessionLocal, init_db

    init_db()
    db = SessionLocal()

    # 먼저 원두 로드
    from services.bean_service import BeanService
    bean_service = BeanService(db)
    bean_service.init_default_beans()

    # 블렌드 로드
    service = BlendService(db)
    count = service.init_default_blends()
    print(f"✅ {count}개 블렌드 로드 완료")

    # 요약
    summary = service.get_blends_summary()
    print(f"📊 총 블렌드: {summary['total_blends']}개")
    print(f"타입: {summary['by_type']}")

    db.close()
