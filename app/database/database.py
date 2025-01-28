import logging

from redis.asyncio import Redis

from app.config import settings

async_redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    username=settings.REDIS_USER,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)

# logging.info(f"{settings.REDIS_HOST}:{settings.REDIS_PORT}")


async def get_db():
    async with async_redis.client() as redis:
        try:
            yield redis
        finally:
            await redis.close()
