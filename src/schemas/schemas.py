from pydantic import BaseModel
from typing import List

class SimpleProduct(BaseModel):
    id: int | None = None
    name: str
    price: float
    available: bool
    
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int | None = None
    name: str
    pwd: str
    phone: str
    product: List[SimpleProduct] = []

    class Config:
        orm_mode = True

class LoginData(BaseModel):
    pwd: str
    phone: str
    
class SimpleUser(BaseModel):
    id: int | None = None
    name: str
    phone: str

    class Config:
        orm_mode = True

class LoginSucess(BaseModel):
    user : SimpleUser
    acess_token: str

class Product(BaseModel):
    id: int | None = None
    name: str
    details: str
    price: float
    available: bool = False
    size: str
    user_id: int | None = None
    user: SimpleUser | None = None

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int | None = None
    quantity: int
    delivery_adress: str | None = None
    delivery: bool
    notes: str | None = "No Notes"

    user_id: int | None = None
    product_id: int | None = None

    user: SimpleUser | None = None
    product: SimpleProduct | None = None

    class Config:
        orm_mode = True