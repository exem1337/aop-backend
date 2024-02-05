from fastapi import HTTPException
from sqlalchemy import select, and_, delete

from enums.role import ERole
from services.auth.database import get_user_db, CourseAndUsersDB
from services.user_service import check_existence_and_get_user_by_id


async def append_user_to_course(user_id: int, course_id: int):
    async with await get_user_db() as session:
        course_and_user = CourseAndUsersDB(
            user_id=user_id,
            course_id=course_id
        )

        session.add(course_and_user)
        await session.commit()
        await session.refresh(course_and_user)

        return course_and_user


async def get_user_courses(user_id: int):
    async with await get_user_db() as session:
        stmt = select(CourseAndUsersDB).where(and_(CourseAndUsersDB.user_id == user_id))
        courses = (await session.execute(stmt)).scalars().all()

        return courses


async def check_course_availability(user_id: int, course_id: int):
    async with await get_user_db() as session:
        user = await check_existence_and_get_user_by_id(user_id=user_id)
        if user.role == ERole.OPERATOR.value:
            return True

        stmt = select(CourseAndUsersDB).where(and_(CourseAndUsersDB.user_id == user_id, CourseAndUsersDB.course_id == course_id))
        course = (await session.execute(stmt)).scalar()

        if not course:
            raise HTTPException(status_code=403, detail="Данная дисциплина недоступна")

        return True


async def delete_all_course_appends(course_id: int):
    async with await get_user_db() as session:
        stmt = delete(CourseAndUsersDB).where(and_(CourseAndUsersDB.course_id == course_id))
        await session.execute(stmt)
        await session.commit()
