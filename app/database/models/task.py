from app.database.connection import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Enum as SqlEnum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.models.enums import TaskPhase, TaskPriority, TaskType


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id= Column(Integer, ForeignKey("projects.id"), nullable=False)
    task_number = Column(String(20), unique=True, nullable=False, index=True)
    task_type = Column(SqlEnum(TaskType), nullable=False, default=TaskType.TASK)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    phase = Column(SqlEnum(TaskPhase), default=TaskPhase.TO_DO, nullable=False, index=True)
    priority = Column(SqlEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False, index=True)
    due_date = Column(Date, nullable=True, index=True)
    created_by= Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # relationship
    project = relationship("Project", back_populates="tasks")
    creator = relationship("User", back_populates="created_tasks", foreign_keys=[created_by])
    assignee = relationship("User", back_populates="assigned_tasks", foreign_keys=[assigned_to])
    comments = relationship("Comment", back_populates="task",  cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="task", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")