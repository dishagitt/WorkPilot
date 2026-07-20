from sqlalchemy.orm import Session
from app.database.models.workspace import WorkspaceMember
from app.database.models.project import ProjectMember
from fastapi import HTTPException
from app.services.project_service import ProjectService
from app.database.models.enums import UserRole


def check_workspace_access(db: Session, workspace_id: int, user_id: int):
    membership = (
            db.query(WorkspaceMember)
            .filter(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == user_id,
                WorkspaceMember.is_deleted == False
            )
            .first()
        )

    if not membership:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this workspace"
            )
    
    return membership


def check_project_access(db: Session, project_id: int, user_id: int):
    membership = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
                ProjectMember.is_deleted == False
            )
            .first()
        )

    if not membership:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this project"
            )
    
    return membership


def get_accessible_project(project_id: int, db: Session, current_user):
    project = ProjectService.get_project_by_id(project_id, db)

    if current_user.role != UserRole.ADMIN:
        check_project_access(db, project_id, current_user.id)

    return project