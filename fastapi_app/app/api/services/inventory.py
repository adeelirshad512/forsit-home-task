from sqlalchemy.orm import Session
from app.api.queries.inventory import InventoryQuery
from app.api.queries.product import ProductQuery
from app.api.schemas.inventory import PageInventoryResponse, InventoryUpdate, InventoryResponse, LowStockAlert
from app.core.enums import ErrorType
from app.core.exceptions import CustomBusinessError
from app.core.response import success_response
from app.core.logger import logger
from fastapi import status
from datetime import datetime, timezone
from functools import lru_cache

class InventoryService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_query = InventoryQuery(db)
        self.product_query = ProductQuery(db)

    def update_inventory(self, product_id: int, inventory: InventoryUpdate) -> InventoryResponse:
        product = self.product_query.get_product_by_id(product_id)
        if not product:
            raise CustomBusinessError(
                message="Product not found",
                error_type=ErrorType.NOT_FOUND_ERROR,
                status_code=status.HTTP_404_NOT_FOUND
            )
        inventory_data = inventory.model_dump()
        inventory_data["product_id"] = product_id 
        inventory_data["updated_at"] = datetime.now(timezone.utc)

        updated_inventory = self.inventory_query.update_inventory(inventory_data)
        logger.info(f"Inventory updated for product ID: {product_id}")
        return success_response(InventoryResponse.model_validate(updated_inventory), InventoryResponse)

    @lru_cache(maxsize=128)
    def get_inventory(self, product_id: int) -> InventoryResponse:
        inventory = self.inventory_query.get_inventory_by_product_id(product_id)
        if not inventory:
            raise CustomBusinessError(
                message="Inventory not found",
                error_type=ErrorType.NOT_FOUND_ERROR,
                status_code=status.HTTP_404_NOT_FOUND
            )
        return success_response(InventoryResponse.model_validate(inventory), InventoryResponse)

    @lru_cache(maxsize=128)
    def get_inventory_history(self, product_id: int, skip: int = 0, limit: int = 100) -> PageInventoryResponse:
        inventory_history = self.inventory_query.get_inventory_history(product_id, skip, limit)
        return success_response(inventory_history, PageInventoryResponse)

    @lru_cache(maxsize=128)
    def get_low_stock_alerts(self, threshold: int = 10) -> list[LowStockAlert]:
        low_stock_alerts = self.inventory_query.get_low_stock_alerts(threshold)
        return success_response(low_stock_alerts, list[LowStockAlert])