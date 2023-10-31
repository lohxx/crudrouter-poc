from typing import List, Optional
from datetime import date, datetime

from pydantic import BaseModel, Field
from poc.web.api import OrmBase

from poc.web.api.task.schema import PersistedTask

class Project(BaseModel):
    name: str
    due_date: Optional[date] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)


class PersistedProject(Project, OrmBase):
    tasks: List[PersistedTask] = []


class PartialProject(Project):
    name: Optional[str] = None
    created_at: Optional[datetime] = None