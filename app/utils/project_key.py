import re
from sqlalchemy.orm import Session

from app.database.models.project import Project


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