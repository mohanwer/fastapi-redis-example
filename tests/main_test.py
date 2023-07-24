from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from redis.asyncio.client import Redis

from server.main import app
from server.redis_client.utils import get_object
from server.redis_client.settings import  redis_settings


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def redis_test_session() -> Redis:
    return Redis(
        host=redis_settings.host,
        port=redis_settings.port
    )


@pytest.mark.asyncio
async def test_cacheing_on_data_api(
    redis_test_session: Redis,
    test_client: TestClient
):
    cached_key = str(uuid4())

    response = test_client.get(f"/data/{cached_key}")
    assert response.status_code == 200
    data = response.json()

    cached_value = await get_object(cached_key, redis_test_session)
    assert data == cached_value == cached_value
