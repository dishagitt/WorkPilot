from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from fastapi import Form
from datetime import datetime
from app.database.models.enums import ProjectMemberRole


class ProjectMemberCreate(BaseModel):
    user_id: int
    role: Optional[ProjectMemberRole] = None

    @classmethod
    def as_form(
        cls,
        user_id: int = Form(...),
        role: ProjectMemberRole = Form(...),
    ):
        return cls(
            user_id=user_id,
            role=role
        )


class ProjectMemberRoleUpdate(BaseModel):
    user_id: int
    role: ProjectMemberRole = ProjectMemberRole.DEVELOPER

    @classmethod
    def as_form(
        cls,
        user_id: Optional[int] = Form(None),
        role: Optional[ProjectMemberRole] = Form(None),
    ):
        return cls(
            user_id=user_id,
            role=role
        )


class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: ProjectMemberRole
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProjectMemberListResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: ProjectMemberRole
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkspaceMemberListResponse(BaseModel):
    id: int
    full_name: str
    email: str
    joined_at: datetime
    total_projects: int

    model_config = ConfigDict(from_attributes=True)