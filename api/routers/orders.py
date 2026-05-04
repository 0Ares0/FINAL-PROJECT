from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(tags=["Orders"], prefix="/orders")


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)


@router.get("/staff/pending", tags=["Staff"])
def get_pending_orders(db: Session = Depends(get_db)):
    return controller.get_pending_orders(db)


@router.get("/staff/by-status/{order_status}", tags=["Staff"])
def get_orders_by_status(order_status: str, db: Session = Depends(get_db)):
    return controller.get_orders_by_status(db, order_status)


@router.patch("/staff/{item_id}/status/{new_status}", tags=["Staff"])
def update_order_status(item_id: int, new_status: str, db: Session = Depends(get_db)):
    return controller.update_order_status(db, item_id, new_status)


@router.get("/staff/popular-sandwich", tags=["Staff"])
def get_most_popular_sandwich(db: Session = Depends(get_db)):
    return controller.get_most_popular_sandwich(db)


@router.get("/staff/revenue/{date}", tags=["Staff"])
def get_daily_revenue(date: str, db: Session = Depends(get_db)):
    return controller.get_daily_revenue(db, date)


@router.get("/staff/customer/{customer_name}", tags=["Staff"])
def get_orders_for_customer(customer_name: str, db: Session = Depends(get_db)):
    return controller.get_orders_for_customer(db, customer_name)


@router.get("/staff/sandwich-counts", tags=["Staff"])
def get_order_count_by_sandwich(db: Session = Depends(get_db)):
    return controller.get_order_count_by_sandwich(db)


@router.get("/staff/completed-today", tags=["Staff"])
def get_completed_orders_today(db: Session = Depends(get_db)):
    return controller.get_completed_orders_today(db)


@router.get("/customer/{item_id}/status", tags=["Customer"])
def get_order_status(item_id: int, db: Session = Depends(get_db)):
    return controller.get_order_status(db, item_id)


@router.get("/customer/{item_id}/summary", tags=["Customer"])
def get_order_details_for_customer(item_id: int, db: Session = Depends(get_db)):
    return controller.get_order_details_for_customer(db, item_id)


@router.get("/customer/history/{customer_name}", tags=["Customer"])
def get_my_order_history(customer_name: str, db: Session = Depends(get_db)):
    return controller.get_my_order_history(db, customer_name)


@router.get("/customer/{item_id}/wait", tags=["Customer"])
def get_estimated_wait(item_id: int, db: Session = Depends(get_db)):
    return controller.get_estimated_wait(db, item_id)


@router.get("/customer/recent/{limit}", tags=["Customer"])
def get_recent_orders(limit: int = 5, db: Session = Depends(get_db)):
    return controller.get_recent_orders(db, limit)


@router.patch("/customer/{item_id}/cancel", tags=["Customer"])
def cancel_order(item_id: int, db: Session = Depends(get_db)):
    return controller.cancel_order(db, item_id)


@router.get("/customer/ready/pickup", tags=["Customer"])
def get_orders_ready_for_pickup(db: Session = Depends(get_db)):
    return controller.get_orders_is_ready(db)
