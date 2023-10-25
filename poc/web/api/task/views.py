from typing import List, Optional

from fastapi import Request, Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi_crudrouter.core.databases import pydantify_record

from poc.db.models.todos import Task, TaskStatus
from poc.db.dependencies import sync_db_session
from poc.db.utils import get_all_tasks
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
def update_task(body: TaskSchema) -> PersistedTask:
    print(dir(body))
    return True


@router.get('')
def overloaded_get_all(
    where: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 20,
    db_session=Depends(sync_db_session),
) -> Optional[List[PersistedTask]]:
    tasks = get_all_tasks(db_session, Task, page, per_page, extra_filters=where)

    try:
        return [PersistedTask(**task.as_dict()) for task in tasks]
    except AttributeError:
        return [PersistedTask(**task[0].as_dict()) for task in tasks]