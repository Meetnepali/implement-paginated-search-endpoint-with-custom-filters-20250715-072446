from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Optional
from app.models import Order, OrderCreate, OrderUpdate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

# In-memory database dependency (simple dict)
def get_order_db():
    # In production, replace this with actual DB connection/session
    if not hasattr(get_order_db, "_db"):
        get_order_db._db = {}
        get_order_db._auto_id = 1
    return get_order_db._db

def get_next_id():
    if not hasattr(get_order_db, "_auto_id"):
        get_order_db._auto_id = 1
    next_id = get_order_db._auto_id
    get_order_db._auto_id += 1
    return next_id

router = APIRouter()

@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED, responses={
    422: {"description": "Validation Error", "content": {"application/json": {"example": {"error": "..."}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"error": "..."}}}},
})
def create_order(order: OrderCreate, db: Dict[int, dict] = Depends(get_order_db)):
    try:
        data = order.dict()
    except ValidationError as ve:
        return JSONResponse(status_code=422, content={"error": str(ve)})
    order_id = get_next_id()
    new_order = Order(id=order_id, **data)
    db[order_id] = jsonable_encoder(new_order)
    return new_order

@router.get("/", response_model=List[Order], summary="List Orders", responses={
    200: {"description": "List of orders."},
})
def list_orders(
    db: Dict[int, dict] = Depends(get_order_db),
    skip: int = Query(0, ge=0, description="Number of records to skip."),
    limit: int = Query(10, gt=0, description="Max number of records to return."),
    customer: Optional[str] = Query(None, description="Filter by customer name substring."),
):
    orders = list(db.values())
    if customer:
        orders = [o for o in orders if customer.lower() in o['customer'].lower()]
    return orders[skip:skip+limit]

@router.get("/{order_id}", response_model=Order, responses={
    404: {"description": "Order Not Found", "content": {"application/json": {"example": {"error": "Not found"}}}}
})
def get_order(order_id: int, db: Dict[int, dict] = Depends(get_order_db)):
    order = db.get(order_id)
    if not order:
        return JSONResponse(status_code=404, content={"error": "Order not found"})
    return order

@router.put("/{order_id}", response_model=Order, responses={
    404: {"description": "Order Not Found", "content": {"application/json": {"example": {"error": "Not found"}}}},
    422: {"description": "Validation Error", "content": {"application/json": {"example": {"error": "Validation error message"}}}},
})
def update_order(order_id: int, order_update: OrderUpdate, db: Dict[int, dict] = Depends(get_order_db)):
    stored = db.get(order_id)
    if not stored:
        return JSONResponse(status_code=404, content={"error": "Order not found"})
    try:
        data = order_update.dict(exclude_unset=True)
    except ValidationError as ve:
        return JSONResponse(status_code=422, content={"error": str(ve)})
    updated = {**stored, **data}
    try:
        # Validate using Order model
        result = Order(**updated)
    except ValidationError as ve:
        return JSONResponse(status_code=422, content={"error": str(ve)})
    db[order_id] = jsonable_encoder(result)
    return result

@router.delete("/{order_id}", response_model=dict, responses={
    404: {"description": "Order Not Found", "content": {"application/json": {"example": {"error": "Not found"}}}}
})
def delete_order(order_id: int, db: Dict[int, dict] = Depends(get_order_db)):
    if order_id not in db:
        return JSONResponse(status_code=404, content={"error": "Order not found"})
    db.pop(order_id)
    return {"message": "Order deleted"}
