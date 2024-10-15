from uuid import UUID

from app.api.v1.schemas.base import Base

from app.api.v1.schemas.film_rating import FilmRating


class FilmReviews(Base):
    text: str
    author_id: UUID
    film_rating: FilmRating | None
    draft: bool
