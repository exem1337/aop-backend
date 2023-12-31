from sqlalchemy import String, Column, Integer
from database import Base


class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name = Column(String, unique=True, index=True)