from fastapi import HTTPException
from sqlalchemy import and_, select

from enums.role import available_roles, ERole
from services.auth.database import get_user_db, UserDB


async def check_user_not_exist_by_email(email: str) -> bool:
    async with await get_user_db() as session:
        stmt = select(UserDB).where(and_(UserDB.email == email))
        user = (await session.execute(stmt)).scalar()

        if user:
            raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует")

        return False


async def check_existence_and_get_user_by_email(email: str, del_password: bool = True):
    async with await get_user_db() as session:
        stmt = select(UserDB).where(and_(UserDB.email == email))
        user = (await session.execute(stmt)).scalar()

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if del_password:
            del user.password

        return user


async def check_existence_and_get_user_by_id(user_id: int, del_password: bool = True):
    async with await get_user_db() as session:
        stmt = select(UserDB).where(and_(UserDB.id == user_id))
        user = (await session.execute(stmt)).scalar()

        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        if del_password:
            del user.password

        return user


def check_available_roles(role: str):
    if role not in available_roles:
        raise HTTPException(status_code=422, detail="Данной роли не существует")


def check_user_not_student(role: str) -> bool:
    check_available_roles(role)

    if role == ERole.STUDENT.value:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    return True


def check_user_is_operator(role: str) -> bool:
    check_available_roles(role)

    if role != ERole.OPERATOR.value:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    return True
