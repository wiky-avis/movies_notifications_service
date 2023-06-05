import uvicorn as uvicorn
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Movies Notifications Service",
        openapi_url="/openapi.json",
        docs_url="/swagger",
        openapi_prefix="",
    )
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="settings.project_host",
        port="settings.project_port",
        log_config="logger.LOGGING",
        reload=True,
    )
