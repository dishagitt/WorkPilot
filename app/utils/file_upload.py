import os
import uuid
import shutil

from fastapi import UploadFile


def save_file(upload: UploadFile, folder: str):

    extension = upload.filename.split(".")[-1].lower()

    filename = f"{uuid.uuid4()}.{extension}"

    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)

    return f"/static/{os.path.basename(folder)}/{filename}"