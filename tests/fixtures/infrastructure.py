import os
from typing import AsyncGenerator, AsyncIterator

import pytest
from adaptix import Retort
from aiohttp import ClientSession
from httpx import AsyncClient
from litestar import Litestar
from pytest_asyncio import fixture
from sqlalchemy import Table
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from costy.infrastructure.db.main import get_metadata
from costy.infrastructure.db.orm import create_tables
from costy.main.web import init_app


@fixture(scope='session')
async def db_url() -> str:  # type: ignore
    try:
        return os.environ['TEST_DB_URL']
    except KeyError:
        pytest.fail("TEST_DB_URL env variable not set")


@fixture(scope='session')
async def db_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url, future=True)


@fixture(scope='session')
async def db_sessionmaker(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(db_engine)


@fixture
async def db_session(db_sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
    session = db_sessionmaker()
    yield session
    # clean up database
    await session.rollback()


@fixture(scope='session')
async def db_tables(db_engine: AsyncEngine) -> AsyncGenerator[None, dict[str, Table]] | None:
    metadata = get_metadata()
    tables = create_tables(metadata)

    try:
        async with db_engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)
    except OperationalError:
        pytest.fail("Connection to database is faield.")

    yield tables

    async with db_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@fixture
async def web_session() -> AsyncIterator[ClientSession]:
    async with AsyncClient() as client:
        yield client


@fixture
async def app(db_url) -> Litestar:
    return init_app(db_url)


@fixture
async def retort() -> Retort:
    return Retort()