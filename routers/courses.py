from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import delete, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.course import CourseCreateSchema, CourseAndUser
from services.auth.auth_utils import verify_jwt_token_and_get_user
from services.auth.database import CourseDB, get_user_db, CourseAndUsersDB
from services.course_service import get_user_courses, append_user_to_course, delete_all_course_appends, \
    check_course_availability
from services.user_service import check_user_not_student, check_user_is_operator

router = APIRouter()
oauth2_scheme = HTTPBearer()


@router.post("/create_course", tags=["course"])
async def create_course(course: CourseCreateSchema, user_db: AsyncSession = Depends(get_user_db), credentials=Depends(oauth2_scheme)):
    check_user_not_student((await verify_jwt_token_and_get_user(credentials.credentials)).role)

    try:
        new_course = CourseDB(
            name=course.name,
            description=course.description,
            author_id=course.author_id
        )

        user_db.add(new_course)
        await user_db.commit()
        await user_db.refresh(new_course)

        await append_user_to_course(new_course.author_id, new_course.id)

        return new_course

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my_courses", tags=["course"])
async def my_courses(credentials=Depends(oauth2_scheme)):
    user = await verify_jwt_token_and_get_user(credentials.credentials)
    return await get_user_courses(user.id)


@router.post("/course_append", tags=["course"])
async def course_append(params: CourseAndUser, credentials=Depends(oauth2_scheme)):
    check_user_not_student((await verify_jwt_token_and_get_user(credentials.credentials)).role)
    return await append_user_to_course(params.user_id, params.course_id)


@router.delete("/course_delete/{course_id}", tags=["course"])
async def course_delete(
        course_id: int, user_db: AsyncSession = Depends(get_user_db), credentials=Depends(oauth2_scheme)
):
    check_user_not_student((await verify_jwt_token_and_get_user(credentials.credentials)).role)

    await delete_all_course_appends(course_id)

    stmt = delete(CourseDB).where(and_(CourseDB.id == course_id))
    await user_db.execute(stmt)
    await user_db.commit()


@router.post('/delete_course_connection', tags=["course"])
async def delete_course_connection(
        course_id: int, user_id: int, user_db: AsyncSession = Depends(get_user_db), credentials=Depends(oauth2_scheme)
):
    check_user_not_student((await verify_jwt_token_and_get_user(credentials.credentials)).role)
    stmt = delete(CourseAndUsersDB).where(and_(CourseAndUsersDB.id == course_id, CourseAndUsersDB.user_id == user_id))
    await user_db.execute(stmt)
    await user_db.commit()


@router.get("/get_all_courses", tags=["course"])
async def get_all_courses(user_db: AsyncSession = Depends(get_user_db), credentials=Depends(oauth2_scheme)):
    check_user_is_operator((await verify_jwt_token_and_get_user(credentials.credentials)).role)
    all_courses = (await user_db.execute(select(CourseDB))).scalars().all()
    return all_courses


@router.get("/get_course/{course_id}", tags=["course"])
async def get_course(course_id: int, user_db: AsyncSession = Depends(get_user_db), credentials=Depends(oauth2_scheme)):
    await check_course_availability((await verify_jwt_token_and_get_user(credentials.credentials)).id, course_id)
    stmt = select(CourseDB).where(and_(CourseDB.id == course_id))
    result = (await user_db.execute(stmt)).scalar()

    if not result:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")

    return result
