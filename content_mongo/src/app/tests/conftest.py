import pytest
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from app.models import FilmBookmarks, FilmRating, FilmReviews
from app.settings.mongodb import settings as mongo_settings


@pytest.fixture(scope="session")
async def beanie_db():
    mongo_client = AsyncMongoMockClient(
        str(mongo_settings.DSN), connectTimeoutMS=250
    )
    await init_beanie(
        database=mongo_client.test_db,
        document_models=[FilmRating, FilmReviews, FilmBookmarks],
    )
    return
