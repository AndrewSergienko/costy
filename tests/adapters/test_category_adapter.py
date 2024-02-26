import pytest
from pytest_asyncio import fixture
from sqlalchemy import insert

from costy.adapters.db.category_gateway import CategoryGateway
from costy.domain.models.category import Category, CategoryType
from costy.domain.models.user import UserId


@fixture
async def category_gateway(db_session, db_tables, retort) -> CategoryGateway:
    return CategoryGateway(db_session, db_tables["categories"], retort)


@fixture()
async def db_user_id(db_session, db_tables) -> UserId:
    created_user_record = await db_session.execute(insert(db_tables["users"]).values(auth_id="test"))
    return UserId(created_user_record.inserted_primary_key[0])


@pytest.mark.asyncio
async def test_save_category(category_gateway, db_session, db_tables, db_user_id):
    general_category = Category(id=None, name="general category")
    personal_category = Category(id=None, name="user category", user_id=db_user_id, kind=CategoryType.PERSONAL.value)

    await category_gateway.save_category(general_category)
    await category_gateway.save_category(personal_category)

    assert general_category.id is not None
    assert personal_category.id is not None


@pytest.mark.asyncio
async def test_get_category(category_gateway, db_session, db_tables, db_user_id):
    general_category = Category(id=None, name="general category")
    personal_category = Category(id=None, name="user category", user_id=db_user_id, kind=CategoryType.PERSONAL.value)
    await category_gateway.save_category(general_category)
    await category_gateway.save_category(personal_category)

    created_general_category = await category_gateway.get_category(general_category.id)
    created_personal_category = await category_gateway.get_category(personal_category.id)

    assert general_category == created_general_category
    assert personal_category == created_personal_category


@pytest.mark.asyncio
async def test_delete_category(category_gateway, db_session, db_tables, db_user_id):
    general_category = Category(id=None, name="general category")
    personal_category = Category(id=None, name="user category", user_id=db_user_id, kind=CategoryType.PERSONAL.value)
    await category_gateway.save_category(general_category)
    await category_gateway.save_category(personal_category)

    await category_gateway.delete_category(general_category.id)
    await category_gateway.delete_category(personal_category.id)

    assert await category_gateway.get_category(general_category.id) is None
    assert await category_gateway.get_category(personal_category.id) is None


@pytest.mark.asyncio
async def test_find_categories(category_gateway, db_session, db_tables, db_user_id):
    created_categories = []
    for i in range(5):
        category = Category(
            id=None,
            name=f"category {i}",
            user_id=db_user_id,
        )
        await category_gateway.save_category(category)
        created_categories.append(category)

    categories = await category_gateway.find_categories(db_user_id)

    assert categories == created_categories
