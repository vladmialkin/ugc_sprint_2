from uuid import uuid4

import pytest
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from app.models import FilmBookmarks
from app.settings.mongodb import settings as mongo_settings


@pytest.mark.asyncio
async def test_create_film_bookmarks():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db, document_models=[FilmBookmarks]
    )

    film_id = uuid4()
    user_id = uuid4()

    film_bookmarks = FilmBookmarks(
        type="Посмотреть позже", film_id=film_id, user_id=user_id
    )
    await film_bookmarks.insert()

    assert film_bookmarks is not None
    assert film_bookmarks.type == "Посмотреть позже"
    assert film_bookmarks.film_id == film_id
    assert film_bookmarks.user_id == user_id


@pytest.mark.asyncio
async def test_update_film_bookmarks():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db, document_models=[FilmBookmarks]
    )
    film_id = uuid4()
    user_id = uuid4()

    film_bookmarks = FilmBookmarks(
        type="Посмотреть позже", film_id=film_id, user_id=user_id
    )
    await film_bookmarks.insert()

    film_bookmarks.type = "Шедевры"
    await film_bookmarks.save()

    updated_film_bookmarks = await FilmBookmarks.get(film_bookmarks.id)

    assert updated_film_bookmarks.type == "Шедевры"


@pytest.mark.asyncio
async def test_delete_film_bookmarks():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db, document_models=[FilmBookmarks]
    )

    film_id = uuid4()
    user_id = uuid4()

    film_bookmarks = FilmBookmarks(
        type="Посмотреть позже", film_id=film_id, user_id=user_id
    )
    await film_bookmarks.insert()

    deleted_film_bookmarks = await FilmBookmarks.get(film_bookmarks.id)

    assert deleted_film_bookmarks is not None

    await deleted_film_bookmarks.delete()

    result = await FilmBookmarks.get(deleted_film_bookmarks.id)

    assert result is None
