import sys

import uvicorn as uvicorn
from fastapi import FastAPI

from templates_service.api.v1 import router
from templates_service.containers import Container
from templates_service.middleware.request_id import RequestIdMiddleware
from templates_service.settings import logger, settings


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    app = FastAPI(
        title="Movies Notifications Service",
        openapi_url="/openapi.json",
        docs_url="/swagger",
        openapi_prefix="",
    )
    app.container = container  # type: ignore

    app.include_router(router)

    app.middleware("http")(RequestIdMiddleware())

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.app.host,
        port=settings.app.port,
        log_config=logger.LOGGING,
        reload=True,
    )
