import sys

import uvicorn as uvicorn
from fastapi import FastAPI

from notifications_api.src.api import v1
from notifications_api.src.containers import Container
from notifications_api.src.settings import logger, settings


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    app = FastAPI(
        on_startup=[],
        on_shutdown=[],
        title="test",
        openapi_url="/openapi.json",
        docs_url="/swagger",
        openapi_prefix="",
    )
    app.container = container  # type: ignore

    app.include_router(v1.router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.project_host,
        port=settings.project_port,
        log_config=logger.LOGGING,
        reload=True,
    )
