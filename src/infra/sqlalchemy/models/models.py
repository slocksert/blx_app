from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from src.infra.sqlalchemy.config.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    pwd = Column(String)
    phone = Column(String)

    product = relationship("Product", back_populates="user")
    order = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = 'product'

    id =  Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    details = Column(String)
    available = Column(Boolean)
    size = Column(String)

    user_id = Column(Integer, ForeignKey("user.id", name="blx_user"))
    user = relationship("User", back_populates="product")

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    delivery = Column(Boolean)
    delivery_adress = Column(String)
    notes = Column(String)

    user_id = Column(Integer, ForeignKey("user.id", name="blx_user"))
    product_id = Column(Integer, ForeignKey("product.id", name="blx_product"))

    user = relationship("User", back_populates="order")
    product = relationship("Product")