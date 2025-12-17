from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- OCR/Analysis Schemas ---
class OCRItem(BaseModel):
    bean_name: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None

class OCRResponse(BaseModel):
    supplier_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    items: List[OCRItem] = []
    drive_link: Optional[str] = None

# --- Inbound Document DB Schemas ---
class InboundDocumentBase(BaseModel):
    supplier_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    image_url: Optional[str] = None
    drive_file_id: Optional[str] = None
    notes: Optional[str] = None

class InboundDocumentCreate(InboundDocumentBase):
    pass

class InboundDocument(InboundDocumentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- API Request Schemas ---
class AnalyzeUrlRequest(BaseModel):
    url: str

class InboundConfirmRequest(BaseModel):
    # Data to save to DB (Log + Document)
    document: InboundDocumentCreate
    items: List[OCRItem] # Validated list of items
