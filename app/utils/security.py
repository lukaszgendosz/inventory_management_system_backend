from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import uuid

from fastapi.security import OAuth2PasswordBearer
import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
crypt_context = CryptContext(schemes=["argon2"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return crypt_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return crypt_context.verify(password, hash)


def create_token(data: dict, expires_delta: timedelta | None = None, is_refresh: bool = False):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode["exp"] = expire
    to_encode["is_refresh"] = is_refresh
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return token_data
    except jwt.PyJWTError as e:
        raise e
