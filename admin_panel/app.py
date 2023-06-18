import os

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
    unauthorized_error_exception,
)
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from tortoise.contrib.fastapi import register_tortoise

from admin_panel.common.models.admin import Admin
from admin_panel.providers.login import LoginProvider
from admin_panel.settings import logger, settings
from admin_panel.settings.constants import BASE_DIR


def create_app():
    """
    Это не совсем похоже на стандартную настройку апишки на FastAPI.
    Почти весь код ниже идет из коробки в документации к фреймворку
    Сначала настраивается стандартный формат админки и ошибки
    Также подключается Redis для кеширования токенов
    Для работы с БД используется tortoise
    """
    app = FastAPI()
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "static")),
        name="static",
    )

    @app.get("/")
    async def index():
        return RedirectResponse(url="/admin")

    admin_app.add_exception_handler(
        HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception
    )
    admin_app.add_exception_handler(
        HTTP_404_NOT_FOUND, not_found_error_exception
    )
    admin_app.add_exception_handler(
        HTTP_403_FORBIDDEN, forbidden_error_exception
    )
    admin_app.add_exception_handler(
        HTTP_401_UNAUTHORIZED, unauthorized_error_exception
    )

    @app.on_event("startup")
    async def startup():
        r = redis.from_url(
            settings.cache.url,
            decode_responses=True,
            encoding="utf8",
        )
        await admin_app.configure(
            logo_url="https://preview.tabler.io/static/logo-white.svg",  # Логотип внутри админки
            template_folders=[
                os.path.join(BASE_DIR, "templates")
            ],  # Шаблоны на Jinja2
            favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",  # Небольшая иконка во вкладке
            providers=[
                LoginProvider(
                    login_logo_url="https://preview.tabler.io/static/logo.svg",  # Логотип в левом углу, который кидает на главную
                    admin_model=Admin,
                )  # Для возможности заходить в аккаунт
            ],
            redis=r,  # Редис для кеширования токенов
            language_switch=False,  # Убирает локализацию в меню
        )

    app.mount("/admin", admin_app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    register_tortoise(
        app,
        config={
            "connections": {"default": settings.db.url},
            "apps": {
                "models": {
                    "models": ["admin_panel.models"],
                    "default_connection": "default",
                }
            },
        },
        generate_schemas=True,
    )

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
