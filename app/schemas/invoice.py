from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InvoiceBase(BaseModel):
    order_id: int
    invoice_number: str
    tax: float = 0.0
    total_amount: float

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceOut(InvoiceBase):
    id: int
    pdf_path: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True
