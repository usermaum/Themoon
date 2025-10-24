"""
Excel 동기화 서비스
Excel 파일에서 데이터 임포트/엑스포트
"""

import pandas as pd
from io import BytesIO
from datetime import datetime
from models.database import SessionLocal, Bean, Blend, BlendRecipe, Inventory, Transaction, CostSetting
from services.bean_service import BeanService
from services.blend_service import BlendService


class ExcelService:
    """Excel 동기화 서비스"""

    def __init__(self, db):
        """초기화"""
        self.db = db
        self.bean_service = BeanService(db)
        self.blend_service = BlendService(db)

    def import_beans_from_excel(self, file_data: bytes):
        """Excel에서 원두 데이터 임포트"""
        try:
            # Excel 읽기
            df = pd.read_excel(file_data, sheet_name=0)

            # 필수 컬럼 확인
            required_columns = ['원두명', '로스팅', '가격/kg']
            for col in required_columns:
                if col not in df.columns:
                    return {"success": False, "error": f"필수 컬럼 '{col}'이 없습니다."}

            # 데이터 임포트
            imported_count = 0
            error_count = 0
            errors = []

            for idx, row in df.iterrows():
                try:
                    # 이미 존재하는 원두 확인
                    bean_name = str(row['원두명']).strip()
                    existing = self.db.query(Bean).filter(Bean.name == bean_name).first()

                    if existing:
                        # 기존 원두 업데이트
                        existing.roast_level = str(row['로스팅']).strip()
                        existing.price_per_kg = float(row['가격/kg'])
                        existing.updated_at = datetime.utcnow()
                    else:
                        # 새 원두 추가
                        bean = Bean(
                            no=int(row.get('No', 0)) if pd.notna(row.get('No')) else 0,
                            name=bean_name,
                            country_code=str(row.get('국가', '')).strip() if pd.notna(row.get('국가')) else None,
                            roast_level=str(row['로스팅']).strip(),
                            price_per_kg=float(row['가격/kg']),
                            description=str(row.get('설명', '')).strip() if pd.notna(row.get('설명')) else None,
                            status="active"
                        )
                        self.db.add(bean)

                    imported_count += 1

                except Exception as e:
                    error_count += 1
                    errors.append(f"행 {idx + 1}: {str(e)}")

            self.db.commit()

            return {
                "success": True,
                "imported_count": imported_count,
                "error_count": error_count,
                "errors": errors
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def import_blends_from_excel(self, file_data: bytes):
        """Excel에서 블렌드 데이터 임포트"""
        try:
            # Excel 읽기
            df = pd.read_excel(file_data, sheet_name=0)

            # 필수 컬럼 확인
            required_columns = ['블렌드명', '타입']
            for col in required_columns:
                if col not in df.columns:
                    return {"success": False, "error": f"필수 컬럼 '{col}'이 없습니다."}

            # 데이터 임포트
            imported_count = 0
            error_count = 0
            errors = []

            for idx, row in df.iterrows():
                try:
                    # 이미 존재하는 블렌드 확인
                    blend_name = str(row['블렌드명']).strip()
                    existing = self.db.query(Blend).filter(Blend.name == blend_name).first()

                    if existing:
                        # 기존 블렌드 업데이트
                        existing.blend_type = str(row['타입']).strip()
                        existing.description = str(row.get('설명', '')).strip() if pd.notna(row.get('설명')) else None
                        existing.updated_at = datetime.utcnow()
                    else:
                        # 새 블렌드 추가
                        blend = Blend(
                            name=blend_name,
                            blend_type=str(row['타입']).strip(),
                            description=str(row.get('설명', '')).strip() if pd.notna(row.get('설명')) else None,
                            total_portion=int(row.get('포션', 0)) if pd.notna(row.get('포션')) else 0,
                            status="active"
                        )
                        self.db.add(blend)

                    imported_count += 1

                except Exception as e:
                    error_count += 1
                    errors.append(f"행 {idx + 1}: {str(e)}")

            self.db.commit()

            return {
                "success": True,
                "imported_count": imported_count,
                "error_count": error_count,
                "errors": errors
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def export_beans_to_excel(self):
        """원두 데이터를 Excel로 내보내기"""
        beans = self.db.query(Bean).all()

        data = []
        for bean in beans:
            data.append({
                "No": bean.no,
                "원두명": bean.name,
                "국가": bean.country_code or "-",
                "로스팅": bean.roast_level,
                "가격/kg": bean.price_per_kg,
                "상태": bean.status,
                "설명": bean.description or ""
            })

        df = pd.DataFrame(data)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="원두", index=False)

        output.seek(0)
        return output

    def export_blends_to_excel(self):
        """블렌드 데이터를 Excel로 내보내기"""
        blends = self.db.query(Blend).all()

        data = []
        for blend in blends:
            recipes = self.db.query(BlendRecipe).filter(BlendRecipe.blend_id == blend.id).all()
            recipe_str = ", ".join([f"{self.db.query(Bean).filter(Bean.id == r.bean_id).first().name}({r.portion_count})"
                                   for r in recipes])

            data.append({
                "블렌드명": blend.name,
                "타입": blend.blend_type,
                "포션": blend.total_portion,
                "레시피": recipe_str,
                "상태": blend.status,
                "설명": blend.description or ""
            })

        df = pd.DataFrame(data)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="블렌드", index=False)

        output.seek(0)
        return output

    def export_inventory_to_excel(self):
        """재고 데이터를 Excel로 내보내기"""
        inventory = self.db.query(Inventory).all()

        data = []
        for inv in inventory:
            bean = self.db.query(Bean).filter(Bean.id == inv.bean_id).first()

            if bean:
                data.append({
                    "원두명": bean.name,
                    "현재재고": inv.quantity_kg,
                    "최소": inv.min_quantity_kg,
                    "최대": inv.max_quantity_kg,
                    "가격/kg": bean.price_per_kg,
                    "총가치": inv.quantity_kg * bean.price_per_kg
                })

        df = pd.DataFrame(data)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="재고", index=False)

        output.seek(0)
        return output

    def export_transactions_to_excel(self, days: int = 30):
        """거래 데이터를 Excel로 내보내기"""
        from datetime import timedelta

        start_date = datetime.now() - timedelta(days=days)
        transactions = self.db.query(Transaction).filter(
            Transaction.created_at >= start_date
        ).all()

        data = []
        for trans in transactions:
            bean = self.db.query(Bean).filter(Bean.id == trans.bean_id).first()

            if bean:
                data.append({
                    "날짜": trans.created_at.strftime("%Y-%m-%d %H:%M"),
                    "거래유형": trans.transaction_type,
                    "원두명": bean.name,
                    "수량": trans.quantity_kg,
                    "단가": trans.price_per_unit,
                    "합계": trans.total_amount,
                    "설명": trans.description or ""
                })

        df = pd.DataFrame(data)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="거래기록", index=False)

        output.seek(0)
        return output

    def export_all_to_excel(self):
        """모든 데이터를 Excel로 내보내기"""
        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 원두 데이터
            beans = self.db.query(Bean).all()
            bean_data = []
            for bean in beans:
                bean_data.append({
                    "No": bean.no,
                    "원두명": bean.name,
                    "국가": bean.country_code or "-",
                    "로스팅": bean.roast_level,
                    "가격/kg": bean.price_per_kg,
                    "상태": bean.status
                })
            df_beans = pd.DataFrame(bean_data)
            df_beans.to_excel(writer, sheet_name="원두", index=False)

            # 블렌드 데이터
            blends = self.db.query(Blend).all()
            blend_data = []
            for blend in blends:
                recipes = self.db.query(BlendRecipe).filter(BlendRecipe.blend_id == blend.id).all()
                recipe_str = ", ".join([f"{self.db.query(Bean).filter(Bean.id == r.bean_id).first().name}({r.portion_count})"
                                       for r in recipes])
                blend_data.append({
                    "블렌드명": blend.name,
                    "타입": blend.blend_type,
                    "포션": blend.total_portion,
                    "레시피": recipe_str,
                    "상태": blend.status
                })
            df_blends = pd.DataFrame(blend_data)
            df_blends.to_excel(writer, sheet_name="블렌드", index=False)

            # 재고 데이터
            inventory = self.db.query(Inventory).all()
            inv_data = []
            for inv in inventory:
                bean = self.db.query(Bean).filter(Bean.id == inv.bean_id).first()
                if bean:
                    inv_data.append({
                        "원두명": bean.name,
                        "현재": inv.quantity_kg,
                        "최소": inv.min_quantity_kg,
                        "최대": inv.max_quantity_kg
                    })
            df_inventory = pd.DataFrame(inv_data)
            df_inventory.to_excel(writer, sheet_name="재고", index=False)

        output.seek(0)
        return output

    def create_import_template(self):
        """임포트 템플릿 생성"""
        output = BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 원두 임포트 템플릿
            bean_template = pd.DataFrame({
                "No": [1, 2],
                "원두명": ["에티오피아", "케냐"],
                "국가": ["Eth", "K"],
                "로스팅": ["W", "N"],
                "가격/kg": [25000, 30000],
                "설명": ["설명 입력", "설명 입력"]
            })
            bean_template.to_excel(writer, sheet_name="원두_템플릿", index=False)

            # 블렌드 임포트 템플릿
            blend_template = pd.DataFrame({
                "블렌드명": ["풀문 블렌드", "뉴문 블렌딩"],
                "타입": ["풀문", "뉴문"],
                "포션": [4, 3],
                "설명": ["설명 입력", "설명 입력"]
            })
            blend_template.to_excel(writer, sheet_name="블렌드_템플릿", index=False)

        output.seek(0)
        return output
