from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.api.models.product import Product
from app.api.models.sale import Sale
from app.api.models.inventory import Inventory
from datetime import datetime, timedelta, timezone
from app.core.logger import logger

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
            logger.info("Products added.")
        else:
            logger.info("Products already exist. Skipping.")

        if db.query(Sale).count() == 0:
            sales = [
                Sale(product_id=1, quantity=2, total_amount=1999.98, sale_date=datetime.now(timezone.utc) - timedelta(days=1)),
                Sale(product_id=2, quantity=5, total_amount=99.95, sale_date=datetime.now(timezone.utc) - timedelta(days=2)),
                Sale(product_id=3, quantity=3, total_amount=89.97, sale_date=datetime.now(timezone.utc))
            ]
            db.add_all(sales)
            db.commit()
            logger.info("Sales added.")
        else:
            logger.info("Sales already exist. Skipping.")

        if db.query(Inventory).count() == 0:
            inventories = [
                Inventory(product_id=1, stock=50, updated_at=datetime.now(timezone.utc)),
                Inventory(product_id=2, stock=5, updated_at=datetime.now(timezone.utc)),
                Inventory(product_id=3, stock=100, updated_at=datetime.now(timezone.utc))
            ]
            db.add_all(inventories)
            db.commit()
            logger.info("Inventory added.")
        else:
            logger.info(" Inventory already exists. Skipping.")

        logger.info("Seeding completed successfully.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error during seeding data: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
