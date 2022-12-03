from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repository.orders import OrderRepository
from src.schemas import schemas
from src.routers.auth_utils import get_logged_user

router = APIRouter()

@router.post('/orders', status_code=status.HTTP_201_CREATED, response_model= schemas.Order)
async def create_order(order: schemas.Order ,db: Session = Depends(get_db)):
    return OrderRepository(db).create(order)

@router.get('/orders/{user_id}', response_model= schemas.Order)
async def order_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return OrderRepository(db).get_by_id(user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {id} not found")

@router.get('/orders/{user_id}/sales')
async def sales(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)):
    return OrderRepository(db).get_sales(user.id)

@router.get('/orders')
async def my_orders(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)):
    return OrderRepository(db).orders_per_user_id(user.id)

@router.delete('/orders/{id}')
async def delete_order(id:int, db: Session = Depends(get_db)):
    OrderRepository(db).delete(id)
    return {"msg":"Order deleted"}

@router.put('/orders/{id}')
async def update_order(id:int, order: schemas.Order, db: Session = Depends(get_db)):
    OrderRepository(db).update(id, order)
    order.id = id
    return order
