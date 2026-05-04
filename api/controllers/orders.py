from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model
from ..models import order_details as detail_model
from ..models import sandwiches as sandwich_model
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        status=(
            request.status
            if hasattr(request, "status") and request.status
            else "pending"
        ),
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_pending_orders(db: Session):
    return db.query(model.Order).filter(model.Order.status == "pending").all()


def get_orders_by_status(db: Session, order_status: str):
    return db.query(model.Order).filter(model.Order.status == order_status).all()


def update_order_status(db: Session, item_id: int, new_status: str):
    item = db.query(model.Order).filter(model.Order.id == item_id)
    if not item.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!"
        )
    item.update({"status": new_status}, synchronize_session=False)
    db.commit()
    return item.first()


def get_most_popular_sandwich(db: Session):
    result = (
        db.query(
            sandwich_model.Sandwich.sandwich_name,
            func.sum(detail_model.OrderDetail.amount).label("total_ordered"),
        )
        .join(
            detail_model.OrderDetail,
            detail_model.OrderDetail.sandwich_id == sandwich_model.Sandwich.id,
        )
        .group_by(sandwich_model.Sandwich.id)
        .order_by(func.sum(detail_model.OrderDetail.amount).desc())
        .first()
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No order data found."
        )
    return {"sandwich_name": result[0], "total_ordered": result[1]}


def get_daily_revenue(db: Session, date: str):
    orders_on_date = (
        db.query(model.Order)
        .filter(func.date(model.Order.order_date) == date)
        .filter(model.Order.status == "completed")
        .all()
    )
    total = 0.0
    for order in orders_on_date:
        for detail in order.order_details:
            if detail.sandwich and detail.sandwich.price:
                total += float(detail.sandwich.price) * detail.amount
    return {"date": date, "total_revenue": round(total, 2)}


def get_orders_for_customer(db: Session, customer_name: str):
    return (
        db.query(model.Order)
        .filter(model.Order.customer_name.ilike(f"%{customer_name}%"))
        .all()
    )


def get_order_count_by_sandwich(db: Session):
    result = (
        db.query(
            sandwich_model.Sandwich.sandwich_name,
            func.sum(detail_model.OrderDetail.amount).label("total_ordered"),
        )
        .join(
            detail_model.OrderDetail,
            detail_model.OrderDetail.sandwich_id == sandwich_model.Sandwich.id,
        )
        .group_by(sandwich_model.Sandwich.id)
        .order_by(func.sum(detail_model.OrderDetail.amount).desc())
        .all()
    )
    return [{"sandwich_name": r[0], "total_ordered": r[1]} for r in result]


def get_completed_orders_today(db: Session):
    from datetime import date

    today = str(date.today())
    count = (
        db.query(func.count(model.Order.id))
        .filter(func.date(model.Order.order_date) == today)
        .filter(model.Order.status == "completed")
        .scalar()
    )
    return {"date": today, "completed_orders": count}


def get_order_status(db: Session, item_id: int):
    item = db.query(model.Order).filter(model.Order.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!"
        )
    return {
        "order_id": item.id,
        "customer_name": item.customer_name,
        "status": item.status,
        "order_date": item.order_date,
    }


def get_order_details_for_customer(db: Session, item_id: int):
    item = db.query(model.Order).filter(model.Order.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!"
        )
    details = []
    total = 0.0
    for d in item.order_details:
        price = float(d.sandwich.price) if d.sandwich and d.sandwich.price else 0.0
        subtotal = price * d.amount
        total += subtotal
        details.append(
            {
                "sandwich": d.sandwich.sandwich_name if d.sandwich else "Unknown",
                "quantity": d.amount,
                "unit_price": price,
                "subtotal": round(subtotal, 2),
            }
        )
    return {"order_id": item.id, "items": details, "total": round(total, 2)}


def get_my_order_history(db: Session, customer_name: str):
    return (
        db.query(model.Order)
        .filter(model.Order.customer_name.ilike(f"%{customer_name}%"))
        .order_by(model.Order.order_date.desc())
        .all()
    )


def get_estimated_wait(db: Session, item_id: int):
    item = db.query(model.Order).filter(model.Order.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!"
        )
    orders_ahead = (
        db.query(func.count(model.Order.id))
        .filter(model.Order.id < item_id)
        .filter(model.Order.status.in_(["pending", "in-progress"]))
        .scalar()
    )
    return {
        "order_id": item_id,
        "orders_ahead": orders_ahead,
        "estimated_wait_minutes": orders_ahead * 5,
        "current_status": item.status,
    }


def get_recent_orders(db: Session, limit: int = 5):
    return (
        db.query(model.Order).order_by(model.Order.order_date.desc()).limit(limit).all()
    )


def cancel_order(db: Session, item_id: int):
    item = db.query(model.Order).filter(model.Order.id == item_id)
    order = item.first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!"
        )
    if order.status not in ("pending",):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order with status '{order.status}'. Only pending orders can be cancelled.",
        )
    item.update({"status": "cancelled"}, synchronize_session=False)
    db.commit()
    return {"order_id": item_id, "message": "Order successfully cancelled."}


def get_orders_is_ready(db: Session):
    return db.query(model.Order).filter(model.Order.status == "ready").all()
