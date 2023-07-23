from typing import Optional

from redis import asyncio

# thread safe global connection pool
_REDIS_CONNECTION_POOL: Optional[asyncio.ConnectionPool] = None


def start_redis_connection_pool() -> None:
    # Intended to be called during the application startup process
    global _REDIS_CONNECTION_POOL
    if not _REDIS_CONNECTION_POOL:
        _REDIS_CONNECTION_POOL = asyncio.ConnectionPool()


async def disconnect_from_redis() -> None:
    # Called during application shutdown
    if _REDIS_CONNECTION_POOL:
        await _REDIS_CONNECTION_POOL.disconnect()


def get_connection_pool() -> asyncio.ConnectionPool:
    if not _REDIS_CONNECTION_POOL:
        start_redis_connection_pool()
    return _REDIS_CONNECTION_POOL


def get_redis_connection() -> asyncio.Redis:
    conn = get_connection_pool()
    return asyncio.Redis(
        connection_pool=conn,
        auto_close_connection_pool=False,
    )