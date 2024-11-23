from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import ConnectionPool, Redis

from config import settings

REDIS_URL = settings.get_redis_url()

redis_pool = ConnectionPool.from_url(REDIS_URL, max_connections=5)

redis = Redis(connection_pool=redis_pool)

redis_storage = RedisStorage(redis)

redis_session_middleware = session_middleware(redis_storage)
