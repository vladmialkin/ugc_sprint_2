from uuid import UUID

from beanie import Document, Link
from bson import UuidRepresentation
from pydantic import Field


class FilmBookmarks(Document):
    type: str
    user_id: UUID
    film_id: UUID

    class Settings:
        collection = "film_bookmarks"


class FilmRating(Document):
    number: int = Field(le=10, ge=0)
    film_id: UUID
    user_id: UUID

    class Settings:
        collection = "rating"
        uuid_representation = UuidRepresentation.STANDARD


class FilmReviews(Document):
    text: str
    author_id: UUID
    film_rating: Link[FilmRating] | None
    draft: bool

    class Settings:
        collection = "reviews"
        uuid_representation = UuidRepresentation.STANDARD
