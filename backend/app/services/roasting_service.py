"""
로스팅 서비스 - 비즈니스 로직
Ref: Documents/Planning/Themoon_Rostings_v2.md
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.bean import Bean, BeanType, RoastProfile
from app.models.inventory_log import InventoryLog, InventoryChangeType
from app.models.blend import Blend

def generate_roasted_bean_sku(green_bean: Bean, profile: RoastProfile) -> str:
    """원두 SKU 생성 (예: Yirgacheffe-신콩)"""
    # 우리 드립바는 두 가지 맛(신콩, 탄콩)을 주로 사용
    profile_kr = "신콩" if profile == RoastProfile.LIGHT else "탄콩" if profile == RoastProfile.DARK else "미디엄"
    return f"{green_bean.name}-{profile_kr}"

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
        profile_kr = "신콩" if roast_profile == RoastProfile.LIGHT else "탄콩" if roast_profile == RoastProfile.DARK else "미디엄"
        roasted_bean = Bean(
            name=f"{green_bean.name} {profile_kr}",
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

def create_blend_roasting(
    db: Session,
    blend_id: int,
    output_weight: float,
    input_weight: float = None,
    notes: str = None
):
    """
    블렌드 로스팅 로직
    1. 블렌드 레시피 기반 생두 투입량 자동 계산 및 차감
    2. 블렌드 원두(Roasted) 생성 및 입고
    """
    # 1. 블렌드 조회
    blend = db.query(Blend).filter(Blend.id == blend_id).first()
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
        bean_id = item['bean_id']
        ratio = item['ratio']
        
        bean = db.query(Bean).filter(Bean.id == bean_id).first()
        if not bean:
            raise HTTPException(status_code=404, detail=f"Bean ID {bean_id} in recipe not found")

        # 필요량 계산
        if input_weight:
            # 실제 투입량이 주어진 경우 비율대로 배분
            required_input = input_weight * ratio
        else:
            # 목표 생산량 역산: (목표량 * 비율) / (1 - 손실률)
            loss_rate = bean.expected_loss_rate if bean.expected_loss_rate is not None else 0.15
            target_part_weight = output_weight * ratio
            required_input = target_part_weight / (1 - loss_rate)
        
        if bean.quantity_kg < required_input:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {bean.name}. Required: {required_input:.2f}kg, Available: {bean.quantity_kg:.2f}kg")
            
        input_items.append({
            "bean": bean,
            "required_input": required_input,
            "cost": required_input * bean.avg_price
        })
        
        total_input_cost += required_input * bean.avg_price
        total_input_weight += required_input

    # 3. 재고 차감 실행
    for item in input_items:
        bean = item['bean']
        amount = item['required_input']
        
        bean.quantity_kg -= amount
        
        log = InventoryLog(
            bean_id=bean.id,
            change_type=InventoryChangeType.ROASTING_INPUT,
            change_amount=-amount,
            current_quantity=bean.quantity_kg,
            notes=f"Used for Blend: {blend.name}"  
        )
        db.add(log)

    # 4. 블렌드 원두 생성/업데이트
    production_cost = total_input_cost / output_weight if output_weight > 0 else 0
    sku = f"BLEND-{blend.id}-{blend.name.replace(' ', '')}"
    
    # Check if roasted blend bean exists
    roasted_bean = db.query(Bean).filter(Bean.sku == sku).first()
    
    if not roasted_bean:
        roast_profile = RoastProfile.MEDIUM
        roasted_bean = Bean(
            name=f"{blend.name}",
            type=BeanType.ROASTED_BEAN,
            sku=sku,
            origin="Blend",
            roast_profile=roast_profile,
            quantity_kg=0.0,
            avg_price=production_cost,
            cost_price=production_cost,
            notes=f"Blend based on {blend.name}"
        )
        db.add(roasted_bean)
        db.flush()
    else:
        # 이동평균법 단가 갱신
        current_val = roasted_bean.quantity_kg * roasted_bean.avg_price
        new_val = output_weight * production_cost
        total_qty = roasted_bean.quantity_kg + output_weight
        
        if total_qty > 0:
            roasted_bean.avg_price = (current_val + new_val) / total_qty
            roasted_bean.cost_price = production_cost

    roasted_bean.quantity_kg += output_weight
    
    # 생산 로그
    loss_p = (total_input_weight - output_weight) / total_input_weight * 100 if total_input_weight > 0 else 0
    out_log = InventoryLog(
        bean_id=roasted_bean.id,
        change_type=InventoryChangeType.ROASTING_OUTPUT,
        change_amount=output_weight,
        current_quantity=roasted_bean.quantity_kg,
        notes=f"Blend Roasting: {blend.name} (Loss: {loss_p:.1f}%)"
    )
    db.add(out_log)

    db.commit()
    db.refresh(roasted_bean)
    
    return roasted_bean
