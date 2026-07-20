import os
import uuid
import shutil
from fastapi import UploadFile
from pathlib import Path
from fastapi import HTTPException

STATIC_DIR = Path("app/static")


allowed_extensions = {
    "jpg",
    "jpeg",
    "png",
    "pdf",
    "doc",
    "docx",
    "xlsx",
    "pptx",
    "zip"
}

def save_file(upload: UploadFile, folder: str):

    extension = Path(upload.filename).suffix.lower().replace(".", "")

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )

    filename = f"{uuid.uuid4()}.{extension}"

    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    return f"/static/{os.path.basename(folder)}/{filename}"



def delete_file(file_url: str):
    if not file_url:
        return

    # Never delete the default workspace logo
    if file_url == "/static/workspace_logos/default-workspace.png":
        return
    
    # Never delete the default profile image
    if file_url == "/static/profile_photos/default-profile.png":
        return

    # Remove leading "/static/"
    relative_path = file_url.replace("/static/", "")

    file_path = STATIC_DIR / relative_path

    if file_path.exists():
        file_path.unlink()