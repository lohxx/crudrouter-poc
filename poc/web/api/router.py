from fastapi.routing import APIRouter

from poc.web.api import task

api_router = APIRouter()
api_router.include_router(task.router)
