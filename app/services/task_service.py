from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.database.models.task import Task
from app.database.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.database.models.enums import TaskPhase
from app.services.user_service import get_user_by_id
from app.utils.membership import get_accessible_project, check_project_access
from app.utils.key_num import generate_task_number
import traceback



class TaskService():

    @staticmethod
    def create_task(project_id: int, data: TaskCreate, db: Session, current_user_id: int):
        try:
            # check user exists
            current_user = get_user_by_id(db, current_user_id)

            # Admin can create anywhere.
            # Members can create only in their own projects.
            get_accessible_project(project_id, db, current_user)

            # Validate assignee
            if data.assigned_to is not None:
                assigned_user = get_user_by_id(db, data.assigned_to)
                check_project_access(db, project_id, data.assigned_to)

            # Generate task number
            task_number = generate_task_number(db, project_id)

            # create task
            task = Task(
                project_id = project_id,
                task_number = task_number,
                task_type = data.task_type,
                title = data.title,
                description = data.description,
                priority = data.priority,
                due_date = data.due_date,
                created_by = current_user_id,
                assigned_to = data.assigned_to
            )

            db.add(task)
            db.commit()
            db.refresh(task)
            
            return TaskResponse(
                        id=task.id,
                        project_id = task.project_id,
                        task_number = task.task_number,
                        task_type = data.task_type,
                        title = data.title,
                        description = data.description,
                        phase=TaskPhase.TO_DO,
                        priority = data.priority,
                        due_date = (data.due_date
                                    if task.due_date else None),
                        created_by_name = f"{current_user.first_name} {current_user.last_name}",
                        assigned_to_name =  (f"{assigned_user.first_name} {assigned_user.last_name}"
                                             if task.assigned_to else None)
            )

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            traceback.print_exc()
            raise
                
            

    @staticmethod
    def get_task_by_id(task_id: int, db: Session):
        task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
        
        return task
    


    @staticmethod
    def all_task_list(project_id: int, db: Session, current_user_id: int):
        try:
            current_user = get_user_by_id(db, current_user_id)
            get_accessible_project(project_id, db, current_user)
            task_list = (db.query(Task)
                            .filter(
                                Task.project_id == project_id,
                                Task.is_deleted == False
                            )
                            .order_by(Task.task_number)
                            .all()
            )

            return task_list

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
    def my_task_list(project_id: int, db: Session, current_user_id: int):
        try:
            current_user = get_user_by_id(db, current_user_id)
            get_accessible_project(project_id, db, current_user)
            task_list = (db.query(Task)
                            .filter(
                                Task.project_id == project_id, 
                                Task.assigned_to == current_user_id, 
                                Task.is_deleted == False
                            )
                            .order_by(Task.task_number)
                            .all()
            )

            return task_list

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
    def update_task(task_id: int, data: TaskUpdate, db: Session, current_user_id: int):
        try:
            task = TaskService.get_task_by_id(task_id, db)

            current_user = get_user_by_id(db, current_user_id)
            get_accessible_project(task.project_id, db, current_user)

            if task.created_by is not None:
                created_by_user = get_user_by_id(db, task.created_by)
            
            # update task
            if data.task_type is not None:
                task.task_type = data.task_type
            if data.title is not None:
                task.title = data.title
            if data.description is not None:
                task.description = data.description
            if data.phase is not None:
                task.phase = data.phase
            if data.priority is not None:
                task.priority = data.priority
            if data.due_date is not None:
                task.due_date = data.due_date
            if data.assigned_to is not None:
                get_user_by_id(db, data.assigned_to)
                check_project_access(db, task.project_id, data.assigned_to)
                task.assigned_to = data.assigned_to
            
            assigned_user = get_user_by_id(db, task.assigned_to)

            db.commit()
            db.refresh(task)

            return TaskResponse(
                        id=task.id,
                        project_id = task.project_id,
                        task_number = task.task_number,
                        task_type = task.task_type,
                        title = task.title,
                        description = task.description,
                        phase=task.phase,
                        priority = task.priority,
                        due_date = (task.due_date
                                    if task.due_date else None),
                        created_by_name = f"{created_by_user.first_name} {created_by_user.last_name}",
                        assigned_to_name =  (f"{assigned_user.first_name} {assigned_user.last_name}"
                                             if task.assigned_to else None)
        )

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            back.print_exc()
            raisetrace
        
    

    @staticmethod
    def delete_task(task_id: int, db: Session, current_user_id: int):
        try:
            # check task existence
            task = TaskService.get_task_by_id(task_id, db)

            # get current user
            current_user = get_user_by_id(db, current_user_id)

            # check memebr access
            get_accessible_project(task.project_id, db, current_user)

            # soft delete task 
            task.is_deleted = True

            db.commit()            

            # return True
            return {"message" : "Task deleted successfully"}

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error."
            )