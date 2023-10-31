from poc.db.models.todos import Task
from poc.web.api.task.schema import PartialTask, Task as TaskSchema, PersistedTask

from poc.web.api import create_router


router = create_router(PersistedTask, TaskSchema, Task, 'task', partial_model=PartialTask)