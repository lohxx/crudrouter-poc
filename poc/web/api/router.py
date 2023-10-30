from fastapi.routing import APIRouter

from poc.web.api import task
from poc.web.api import project

api_router = APIRouter()
api_router.include_router(task.router)
api_router.include_router(project.router)
