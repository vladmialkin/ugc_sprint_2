from uuid import UUID

from app.models.base import BaseDocument

from app.models.film_rating import FilmRating


class FilmReviews(BaseDocument):
    text: str
    author_id: UUID
    film_rating: FilmRating | None
    draft: bool

    class Settings:
        collection = "reviews"