from fastapi import HTTPException
from sqlalchemy import and_, select

from services.auth.database import get_user_db, UserDB


async def check_user_not_exist_by_email(email: str) -> bool:
    session = await get_user_db()
    stmt = select(UserDB).where(and_(UserDB.email == email))
    user = (await session.execute(stmt)).scalar()

    if user:
        raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует")

    return False


async def check_existence_and_get_user_by_email(email: str, del_password: bool = True):
    session = await get_user_db()
    stmt = select(UserDB).where(and_(UserDB.email == email))
    user = (await session.execute(stmt)).scalar()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if del_password:
        del user.password

    return user


async def check_existence_and_get_user_by_id(user_id: int, del_password: bool = True):
    session = await get_user_db()
    stmt = select(UserDB).where(and_(UserDB.id == user_id))
    user = (await session.execute(stmt)).scalar()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if del_password:
        del user.password

    return user
