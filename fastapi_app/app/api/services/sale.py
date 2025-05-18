from datetime import datetime, timezone
from typing import List, Optional
from app.api.queries.product import ProductQuery
from app.api.queries.sale import SaleQuery
from app.api.schemas.sale import PageSaleResponse, RevenueResponse, SaleCreate, SaleResponse
from app.core.enums import ErrorType, PeriodEnum
from app.core.exceptions import CustomBusinessError
from app.core.logger import logger
from app.core.response import success_response
from fastapi import status
from sqlalchemy.orm import Session
from enum import Enum


class SaleService:
    def __init__(self, db: Session):
        self.db = db
        self.sale_query = SaleQuery(db)
        self.product_query = ProductQuery(db)

    def create_sale(self, sale: SaleCreate) -> SaleResponse:
        product = self.product_query.get_product_by_id(sale.product_id)
        if not product:
            raise CustomBusinessError(
                message="Product not found",
                error_type=ErrorType.NOT_FOUND_ERROR,
                status_code=status.HTTP_404_NOT_FOUND
            )
        sale_data = sale.model_dump()
        sale_data["total_amount"] = product.price * sale.quantity
        sale_data["sale_date"] = datetime.now(timezone.utc)
        created_sale = self.sale_query.create_sale(sale_data)
        logger.info(f"Sale created for product ID: {sale.product_id}")
        return success_response(SaleResponse.model_validate(created_sale), SaleResponse)

    def get_sale(self, sale_id: int) -> SaleResponse:
        sale = self.sale_query.get_sale_by_id(sale_id)
        if not sale:
            raise CustomBusinessError(
                message="Sale not found",
                error_type=ErrorType.NOT_FOUND_ERROR,
                status_code=status.HTTP_404_NOT_FOUND
            )
        return success_response(SaleResponse.model_validate(sale), SaleResponse)

    def get_sales(
        self,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        product_id: Optional[int] = None,
        category: Optional[str] = None,
    ) -> PageSaleResponse:
        paginated_sales = self.sale_query.get_sales(skip, limit, start_date, end_date, product_id, category)
        return success_response(paginated_sales, PageSaleResponse)

    def get_revenue(
        self,
        period: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: Optional[str] = None,
    ) -> List[RevenueResponse]:
        if period not in PeriodEnum.__members__.values() and period not in [e.value for e in PeriodEnum]:
            raise CustomBusinessError(
                message="Invalid period",
                error_type=ErrorType.VALIDATION_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        revenue_data = self.sale_query.get_revenue(period, start_date, end_date, category)
        return [
            RevenueResponse(
                period=str(item.period),
                total_amount=float(item.total_amount)
            )
            for item in revenue_data
        ]
