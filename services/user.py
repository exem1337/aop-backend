from fastapi import HTTPException
from models.user import User
from sqlalchemy.orm import Session
from dto import user

def create_user(data: user.User, db: Session):
  user = User(name=data.name)
  try:
    db.add(user)
    db.commit()
    db.refresh()
  except Exception as e:
    print(e)
  return user

def get_user(id: int, db: Session):
  user = db.query(User).filter(User.id == id).first()

  if not user:
    raise HTTPException(status_code=404, detail="not found user with id = " + str(id))
  
  return user

def update_user(data: user.User, db: Session, id: int):
  user = db.query(User).filter(User.id == id).first()

  if not user:
    raise HTTPException(status_code=404, detail="not found user with id = " + str(id))

  user.name = data.name
  db.add(user)
  db.commit()
  db.refresh(user)
  
  return user

def delete_user(db: Session, id: int):
  user = db.query(User).filter(User.id==id).delete()
  if not user:
    raise HTTPException(status_code=404, detail="not found user with id = " + str(id))
  
  db.commit()
  return