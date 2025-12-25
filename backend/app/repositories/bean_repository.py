from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.bean import Bean, BeanType
from app.schemas.bean import BeanCreate, BeanUpdate
from app.repositories.base_repository import BaseRepository


class BeanRepository(BaseRepository[Bean, BeanCreate, BeanUpdate]):
    def __init__(self, db: Session):
        super().__init__(Bean, db)

    def get_by_name(self, name: str) -> Optional[Bean]:
        return self.db.query(Bean).filter(Bean.name == name).first()

    def get_by_sku(self, sku: str) -> Optional[Bean]:
        """SKU로 원두 조회"""
        return self.db.query(Bean).filter(Bean.sku == sku).first()

    def get_unique_origins(self) -> List[str]:
        """등록된 모든 원두의 원산지 목록 조회"""
        results = self.db.query(Bean.origin).distinct().all()
        return [r[0] for r in results if r[0]]

    def get_unique_varieties(self) -> List[str]:
        """등록된 모든 원두의 품종 목록 조회"""
        results = self.db.query(Bean.variety).distinct().all()
        return [r[0] for r in results if r[0]]

    def search_beans(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        bean_types: Optional[List[str]] = None,
        origin: Optional[str] = None,
        exclude_blend: bool = False,
    ) -> List[Bean]:
        query = self.db.query(Bean)

        if search:
            query = query.filter(
                (Bean.name.contains(search))
                | (Bean.name_ko.contains(search))
                | (Bean.name_en.contains(search))
                | (Bean.origin.contains(search))
                | (Bean.origin_ko.contains(search))
                | (Bean.origin_en.contains(search))
                | (Bean.variety.contains(search))
            )

        if bean_types:
            query = query.filter(Bean.type.in_(bean_types))

        if origin:
            query = query.filter(Bean.origin == origin)

        if exclude_blend:
            query = query.filter(Bean.origin != "Blend")

        return query.offset(skip).limit(limit).all()

    def count_beans(
        self,
        search: Optional[str] = None,
        bean_types: Optional[List[str]] = None,
        origin: Optional[str] = None,
        exclude_blend: bool = False,
    ) -> int:
        query = self.db.query(Bean)

        if search:
            query = query.filter(
                (Bean.name.contains(search))
                | (Bean.name_ko.contains(search))
                | (Bean.name_en.contains(search))
                | (Bean.origin.contains(search))
                | (Bean.origin_ko.contains(search))
                | (Bean.origin_en.contains(search))
                | (Bean.variety.contains(search))
            )

        if bean_types:
            query = query.filter(Bean.type.in_(bean_types))

        if origin:
            query = query.filter(Bean.origin == origin)

        if exclude_blend:
            query = query.filter(Bean.origin != "Blend")

        return query.count()

    def get_total_stock_sum(self) -> float:
        result = self.db.query(Bean).with_entities(Bean.quantity_kg).all()
        return sum(row.quantity_kg for row in result)

    def get_low_stock_beans(self, threshold: float = 5.0, limit: int = 5) -> List[Bean]:
        return (
            self.db.query(Bean)
            .filter(Bean.quantity_kg < threshold)
            .order_by(Bean.quantity_kg.asc())
            .limit(limit)
            .all()
        )

    def count_low_stock_beans(self, threshold: float = 5.0) -> int:
        return self.db.query(Bean).filter(Bean.quantity_kg < threshold).count()

    def get_all_for_check(self) -> List[Bean]:
        """배치 확인을 위한 가벼운 전체 조회 (필요한 컬럼만 조회 가능하지만 현재는 전체 객체 반환)"""
        return self.db.query(Bean).all()
