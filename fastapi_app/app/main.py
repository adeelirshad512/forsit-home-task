from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import Base, engine
from app.core.response import CustomResponse
from app.core.exceptions import CustomBusinessError
from app.api.routers.product import router as product_router
from app.api.routers.sale import router as sale_router
from app.api.routers.inventory import router as inventory_router
from app.core.response import success_response
from app.core.logger import logger
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.core.exception_handlers import business_exception_handler, general_exception_handler, validation_exception_handler
from app.scripts.seed_database import seed_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting E-commerce Admin API server...")
    seed_data()
    yield
    logger.info("Shutting down E-commerce Admin API server...")

app = FastAPI(title="E-commerce Admin API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(sale_router, prefix="/sales", tags=["sales"])
app.include_router(inventory_router, prefix="/inventory", tags=["inventory"])

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CustomBusinessError, business_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return success_response({"message": "E-commerce Admin API"})
