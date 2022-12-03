from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.sqlalchemy.models import models
from sqlalchemy import select, delete, update

class ProductRepository():

    def __init__(self, db: Session):
        self.db = db

    def create(self, product: schemas.Product):
        db_product = models.Product(name=product.name, details=product.details, price=product.price, available=product.available, size=product.size, user_id=product.user_id)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def list(self):
        statement = select(models.Product)
        result = self.db.execute(statement).scalars().all()
        return result

    def list_by_id(self, id:int):
        statement = select(models.Product).where(models.Product.id == id)
        result = self.db.execute(statement).scalars().first()
        return result

    def delete(self, id:int):
        statement = delete(models.Product).where(models.Product.id == id)
        self.db.execute(statement)
        self.db.commit()

    def delete_all(self):
        statement = delete(models.Product)
        self.db.execute(statement)
        self.db.commit()

    def update(self, id:int,product: schemas.Product):
        statement = update(models.Product).where(models.Product.id == id).values(
            name=product.name, details=product.details, price=product.price, available=product.available, size=product.size
        )
        self.db.execute(statement)
        self.db.commit()