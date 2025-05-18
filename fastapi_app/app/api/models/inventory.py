from sqlalchemy import Column, Integer, ForeignKey, DateTime, Index
from app.config.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    stock = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False, index=True)

    __table_args__ = (
        Index("idx_inventory_product", "product_id"),
    )