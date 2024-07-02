from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    id: int
    title: str
    content: str
    type: str
    created_at: datetime
    updated_at: datetime
