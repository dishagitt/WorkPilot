from fastapi import APIRouter, Depends
from app.database.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from sqlalchemy.orm import Session
from app.services.project_service import ProjectService

router = APIRouter(tags=["Project"], prefix="/project")


@router.post("/create", response_model=ProjectResponse)
def create_project(workspace_id: int, data: ProjectCreate = Depends(ProjectCreate.as_form), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return ProjectService.create_project_service(workspace_id, db, data, current_user.id)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return ProjectService.get_project_by_id(project_id, db)


@router.get("/active-projects/{workspace_id}")
def active_project_list(workspace_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return ProjectService.get_all_active_projects(db, workspace_id, current_user.id)


@router.get("/archived-projects/{workspace_id}")
def archived_project_list(workspace_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return ProjectService.get_all_archived_projects(db, workspace_id, current_user.id)


@router.patch("/edit/{project_id}", response_model=ProjectResponse)
def edit_project(project_id: int, data: ProjectUpdate = Depends(ProjectUpdate.as_form), db: Session =Depends(get_db), current_user = Depends(get_current_user)):
    return ProjectService.update_project(project_id, data, db, current_user.id)


@router.delete("/delete/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return ProjectService.delete_project(project_id, db, current_user.id)