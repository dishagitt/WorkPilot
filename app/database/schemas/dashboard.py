from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from app.database.models.enums import TaskPhase, TaskPriority, ActivityAction

class DashboardSummaryResponse(BaseModel):
    total_projects: int
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int

    model_config = ConfigDict(from_attributes=True)


class DashboardTaskResponse(BaseModel):
    id: int
    task_number: str
    title: str
    project_name: str
    priority: TaskPriority
    phase: TaskPhase
    due_date: date | None

    model_config = ConfigDict(from_attributes=True)


class DashboardProjectResponse(BaseModel):
    id: int
    project_name: str
    total_tasks: int

    model_config = ConfigDict(from_attributes=True)

class DashboardActivityResponse(BaseModel):
    id: int
    task_number: str
    action: ActivityAction
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeadlineTaskResponse(BaseModel):
    id: int
    task_number: str
    title: str
    due_date: date
    priority: TaskPriority

    model_config = ConfigDict(from_attributes=True)


class DashboardDeadlineResponse(BaseModel):
    due_today: list[DeadlineTaskResponse]
    overdue: list[DeadlineTaskResponse]