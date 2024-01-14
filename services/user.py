from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
from dto import user as UserDTO

def create_user(data: UserDTO.User, db: Session):
    user = User(name=data.name)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error creating user")
    return user

def get_user(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    return user

def update_user(data: UserDTO.User, db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    user.name = data.name
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

def delete_user(db: Session, id: int):
    user = db.query(User).filter(User.id==id).delete()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    db.commit()
    return