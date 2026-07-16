from sqlalchemy.orm import Session
from app.database.models.user import User
from fastapi import HTTPException, status


def get_user_by_email(db: Session, email:str):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_by_id(db: Session, user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.is_deleted == True:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    return user
