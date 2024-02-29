from litestar import Controller, get, post

from costy.application.common.id_provider import IdProvider
from costy.application.operation.dto import ListOperationDTO, NewOperationDTO
from costy.domain.models.operation import Operation, OperationId
from costy.presentation.interactor_factory import InteractorFactory


class OperationController(Controller):
    path = '/operations'

    @get()
    async def get_list_operations(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        from_time: int | None,
        to_time: int | None,
    ) -> list[Operation]:
        data = ListOperationDTO(from_time, to_time)
        async with ioc.read_list_operation(id_provider) as read_operations:
            return await read_operations(data)

    @post()
    async def create_operation(
        self,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        data: NewOperationDTO,
    ) -> OperationId:
        async with ioc.create_operation(id_provider) as create_operation:
            return await create_operation(data)
