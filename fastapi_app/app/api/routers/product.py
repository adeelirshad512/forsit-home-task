from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.api.schemas.product import PageProductResponse, ProductCreate, ProductResponse
from app.api.services.product import ProductService
from app.core.response import success_response
from app.core.auth import get_api_key

router = APIRouter()

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
    api_key: str = Depends(get_api_key),
):
    return product_service.create_product(product)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    api_key: str = Depends(get_api_key),
):
    return product_service.get_product(product_id)

@router.get("/", response_model=PageProductResponse)
def get_products(
    skip: int = 0,
    limit: int = 100,
    product_service: ProductService = Depends(get_product_service),
    api_key: str = Depends(get_api_key),
):
    return product_service.get_products(skip, limit)
