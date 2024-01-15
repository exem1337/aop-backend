from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base: DeclarativeMeta = declarative_base()


class BaseUserTable(Base):
    __tablename__ = "user"
    __allow_unmapped__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    middle_name: str = Column(String, nullable=False)
    role: str = Column(String, nullable=False)
    status: str = Column(String, nullable=True)
    email: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    created_at: str = Column(TIMESTAMP, default=datetime.utcnow)


class UserDB(BaseUserTable, Base):
    pass


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db() -> AsyncSession:
    return async_session_maker()
