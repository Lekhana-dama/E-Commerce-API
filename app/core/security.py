import bcrypt
from jose import jwt
from config import SECRET_KEY
ALGORITHM="HS256"

def hash_password(password:str)->str:
    password_bytes=password.encode("utf-8")
    salt=bcrypt.gensalt()
    hash_password=bcrypt.hashpw(password_bytes,salt)
    return hash_password.decode("utf-8")
def verify_password(password:str,hashed_password:str)->bool:
    password_bytes=password.encode("utf-8")
    hash_password_bytes=hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes,hash_password_bytes)

def create_access_token(data:dict)->str:
    token=jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    return token

def decode_access_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None
