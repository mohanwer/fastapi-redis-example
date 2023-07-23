import asyncio

from fastapi import FastAPI

import redis_utils

app = FastAPI()


@app.get("/data/{id}")
@redis_utils.read_through_cache(key_name='id', expires_in_seconds=10)
async def cached_api(id: str) -> str:
    await asyncio.sleep(1)
    return id
