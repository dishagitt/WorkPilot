import os
import uuid
import shutil
from fastapi import UploadFile
from pathlib import Path

STATIC_DIR = Path("app/static")


def save_file(upload: UploadFile, folder: str):

    extension = upload.filename.split(".")[-1].lower()

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