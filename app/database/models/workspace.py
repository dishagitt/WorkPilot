from app.database.connection import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Enum as SqlEnum, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.models.enums import WorkspaceMemberRole

class Workspace(Base):
	__tablename__ = "workspaces"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(100), nullable=False, unique=True)
	description = Column(Text, nullable=True)
	logo_url = Column(String(255), nullable=True)
	slug = Column(String(255), unique=True, nullable=False, index=True)
	created_by= Column(Integer, ForeignKey("users.id"), nullable=False)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime(timezone=True),  server_default=func.now())
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
	
    #relationships
	owner = relationship("User", back_populates="owned_workspaces", foreign_keys=[created_by])
	projects = relationship("Project", back_populates="workspace", cascade="all, delete-orphan")
	members = relationship("WorkspaceMember", back_populates="workspace", cascade="all, delete-orphan")


class WorkspaceMember(Base):
	__tablename__ = "workspace_members"
	__table_args__ = (UniqueConstraint("workspace_id", "user_id", name="uq_workspace_user"),)
	id = Column(Integer, primary_key=True, index=True)
	workspace_id= Column(Integer, ForeignKey("workspaces.id"), nullable=False)
	user_id= Column(Integer, ForeignKey("users.id"), nullable=False) 
	role = Column(SqlEnum(WorkspaceMemberRole), nullable=False, default=WorkspaceMemberRole.MEMBER)
	joined_at = Column(DateTime(timezone=True),  server_default=func.now())
	is_active = Column(Boolean, default=True, nullable=False)

	#relationships
	workspace = relationship("Workspace", back_populates="members")
	user = relationship("User", back_populates="workspace_memberships")