from datetime import datetime
from enum import Enum

from app.api.models.product import Product
from app.api.models.sale import Sale
from app.api.schemas.sale import RevenueResponse, SaleResponse
from app.core.response import Page
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.core.enums import PeriodEnum

class SaleQuery:
    def __init__(self, db: Session):
        self.db = db

    def get_sale_by_id(self, sale_id: int):
        return self.db.query(Sale).filter(Sale.id == sale_id).first()

    def get_sales(self, skip: int = 0, limit: int = 100, start_date: datetime | None = None, end_date: datetime | None = None, product_id: int | None = None, category: str | None = None):
        query = self.db.query(Sale).join(Product, Sale.product_id == Product.id)
        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
        if product_id:
            query = query.filter(Sale.product_id == product_id)
        if category:
            query = query.filter(Product.category == category)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return Page[SaleResponse](items=items, total=total, page=skip // limit + 1, size=limit)

    def get_revenue(self, period: PeriodEnum, start_date: datetime | None = None, end_date: datetime | None = None, category: str | None = None):
        if period == PeriodEnum.DAILY:
            date_group = func.DATE(Sale.sale_date)
        elif period == PeriodEnum.WEEKLY:
            date_group = func.DATE(func.DATE_SUB(Sale.sale_date, func.INTERVAL(func.WEEKDAY(Sale.sale_date), text('DAY'))))
        elif period == PeriodEnum.MONTHLY:
            date_group = func.DATE_FORMAT(Sale.sale_date, '%Y-%m-01')
        elif period == PeriodEnum.ANNUAL:
            date_group = func.DATE_FORMAT(Sale.sale_date, '%Y-01-01')
        else:
            raise ValueError(f"Unsupported period: {period}")

        query = (
            self.db.query(
                date_group.label('period'),
                func.sum(Sale.total_amount).label('total_amount')
            )
            .join(Product, Sale.product_id == Product.id)
            .group_by(date_group)
            .order_by(date_group)
        )

        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
        if category:
            query = query.filter(Product.category == category)

        results = query.all()
        return [
            RevenueResponse(period=str(result.period), total_amount=float(result.total_amount))
            for result in results
        ]

    def create_sale(self, sale: dict):
        db_sale = Sale(**sale)
        self.db.add(db_sale)
        self.db.commit()
        self.db.refresh(db_sale)
        return db_sale
