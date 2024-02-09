from dataclasses import dataclass
from typing import NewType

from costy.domain.models.category import CategoryId
from costy.domain.models.user import UserId

OperationId = NewType("OperationId", int)


@dataclass
class Operation:
    id: OperationId | None
    amount: int
    description: str | None
    time: int
    user_id: UserId
    category_id: CategoryId