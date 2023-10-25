from importlib import metadata
from urllib.parse import urlencode

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.responses import UJSONResponse

from poc.web.api.router import api_router
from poc.db.utils import FilterNotSupported
from poc.web.lifetime import register_shutdown_event, register_startup_event


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="poc",
        version=metadata.version("poc"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    @app.exception_handler(FilterNotSupported)
    async def unicorn_exception_handler(request: Request, exc: FilterNotSupported):
        return JSONResponse(
            status_code=400,
            content={"message": f"Filtro não suportado"},
        )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)
    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
