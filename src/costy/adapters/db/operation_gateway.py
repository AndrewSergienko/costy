from adaptix import Retort
from sqlalchemy import Table, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from costy.application.common.operation_gateway import (
    OperationDeleter,
    OperationReader,
    OperationSaver,
    OperationsReader,
)
from costy.domain.models.operation import Operation, OperationId
from costy.domain.models.user import UserId


class OperationGateway(
    OperationReader, OperationSaver, OperationDeleter, OperationsReader
):
    def __init__(self, session: AsyncSession, table: Table, retort: Retort):
        self.session = session
        self.table = table
        self.retort = retort

    async def get_operation(self, operation_id: OperationId) -> Operation | None:
        query = select(self.table).where(self.table.c.id == operation_id)
        result = await self.session.scalar(query)
        data = next(result.mapping(), None)
        return self.retort.load(data, Operation) if data else None

    async def save_operation(self, operation: Operation) -> None:
        values = self.retort.dump(operation)
        query = insert(self.table).values(**values)
        result = await self.session.execute(query)
        operation.id = OperationId(result.inserted_primary_key)

    async def delete_operation(self, operation_id: OperationId) -> None:
        query = delete(self.table).where(self.table.c.id == operation_id)
        await self.session.execute(query)

    async def find_operations_by_user(
        self,
        user_id: UserId,
        from_time: int | None,
        to_time: int | None
    ) -> list[Operation]:
        query = select(self.table).where(self.table.c.user_id == user_id)
        if from_time:
            query = query.where(self.table.c.time >= from_time)
        if to_time:
            query = query.where(self.table.c.time <= to_time)
        result = await self.session.scalars(query)
        return self.retort.dump(result.mapping(), list[Operation])
