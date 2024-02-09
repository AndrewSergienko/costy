from abc import ABC, abstractmethod
from typing import AsyncContextManager

from costy.application.authenticate import Authenticate
from costy.application.category.create_category import CreateCategory
from costy.application.category.read_available_categories import (
    ReadAvailableCategories,
)
from costy.application.common.id_provider import IdProvider
from costy.application.operation.create_operation import CreateOperation
from costy.application.operation.read_list_operation import ReadListOperation
from costy.application.operation.read_operation import ReadOperation
from costy.application.user.create_user import CreateUser


class InteractorFactory(ABC):
    @abstractmethod
    def authenticate(self) -> AsyncContextManager[Authenticate]:
        pass

    @abstractmethod
    def create_user(self) -> AsyncContextManager[CreateUser]:
        pass

    @abstractmethod
    def create_operation(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[CreateOperation]:
        pass

    @abstractmethod
    def read_operation(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[ReadOperation]:
        pass

    @abstractmethod
    def read_list_operation(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[ReadListOperation]:
        pass

    @abstractmethod
    def create_category(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[CreateCategory]:
        pass

    @abstractmethod
    def read_available_categories(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[ReadAvailableCategories]:
        pass