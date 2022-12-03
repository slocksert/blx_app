from fastapi import APIRouter, Depends, status, HTTPException
from src.schemas import schemas
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repository.product import ProductRepository
from typing import List

router = APIRouter()

@router.post('/products', status_code=status.HTTP_201_CREATED, response_model=schemas.SimpleProduct)
async def signup(product: schemas.Product, db: Session = Depends(get_db)):
    product_created = ProductRepository(db).create(product)
    return product_created

@router.get('/products', status_code=status.HTTP_200_OK, response_model=List[schemas.Product])
async def list_products(db: Session = Depends(get_db)):
    products = ProductRepository(db).list()
    return products

@router.get('/products/{id}', status_code=status.HTTP_200_OK)
async def id_products(id: int, db: Session = Depends(get_db)):
    product = ProductRepository(db).list_by_id(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the ID {id} was not found")
    else:
        return product

@router.delete('/products/{id}', status_code=status.HTTP_200_OK)
async def delete_products(id: int, db: Session = Depends(get_db)):
    ProductRepository(db).delete(id)
    return {"msg":'Product removed'}

@router.put('/products/{id}', response_model=schemas.SimpleProduct)
async def update_products(id:int ,product: schemas.Product, db:Session = Depends(get_db)):
    ProductRepository(db).update(id, product)
    product.id = id
    return product