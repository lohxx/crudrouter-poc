from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field

from poc.db.models.todos import TaskStatus
from poc.web.api import OrmBase

class Task(BaseModel):
    name: str
    project_id: Optional[int] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now) 
    status: Optional[TaskStatus] = Field(default=TaskStatus.pending.value)


class PersistedTask(Task, OrmBase):
    pass


class PartialTask(Task):
    name: Optional[str]
    status: Optional[TaskStatus]
    created_at: Optional[datetime]