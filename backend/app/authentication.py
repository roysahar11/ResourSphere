from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app import config, users

# Initialize Passlib's context for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration for JWT
JWT_SECRET_KEY = config.load_jwt_secret_key()
ALGORITHM = config.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRATION_MINUTES = config.ACCESS_TOKEN_EXPIRATION_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now() + expires_delta
#     else:
#         expire = datetime.now() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

def generate_access_token(username: str):
    expiration_delta = timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRATION_MINUTES)
    expires_at = datetime.now() + expiration_delta
    data = {"username": username, "exp": expires_at}
    encoded_token = jwt.encode(data, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_token

def get_username_from_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return username
    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
        )