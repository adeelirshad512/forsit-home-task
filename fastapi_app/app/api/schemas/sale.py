from datetime import datetime
from typing import Optional

from app.core.response import Page
from pydantic import (BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt,
                      model_validator)


class SaleBase(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt
    total_amount: PositiveFloat
    sale_date: datetime

class SaleCreate(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt

    model_config = ConfigDict(extra="forbid")

class SaleResponse(SaleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RevenueResponse(BaseModel):
    period: str
    total_amount: float = Field(default=0.0, description="Total amount rounded to 2 decimal places")

    @model_validator(mode="before")
    @classmethod
    def round_total_amount(cls, values):
        if "total_amount" in values:
            values["total_amount"] = round(values["total_amount"], 2)
        return values

    model_config = ConfigDict(from_attributes=True)

PageSaleResponse = Page[SaleResponse]
