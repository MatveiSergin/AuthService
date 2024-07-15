from redis import asyncio as aioredis
from settings.settings import settings
class Cache(aioredis.Redis):
    async def set(
            self,
            name: str,
            value: str,
            ex: None | int  = None,
            px: None | int = None,
            nx: bool = False,
            xx: bool = False,
            keepttl: bool = False,
            get: bool = False,
            exat = None,
            pxat = None,
    ) -> bool | None:
        if ex is None:
            ex = settings.EXPIRE_REDIS
        return await super().set(name, value, ex=ex)

cache = Cache(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT)


