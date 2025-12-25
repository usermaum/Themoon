"""
Bean CRUD 서비스 (Refactored for Clean Architecture)

Ref: Documents/Planning/Themoon_Rostings_v2.md
"""
from typing import List, Optional
from app.models.bean import Bean
from app.schemas.bean import BeanCreate, BeanUpdate
from app.repositories.bean_repository import BeanRepository

class BeanService:
    def __init__(self, repository: BeanRepository):
        self.repository = repository

    def get_bean(self, bean_id: int) -> Optional[Bean]:
        """ID로 원두 조회"""
        return self.repository.get(bean_id)

    def get_bean_by_sku(self, sku: str) -> Optional[Bean]:
        """SKU로 원두 조회"""
        return self.repository.get_by_sku(sku)

    def get_unique_origins(self) -> List[str]:
        """모든 원산지 목록 조회"""
        return self.repository.get_unique_origins()

    def get_unique_varieties(self) -> List[str]:
        """모든 품종 목록 조회"""
        return self.repository.get_unique_varieties()

    def get_beans(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        bean_types: Optional[List[str]] = None,
        origin: Optional[str] = None,
        exclude_blend: bool = False,
    ) -> List[Bean]:
        """원두 목록 조회 (검색 및 필터링)"""
        return self.repository.search_beans(
            skip=skip,
            limit=limit,
            search=search,
            bean_types=bean_types,
            origin=origin,
            exclude_blend=exclude_blend,
        )

    def create_bean(self, bean: BeanCreate) -> Bean:
        """새 원두 등록"""
        return self.repository.create(bean)

    def update_bean(self, bean_id: int, bean: BeanUpdate) -> Optional[Bean]:
        """원두 정보 수정"""
        db_bean = self.repository.get(bean_id)
        if not db_bean:
            return None
        return self.repository.update(db_bean, bean)

    def delete_bean(self, bean_id: int) -> bool:
        """원두 삭제"""
        obj = self.repository.remove(bean_id)
        return bool(obj)

    def get_beans_count(
        self,
        search: Optional[str] = None,
        bean_types: Optional[List[str]] = None,
        origin: Optional[str] = None,
        exclude_blend: bool = False,
    ) -> int:
        """전체 원두 개수 조회 (필터 포함)"""
        return self.repository.count_beans(
            search=search,
            bean_types=bean_types,
            origin=origin,
            exclude_blend=exclude_blend,
        )

    def update_bean_quantity(self, bean_id: int, quantity_change: float) -> Optional[Bean]:
        """원두 재고량 조정"""
        db_bean = self.repository.get(bean_id)
        if not db_bean:
            return None
        
        # 비즈니스 로직
        new_quantity = db_bean.quantity_kg + quantity_change
        if new_quantity < 0:
            new_quantity = 0
            
        return self.repository.update(db_bean, {"quantity_kg": new_quantity})

    def get_total_stock(self) -> float:
        """전체 원두 재고량 합계 조회"""
        return self.repository.get_total_stock_sum()

    def get_low_stock_beans(self, threshold: float = 5.0, limit: int = 5) -> List[Bean]:
        """재고 부족 원두 리스트 조회"""
        return self.repository.get_low_stock_beans(threshold, limit)

    def count_low_stock_beans(self, threshold: float = 5.0) -> int:
        """재고 부족 원두 총 개수 조회"""
        return self.repository.count_low_stock_beans(threshold)

    def check_existing_beans(self, names: List[str]) -> List[dict]:
        """여러 원두 이름에 대해 DB 존재 여부 확인"""
        results = []
        all_beans = self.repository.get_all_for_check()

        for name in names:
            name_clean = name.strip().lower().replace(" ", "")
            found = None

            for bean in all_beans:
                # Check Korean Name
                if (
                    bean.name_ko and bean.name_ko.strip().replace(" ", "") == name_clean
                ):
                    found = bean
                    break
                # Check English Name
                if bean.name_en and bean.name_en.strip().lower().replace(" ", "") == name_clean:
                    found = bean
                    break
                # Check Main Name
                if bean.name and bean.name.strip().lower().replace(" ", "") == name_clean:
                    found = bean
                    break
                
                if bean.name_ko and name_clean in bean.name_ko.replace(" ", ""):
                    found = bean

            if found:
                results.append(
                    {
                        "input_name": name,
                        "status": "MATCH",
                        "bean_id": found.id,
                        "bean_name": found.name_ko or found.name,
                    }
                )
            else:
                results.append(
                    {"input_name": name, "status": "NEW", "bean_id": None, "bean_name": None}
                )

        return results
