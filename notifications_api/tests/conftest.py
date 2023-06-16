import pytest_asyncio
from httpx import AsyncClient

from notifications_api.src.app import app


@pytest_asyncio.fixture
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
