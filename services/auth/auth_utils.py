from datetime import datetime, timedelta
import jwt
import bcrypt
from fastapi import HTTPException
from jose import JWTError
from starlette import status

from config import JWT_SECRET_KEY
from models.user import AddUser
from services.user_service import check_existence_and_get_user_by_email


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_jwt_token(user_info: AddUser) -> str:
    expiration_time = datetime.utcnow() + timedelta(days=1)
    payload = {"user_info": AddUser.from_orm(user_info).model_dump(), "exp": expiration_time}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token


async def verify_jwt_token_and_get_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms="HS256")
        user_email: str = payload.get("user_info").get("email")

        if user_email is None:
            raise credentials_exception

        expiration_time = payload.get("exp")
        if expiration_time is not None:
            if datetime.utcnow() > datetime.fromtimestamp(expiration_time):
                raise credentials_exception

        user = await check_existence_and_get_user_by_email(user_email)
        return user

    except JWTError:
        raise credentials_exception
