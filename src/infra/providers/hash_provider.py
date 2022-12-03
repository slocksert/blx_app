from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])

def verify_hash(plain_text, hashed_text):
    return pwd_context.verify(plain_text, hashed_text)

def generate_hash(plain_text):
    return pwd_context.hash(plain_text)