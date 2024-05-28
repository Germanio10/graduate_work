from functools import lru_cache

from core.config import CACHE_EXPIRE_IN_SECONDS
from db.abstract_cache_repository import AbstractCacheRepository
from db.redis import get_redis
from fastapi import Depends
from redis.asyncio import Redis


class RedisCacheRepository(AbstractCacheRepository):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def get(self, key: str) -> str | None:
        data = await self._redis.get(key)
        if not data:
            return None
        return data.decode('utf-8')

    async def set(self, key: str, value: str):
        await self._redis.set(key, value, CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_cache_repository(
    redis: Redis = Depends(get_redis),
) -> AbstractCacheRepository:
    return RedisCacheRepository(redis=redis)
