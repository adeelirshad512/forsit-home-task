from pydantic import BaseModel, constr, PositiveFloat, PositiveInt, ConfigDict
from app.core.response import Page

class ProductBase(BaseModel):
    name: constr(min_length=1, max_length=255)
    category: constr(min_length=1, max_length=100)
    price: PositiveFloat

    model_config = ConfigDict(extra="forbid")

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

PageProductResponse = Page[ProductResponse]