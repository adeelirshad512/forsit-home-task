from typing import Optional
from app.api.queries.product import ProductQuery
from app.api.schemas.product import PageProductResponse, ProductCreate, ProductResponse
from app.core.enums import ErrorType
from app.core.exceptions import CustomBusinessError
from app.core.logger import logger
from app.core.response import success_response
from fastapi import status
from sqlalchemy.orm import Session
from functools import lru_cache

class ProductService:
    def __init__(self, db: Session, product_query: Optional[ProductQuery] = None):
        self.db = db
        self.product_query: ProductQuery = product_query or ProductQuery(db)

    def create_product(self, product: ProductCreate) -> ProductResponse:
        if self.product_query.get_product_by_name(product.name):
            logger.warning(f"Duplicate product creation attempt with name: {product.name}")
            raise CustomBusinessError(
                message="Product name already exists",
                error_type=ErrorType.DUPLICATION_ERROR,
                status_code=status.HTTP_409_CONFLICT
            )
        product_data = product.model_dump()
        created_product = self.product_query.create_product(product_data)
        logger.info(f"Product created successfully: id={created_product.id}, name={created_product.name}")
        return success_response(ProductResponse.model_validate(created_product), ProductResponse)

    @lru_cache(maxsize=128)
    def get_product(self, product_id: int) -> ProductResponse:
        product = self.product_query.get_product_by_id(product_id)
        if product is None:
            raise CustomBusinessError(
                message="Product not found",
                error_type=ErrorType.NOT_FOUND_ERROR,
                status_code=status.HTTP_404_NOT_FOUND
            )
        return success_response(ProductResponse.model_validate(product), ProductResponse)

    @lru_cache(maxsize=128)
    def get_products(self, skip: int = 0, limit: int = 100) -> PageProductResponse:
        paginated_products = self.product_query.get_products(skip=skip, limit=limit)
        return success_response(paginated_products, PageProductResponse)