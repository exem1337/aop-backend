from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import AddUser
from services.auth.auth_utils import hash_password
from services.auth.database import get_user_db, UserDB
from services.user_service import check_existence_and_get_user_by_id, check_user_not_exist_by_email

router = APIRouter()
oauth2_scheme = HTTPBearer()


@router.post("/user_create", tags=["User"])
async def create_user(user: AddUser, user_db: AsyncSession = Depends(get_user_db), credentials=Depends(oauth2_scheme)):
    await check_user_not_exist_by_email(user.email)

    try:
        hashed_password = hash_password(user.password)

        new_user = UserDB(
            email=user.email,
            password=str(hashed_password),
            name=user.name,
            last_name=user.last_name,
            middle_name=user.middle_name,
            role=user.role,
            status=user.status
        )

        user_db.add(new_user)
        await user_db.commit()
        await user_db.refresh(new_user)

        del new_user.password

        return new_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/user_delete", tags=["User"])
async def delete_user(user_id: int, user_db: AsyncSession = Depends(get_user_db), credentials=Depends(oauth2_scheme)):
    try:
        await check_existence_and_get_user_by_id(user_id)
        stmt = delete(UserDB).where(and_(UserDB.id == user_id))
        await user_db.execute(stmt)
        await user_db.commit()

        return {"message": "Пользователь успешно удален"}

    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user_get", tags=["User"])
async def get_user(user_id: int, credentials=Depends(oauth2_scheme)):
    try:
        return await check_existence_and_get_user_by_id(user_id)

    except HTTPException as exc:
        raise exc
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
