from fastapi import APIRouter, Depends
from app.api.services.inventory import InventoryService
from app.api.schemas.inventory import InventoryUpdate, InventoryResponse, PageInventoryResponse, LowStockAlert
from app.core.auth import get_api_key
from sqlalchemy.orm import Session
from app.config.database import get_db

router = APIRouter()

@router.put("/{product_id}", response_model=InventoryResponse)
async def update_inventory(product_id: int, inventory: InventoryUpdate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    inventory_service = InventoryService(db)
    return inventory_service.update_inventory(product_id, inventory)

@router.get("/{product_id}", response_model=InventoryResponse)
async def get_inventory(product_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    inventory_service = InventoryService(db)
    return inventory_service.get_inventory(product_id)

@router.get("/{product_id}/history", response_model=PageInventoryResponse)
async def get_inventory_history(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    inventory_service = InventoryService(db)
    return inventory_service.get_inventory_history(product_id, skip, limit)

@router.get("/low-stock/", response_model=list[LowStockAlert])
async def get_low_stock_alerts(threshold: int = 10, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    inventory_service = InventoryService(db)
    return inventory_service.get_low_stock_alerts(threshold)