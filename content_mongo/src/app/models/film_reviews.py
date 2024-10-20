from uuid import UUID

from beanie import Link
from bson import UuidRepresentation

from app.models.base import BaseDocument
from app.models.film_rating import FilmRating


class FilmReviews(BaseDocument):
    text: str
    author_id: UUID
    film_rating: Link[FilmRating] | None
    draft: bool

    class Settings:
        collection = "reviews"
        uuid_representation = UuidRepresentation.STANDARD
