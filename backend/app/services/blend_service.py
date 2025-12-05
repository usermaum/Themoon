from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import List, Optional
from app.models.bean import Bean, BeanType
from app.models.recipe import Recipe
from app.schemas.blend import BlendCreate, BlendUpdate, BlendRecipeItem
from app.schemas.bean import BeanCreate as BeanSchemaCreate

class BlendService:
    def get_blends(self, db: Session, skip: int = 0, limit: int = 100) -> List[Bean]:
        """블렌드 제품 목록 조회 (Recipes 포함)"""
        return db.query(Bean).filter(Bean.type == BeanType.BLEND)\
            .options(joinedload(Bean.recipes))\
            .offset(skip).limit(limit).all()

    def get_blend(self, db: Session, blend_id: int) -> Optional[Bean]:
        """블렌드 제품 상세 조회"""
        return db.query(Bean).filter(Bean.id == blend_id, Bean.type == BeanType.BLEND)\
            .options(joinedload(Bean.recipes))\
            .first()

    def create_blend(self, db: Session, blend_data: BlendCreate) -> Bean:
        """새 블렌드 제품 생성 및 레시피 등록"""
        # 1. Create Bean
        new_bean = Bean(
            name=blend_data.name,
            type=BeanType.BLEND,
            notes=blend_data.notes,
            # Blends don't have origin/variety inherently, or could be 'Blend'
            origin="Blend",
            variety="Blend",
            quantity_kg=0.0,
            cost_price=0.0 
        )
        db.add(new_bean)
        db.flush() # ID generation

        # 2. Create Recipes
        if blend_data.recipe:
            for item in blend_data.recipe:
                recipe_entry = Recipe(
                    blend_bean_id=new_bean.id,
                    ingredient_bean_id=item.bean_id,
                    ratio_percent=item.ratio * 100 # Convert 0.5 to 50%
                )
                db.add(recipe_entry)
        
        db.commit()
        db.refresh(new_bean)
        return new_bean

    def update_blend(self, db: Session, blend_id: int, blend_update: BlendUpdate) -> Optional[Bean]:
        db_blend = self.get_blend(db, blend_id)
        if not db_blend:
            return None
        
        # Update Basic Info
        if blend_update.name:
            db_blend.name = blend_update.name
        if blend_update.notes:
            db_blend.notes = blend_update.notes
            
        # Update Recipe (Full Replace for simplicity)
        if blend_update.recipe is not None:
            # Delete old recipes
            db.query(Recipe).filter(Recipe.blend_bean_id == blend_id).delete()
            # Add new
            for item in blend_update.recipe:
                recipe_entry = Recipe(
                    blend_bean_id=blend_id,
                    ingredient_bean_id=item.bean_id,
                    ratio_percent=item.ratio * 100
                )
                db.add(recipe_entry)

        db.commit()
        db.refresh(db_blend)
        return db_blend

    def delete_blend(self, db: Session, blend_id: int) -> bool:
        db_blend = self.get_blend(db, blend_id)
        if not db_blend:
            return False
        
        # Recipes should be deleted via cascade or manually
        db.query(Recipe).filter(Recipe.blend_bean_id == blend_id).delete()
        db.delete(db_blend)
        db.commit()
        return True

    def calculate_max_production(self, db: Session, blend_id: int) -> float:
        """현재 재고 기준 최대 생산 가능량 계산"""
        blend = self.get_blend(db, blend_id)
        if not blend or not blend.recipes:
            return 0.0
            
        max_amounts = []
        for recipe in blend.recipes:
            ingredient = db.query(Bean).get(recipe.ingredient_bean_id)
            if not ingredient:
                continue
            
            # Recipe ratio is percent (e.g. 50.0 for 50%)
            ratio = recipe.ratio_percent / 100.0
            if ratio <= 0:
                continue
                
            # Max possible for this ingredient = stock / ratio
            max_possible = ingredient.quantity_kg / ratio
            max_amounts.append(max_possible)
            
        if not max_amounts:
            return 0.0
            
        return min(max_amounts)

    def process_production(self, db: Session, blend_id: int, production_data: 'BlendingProduction') -> 'BlendingResponse':
        """블렌드 제품 생산 (재료 소모 -> 블렌드 재고 증가)"""
        from app.models.inventory_log import InventoryLog, TransactionType
        from app.schemas.blend import BlendingResponse
        from fastapi import HTTPException
        
        blend = self.get_blend(db, blend_id)
        if not blend:
             raise HTTPException(status_code=404, detail="Blend product not found")
             
        if not blend.recipes:
             raise HTTPException(status_code=400, detail="Blend has no recipe defined")

        required_amount = production_data.amount
        
        # 1. Validation & Calculation
        total_input_cost = 0.0
        ingredient_consumption = [] # [(bean, amount), ...]
        
        for recipe in blend.recipes:
            ratio = recipe.ratio_percent / 100.0
            needed_kg = required_amount * ratio
            
            ingredient = db.query(Bean).get(recipe.ingredient_bean_id)
            if not ingredient:
                raise HTTPException(status_code=400, detail=f"Ingredient bean {recipe.ingredient_bean_id} not found")
                
            if ingredient.quantity_kg < needed_kg:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {ingredient.name}. Needed: {needed_kg}kg, Available: {ingredient.quantity_kg}kg")
                
            unit_cost = ingredient.cost_price if (ingredient.cost_price and ingredient.cost_price > 0) else (ingredient.purchase_price_per_kg or 0)
            total_input_cost += (needed_kg * unit_cost)
            ingredient_consumption.append((ingredient, needed_kg))

        # 2. Execution
        transaction_ids = []
        
        # A. Consume Ingredients
        for ingredient, amount in ingredient_consumption:
            ingredient.quantity_kg -= amount
            log = InventoryLog(
                bean_id=ingredient.id,
                transaction_type="BLENDING_IN",
                quantity_change=-amount,
                current_quantity=ingredient.quantity_kg,
                reason=f"Blending for {blend.name}"
            )
            db.add(log)
            db.flush()
            transaction_ids.append(log.id)
            
        # B. Produce Blend
        new_unit_cost = total_input_cost / required_amount if required_amount > 0 else 0
        
        # Update Weighted Average Cost
        current_val = blend.quantity_kg * (blend.cost_price or 0)
        new_val = required_amount * new_unit_cost
        total_qty = blend.quantity_kg + required_amount
        
        avg_cost = 0
        if total_qty > 0:
            avg_cost = (current_val + new_val) / total_qty
            
        blend.quantity_kg += required_amount
        blend.cost_price = avg_cost
        
        log_out = InventoryLog(
            bean_id=blend.id,
            transaction_type="BLENDING_OUT",
            quantity_change=required_amount,
            current_quantity=blend.quantity_kg,
            reason=f"Blending Production ({production_data.note or ''})"
        )
        db.add(log_out)
        db.flush()
        transaction_ids.append(log_out.id)
        
        db.commit()
        db.refresh(blend)
        
        return BlendingResponse(
            transaction_ids=transaction_ids,
            cost_price=avg_cost,
            produced_amount=required_amount
        )

blend_service = BlendService()
