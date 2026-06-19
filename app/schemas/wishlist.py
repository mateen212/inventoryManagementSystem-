from pydantic import BaseModel
from datetime import datetime

class WishlistBase(BaseModel):
    user_id: int
    product_id: int

class WishlistCreate(WishlistBase):
    pass

class WishlistOut(WishlistBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
