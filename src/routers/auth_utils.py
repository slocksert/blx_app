from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.infra.sqlalchemy.config.database import get_db
from src.infra.providers import token_provider
from jose import JWTError
from src.infra.sqlalchemy.repository.user import UserRepository

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

def get_logged_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    try:
        phone: str = token_provider.verify_acess_token(token)
    except JWTError:
        raise exception
        
    if not phone:
        raise exception

    user = UserRepository(db).get_by_phone(phone)
    if not user:
        raise exception

    return user