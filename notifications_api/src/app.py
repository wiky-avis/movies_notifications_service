import sys

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from notifications_api.src.api import srv
from notifications_api.src.common.connectors.amqp import (
    AMQPSenderPikaConnector,
)
from notifications_api.src.common.connectors.db import DbConnector
from notifications_api.src.common.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from notifications_api.src.containers import Container
from notifications_api.src.settings import logger, settings


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    app = FastAPI(
        on_startup=[
            DbConnector.connect,
            AMQPSenderPikaConnector.setup,
        ],
        on_shutdown=[
            DbConnector.disconnect,
            AMQPSenderPikaConnector.close,
        ],
        exception_handlers={
            HTTPException: http_exception_handler,
            RequestValidationError: request_validation_exception_handler,
        },
        title="test",
        openapi_url="/openapi.json",
        docs_url="/api/swagger",
        openapi_prefix="",
    )
    app.container = container  # type: ignore

    app.include_router(srv.router)

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
