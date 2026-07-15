from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from fastapi import Form
from datetime import date as Date
from app.database.models.enums import TaskPhase, TaskPriority, TaskType


class TaskCreate(BaseModel):
    task_type: TaskType.TASK
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., max_length=500)
    priority: TaskPriority = TaskPriority.MEDIUM 
    due_date: Optional[Date] = None
    assigned_to: Optional[int] = None

    @classmethod
    def as_form(
        cls,
        task_type: TaskType = Form(...),
        title: str = Form(...),
        description: str = Form(...),
        priority: TaskPriority = Form(TaskPriority.MEDIUM ),
        due_date: Optional[Date] = Form(None),
        assigned_to: Optional[int] = Form(None)
    ):
        return cls(
            task_type=task_type,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to
        )



class TaskUpdate(BaseModel):
    task_type: Optional[TaskType] = Field(default=None)
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    phase: Optional[TaskPhase] = Field(default=None)
    priority: Optional[TaskPriority] = Field(default=None)
    due_date: Optional[Date] = Field(default=None)
    assigned_to: Optional[int] = Field(default=None)

    @classmethod
    def as_form(
        cls,
        task_type:  Optional[TaskType] = Form(None),
        title: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        phase: Optional[TaskPhase] = Form(None),
        priority: Optional[TaskPriority] = Form(None),
        due_date: Optional[Date] = Form(None),
        assigned_to: Optional[int] = Form(None)
    ):
        return cls(
            task_type=task_type,
            title=title,
            description=description,
            phase=phase,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to
        )
    

class TaskResponse(BaseModel):
    id: int
    project_id: int
    task_number: str
    task_type: TaskType
    title: str
    description: str
    phase: TaskPhase
    priority: TaskPriority
    due_date: Optional[Date] = None
    created_by_name: str
    assigned_to_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)