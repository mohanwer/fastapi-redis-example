import os

from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str = os.getenv('REDIS_HOST', 'localhost')
    port: int = int(os.getenv('REDIS_PORT', '6379'))


redis_settings = RedisSettings()
