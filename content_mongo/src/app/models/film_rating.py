from uuid import UUID

from app.models.base import BaseDocument
from pydantic import Field


class FilmRating(BaseDocument):
    number: int = Field(le=10, ge=0)
    film_id: UUID
    user_id: UUID

    class Settings:
        collection = "rating"
