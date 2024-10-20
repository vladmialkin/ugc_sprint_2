from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from app.api import v1_router
from app.models.film_bookmarks import FilmBookmarks
from app.models.film_rating import FilmRating
from app.models.film_reviews import FilmReviews
from app.settings.api import settings as api_settings
from app.settings.mongodb import settings as mongo_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    client = AsyncIOMotorClient(mongo_settings.DSN)
    await init_beanie(
        database=client.test,
        document_models=[FilmRating, FilmReviews, FilmBookmarks],
    )
    yield
    client.close()


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=api_settings.OPENAPI_URL,
    docs_url=api_settings.DOCS_URL,
    redoc_url=api_settings.REDOC_URL,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(v1_router)
