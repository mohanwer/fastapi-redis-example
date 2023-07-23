import asyncio
import functools
from redis import asyncio as async_redis
from typing import Any, Optional, Callable
import pickle

import redis_connection


async def get_object(key: str, r: Optional[async_redis.Redis] = None) -> Optional[Any]:
    # get an object from redis based on a key
    redis = r or redis_connection.get_redis_connection()
    binary_obj = await redis.get(key)

    # convert the binary object to a python object using pickle
    return pickle.loads(binary_obj) if binary_obj else None


async def save_object(
        key: str, obj: Any, expire: Optional[int] = 0
) -> None:
    redis = redis_connection.get_redis_connection()

    # convert a python object to binary
    binary_object = pickle.dumps(obj)
    if expire:
        # if we have an expiration passed in, set it so redis will automatically remove the object
        await redis.setex(key, expire, binary_object)
    else:
        # if there is no expiration, save the object indefinitely
        # be careful with this as you will have to manage removing this object from cache and run the risk
        # of running out of space in redis if done poorly.
        await redis.set(key, binary_object)


def read_through_cache(
    key_name: str, expires_in_seconds: int
) -> Callable[..., Callable]:
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        async def wrapper(
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            key = kwargs[key_name]
            cached_value = await get_object(key)
            if cached_value:
                return cached_value

            if asyncio.iscoroutinefunction(f):
                res = await f(*args, **kwargs)
            else:
                res = f(*args, **kwargs)

            await save_object(
                key=key, obj=res, expire=expires_in_seconds
            )
            return res

        return wrapper

    return decorator