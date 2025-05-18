from sqlalchemy import Column, Integer, String, Float, Index
from app.config.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)

    __table_args__ = (
        Index("idx_product_name", "name"),
    )