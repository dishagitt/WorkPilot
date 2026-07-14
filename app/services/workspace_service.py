from app.database.models.workspace import Workspace, WorkspaceMember
from app.database.models.enums import WorkspaceMemberRole
from app.database.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceListResponse
from sqlalchemy.orm import Session
from slugify import slugify
from app.database.models.project import Project
from app.database.models.task import Task
from sqlalchemy import func
from app.services.user_service import get_user_by_id
from fastapi import HTTPException, status
from app.utils.membership import workspace_membership


def create_workspace_service(db: Session, data: WorkspaceCreate, current_user_id: int, logo_url: str | None = None):
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
    db.flush()      # Gets workspace.id without committing

    workspace_member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=current_user_id,
        role=WorkspaceMemberRole.OWNER
    )
    db.add(workspace_member)
    db.commit()
    db.refresh(workspace)
        
    return workspace


def all_workspaces_list(db: Session):
    all_workspaces = db.query(Workspace).filter(Workspace.is_active == True).all()
    total_workspace_projcts = projects_count(db)
    total_workspace_members = members_count(db)
    total_workspace_open_tasks = open_tasks_count(db)
    return [
    WorkspaceListResponse(
        id = workspace.id,
        name = workspace.name,
        workspace_owner = workspace.workspace_owner,
        logo_url = workspace.logo_url,
        slug = workspace.slug,
        total_projects = total_workspace_projcts,
        total_members = total_workspace_members,
        total_open_tasks = total_workspace_open_tasks
    )
    for workspace in all_workspaces
]


def get_workspace_by_id(db: Session, workspace_id: int):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    return workspace

def projects_count(db: Session):
    projects_count = db.query(func.count(Project.id)).scalar()
    return projects_count


def members_count(db: Session):
    workspace_member_count = db.query(func.count(WorkspaceMember.id)).scalar()
    return workspace_member_count


def open_tasks_count(db: Session):
    open_task_count = db.query(func.count(Task.id)).filter(Task.phase != "DONE").scalar()
    return open_task_count


def delete_workspace_service(workspace_id: int, db: Session, current_user_id: int):

    membership = workspace_membership(db, workspace_id, current_user_id)

    if membership.role != WorkspaceMemberRole.OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only workspace owner can delete workspace"
        )

    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )


    workspace.is_active = False
    db.commit()

    return True


def update_workspace_service(workspace_id, db: Session, current_user_id: int, data: WorkspaceUpdate,  logo_url: str | None = None):
    
    membership = workspace_membership(db, workspace_id, current_user_id)

    if membership.role != WorkspaceMemberRole.OWNER:
        raise HTTPException(
            status_code=403,
            detail="Only workspace owner can edit workspace"
        )
    
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )

    # update data
    if data.name is not None:
        workspace.name = data.name
    if data.description is not None:
        workspace.description = data.description
    if logo_url is not None:
        workspace.logo_url = logo_url

    db.commit()
    db.refresh(workspace)
    return workspace