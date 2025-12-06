"""
로스팅 서비스 - 비즈니스 로직
Ref: Documents/Planning/Themoon_Rostings_v2.md
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.bean import Bean, BeanType, RoastProfile
from app.models.inventory_log import InventoryLog, InventoryChangeType

def generate_roasted_bean_sku(green_bean: Bean, profile: RoastProfile) -> str:
    """원두 SKU 생성 (예: Yirgacheffe-LIGHT)"""
    # 기본적으로 '이름-프로필' 형식을 따름 (영문 변환 로직이 필요할 수 있으나 현재는 이름 사용)
    # 실제로는 영문명이나 별도 코드를 쓰는게 좋음. 일단은 임시로 이름 사용
    return f"{green_bean.name}-{profile.value}"

def create_single_origin_roasting(
    db: Session,
    green_bean_id: int,
    input_weight: float,
    output_weight: float,
    roast_profile: RoastProfile,
    notes: str = None
):
    """
    싱글 오리진 로스팅 로직
    1. 생두 재고 차감
    2. 원두 재고 증가 (없으면 생성)
    3. 원가 및 손실률 계산
    """
    # 1. 생두 조회 및 검증
    green_bean = db.query(Bean).filter(Bean.id == green_bean_id).first()
    if not green_bean:
        raise HTTPException(status_code=404, detail="Green bean not found")
    
    if green_bean.quantity_kg < input_weight:
        raise HTTPException(status_code=400, detail=f"Not enough green bean inventory. Current: {green_bean.quantity_kg}kg")

    # 2. 생두 재고 차감 (투입)
    old_quantity = green_bean.quantity_kg
    green_bean.quantity_kg -= input_weight
    
    # 생두 재고 로그
    input_log = InventoryLog(
        bean_id=green_bean.id,
        change_type=InventoryChangeType.ROASTING_INPUT,
        change_amount=-input_weight,
        current_quantity=green_bean.quantity_kg,
        notes=f"Roasting Input to {roast_profile}"
    )
    db.add(input_log)

    # 3. 원두(Roasted Bean) 조회 또는 생성
    sku = generate_roasted_bean_sku(green_bean, roast_profile)
    roasted_bean = db.query(Bean).filter(Bean.sku == sku).first()

    # 원가 계산 (투입 생두 비용 / 생산량)
    # 단순화: 가스비, 인건비 등 제외하고 재료비만 계산
    input_cost = input_weight * green_bean.avg_price
    production_cost = input_cost / output_weight if output_weight > 0 else 0
    
    if not roasted_bean:
        # 원두 신규 생성
        roasted_bean = Bean(
            name=f"{green_bean.name} {roast_profile.value}",
            type=BeanType.ROASTED_BEAN,
            sku=sku,
            origin=green_bean.origin,    # 생두 정보 상속
            variety=green_bean.variety,
            grade=green_bean.grade,
            processing_method=green_bean.processing_method,
            roast_profile=roast_profile,
            parent_bean_id=green_bean.id,
            quantity_kg=0.0,             # 아래에서 더함
            avg_price=production_cost,   # 초기 원가는 이번 생산 원가
            cost_price=production_cost
        )
        db.add(roasted_bean)
        db.flush() # ID 생성을 위해 flush
    else:
        # 기존 원두 재고에 합산 (이동평균법 단가 갱신)
        # (기존재고 * 기존단가 + 신규생산 * 신규단가) / 전체재고
        current_value = roasted_bean.quantity_kg * roasted_bean.avg_price
        new_value = output_weight * production_cost
        total_quantity = roasted_bean.quantity_kg + output_weight
        
        if total_quantity > 0:
            roasted_bean.avg_price = (current_value + new_value) / total_quantity
            roasted_bean.cost_price = production_cost # 최근 생산 원가 갱신

    # 4. 원두 재고 증가 (생산)
    roasted_bean.quantity_kg += output_weight
    
    # 원두 재고 로그
    output_log = InventoryLog(
        bean_id=roasted_bean.id,
        change_type=InventoryChangeType.ROASTING_OUTPUT,
        change_amount=output_weight,
        current_quantity=roasted_bean.quantity_kg,
        notes=f"Roasting Output from {green_bean.name} (Loss: {((input_weight-output_weight)/input_weight*100):.1f}%)"
    )
    db.add(output_log)
    
    db.commit()
    db.refresh(roasted_bean)
    
    return roasted_bean
