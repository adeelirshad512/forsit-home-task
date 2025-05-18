from pydantic import BaseModel, PositiveInt, NonNegativeInt, ConfigDict
from datetime import datetime
from app.core.response import Page

class InventoryBase(BaseModel):
    product_id: PositiveInt
    stock: NonNegativeInt
    updated_at: datetime

class InventoryUpdate(BaseModel):
    stock: NonNegativeInt

    model_config = ConfigDict(extra="forbid")

class InventoryResponse(InventoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class LowStockAlert(BaseModel):
    product_id: int
    product_name: str
    stock: int

PageInventoryResponse = Page[InventoryResponse]