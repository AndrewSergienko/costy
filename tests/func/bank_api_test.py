import pytest
from httpx import AsyncClient

from src.app.domain.bank_api import BankInfo, BankInfoProperty
from src.app.services.bank_api import get_bank_managers_by_user, update_banks_costs
from src.app.services.operations import get_all_operations
from src.app.services.uow.sqlalchemy import SqlAlchemyUnitOfWork
from src.database import Database
from tests.patterns import create_and_auth_func_user, create_model_user


@pytest.mark.asyncio
async def test_update_costs_with_banks(database: Database):
    async with database.sessionmaker() as session:
        # КРОК 1: Створення менеджерів
        uow = SqlAlchemyUnitOfWork(session)
        user = await create_model_user(uow)
        bank_info = BankInfo(bank_name="monobank", user_id=user.id)
        async with uow:
            await uow.banks_info.add(bank_info)
            await uow.banks_info.add(
                BankInfoProperty(
                    name="X-Token",
                    value="uZFOvRJNeXoVHYTUA_8NgHneWUz8IsG8dRPUbx60mbM4",
                    value_type="str",
                    manager=bank_info,
                )
            )
            await uow.commit()

        # КРОК 2: Запис в базу даних витрат за допомогою менеджерів
        managers = await get_bank_managers_by_user(uow, user_id=user.id)
        await update_banks_costs(uow, managers)

        # КРОК 3: Перевірка записів
        # Тест буде пройдений, якщо буде хоча б одна операція
        # TODO: Створити алгоритм перевірки відносно запиту до API
        operations = await get_all_operations(uow, user_id=user.id)
        assert len(operations) > 0


@pytest.mark.asyncio
async def test_add_bank_info_with_endpoint(client_db: AsyncClient):
    auth_data = await create_and_auth_func_user(client_db)
    token = auth_data["token"]
    headers = {"Authorization": token}

    response = await client_db.post(
        "/bankapi/add/",
        json={
            "bank_name": "monobank",
            "X-Token": "uZFOvRJNeXoVHYTUA_8NgHneWUz8IsG8dRPUbx60mbM4",
        },
        headers=headers,
    )
    assert response.status_code == 201
