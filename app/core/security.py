from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import bcrypt
from app.core.config import get_settings

settings = get_settings()

def hash_password(password: str) -> str:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) \
        if expires_delta is None else datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    jwt_encode = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return jwt_encode

def decode_access_token(token: str) -> dict:
    try: 
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload 
    except JWTError:
        raise JWTError("Invalid token")
    