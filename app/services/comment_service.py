from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.database.models.comment import Comment
from app.database.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.services.user_service import get_user_by_id
from app.utils.membership import get_accessible_project
from app.services.task_service import TaskService
import traceback


class CommentService():

    @staticmethod
    def create_comment(task_id: int, data: CommentCreate, db: Session, current_user_id: int):
        try:
            task = TaskService.get_task_by_id(task_id, db)

            current_user = get_user_by_id(db, current_user_id)
            get_accessible_project(task.project_id, db, current_user)

            # create comment
            comment = Comment(
                task_id = task.id,
                user_id = current_user_id,
                content = data.content
            )

            db.add(comment)
            db.commit()
            db.refresh(comment)
            
            return CommentResponse(
                        id=comment.id,
                        task_id=comment.task_id,
                        user_id=comment.user_id,
                        content=comment.content,
                        created_at=comment.created_at,
                        updated_at=comment.updated_at,
                        commenter=f"{current_user.first_name} {current_user.last_name}"
            )

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
    def get_comment_by_id(comment_id: int, db: Session):
        comment = db.query(Comment).filter(Comment.id == comment_id).first()

        if not comment:
            raise HTTPException(
                status_code=404,
                detail="Commet not found"
            )
        
        return comment


    @staticmethod
    def get_comment(comment_id: int, db: Session):
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        current_user = get_user_by_id(db, comment.user_id)

        if not comment:
            raise HTTPException(
                status_code=404,
                detail="Commet not found"
            )
        
        return CommentResponse(
                        id=comment.id,
                        task_id=comment.task_id,
                        user_id=comment.user_id,
                        content=comment.content,
                        created_at=comment.created_at,
                        updated_at=comment.updated_at,
                        commenter=f"{current_user.first_name} {current_user.last_name}"
            )


    @staticmethod
    def get_comment_list(task_id: int, db: Session, current_user_id: int):
        task = TaskService.get_task_by_id(task_id, db)

        current_user = get_user_by_id(db, current_user_id)
        get_accessible_project(task.project_id, db, current_user)

        comment_list = db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at.desc()).all()

        response = []

        for comment in comment_list:

            commenter = get_user_by_id(db, comment.user_id)

            response.append(
                CommentResponse(
                    id=comment.id,
                    task_id=comment.task_id,
                    user_id=comment.user_id,
                    content=comment.content,
                    created_at=comment.created_at,
                    updated_at=comment.updated_at,
                    commenter=f"{commenter.first_name} {commenter.last_name}"
                )
            )

        return response
    


    @staticmethod
    def update_comment(comment_id: int, data: CommentUpdate, db: Session, current_user_id: int):
        try:
            comment = CommentService.get_comment_by_id(comment_id, db)

            if ( comment.user_id != current_user_id):
                raise HTTPException(
                    status_code=403,
                    detail="You are not allowed to edit this comment."
                )

            if comment.user_id is not None:
                commenter  = get_user_by_id(db, comment.user_id)

             # update comment
            if data.content is not None:
                comment.content = data.content

            db.commit()
            db.refresh(comment)
            
            return CommentResponse(
                        id=comment.id,
                        task_id=comment.task_id,
                        user_id=comment.user_id,
                        content=comment.content,
                        created_at=comment.created_at,
                        updated_at=comment.updated_at,
                        commenter=f"{commenter.first_name} {commenter.last_name}"
            )

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            # raise HTTPException(
            #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     detail="Internal server error."
            # )
            traceback.print_exc()
            raise