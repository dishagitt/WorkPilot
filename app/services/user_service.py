from sqlalchemy.orm import Session
from app.database.models.user import User
from fastapi import HTTPException, status
from app.database.schemas.user import UserUpdate, ChangePassword
from app.database.models.enums import UserRole
from app.core.security import verify_password, hash_password


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


def get_user_list(db: Session, current_user_id: int):
    try:
        current_user = get_user_by_id(db, current_user_id)

        # user list for admin
        if current_user.role != UserRole.ADMIN:
           raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )
        all_users = (db.query(User).
                        filter(
                            User.role != UserRole.ADMIN,
                            User.is_deleted == False)
                            .all()
                        )
        
        return all_users
    
    except HTTPException:
            db.rollback()
            raise

    except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )


def update_user_service(user_id: int, data: UserUpdate, db: Session, current_user_id: int, photo_url: str | None = None):
    if user_id == current_user_id:
        user = get_user_by_id(db, user_id)

        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if  photo_url is not None:
             user.photo_url = photo_url

        db.commit()
        db.refresh(user)

        return user
    else: 
         raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can not change other user's profile"
            )
    

def delete_user_service(user_id: int, db: Session, current_user_id: int):
    current_user = get_user_by_id(db, current_user_id)

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete user"
        )

    user = get_user_by_id(db, user_id)

    user.is_deleted = True
    db.commit()

    # return True
    return {"message" : "user deleted successfully"} 


def change_password_service(user_id: int, data: ChangePassword, db: Session, current_user_id: int):
    if user_id == current_user_id:
        current_user = get_user_by_id(db, current_user_id)

        if not verify_password(data.old_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid old password"
            )
        
        if data.new_password != data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Confirm password not match"
            )
        
        new_password_hash = hash_password(data.new_password)
        current_user.password_hash = new_password_hash

        db.commit()
        db.refresh(current_user)

        # return True
        return {"message" : "Password updated successfully"} 
    
    else: 
         raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can not change other user's password"
            )