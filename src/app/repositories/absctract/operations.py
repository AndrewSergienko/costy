from abc import abstractmethod

from src.app.domain.operations import Operation
from src.app.repositories.absctract.base import AbstractRepository


class AOperationRepository(AbstractRepository):
    @abstractmethod
    async def get(self, field, value) -> Operation:
        raise NotImplementedError
