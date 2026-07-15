from sqlalchemy.orm import Session
from app.database.models.workspace import WorkspaceMember
from app.database.models.project import ProjectMember
from fastapi import HTTPException


def workspace_membership(db: Session, workspace_id: int, current_user_id: int):
    membership = (
            db.query(WorkspaceMember)
            .filter(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == current_user_id,
                WorkspaceMember.is_active == True
            )
            .first()
        )

    if not membership:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this workspace"
            )
    
    return membership


def project_membership(db: Session, project_id: int, current_user_id: int):
    membership = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user_id,
                ProjectMember.is_active == True
            )
            .first()
        )

    if not membership:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this project"
            )
    
    return membership