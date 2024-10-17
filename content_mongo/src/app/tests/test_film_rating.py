from uuid import uuid4

import pytest
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from app.models import FilmRating
from app.settings.mongodb import settings as mongo_settings


@pytest.mark.asyncio
async def test_create_film_rating():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db, document_models=[FilmRating]
    )

    film_id = uuid4()
    user_id = uuid4()

    film_rating = FilmRating(number=1, film_id=film_id, user_id=user_id)
    await film_rating.insert()

    assert film_rating is not None
    assert film_rating.number == 1
    assert film_rating.film_id == film_id
    assert film_rating.user_id == user_id


@pytest.mark.asyncio
async def test_update_film_rating():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db, document_models=[FilmRating]
    )
    film_id = uuid4()
    user_id = uuid4()

    film_rating = FilmRating(number=1, film_id=film_id, user_id=user_id)
    await film_rating.insert()

    film_rating.number = 9
    await film_rating.save()

    updated_film_rating = await FilmRating.get(film_rating.id)

    assert updated_film_rating.number == 9


@pytest.mark.asyncio
async def test_delete_film_rating():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db, document_models=[FilmRating]
    )

    film_id = uuid4()
    user_id = uuid4()

    film_rating = FilmRating(number=1, film_id=film_id, user_id=user_id)
    await film_rating.insert()

    deleted_film_rating = await FilmRating.get(film_rating.id)

    assert deleted_film_rating is not None

    await deleted_film_rating.delete()

    result = await FilmRating.get(deleted_film_rating.id)

    assert result is None
