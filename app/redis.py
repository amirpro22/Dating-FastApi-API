import aioredis
from app.config import settings



redis_pool = aioredis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=1,
        max_connections=100,
        encoding='utf8',
    )

