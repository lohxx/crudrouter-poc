from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field

from poc.db.models.todos import TaskStatus
from poc.web.api import OrmBase

class Task(BaseModel):
    name: str
    project_id: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now) 
    status: TaskStatus = Field(default=TaskStatus.pending.value)


class PersistedTask(Task, OrmBase):
    pass
