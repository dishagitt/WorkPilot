from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from fastapi import Form
from datetime import datetime
from app.database.models.enums import ProjectMemberRole, UserRole


class ProjectMemberCreate(BaseModel):
    role: ProjectMemberRole = ProjectMemberRole.DEVELOPER

    @classmethod
    def as_form(
        cls,
        role: ProjectMemberRole = Form(ProjectMemberRole.DEVELOPER),
    ):
        return cls(role=role)


class ProjectMemberRoleUpdate(BaseModel):
    role: Optional[ProjectMemberRole] = None

    @classmethod
    def as_form(
        cls,
        role: Optional[ProjectMemberRole] = Form(None),
    ):
        return cls(role=role)


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