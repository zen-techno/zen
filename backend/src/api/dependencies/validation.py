from fastapi.exceptions import HTTPException
from fastapi import status
from uuid import UUID

from backend.src.api.dependencies.services import UserServiceDepends
from backend.src.schemas.users import UserReadSchema


async def valid_user_uuid(uuid: UUID, user_service: UserServiceDepends) -> UserReadSchema:
    user = await user_service.get_user_by_uuid(id_=uuid)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
