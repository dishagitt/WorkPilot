from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from fastapi import Form
from app.database.models.enums import ProjectStatus


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: Optional[str] = Form(None)
    ):
        return cls(
            name=name,
            description=description
        )



class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    status: Optional[ProjectStatus] = Field(None)

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        status: Optional[ProjectStatus] = Form(None)
    ):
        return cls(
            name=name,
            description=description,
            status=status
        )
    

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    key: str
    status: ProjectStatus
    created_by: int
    model_config = ConfigDict(from_attributes=True)