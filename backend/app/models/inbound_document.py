from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.utils.timezone import get_kst_now

class InboundDocument(Base):
    __tablename__ = "inbound_documents"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String, unique=True, index=True, nullable=True, comment="Contract/Order Number")
    
    supplier_name = Column(String, nullable=True) # Snapshot
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    receiver_name = Column(String, nullable=True)
    
    invoice_date = Column(String, nullable=True)
    total_amount = Column(Float, nullable=True)
    image_url = Column(String, nullable=True, comment="Legacy / Primary View Link")
    drive_file_id = Column(String, nullable=True, comment="Legacy / Main Filename")
    
    # Tiered Storage
    original_image_path = Column(String(500), nullable=True)
    webview_image_path = Column(String(500), nullable=True)
    thumbnail_image_path = Column(String(500), nullable=True)
    image_width = Column(Integer, nullable=True)
    image_height = Column(Integer, nullable=True)
    file_size_bytes = Column(Integer, nullable=True)
    processing_status = Column(String(20), default="pending")
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_kst_now)

    # Relationships
    supplier = relationship("app.models.supplier.Supplier", back_populates="inbound_documents")
    inventory_logs = relationship("app.models.inventory_log.InventoryLog", back_populates="inbound_document")

    # New relationships for OCR data (Option B redesign)
    detail = relationship("app.models.inbound_document_detail.InboundDocumentDetail", back_populates="inbound_document", uselist=False)
    receiver = relationship("app.models.inbound_receiver.InboundReceiver", back_populates="inbound_document", uselist=False)
    items = relationship("app.models.inbound_item.InboundItem", back_populates="inbound_document", order_by="app.models.inbound_item.InboundItem.item_order")
