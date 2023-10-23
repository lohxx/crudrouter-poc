from importlib import metadata
from urllib.parse import urlencode

from fastapi import FastAPI, Request
from fastapi.responses import UJSONResponse

from poc.web.api.router import api_router
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

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    @app.middleware("http")
    async def update_pagination_params(request: Request, call_next):
        if request.query_params.get('page') and request.query_params.get('per_page'):
            # update request query parameters
            params = dict(request.query_params)
            params['skip'] = request.query_params.get('page')
            params['limit'] = request.query_params.get('per_page')
            request.scope['query_string'] = urlencode(params).encode('utf-8')

        response = await call_next(request)
        return response

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
