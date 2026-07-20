from fastapi import APIRouter, Depends
from app.database.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from sqlalchemy.orm import Session
from app.services.task_service import TaskService

router = APIRouter(tags=["Task"])


@router.post("/task/create", response_model=TaskResponse)
def create_task(project_id: int, data: TaskCreate = Depends(TaskCreate.as_form), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return TaskService.create_task(project_id, data, db, current_user.id)


@router.get("/task/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return TaskService.get_task_by_id(task_id, db)


@router.get("/all-tasks/{project_id}")
def get_all_task_list(project_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return TaskService.all_task_list(project_id, db, current_user.id)


@router.get("/my-tasks/{project_id}")
def my_task_list(project_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return TaskService.my_task_list(project_id, db, current_user.id)


@router.patch("/task/edit/{task_id}", response_model=TaskResponse)
def edit_task(task_id: int, data: TaskUpdate = Depends(TaskUpdate.as_form), db: Session =Depends(get_db), current_user = Depends(get_current_user)):
    return TaskService.update_task(task_id, data, db, current_user.id)


@router.delete("/task/delete/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return TaskService.delete_task(task_id, db, current_user.id)