from app.database.models.workspace import Workspace, WorkspaceMember
from app.database.models.enums import UserRole, TaskPhase
from app.database.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceListResponse
from sqlalchemy.orm import Session
from slugify import slugify
from app.database.models.project import Project
from app.database.models.task import Task
from sqlalchemy import func
from app.services.user_service import get_user_by_id
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.utils.file_upload import delete_file


def create_workspace_service(db: Session, data: WorkspaceCreate, current_user_id: int, logo_url: str | None = None):
    current_user = get_user_by_id(db, current_user_id)

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admin can create workspace."
        )
    
    existing = db.query(Workspace).filter(
        Workspace.name == data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Workspace name already exists."
        )

    base_slug = slugify(data.name)
    slug = base_slug

    counter = 1

    while db.query(Workspace).filter(Workspace.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    workspace = Workspace(
        name = data.name,
        description = data. description,
        logo_url=logo_url,
        slug = slug,
        created_by = current_user_id
    )
    
    db.add(workspace)
    try:
        db.commit()
        db.refresh(workspace)
    except IntegrityError: 
        db.rollback()
        if logo_url:
            delete_file(logo_url)
        raise HTTPException(
            status_code=409,
            detail="Workspace with this name already exists."
        )
        
    return workspace


def all_workspaces_list(db: Session, current_user_id: int):
    current_user = get_user_by_id(db, current_user_id)

    # workspace list for admin
    if current_user.role == UserRole.ADMIN:
        all_workspaces = db.query(Workspace).filter(Workspace.is_deleted == False).all()
        
    # workspace list for member (workspaces in which user is member)
    else:
        all_workspaces = (db.query(Workspace)
            .join(
                WorkspaceMember,
                Workspace.id == WorkspaceMember.workspace_id
            )
            .filter(
                WorkspaceMember.user_id == current_user_id,
                WorkspaceMember.is_deleted == False,
                Workspace.is_deleted == False
            )
            .all()
        )
            
    return [
    WorkspaceListResponse(
        id = workspace.id,
        name = workspace.name,
        workspace_owner = workspace.workspace_owner,
        logo_url = workspace.logo_url,
        slug = workspace.slug,
        created_by = current_user_id,
        # total_projects = projects_count(db, workspace.id),
        # total_members = members_count(db, workspace.id),
        # total_open_tasks = open_tasks_count(db, workspace.id)
        total_projects = 1,
        total_members = 2,
        total_open_tasks = 3 
    )
    for workspace in all_workspaces
]


def get_workspace_by_id(db: Session, workspace_id: int):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace or workspace.is_deleted == True:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    return workspace


def projects_count(db: Session, workspace_id: int):
    return (
        db.query(func.count(Project.id))
        .filter(
            Project.workspace_id == workspace_id,
            Project.is_deleted == False
        )
        .scalar()
    )


def members_count(db: Session, workspace_id: int):
    return (
        db.query(func.count(WorkspaceMember.id))
        .filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.is_deleted == False
        )
        .scalar()
    )


def open_tasks_count(db: Session, workspace_id: int):
    return (
        db.query(func.count(Task.id))
        .join(Project, Task.project_id == Project.id)
        .filter(
            Project.workspace_id == workspace_id,
            Project.is_deleted == False,
            Task.is_deleted == False,
            Task.phase != TaskPhase.DONE
        )
        .scalar()
    )


def delete_workspace_service(workspace_id: int, db: Session, current_user_id: int):
    current_user = get_user_by_id(db, current_user_id)

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admin can delete workspace"
        )

    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )

    workspace.is_deleted = True
    db.commit()

    # return True
    return {"message" : "workspace deleted successfully"} 


def update_workspace_service(workspace_id, db: Session, current_user_id: int, data: WorkspaceUpdate,  logo_url: str | None = None):
    current_user = get_user_by_id(db, current_user_id)

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only admin can edit workspace."
        )
    
    workspace = get_workspace_by_id(db, workspace_id)

    # update data
    if workspace.is_deleted == False:
        if data.name is not None:
            workspace.name = data.name
        if data.description is not None:
            workspace.description = data.description
        if logo_url is not None:
            workspace.logo_url = logo_url

        db.commit()
        db.refresh(workspace)
        return workspace