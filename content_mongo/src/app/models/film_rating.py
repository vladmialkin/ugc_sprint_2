from uuid import UUID

from bson import UuidRepresentation
from pydantic import Field

from app.models.base import BaseDocument


class FilmRating(BaseDocument):
    number: int = Field(le=10, ge=0)
    film_id: UUID
    user_id: UUID

    class Settings:
        collection = "rating"
        uuid_representation = UuidRepresentation.STANDARD
