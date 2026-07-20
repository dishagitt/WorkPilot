from fastapi import APIRouter, Depends
from app.database.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from sqlalchemy.orm import Session
from app.services.comment_service import CommentService

router = APIRouter(tags=["Comment"])


@router.post("/tasks/{task_id}/comments", response_model=CommentResponse)
def create_comment(task_id: int, data: CommentCreate = Depends(CommentCreate.as_form), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return CommentService.create_comment(task_id, data, db, current_user.id)


@router.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return CommentService.get_comment(comment_id, db)


@router.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def get_all_comment_list(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return CommentService.get_comment_list(task_id, db, current_user.id)


@router.patch("/comments/{comment_id}", response_model=CommentResponse)
def edit_comment(comment_id: int, data: CommentUpdate = Depends(CommentUpdate.as_form), db: Session =Depends(get_db), current_user = Depends(get_current_user)):
    return CommentService.update_comment(comment_id, data, db, current_user.id)


