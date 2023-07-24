import asyncio

import uvicorn
from fastapi import FastAPI

from server.redis_client.utils import read_through_cache

app = FastAPI()


@app.get("/data/{id}")
@read_through_cache(key_name='id', expires_in_seconds=10)
async def cached_api(id: str) -> str:
    await asyncio.sleep(1)
    return id


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8001)
