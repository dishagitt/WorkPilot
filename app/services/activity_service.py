from sqlalchemy.orm import Session
from app.database.models.activity import Activity
from app.database.models.enums import ActivityAction
from app.database.models.user import User
from app.database.models.task import Task
from app.utils.membership import get_accessible_project
from fastapi import HTTPException, status


class  ActivityService:

    @staticmethod
    def create_activity(
        db: Session,
        task_id: int,
        user_id: int,
        action: ActivityAction,
        old_value: str | None = None,
        new_value: str | None = None,
    ):
        activity = Activity(
            task_id=task_id,
            user_id=user_id,
            action=action,
            old_value=old_value,
            new_value=new_value,
        )

        db.add(activity)

    
    @staticmethod
    def get_task_activities(task_id: int, db: Session, current_user: User):
        try:
            task = (
                db.query(Task)
                    .filter(
                        Task.id == task_id,
                        Task.is_deleted == False
                    )
                    .first()
                )

            if not task:
                    raise HTTPException(
                        status_code=404,
                        detail="Task not found."
                    )

            get_accessible_project(task.project_id, db, current_user)

            activities = (db.query(Activity)
                .join(
                    Task,
                    Task.id == Activity.task_id
                    )
                .filter(
                    Activity.task_id == task_id,
                    Task.is_deleted == False
                    )
                .all()
            )

            return activities

        except HTTPException:
            raise

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )