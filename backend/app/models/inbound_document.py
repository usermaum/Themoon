from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class InboundDocument(Base):
    __tablename__ = "inbound_documents"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String, unique=True, index=True, nullable=True, comment="Contract/Order Number")
    
    supplier_name = Column(String, nullable=True) # Snapshot
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    receiver_name = Column(String, nullable=True)
    
    invoice_date = Column(String, nullable=True)
    total_amount = Column(Float, nullable=True)
    image_url = Column(String, nullable=True, comment="Google Drive WebView Link or Local Path")
    drive_file_id = Column(String, nullable=True, comment="Google Drive File ID or Local Filename")
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())

    # Relationships
    supplier = relationship("app.models.supplier.Supplier", back_populates="inbound_documents")
    inventory_logs = relationship("app.models.inventory_log.InventoryLog", back_populates="inbound_document")
