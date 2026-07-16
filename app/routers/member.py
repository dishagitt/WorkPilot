from fastapi import APIRouter, Depends
from app.database.schemas.member import ProjectMemberCreate, ProjectMemberRoleUpdate, ProjectMemberResponse, ProjectMemberListResponse, WorkspaceMemberListResponse
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from sqlalchemy.orm import Session
from app.services.member_service import MemberService
from typing import List

router = APIRouter(tags=["Member"])


@router.post("/project/members/create", response_model=ProjectMemberResponse)
def add_project_member(project_id: int, data: ProjectMemberCreate = Depends(ProjectMemberCreate.as_form), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return MemberService.create_member_service(project_id, data, db, current_user.id)


@router.get("/project/{project_id}/members", response_model=List[ProjectMemberListResponse])
def project_member_list(project_id: int, db: Session = Depends(get_db)):
    return MemberService.project_member_list_Service(project_id, db)


@router.patch("/project/{project_id}/members", response_model=ProjectMemberResponse)
def update_project_member_role(project_id: int, data: ProjectMemberRoleUpdate = Depends(ProjectMemberRoleUpdate.as_form), db: Session =Depends(get_db), current_user = Depends(get_current_user)):
    return MemberService.update_member_role_service(project_id, data, db, current_user.id)


@router.delete("/project/{project_id}/members/{user_id}")
def remove_project_member(project_id: int, user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return MemberService.remove_member_service(project_id, user_id, db, current_user.id)


@router.get("/workspace/{workspace_id}/members", response_model=List[WorkspaceMemberListResponse])
def workspace_member_list(workspace_id: int, db: Session = Depends(get_db)):
    return MemberService.workspace_member_list_service(workspace_id, db)