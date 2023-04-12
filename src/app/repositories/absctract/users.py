from abc import abstractmethod

from src.app.models.users import User
from src.app.repositories.absctract.base import AbstractRepository


class AUserRepository(AbstractRepository):
    @abstractmethod
    async def get(self, field, value) -> User:
        raise NotImplementedError