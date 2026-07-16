from sqlalchemy.orm import Session
from app.database.models.project import ProjectMember, Project
from app.database.models.workspace import WorkspaceMember
from app.database.schemas.member import ProjectMemberCreate, ProjectMemberRoleUpdate, ProjectMemberListResponse, WorkspaceMemberListResponse
from app.services.user_service import get_user_by_id
from app.database.models.enums import UserRole, ProjectStatus
from fastapi import HTTPException, status
from app.services.project_service import ProjectService
from app.services.workspace_service import get_workspace_by_id
from sqlalchemy import func



class MemberService():

    @staticmethod
    def create_member_service(project_id: int, data: ProjectMemberCreate, db: Session, current_user_id: int):
        try:
            current_user = get_user_by_id(db, current_user_id)

            if current_user.role != UserRole.ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only admin can add members"
                )
            
            project = ProjectService.get_project_by_id(project_id, db)

            if project.status == ProjectStatus.ACTIVE:

                get_user_by_id(db, data.user_id)
                
                existing_project_member = (
                    db.query(ProjectMember)
                    .filter(
                        ProjectMember.project_id == project_id,
                        ProjectMember.user_id == data.user_id,
                        ProjectMember.is_deleted == False
                    )
                    .first()
                )

                if existing_project_member:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="User is already a member of this project."
                    )
                
                # check if user is already a member of the workspace this project belongs to
                existing_workspace_member = (
                    db.query(WorkspaceMember)
                    .filter(
                        WorkspaceMember.workspace_id == project.workspace_id,
                        WorkspaceMember.user_id == data.user_id,
                        WorkspaceMember.is_deleted == False
                    )
                    .first()
                )
                # if not already worksapce member then add 
                if not existing_workspace_member:

                    workspace_member = WorkspaceMember(
                        workspace_id=project.workspace_id,
                        user_id=data.user_id
                    )

                    db.add(workspace_member)

                # add member to project
                project_member = ProjectMember(
                    project_id = project_id,
                    user_id = data.user_id,
                    role = data.role
                )

                db.add(project_member)
                db.commit()
                db.refresh(project_member)

                return project_member
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can not add member in Archived Project"
                )
        
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
    def update_member_role_service(project_id: int, data: ProjectMemberRoleUpdate, db: Session, current_user_id: int):
        try:
            current_user = get_user_by_id(db, current_user_id)

            if current_user.role != UserRole.ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only admin can change member role"
                )
            
            project = ProjectService.get_project_by_id(project_id, db)

            if project.status == ProjectStatus.ACTIVE:
                get_user_by_id(db, data.user_id)

                existing_project_member = (
                    db.query(ProjectMember)
                    .filter(
                        ProjectMember.project_id == project_id,
                        ProjectMember.user_id == data.user_id,
                        ProjectMember.is_deleted == False
                    )
                    .first()
                )

                if not existing_project_member:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Project member not found."
                    )
                
                if data.role is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Role is required."
                    )

                # update project member role
                if data.role is not None:
                    if existing_project_member.role == data.role:
                        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail="User already has this role."
                        )
                    existing_project_member.role = data.role
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can not update member role in Archived Project"
                )

            db.commit()
            db.refresh(existing_project_member)
            return existing_project_member
        
        
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
    def remove_member_service(project_id: int, user_id: int, db: Session, current_user_id: int):
        try:
            current_user = get_user_by_id(db, current_user_id)

            if current_user.role != UserRole.ADMIN:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only admin can remove member from project"
                )
            
            project = ProjectService.get_project_by_id(project_id, db)

            if project.status == ProjectStatus.ACTIVE:
                get_user_by_id(db, user_id)

                existing_project_member = (
                    db.query(ProjectMember)
                    .filter(
                        ProjectMember.project_id == project_id,
                        ProjectMember.user_id == user_id,
                        ProjectMember.is_deleted == False
                    )
                    .first()
                )

                if not existing_project_member:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Project member not found."
                    )
                
                existing_project_member.is_deleted = True
                db.commit()

                # return True
                return {"message" : "Member removed from project successfully"} 
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can not remove member from Archived Project"
                )
        
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
    def project_member_list_Service(project_id: int, db: Session):
        ProjectService.get_project_by_id(project_id, db)

        members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.is_deleted == False).all()

        return [
            ProjectMemberListResponse(
                id=member.id,
                full_name=f"{member.user.first_name} {member.user.last_name}",
                email=member.user.email,
                role=member.role,
                joined_at=member.joined_at,
            )
            for member in members
        ]
    

    @staticmethod
    def workspace_member_list_service(workspace_id: int, db: Session):
        get_workspace_by_id(db, workspace_id)

        members = db.query(WorkspaceMember).filter(WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.is_deleted == False).all()

        response = []

        for member in members:

            total_projects = (
                db.query(func.count(ProjectMember.id))
                .join(
                    Project,
                    Project.id == ProjectMember.project_id
                )
                .filter(
                    Project.workspace_id == workspace_id,
                    ProjectMember.user_id == member.user_id,
                    ProjectMember.is_deleted == False,
                    Project.is_deleted == False
                )
                .scalar()
            )

            response.append(
                WorkspaceMemberListResponse(
                    id=member.id,
                    full_name=f"{member.user.first_name} {member.user.last_name}",
                    email=member.user.email,
                    joined_at=member.joined_at,
                    total_projects=total_projects
                )
            )

        return response
    