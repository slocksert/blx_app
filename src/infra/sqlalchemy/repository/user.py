from sqlalchemy.orm import Session
from src.schemas import schemas
from src.infra.sqlalchemy.models import models
from sqlalchemy import select, delete, update

class UserRepository():

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: schemas.User):
        db_user = models.User(name=user.name, pwd=user.pwd, phone=user.phone)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def list(self):
        statement = select(models.User)
        result = self.db.execute(statement).scalars().all()
        return result

    def get_by_id(self, id:int):
        statement = select(models.User).filter_by(id=id)
        result = self.db.execute(statement).first()
        return result

    def delete(self, id:int):
        statement = delete(models.User).where(models.User.id == id)
        self.db.execute(statement)
        self.db.commit()
        
    def update(self, id:int,user: schemas.User):
        statement = update(models.User).where(models.User.id == id).values(
            name=user.name, pwd=user.pwd, phone=user.phone
        )
        self.db.execute(statement)
        self.db.commit()

    def get_by_phone(self, phone: str):
        statement = select(models.User).where(models.User.phone == phone)
        result = self.db.execute(statement).scalars().first()
        return result