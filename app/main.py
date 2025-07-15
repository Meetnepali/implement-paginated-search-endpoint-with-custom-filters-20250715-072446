from fastapi import FastAPI
from app.routes.orders import router as orders_router

app = FastAPI(title="Order Management API", description="API for managing orders and their items.", version="1.0.0")

app.include_router(orders_router, prefix="/orders", tags=["Orders"])
