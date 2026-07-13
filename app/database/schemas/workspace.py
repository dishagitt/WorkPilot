from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from fastapi import Form


class WorkspaceCreate(BaseModel):
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



class WorkspaceUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    logo_url: Optional[str] = None 

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        logo_url: Optional[str] = Form(None)
    ):
        return cls(
            name=name,
            description=description,
            logo_url=logo_url
        )
    

class WorkspaceResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    slug: str
    created_by: int
    model_config = ConfigDict(from_attributes=True)


class WorkspaceListResponse(BaseModel):
    id: int
    name: str
    workspace_owner: str
    logo_url: str
    slug: str
    total_projects: int
    total_members: int
    total_open_tasks: int
    model_config = ConfigDict(from_attributes=True)