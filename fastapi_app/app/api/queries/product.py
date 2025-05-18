from app.api.models.product import Product
from app.api.schemas.product import ProductResponse
from app.core.response import Page
from sqlalchemy import func
from sqlalchemy.orm import Session


class ProductQuery:
    def __init__(self, db: Session):
        self.db = db

    def get_product_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_product_by_name(self, name: str):
        return self.db.query(Product).filter(Product.name == name).first()

    def get_products(self, skip: int = 0, limit: int = 100):
        query = self.db.query(Product)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return Page[ProductResponse](items=items, total=total, page=skip // limit + 1, size=limit)

    def create_product(self, product: dict):
        db_product = Product(**product)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product