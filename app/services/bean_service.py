"""
원두 관리 서비스
CRUD 기능 + 비즈니스 로직
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import sys
import os

# 프로젝트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import Bean, Inventory, BlendRecipe
from utils.constants import BEANS_DATA, get_bean_by_no

class BeanService:
    """원두 관리 서비스"""

    def __init__(self, db: Session):
        self.db = db

    # ═══════════════════════════════════════════════════════════════
    # 📖 조회 (READ)
    # ═══════════════════════════════════════════════════════════════

    def get_all_beans(self, skip: int = 0, limit: int = 100) -> List[Bean]:
        """모든 원두 조회"""
        return self.db.query(Bean).offset(skip).limit(limit).all()

    def get_bean_by_id(self, bean_id: int) -> Optional[Bean]:
        """ID로 원두 조회"""
        return self.db.query(Bean).filter(Bean.id == bean_id).first()

    def get_bean_by_no(self, no: int) -> Optional[Bean]:
        """번호로 원두 조회"""
        return self.db.query(Bean).filter(Bean.no == no).first()

    def get_bean_by_name(self, name: str) -> Optional[Bean]:
        """이름으로 원두 조회"""
        return self.db.query(Bean).filter(Bean.name == name).first()

    def get_beans_by_country(self, country_code: str) -> List[Bean]:
        """국가별 원두 조회"""
        return self.db.query(Bean).filter(Bean.country_code == country_code).all()

    def get_beans_by_roast_level(self, roast_level: str) -> List[Bean]:
        """로스팅 레벨별 원두 조회"""
        return self.db.query(Bean).filter(Bean.roast_level == roast_level).all()

    def get_active_beans(self) -> List[Bean]:
        """활성 원두만 조회"""
        return self.db.query(Bean).filter(Bean.status == "active").all()

    def get_bean_count(self) -> int:
        """전체 원두 개수"""
        return self.db.query(Bean).count()

    # ═══════════════════════════════════════════════════════════════
    # ➕ 생성 (CREATE)
    # ═══════════════════════════════════════════════════════════════

    def create_bean(
        self,
        no: int,
        name: str,
        roast_level: str,
        country_code: str = None,
        country_name: str = None,
        description: str = None,
        price_per_kg: float = 0.0,
        image_url: str = None
    ) -> Bean:
        """새 원두 생성"""
        # 중복 확인
        if self.get_bean_by_no(no) or self.get_bean_by_name(name):
            raise ValueError(f"원두 번호 {no} 또는 이름 '{name}'이 이미 존재합니다")

        bean = Bean(
            no=no,
            name=name,
            roast_level=roast_level,
            country_code=country_code,
            country_name=country_name,
            description=description,
            price_per_kg=price_per_kg,
            image_url=image_url,
            status="active"
        )
        self.db.add(bean)
        self.db.commit()
        self.db.refresh(bean)

        # 재고 자동 생성
        inventory = Inventory(bean_id=bean.id)
        self.db.add(inventory)
        self.db.commit()

        return bean

    # ═══════════════════════════════════════════════════════════════
    # ✏️ 수정 (UPDATE)
    # ═══════════════════════════════════════════════════════════════

    def update_bean(
        self,
        bean_id: int,
        name: str = None,
        roast_level: str = None,
        country_code: str = None,
        country_name: str = None,
        description: str = None,
        price_per_kg: float = None,
        image_url: str = None,
        status: str = None
    ) -> Optional[Bean]:
        """원두 정보 수정"""
        bean = self.get_bean_by_id(bean_id)
        if not bean:
            return None

        if name is not None:
            bean.name = name
        if roast_level is not None:
            bean.roast_level = roast_level
        if country_code is not None:
            bean.country_code = country_code
        if country_name is not None:
            bean.country_name = country_name
        if description is not None:
            bean.description = description
        if price_per_kg is not None:
            bean.price_per_kg = price_per_kg
        if image_url is not None:
            bean.image_url = image_url
        if status is not None:
            bean.status = status

        bean.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(bean)

        return bean

    # ═══════════════════════════════════════════════════════════════
    # 🗑️ 삭제 (DELETE)
    # ═══════════════════════════════════════════════════════════════

    def delete_bean(self, bean_id: int) -> bool:
        """원두 삭제 (소프트 삭제)"""
        bean = self.get_bean_by_id(bean_id)
        if not bean:
            return False

        # 소프트 삭제 (상태만 변경)
        bean.status = "inactive"
        self.db.commit()
        return True

    def hard_delete_bean(self, bean_id: int) -> bool:
        """원두 완전 삭제"""
        bean = self.get_bean_by_id(bean_id)
        if not bean:
            return False

        # 연관 데이터 확인
        blend_recipes = self.db.query(BlendRecipe).filter(BlendRecipe.bean_id == bean_id).all()
        if blend_recipes:
            raise ValueError(f"이 원두는 {len(blend_recipes)}개 블렌드에 포함되어 있습니다")

        self.db.delete(bean)
        self.db.commit()
        return True

    # ═══════════════════════════════════════════════════════════════
    # 📊 분석 & 통계
    # ═══════════════════════════════════════════════════════════════

    def get_beans_summary(self) -> dict:
        """원두 전체 요약"""
        all_beans = self.get_active_beans()
        roast_summary = {}

        for bean in all_beans:
            level = bean.roast_level
            if level not in roast_summary:
                roast_summary[level] = 0
            roast_summary[level] += 1

        return {
            "total_beans": len(all_beans),
            "by_roast_level": roast_summary,
            "beans": all_beans
        }

    def get_most_used_beans(self, limit: int = 5) -> List[dict]:
        """자주 사용되는 원두 TOP N"""
        from sqlalchemy import func
        from models.database import BlendRecipe

        results = self.db.query(
            Bean,
            func.count(BlendRecipe.id).label("usage_count")
        ).outerjoin(BlendRecipe).group_by(Bean.id).order_by(
            desc("usage_count")
        ).limit(limit).all()

        return [{"bean": r[0], "usage_count": r[1]} for r in results]

    # ═══════════════════════════════════════════════════════════════
    # 🔧 초기화 & 데이터 로드
    # ═══════════════════════════════════════════════════════════════

    def init_default_beans(self) -> int:
        """기본 원두 13종 로드"""
        count = 0

        for bean_data in BEANS_DATA:
            existing = self.get_bean_by_no(bean_data["no"])
            if not existing:
                self.create_bean(
                    no=bean_data["no"],
                    name=bean_data["name"],
                    roast_level=bean_data["roast_level"],
                    country_code=bean_data["country_code"],
                    country_name=bean_data["country_name"],
                    description=bean_data["description"],
                    price_per_kg=bean_data["price_per_kg"]
                )
                count += 1

        return count

    def export_as_dict(self) -> List[dict]:
        """딕셔너리로 내보내기 (CSV/Excel용)"""
        beans = self.get_active_beans()
        return [
            {
                "No": b.no,
                "국가코드": b.country_code or "-",
                "국가": b.country_name or "-",
                "원두명": b.name,
                "로스팅": b.roast_level,
                "설명": b.description or "",
                "단가(원/kg)": b.price_per_kg,
            }
            for b in beans
        ]


if __name__ == "__main__":
    # 테스트 코드
    from models.database import SessionLocal, init_db

    init_db()
    db = SessionLocal()
    service = BeanService(db)

    # 기본 원두 로드
    count = service.init_default_beans()
    print(f"✅ {count}개 원두 로드 완료")

    # 전체 조회
    summary = service.get_beans_summary()
    print(f"📊 총 원두: {summary['total_beans']}종")
    print(f"🔥 로스팅 레벨: {summary['by_roast_level']}")

    db.close()
