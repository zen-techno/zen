from redis.asyncio import ConnectionPool, Redis

from src.settings import settings

pool = ConnectionPool(
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.database_name,
    username=settings.redis.user,
    password=settings.redis.password.get_secret_value(),
    decode_responses=True,
)


def get_redis() -> Redis:
    return Redis(connection_pool=pool)
