from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.database.models.attachment import Attachment
from app.database.schemas.attachment import AttachmentResponse
from app.services.user_service import get_user_by_id
from app.utils.membership import get_accessible_project
from app.services.task_service import TaskService
from app.services.comment_service import CommentService
from app.utils.file_handler import delete_file
from app.database.models.user import User
from pathlib import Path
from app.services.activity_service import ActivityService
from app.database.models.enums import ActivityAction

STATIC_DIR = Path("app/static")


class AttachmentService():

    @staticmethod
    def create_task_attachment(task_id: int, db: Session, current_user_id: int, file_name: str, file_url: str | None = None):
        try:
            task = TaskService.get_task_by_id(task_id, db)

            current_user = get_user_by_id(db, current_user_id)
            get_accessible_project(task.project_id, db, current_user)

            # create attachment
            attachment = Attachment(
                 task_id = task_id,
                 file_name = file_name,
                 file_url = file_url,
                 uploaded_by = current_user_id
            )    

            db.add(attachment)

            ActivityService.create_activity(
                db=db,
                task_id=task.id,
                user_id=current_user.id,
                action=ActivityAction.TASK_ATTACHMENT_ADDED,
                old_value=None,
                new_value=attachment.file_name
            )
            
            db.commit()
            db.refresh(attachment)
            
            return AttachmentResponse(
                        id=attachment.id,
                        task_id=attachment.task_id,
                        comment_id=attachment.comment_id,
                        file_name=attachment.file_name,
                        file_url=attachment.file_url,
                        uploaded_by_name=f"{current_user.first_name} {current_user.last_name}",
                        uploaded_at=attachment.uploaded_at
            )

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            if file_url:
                delete_file(file_url)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )
    



    @staticmethod
    def get_attachment_by_id(attachment_id: int, db: Session):
        attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()

        if not attachment:
            raise HTTPException(
                status_code=404,
                detail="Attachment not found"
            )
        
        return attachment
    

    @staticmethod
    def get_task_attachment(task_id: int, db: Session):
        attachment_list = db.query(Attachment).filter(Attachment.task_id == task_id).all()

        task = TaskService.get_task_by_id(task_id, db)
        current_user = get_user_by_id(db, task.created_by)
        get_accessible_project(task.project_id, db, current_user)


        response = []

        for attachment in attachment_list:
            current_user = get_user_by_id(db, attachment.uploaded_by)

            response.append(AttachmentResponse(
                        id=attachment.id,
                        task_id=attachment.task_id,
                        comment_id=attachment.comment_id,
                        file_name=attachment.file_name,
                        file_url=attachment.file_url,
                        uploaded_by_name=f"{current_user.first_name} {current_user.last_name}",
                        uploaded_at=attachment.uploaded_at
            ))
        
        return response

    

    @staticmethod
    def create_comment_attachment(comment_id: int, db: Session, current_user_id: int, file_name: str, file_url: str | None = None):
        try:
            comment = CommentService.get_comment_by_id(comment_id, db)
            task = TaskService.get_task_by_id(comment.task_id, db)

            current_user = get_user_by_id(db, current_user_id)
            get_accessible_project(task.project_id, db, current_user)

            # create attachment
            attachment = Attachment(
                 comment_id = comment_id,
                 file_name = file_name,
                 file_url = file_url,
                 uploaded_by = current_user_id
            )    

            db.add(attachment)

            ActivityService.create_activity(
                db=db,
                task_id=task.id,
                user_id=current_user.id,
                action=ActivityAction.COMMENT_ATTACHMENT_ADDED,
                old_value=None,
                new_value=attachment.file_name
            )

            db.commit()
            db.refresh(attachment)
            
            return AttachmentResponse(
                        id=attachment.id,
                        task_id=attachment.task_id,
                        comment_id=attachment.comment_id,
                        file_name=attachment.file_name,
                        file_url=attachment.file_url,
                        uploaded_by_name=f"{current_user.first_name} {current_user.last_name}",
                        uploaded_at=attachment.uploaded_at
            )

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            if file_url:
                delete_file(file_url)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )
    
    
    @staticmethod
    def get_comment_attachment(comment_id: int, db: Session):
        attachment_list = db.query(Attachment).filter(Attachment.comment_id == comment_id).all()

        comment = CommentService.get_comment_by_id(comment_id,db)
        current_user = get_user_by_id(db, comment.user_id)
        
        task = TaskService.get_task_by_id(comment.task_id, db)
        get_accessible_project(task.project_id, db, current_user)


        response = []

        for attachment in attachment_list:
            current_user = get_user_by_id(db, attachment.uploaded_by)

            response.append(AttachmentResponse(
                        id=attachment.id,
                        task_id=attachment.task_id,
                        comment_id=attachment.comment_id,
                        file_name=attachment.file_name,
                        file_url=attachment.file_url,
                        uploaded_by_name=f"{current_user.first_name} {current_user.last_name}",
                        uploaded_at= attachment.uploaded_at
            ))
        
        return response



    @staticmethod
    def delete_attachment(attachment_id: int, db: Session, current_user_id: int):
        try:
            # check attachment existence
            attachment = AttachmentService.get_attachment_by_id(attachment_id, db)

            # check task/comment existence
            if attachment.task_id:
                task_id = attachment.task_id

            elif attachment.comment_id:
                comment = CommentService.get_comment_by_id(
                    attachment.comment_id,
                    db
                )
                task_id = comment.task_id

            else:
                raise HTTPException(
                    status_code=400,
                    detail="Attachment is not associated with a task or comment."
                )

            if attachment.uploaded_by != current_user_id:
                raise HTTPException(
                    status_code=403,
                    detail="You are not allowed to delete this attachment."
                )

            # hard delete attachment from static and database 
            delete_file(attachment.file_url)
            db.delete(attachment)

            ActivityService.create_activity(
                db=db,
                task_id=task_id,
                user_id=current_user_id,
                action=ActivityAction.ATTACHMENT_REMOVED,
                old_value=attachment.file_name,
                new_value=None
            )

            db.commit()            

            # return True
            return {"message" : "Attachment deleted successfully"}

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )
        
    
    @staticmethod
    def download_attachment_service(attachment_id: int, db: Session, current_user: User):
        try:
            attachment = AttachmentService.get_attachment_by_id(attachment_id, db)
            # Task attachment
            if attachment.task_id:
                task = TaskService.get_task_by_id(attachment.task_id, db)
                get_accessible_project(task.project_id, db, current_user)

            # Comment attachment
            elif attachment.comment_id:
                comment = CommentService.get_comment_by_id(attachment.comment_id, db)
                task = TaskService.get_task_by_id(comment.task_id, db)               
                get_accessible_project(task.project_id, db, current_user)

            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Attachment is not associated with a task or comment."
                )
            
            
            relative_path = attachment.file_url.replace("/static/", "")
            file_path = STATIC_DIR / relative_path

            if not file_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File not found."
                )

            return file_path, attachment

        except HTTPException:
            raise

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )