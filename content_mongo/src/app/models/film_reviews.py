from uuid import UUID

from app.models.base import BaseDocument


class FilmReviews(BaseDocument):
    text: str
    author_id: UUID
    film_rating: UUID
    draft: bool

    class Settings:
        collection = "reviews"
