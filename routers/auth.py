from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from models.auth import AuthSchema
from services.auth.auth_utils import verify_password, create_jwt_token, verify_jwt_token_and_get_user
from services.user_service import check_existence_and_get_user_by_email

router = APIRouter()

oauth2_scheme = HTTPBearer()


@router.post("/login", tags=["Auth"])
async def login(auth_info: AuthSchema):
    user = await check_existence_and_get_user_by_email(auth_info.email, False)

    if not verify_password(auth_info.password, user.password):
        raise HTTPException(status_code=403, detail="Неверный логин или пароль")

    token = create_jwt_token(user)
    return {"token": token}


@router.get("/me", tags=["Auth"])
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    return await verify_jwt_token_and_get_user(credentials.credentials)


