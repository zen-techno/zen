from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

Session = Annotated[AsyncSession, Depends(get_async_session)]
