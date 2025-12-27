from typing import Optional
from sqlalchemy.orm import Session
from app.models.blend import Blend
from app.schemas.blend import BlendCreate, BlendUpdate
from app.repositories.base_repository import BaseRepository


class BlendRepository(BaseRepository[Blend, BlendCreate, BlendUpdate]):
    def __init__(self, db: Session):
        super().__init__(Blend, db)
