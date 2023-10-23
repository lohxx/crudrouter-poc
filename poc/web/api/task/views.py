from typing import Optional

from fastapi import Request
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from poc.db.models.todos import Task, TaskStatus
from poc.db.dependencies import sync_db_session
from poc.web.api.task.schema import Task as TaskSchema, PersistedTask


router = SQLAlchemyCRUDRouter(
    schema=PersistedTask,
    create_schema=TaskSchema, 
    db_model=Task,
    db=sync_db_session,
    prefix='task',
    delete_all_route=False
)

@router.api_route('/{item}', methods=['PATCH'])
def update_task(body: Request):
    print(dir(body))
    return True