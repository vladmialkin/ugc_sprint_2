from uuid import UUID

from bson import UuidRepresentation, Binary

from app.models.base import BaseDocument
from app.models.film_rating import FilmRating
from beanie import Link


class FilmReviews(BaseDocument):
    text: str
    author_id: UUID
    film_rating: Link[FilmRating] | None
    draft: bool

    class Settings:
        collection = "reviews"
