from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = '610a2ee688cda9e724885e23cd2cfdee'
ALGORITHM = 'HS256'
EXPIRES_IN_MIN = 3600


def create_acess_token(data: dict):
    data_acess = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MIN)

    data_acess.update({'exp': expires})
    token_jwt = jwt.encode(data_acess, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def verify_acess_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload.get('sub')