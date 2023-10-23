from __future__ import annotations
from typing import List

import enum
from sqlalchemy import Column, String, Enum, Integer, Date, DateTime

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy import text

from sqlalchemy.orm import declarative_base

Base = declarative_base()


#from poc.db.base import Base

class TaskStatus(str, enum.Enum):
    pending = 'pending'
    done = 'done'


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    due_date = Column(Date)
    created_at = Column(DateTime, server_default=text('NOW()'))
    task: Mapped[List["Task"]] = relationship("Task")


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=text('NOW()'))
    status = Column(Enum(TaskStatus))
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)

    