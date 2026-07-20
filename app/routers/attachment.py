from fastapi import APIRouter, Depends
from app.database.schemas.attachment import AttachmentResponse
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from sqlalchemy.orm import Session
from app.services.attachment_service import AttachmentService
from fastapi import UploadFile, File
from app.utils.file_handler import save_file


router = APIRouter(tags=["Attachment"])


@router.post("/tasks/{task_id}/attachments", response_model=AttachmentResponse)
def upload_task_attachment(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user), file: UploadFile = File(...)):

    file_url = save_file(
            upload=file,
            folder="app/static/task_attachments"
        )
    return AttachmentService.create_task_attachment(task_id, db, current_user.id, file.filename, file_url)

@router.get("/tasks/{task_id}/attachments", response_model=list[AttachmentResponse])
def get_task_attachment(task_id: int, db: Session = Depends(get_db)):
    return AttachmentService.get_task_attachment(task_id, db)


@router.post("/comments/{comment_id}/attachments", response_model=AttachmentResponse)
def upload_comment_attachment(comment_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user), file: UploadFile = File(...)):
    
    file_url = save_file(
            upload=file,
            folder="app/static/comment_attachments"
        )
    return AttachmentService.create_comment_attachment(comment_id, db, current_user.id, file.filename, file_url)


@router.get("/comments/{comment_id}/attachments", response_model=list[AttachmentResponse])
def get_comment_attachment(comment_id: int, db: Session = Depends(get_db)):
    return AttachmentService.get_comment_attachment(comment_id, db)


@router.delete("/attachments/{attachment_id}")
def delete_attachment(attachment_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return AttachmentService.delete_attachment(attachment_id, db, current_user.id)