from sqlalchemy.orm import Session
from app.database.models.user import User
from app.database.schemas.user import UserRegister, UserLogin
from app.services.user_service import get_user_by_email
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, verify_refresh_token
from fastapi import HTTPException, status

def register_user(db: Session, user_data: UserRegister):
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

     # Validate password confirmation
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and Confirm Password do not match."
        )

    user = User(**user_data.model_dump(exclude={"password", "confirm_password"}))
    user.password_hash = hash_password(user_data.password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def  login_user(db: Session, user_data: UserLogin):
    user = get_user_by_email(db, user_data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token({
        "sub": user_data.email,
        "user_id": user.id,
    })
    
    refresh_token = create_refresh_token({
        "sub": user.email,
        "user_id": user.id,
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def refresh_access_token(refresh_token: str):
    if not refresh_token:
        raise ValueError("No refresh token")
    
    payload = verify_refresh_token(refresh_token)

    if not payload:
        raise ValueError("Invalid refresh token")

    new_access_token = create_access_token(
        {
            "sub": payload["sub"],
            "user_id": payload["user_id"],
        }
    )

    return new_access_token