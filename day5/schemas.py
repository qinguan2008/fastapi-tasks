from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    completed: Optional[bool] = None