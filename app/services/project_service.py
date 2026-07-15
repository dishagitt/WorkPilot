from sqlalchemy.orm import Session
from app.database.models.project import Project, ProjectMember
from app.database.models.workspace import Workspace
from app.database.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.utils.membership import project_membership
from app.utils.project_key import generate_project_key
from app.services.user_service import get_user_by_id
from fastapi import HTTPException
from app.database.models.enums import UserRole


class ProjectService:

    @staticmethod
    def create_project_service(workspace_id: int, db: Session, data: ProjectCreate, current_user_id: int):
        current_user = get_user_by_id(db, current_user_id)

        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Only admin can create project."
            )
        
        # project key auto generation
        project_key = generate_project_key(db, data.name)

        project = Project(
            name=data.name,
            key=project_key,     
            description=data.description,
            created_by=current_user_id,
            workspace_id=workspace_id
        )

        db.add(project)
        db.commit()
        db.refresh(project)
        return project


    @staticmethod
    def get_all_projects(db: Session, workspace_id: int, current_user_id: int):
        current_user = get_user_by_id(db, current_user_id)

        # project list for admin workspace wise
        if current_user.role == UserRole.ADMIN:
            project_list = db.query(Project).filter(Project.workspace_id == workspace_id and Project.is_active == True).all()
        # project list for member (projects in which user is member)
        else:
            project_list = (db.query(Project)
            .join(
                ProjectMember,
                Project.id == ProjectMember.project_id
            )
            .filter(
                ProjectMember.user_id == current_user_id,
                ProjectMember.is_active == True,
                Project.is_active == True
            )
            .all()
        )
        return project_list
    
    
    @staticmethod
    def get_project_by_id(project_id: int, db: Session):
        project = db.query(Project).filter(Project.id == project_id).first()

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )
        return project
    

    @staticmethod
    def update_project(project_id: int, data: ProjectUpdate, db: Session, current_user_id: int):
        current_user = get_user_by_id(db, current_user_id)

        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Only admin can edit project."
            )
        
        project = ProjectService.get_project_by_id(project_id, db)

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )
        
        # update data
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.desciption = data.description

        db.commit()
        db.refresh(project)
        return project


    @staticmethod
    def delete_project(project_id, db:Session, current_user_id):
        current_user = get_user_by_id(db, current_user_id)

        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Only admin can delete project"
            )
        
        project = ProjectService.get_project_by_id(project_id, db)

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )
       
        project.is_active = False
        db.commit()

        # return True
        return {"message" : "project deleted successfully"}
