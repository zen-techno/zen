from src.core.repository import SQLAlchemyRepository
from src.models import UserModel


class UserRepository(SQLAlchemyRepository):
    model = UserModel
