from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.response import Page
from app.api.models.inventory import Inventory
from app.api.models.product import Product
from app.api.schemas.inventory import InventoryResponse, LowStockAlert

class InventoryQuery:
    def __init__(self, db: Session):
        self.db = db

    def get_inventory_by_product_id(self, product_id: int):
        return self.db.query(Inventory).filter(Inventory.product_id == product_id).order_by(Inventory.updated_at.desc()).first()

    def get_inventory_history(self, product_id: int, skip: int = 0, limit: int = 100):
        query = self.db.query(Inventory).filter(Inventory.product_id == product_id)
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return Page[InventoryResponse](items=items, total=total, page=skip // limit + 1, size=limit)

    def get_low_stock_alerts(self, threshold: int = 10):
        query = self.db.query(Inventory, Product).join(Product, Inventory.product_id == Product.id).filter(Inventory.stock <= threshold)
        results = query.all()
        return [LowStockAlert(product_id=r.Inventory.product_id, product_name=r.Product.name, stock=r.Inventory.stock) for r in results]

    def update_inventory(self, inventory: dict):
        db_inventory = Inventory(**inventory)
        self.db.add(db_inventory)
        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory