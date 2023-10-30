from __future__ import annotations
import enum
from typing import List

from sqlalchemy import Column, String, Enum, Integer, Date, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import text
from sqlalchemy.orm import declarative_base

from poc.db.meta import meta

Base = declarative_base()


class TaskStatus(str, enum.Enum):
    pending = 'pending'
    done = 'done'


class Project(Base):
    metadata = meta
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    due_date = Column(Date)
    created_at = Column(DateTime, server_default=text('NOW()'))
    tasks: Mapped[List["Task"]] = relationship("Task", lazy="dynamic")



class Task(Base):
    metadata = meta
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=text('NOW()'))
    status = Column(Enum(TaskStatus))
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
