from fastapi import APIRouter, Depends
from app.database.schemas.user import UserUpdate, UserResponse, ChangePassword
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from sqlalchemy.orm import Session
from app.services.user_service import get_user_by_id, update_user_service, delete_user_service, get_user_list, change_password_service
from fastapi import UploadFile, File
from app.utils.file_handler import save_file, delete_file


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["User"])


@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id( db, user_id)


@router.get("/users")
def user_list(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_user_list(db, current_user.id)


@router.patch("/user/edit/{user_id}", response_model=UserResponse)
def update_user_profile(user_id: int, data: UserUpdate = Depends(UserUpdate.as_form), 
                        db: Session = Depends(get_db), current_user = Depends(get_current_user), photo: UploadFile = File(None)):
    user = get_user_by_id(db, user_id)

    new_photo_url = None

    if photo and photo.filename:
        old_photo = user.photo_url

        new_photo_url = save_file(
            upload=photo,
            folder="app/static/profile_photos"
        )

        delete_file(old_photo)

    return update_user_service(user_id, data, db, current_user.id, new_photo_url)


@router.delete("/users/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return delete_user_service(user_id, db, current_user.id)
    
    # return RedirectResponse(
    # url="/users",


@router.post("/user/change-password/{user_id}")
def change_password(user_id: int, data: ChangePassword = Depends(ChangePassword.as_form), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return change_password_service(user_id, data, db, current_user.id)