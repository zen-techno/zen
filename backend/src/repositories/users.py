from backend.src.core.repository import SQLAlchemyRepository
from backend.src.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
