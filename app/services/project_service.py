from sqlalchemy.orm import Session
from app.database.models.project import Project, ProjectMember
from app.database.schemas.project import ProjectCreate, ProjectUpdate
from app.utils.key_num import generate_project_key
from app.services.user_service import get_user_by_id
from fastapi import HTTPException, status
from app.database.models.enums import UserRole, ProjectStatus
from app.services.workspace_service import get_workspace_by_id


class ProjectService:

    @staticmethod
    def create_project_service(workspace_id: int, db: Session, data: ProjectCreate, current_user_id: int):
        current_user = get_user_by_id(db, current_user_id)

        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Only admin can create project."
            )
        
         # Check if project name already exists in this workspace
        existing_project = (
            db.query(Project)
            .filter(
                Project.workspace_id == workspace_id,
                Project.name == data.name
            )
            .first()
        )

        if existing_project:
            raise HTTPException(
                status_code=409,
                detail="A project with this name already exists in the workspace."
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
    def get_all_active_projects(db: Session, workspace_id: int, current_user_id: int):
        try:
            #check if workspace exists
            workspace = get_workspace_by_id(db, workspace_id)
            if workspace:
                current_user = get_user_by_id(db, current_user_id)

                # project list for admin workspace wise
                if current_user.role == UserRole.ADMIN:
                    project_list = db.query(Project).filter(Project.workspace_id == workspace_id, Project.is_deleted == False, Project.status == 'ACTIVE').all()
                # project list for member (projects in which user is member)
                else:
                    project_list = (db.query(Project)
                    .join(
                        ProjectMember,
                        Project.id == ProjectMember.project_id
                    )
                    .filter(
                        ProjectMember.user_id == current_user_id,
                        ProjectMember.is_deleted == False,
                        Project.is_deleted == False,
                        Project.status == ProjectStatus.ACTIVE
                    )
                    .all()
                )
                return project_list
            
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
    def get_all_archived_projects(db: Session, workspace_id: int, current_user_id: int):
        current_user = get_user_by_id(db, current_user_id)

        # project list for admin workspace wise
        if current_user.role == UserRole.ADMIN:
            project_list = db.query(Project).filter(Project.workspace_id == workspace_id, Project.is_deleted == False, Project.status == 'ARCHIVED').all()
        return project_list
    
    
    @staticmethod
    def get_project_by_id(project_id: int, db: Session):
        project = db.query(Project).filter(Project.id == project_id).first()

        if not project or project.is_deleted == True:
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
        
        # update data only if project is active
        try:
            if project.status == ProjectStatus.ACTIVE:
                if data.name is not None:
                    project.name = data.name
                if data.description is not None:
                    project.description = data.description
                if data.status is not None:
                    project.status = data.status
            else:
                if data.status is not None:
                    project.status = data.status

            db.commit()
            db.refresh(project)
            return project
            
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
    def delete_project(project_id, db:Session, current_user_id):
        current_user = get_user_by_id(db, current_user_id)

        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Only admin can delete project"
            )
        
        project = ProjectService.get_project_by_id(project_id, db)
       
        project.is_deleted = True
        db.commit()

        # return True
        return {"message" : "Project deleted successfully"}
    

    @staticmethod
    def change_project_status(project_id: int, db: Session, current_user_id: int):
        current_user = get_user_by_id(db, current_user_id)

        if current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="Only admin can change project status"
            )
        
        project = ProjectService.get_project_by_id(project_id, db)
       
        if project.status == ProjectStatus.ACTIVE:
            project.status = ProjectStatus.ARCHIVED
        else:
            project.status = ProjectStatus.ACTIVE

        db.commit()

        # return project.status
        return {f"message: project status changed to - {project.status}"}