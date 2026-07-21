import re
from sqlalchemy.orm import Session
from app.database.models.project import Project
from app.database.models.task import Task
from fastapi import HTTPException


def generate_project_key(db: Session, project_name: str) -> str:
    # Remove extra spaces
    words = re.findall(r"[A-Za-z0-9]+", project_name.strip())

    if not words:
        raise ValueError("Project name cannot be empty.")

    # 1 or 2 words -> first 3 letters of first word
    if len(words) < 3:
        base_key = words[0][:3].upper()
    # 3 or more words -> first letter of first 3 words
    else:
        base_key = "".join(word[0] for word in words[:3]).upper()

    key = base_key
    counter = 1

    while db.query(Project).filter(Project.key == key).first():
        key = f"{base_key}{counter}"
        counter += 1

    return key




def generate_task_number(db: Session, project_id: int) -> str:
    # Get project
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.is_deleted == False
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    last_task = (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .order_by(Task.id.desc())
        .first()
    )

    if not last_task:
        next_number = 1
    else:
        current_number = int(last_task.task_number.split("-")[-1])
        next_number = current_number + 1

    return f"{project.key}-{next_number}"