from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AttachmentResponse(BaseModel):
    id: int
    task_id: Optional[int] = None
    comment_id: Optional[int] = None
    file_name: str
    file_url: str
    uploaded_by_name: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)