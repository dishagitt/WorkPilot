from app.database.connection import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    task_id= Column(Integer, ForeignKey("tasks.id"), nullable=True)
    comment_id= Column(Integer, ForeignKey("comments.id"), nullable=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(255), nullable=False)
    uploaded_by= Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    task = relationship("Task", back_populates="attachments")
    comment = relationship("Comment", back_populates="attachments")
    user = relationship("User", back_populates="attachments")