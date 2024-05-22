from functools import lru_cache

from db.abstract_cache_repository import AbstractCacheRepository
from db.redis import get_redis
from fastapi import Depends
from redis.asyncio import Redis


class RedisCacheRepository(AbstractCacheRepository):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def get(self, key: str):
        data = await self._redis.get(key)
        return data

    async def set(self, key: str, value: str):
        await self._redis.set(key, value)


@lru_cache()
def get_cache_repository(
    redis: Redis = Depends(get_redis),
) -> AbstractCacheRepository:
    return RedisCacheRepository(redis=redis)
