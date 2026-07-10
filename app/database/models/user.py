from app.database.connection import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    photo_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    owned_workspaces = relationship("Workspace", back_populates="owner")
    created_projects = relationship("Project", back_populates="creator")
    project_memberships = relationship("ProjectMember", back_populates="user")
    workspace_memberships = relationship("WorkspaceMember", back_populates="user")
    created_tasks = relationship("Task", back_populates="creator", foreign_keys="Task.created_by")
    assigned_tasks = relationship("Task", back_populates="assignee", foreign_keys="Task.assigned_to")
    comments = relationship("Comment", back_populates="user")
    activities = relationship("Activity", back_populates="user")
    attachments = relationship("Attachment", back_populates="user")