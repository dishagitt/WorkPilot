from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from fastapi import Form
from datetime import datetime



class CommentCreate(BaseModel):
    content: str

    @classmethod
    def as_form(
        cls,
        content: str = Form(...),
    ):
        return cls(
            content=content
        )


class CommentUpdate(BaseModel):
    content: Optional[str] = None
   
    @classmethod
    def as_form(
        cls,
        content: Optional[str] = Form(None)
    ):
        return cls(
            content=content
        )


class CommentResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    content: str
    created_at: datetime
    updated_at: Optional[datetime]
    commenter: str

    model_config = ConfigDict(from_attributes=True)