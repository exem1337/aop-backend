from database import Base
from sqlalchemy import Column, Integer, String

class User(Base): 
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)