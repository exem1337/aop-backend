from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import AddUser
from services.auth.database import get_user_db, UserDB, get_async_session
import bcrypt

router = APIRouter()


@router.post("/user_create", tags=["User"])
async def create_user(user: AddUser, user_db: AsyncSession = Depends(get_user_db)):
    stmt = select(UserDB).where(and_(UserDB.email == user.email))
    existing_user = (await user_db.execute(stmt)).scalar()

    if existing_user:
        print(existing_user)
        raise HTTPException(status_code=400, detail="Пользователь с такой электронной почтой уже существует")

    try:
        salt = bcrypt.gensalt()
        password_bytes = user.password.encode('utf-8')

        hashed_password = bcrypt.hashpw(password_bytes, salt)

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
async def delete_user(user_id: int, user_db: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(UserDB).where(and_(UserDB.id == user_id))
        existing_user = (await user_db.execute(stmt)).scalar()

        if not existing_user:
            print(existing_user)
            raise HTTPException(status_code=400, detail="Пользователь не найден")

        stmt = delete(UserDB).where(and_(UserDB.id == user_id))
        await user_db.execute(stmt)
        await user_db.commit()

        return {"message": "Пользователь успешно удален"}
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user_get", tags=["User"])
async def get_user(user_id: int, user_db: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(UserDB).where(and_(UserDB.id == user_id))
        existing_user = (await user_db.execute(stmt)).scalar()

        if not existing_user:
            print(existing_user)
            raise HTTPException(status_code=400, detail="Пользователь не найден")

        del existing_user.password

        return existing_user

    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
