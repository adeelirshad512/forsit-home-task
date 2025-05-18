from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from app.config.database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    sale_date = Column(DateTime, nullable=False, index=True)

    __table_args__ = (
        Index("idx_sale_date_product", "sale_date", "product_id"),
    )