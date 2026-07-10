from app.database.connection import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Enum as SqlEnum, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.models.enums import ProjectMemberRole

class Project(Base):
	__tablename__ = "projects"
	id = Column(Integer, primary_key=True, index=True)
	workspace_id= Column(Integer, ForeignKey("workspaces.id"), nullable=False)
	name = Column(String(100), nullable=False, index=True)
	key = Column(String(20), unique=True, nullable=False, index=True)
	description = Column(Text, nullable=True)
	created_by= Column(Integer, ForeignKey("users.id"), nullable=False)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime(timezone=True),  server_default=func.now())
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
	
    #relationships
	creator = relationship("User", back_populates="created_projects", foreign_keys=[created_by])
	workspace = relationship("Workspace", back_populates="projects")
	members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
	tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")


class ProjectMember(Base):
	__tablename__ = "project_members"
	__table_args__ = (UniqueConstraint("project_id", "user_id", name="uq_project_user"),)
	id = Column(Integer, primary_key=True, index=True)
	project_id= Column(Integer, ForeignKey("projects.id"), nullable=False)
	user_id= Column(Integer, ForeignKey("users.id"), nullable=False) 
	role = Column(SqlEnum(ProjectMemberRole), default=ProjectMemberRole.DEVELOPER, nullable=False)
	joined_at = Column(DateTime(timezone=True),  server_default=func.now())
	is_active = Column(Boolean, default=True, nullable=False)
	
	#relationships
	project = relationship("Project", back_populates="members")
	user = relationship("User", back_populates="project_memberships")