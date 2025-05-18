from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.api.models.product import Product
from app.api.models.sale import Sale
from app.api.models.inventory import Inventory
from datetime import datetime, timedelta, timezone

def seed_data():
    db = SessionLocal()
    try:
        if db.query(Product).count() == 0:
            products = [
                Product(name="Laptop", category="Electronics", price=999.99),
                Product(name="T-shirt", category="Clothing", price=19.99),
                Product(name="Book", category="Books", price=29.99)
            ]
            db.add_all(products)
            db.commit()

        if db.query(Sale).count() == 0:
            sales = [
                Sale(product_id=1, quantity=2, total_amount=1999.98, sale_date=datetime.now(datetime.timezone.utc) - timedelta(days=1)),
                Sale(product_id=2, quantity=5, total_amount=99.95, sale_date=datetime.now(datetime.timezone.utc) - timedelta(days=2)),
                Sale(product_id=3, quantity=3, total_amount=89.97, sale_date=datetime.now(datetime.timezone.utc))
            ]
            db.add_all(sales)
            db.commit()

        if db.query(Inventory).count() == 0:
            inventories = [
                Inventory(product_id=1, stock=50, updated_at=datetime.now(datetime.timezone.utc)),
                Inventory(product_id=2, stock=5, updated_at=datetime.now(datetime.timezone.utc)),
                Inventory(product_id=3, stock=100, updated_at=datetime.now(datetime.timezone.utc))
            ]
            db.add_all(inventories)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()