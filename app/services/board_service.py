from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.models.task import Task
from app.database.schemas.task import BoardResponse
from app.database.models.enums import TaskPhase
from app.services.user_service import get_user_by_id
from app.utils.membership import get_accessible_project



class BoardService(): 
    
    @staticmethod
    def project_board(project_id, db, current_user_id):
        try:
            current_user = get_user_by_id(db, current_user_id)
            get_accessible_project(project_id, db, current_user)

            tasks = (db.query(Task)
                    .filter(
                    Task.project_id == project_id,
                    Task.is_deleted == False
                    )
                    .all()
            )

            board = {
                "to_do": [],
                "in_development": [],
                "in_qa": [],
                "done": []
            }

            for task in tasks:

                assigned_user = (
                    get_user_by_id(db, task.assigned_to)
                    if task.assigned_to
                    else None
                )
                            
                task_data = BoardResponse(
                    task_number=task.task_number,
                    task_type=task.task_type,
                    title=task.title,
                    priority=task.priority,
                    due_date=task.due_date,
                    assigned_to_name=(
                        f"{assigned_user.first_name} {assigned_user.last_name}"
                        if assigned_user
                        else None
                    )
                )

                if task.phase == TaskPhase.TO_DO:
                    board["to_do"].append(task_data)

                elif task.phase == TaskPhase.IN_DEVELOPMENT:
                    board["in_development"].append(task_data)

                elif task.phase == TaskPhase.IN_QA:
                    board["in_qa"].append(task_data)

                elif task.phase == TaskPhase.DONE:
                    board["done"].append(task_data)

            return board
        
        except HTTPException:
            raise

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error."
            )
