from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from models.user import User as UserModel

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def get_password_hash(password):
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Функция для создания токена доступа
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для аутентификации пользователя
def authenticate_user(username: str, password: str):
    # Здесь должна быть логика проверки пароля в базе данных или хранилище пользователей
    # Например, использование UserService или другого метода для проверки данных
    user = get_user_from_db(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Пример функции для получения пользователя из базы данных
def get_user_from_db(username: str):
    # Ваша логика получения пользователя из базы данных
    # Например:
    # user = UserModel.query.filter_by(username=username).first()
    # return user
    pass

# Функция для получения текущего пользователя из токена
def get_current_user(token_data: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token_data, credentials_exception)

# Функция для проверки и декодирования токена
def verify_token(token_data: str, credentials_exception):
    try:
        payload = jwt.decode(token_data, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = username
    except JWTError:
        raise credentials_exception
    return token_data