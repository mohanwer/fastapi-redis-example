from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from redis import asyncio as async_redis

import redis_utils
from main import app

client = TestClient(app)


@pytest.fixture
def redis_test_session() -> async_redis.Redis:
    return async_redis.Redis()


@pytest.mark.asyncio
async def test_cacheing_on_data_api(redis_test_session: async_redis):
    cached_key = str(uuid4())

    response = client.get(f"/data/{cached_key}")
    assert response.status_code == 200
    data = response.json()

    cached_value = await redis_utils.get_object(cached_key, redis_test_session)
    assert data == cached_value == cached_value
