from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import select, and_, asc
from sqlalchemy.ext.asyncio import AsyncSession

from models.theme import ThemeCreateSchema
from services.auth.auth_utils import verify_jwt_token_and_get_user
from services.auth.database import get_user_db, ThemeDB
from services.course_service import check_course_availability
from services.user_service import check_user_not_student

router = APIRouter()
oauth2_scheme = HTTPBearer()


@router.post("/create_theme", tags=["themes"])
async def create_theme(
        theme: ThemeCreateSchema, user_db: AsyncSession = Depends(get_user_db), credentials=Depends(oauth2_scheme)
):
    check_user_not_student((await verify_jwt_token_and_get_user(credentials.credentials)).role)

    try:
        new_theme = ThemeDB(
            name=theme.name,
            description=theme.description,
            course_id=theme.course_id
        )

        user_db.add(new_theme)
        await user_db.commit()
        await user_db.refresh(new_theme)
        return new_theme

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_course_themes/{course_id}", tags=["themes"])
async def get_course_themes(
        course_id: int, user_db: AsyncSession = Depends(get_user_db), credentials=Depends(oauth2_scheme)
):
    user = await verify_jwt_token_and_get_user(credentials.credentials)
    await check_course_availability(user.id, course_id)

    stmt = select(ThemeDB).where(and_(ThemeDB.course_id == course_id)).order_by(asc(ThemeDB.created_at))
    return (await user_db.execute(stmt)).scalars().all()
