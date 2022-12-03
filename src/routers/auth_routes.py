from fastapi import APIRouter, Depends, status, HTTPException
from src.schemas import schemas
from src.infra.sqlalchemy.repository.user import UserRepository
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from typing import List
from src.infra.providers import hash_provider, token_provider
from src.routers.auth_utils import get_logged_user

router = APIRouter()

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.SimpleUser)
async def signup(user: schemas.User, db: Session = Depends(get_db)):
    desired_user = UserRepository(db).get_by_phone(user.phone)
    
    if desired_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There's an existing user with this phone number")

    user.pwd = hash_provider.generate_hash(user.pwd)
    user_created = UserRepository(db).create(user)
    return user_created

@router.post('/token', response_model=schemas.LoginSucess)
async def login(login_data: schemas.LoginData, db: Session = Depends(get_db)):
    pwd = login_data.pwd
    phone = login_data.phone

    user = UserRepository(db).get_by_phone(phone)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorret data, try again.")
    
    valid_pwd = hash_provider.verify_hash(pwd, user.pwd)
    if not valid_pwd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorret data, try again.")

    token = token_provider.create_acess_token({"sub": user.phone})
    return schemas.LoginSucess(user=user, acess_token=token)

@router.get('/me')
async def me(user: schemas.User = Depends(get_logged_user)):
    return user

@router.get('/users', status_code=status.HTTP_200_OK, response_model=List[schemas.User])
async def list_users(db: Session = Depends(get_db)):
    users = UserRepository(db).list()
    return users

@router.get('/users/{id}', status_code=status.HTTP_200_OK)
async def id_users(id:int, db: Session = Depends(get_db)):
    users = UserRepository(db).get(id)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

@router.delete('/users/{id}', status_code=status.HTTP_200_OK)
async def delete_user(id:int, db: Session = Depends(get_db)):
    user = UserRepository(db).get_by_id(id)
        
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if user:
        UserRepository(db).delete(id)
        return {"msg":"User was deleted"}
    
@router.put('/users/{id}', response_model=schemas.User)
async def update_user(id:int, user: schemas.User, db: Session = Depends(get_db)):
    UserRepository(db).update(id ,user)
    user.id = id
    return user