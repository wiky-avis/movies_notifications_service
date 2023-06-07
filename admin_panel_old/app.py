# import sys

import uvicorn as uvicorn
from fastapi import FastAPI

# from admin_panel.api import v1
# from admin_panel.containers import Container
from admin_panel_old.middleware.request_id import RequestIdMiddleware
from admin_panel_old.settings import logger, settings


def create_app() -> FastAPI:
    # container = Container()
    # container.wire(modules=[sys.modules[__name__]])

    app = FastAPI(
        title="Movies Notifications Service",
        openapi_url="/openapi.json",
        docs_url="/swagger",
        openapi_prefix="",
    )
    app.container = container  # type: ignore

    # app.include_router(router)

    app.middleware("http")(RequestIdMiddleware())

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.admin_panel.host,
        port=settings.admin_panel.port,
        log_config=logger.LOGGING,
        reload=True,
    )
