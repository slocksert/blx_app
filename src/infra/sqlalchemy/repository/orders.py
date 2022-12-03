from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.sqlalchemy.models import models
from sqlalchemy import select, delete, update

class OrderRepository():
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, order: schemas.Order):
        db_order = models.Order(quantity=order.quantity, delivery=order.delivery, delivery_adress=order.delivery_adress, notes=order.notes, user_id=order.user_id, product_id=order.product_id)
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return order

    def list(self):
        statement = select(models.Order)
        result = self.db.execute(statement).scalars().all()
        return result

    def get_by_id(self, id:int):
        statement = select(models.Order).where(models.Order.id == id)
        result = self.db.execute(statement).scalars().one()
        return result

    def delete(self, id:int):
        statement = delete(models.Order).where(models.Order.id == id)
        self.db.execute(statement)
        self.db.commit()

    def update(self, id:int, order: schemas.Order):
        statement = update(models.Order).where(models.Order.id == id).values(
            quantity=order.quantity, delivery=order.delivery, adress=order.adress, notes=order.notes
        )
        self.db.execute(statement)
        self.db.commit()

    def get_sales(self, user_id:int):
        statement = select(models.Order).join_from(models.Order, models.Product).where(models.Product.user_id == user_id)
        result = self.db.execute(statement).scalars().all()
        return result

    def orders_per_user_id(self, user_id:int):
        statement = select(models.Order).where(models.Order.user_id == user_id)
        result = self.db.execute(statement).scalars().all()
        return result