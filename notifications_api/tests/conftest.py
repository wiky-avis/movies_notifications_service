import pytest_asyncio
from httpx import AsyncClient

from notifications_api.src.app import create_app


@pytest_asyncio.fixture
async def test_app():
    app = create_app()
    await app.router.startup()
    try:
        yield app
    finally:
        await app.router.shutdown()


@pytest_asyncio.fixture
async def test_client(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client
