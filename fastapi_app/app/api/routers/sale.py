from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.schemas.sale import PageSaleResponse, SaleCreate, SaleResponse, RevenueResponse
from app.api.services.sale import SaleService
from app.core.response import ResponseModel, success_response, CustomResponse
from datetime import datetime

router = APIRouter()

def get_sale_service(db: Session = Depends(get_db)) -> SaleService:
    return SaleService(db)

@router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, sale_service: SaleService = Depends(get_sale_service)):
    return sale_service.create_sale(sale)

@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, sale_service: SaleService = Depends(get_sale_service)):
    return sale_service.get_sale(sale_id)

@router.get("/", response_model=PageSaleResponse)
def get_sales(
    skip: int = 0,
    limit: int = 100,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    product_id: int | None = None,
    category: str | None = None,
    sale_service: SaleService = Depends(get_sale_service)
):
    return sale_service.get_sales(skip, limit, start_date, end_date, product_id, category)



@router.get("/revenue/", response_model=ResponseModel[List[RevenueResponse]])
def get_revenue(
    period: str = Query(..., enum=["daily", "weekly", "monthly", "annual"]),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    sale_service: SaleService = Depends(get_sale_service),
):
    data = sale_service.get_revenue(period, start_date, end_date, category)
    return ResponseModel[List[RevenueResponse]](result=data)
