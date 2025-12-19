from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    representative_name = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    registration_number = Column(String, nullable=True)
    
    # Relationship
    inbound_documents = relationship("app.models.inbound_document.InboundDocument", back_populates="supplier")
