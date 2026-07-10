from app.database.connection import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SqlEnum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.models.enums import ActivityAction

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(SqlEnum(ActivityAction), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value =  Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    task = relationship("Task", back_populates="activities")
    user = relationship("User", back_populates="activities")