from sqlalchemy.orm import Session
from app.database.models.user import User


def get_user_by_email(db: Session, email:str):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_by_id(db: Session, user_id:int):
    user = db.query(User).filter(User.id == user_id).first()
    return user