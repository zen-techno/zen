from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.redis import get_redis
from src.storage.sqlalchemy import get_async_session

DatabaseSession = Annotated[AsyncSession, Depends(get_async_session)]
RedisDepends = Annotated[Redis, Depends(get_redis)]
