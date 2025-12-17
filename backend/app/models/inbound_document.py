from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class InboundDocument(Base):
    __tablename__ = "inbound_documents"

    id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String, nullable=True)
    invoice_date = Column(String, nullable=True)
    total_amount = Column(Float, nullable=True)
    image_url = Column(String, nullable=True, comment="Google Drive WebView Link")
    drive_file_id = Column(String, nullable=True, comment="Google Drive File ID")
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())

    # Relationship to InventoryLogs (One Document -> Many Logs)
    inventory_logs = relationship("app.models.inventory_log.InventoryLog", back_populates="inbound_document")
