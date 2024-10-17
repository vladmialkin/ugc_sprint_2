from uuid import uuid4

import pytest
from beanie import WriteRules, init_beanie
from mongomock_motor import AsyncMongoMockClient

from app.models import FilmRating, FilmReviews
from app.settings.mongodb import settings as mongo_settings


@pytest.mark.asyncio
async def test_create_film_reviews():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db,
        document_models=[FilmReviews, FilmRating],
    )

    film_id = uuid4()
    author_id = uuid4()

    film_rating = FilmRating(number=1, film_id=film_id, user_id=author_id)

    assert film_rating is not None

    film_reviews = FilmReviews(
        text="Текст комментария",
        film_rating=film_rating,
        author_id=author_id,
        draft=True,
    )
    await film_reviews.insert(link_rule=WriteRules.WRITE)

    assert film_reviews is not None
    assert film_rating.text == "Текст комментария"
    assert film_rating.film_rating == film_rating
    assert film_rating.author_id == author_id
    assert film_rating.draft == True


@pytest.mark.asyncio
async def test_create_film_reviews():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db,
        document_models=[FilmReviews, FilmRating],
    )

    film_id = uuid4()
    author_id = uuid4()

    film_rating = FilmRating(number=1, film_id=film_id, user_id=author_id)

    await film_rating.insert()

    assert film_rating is not None

    film_reviews = FilmReviews(
        text="Текст комментария",
        film_rating=film_rating,
        author_id=author_id,
        draft=True,
    )
    await film_reviews.insert(link_rule=WriteRules.WRITE)

    film_reviews.text = "Новый текст"
    await film_reviews.save()

    updated_film_reviews = await FilmReviews.get(film_reviews.id)

    assert updated_film_reviews.text == "Новый текст"


@pytest.mark.asyncio
async def test_delete_film_reviews():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db,
        document_models=[FilmReviews, FilmRating],
    )

    film_id = uuid4()
    author_id = uuid4()

    film_rating = FilmRating(number=1, film_id=film_id, user_id=author_id)

    assert film_rating is not None

    await film_rating.insert()

    film_reviews = FilmReviews(
        text="Текст комментария",
        film_rating=film_rating,
        author_id=author_id,
        draft=True,
    )
    await film_reviews.insert(link_rule=WriteRules.WRITE)

    deleted_film_reviews = await FilmReviews.get(film_reviews.id)

    assert deleted_film_reviews is not None

    await deleted_film_reviews.delete()

    result = await FilmReviews.get(deleted_film_reviews.id)

    assert result is None
