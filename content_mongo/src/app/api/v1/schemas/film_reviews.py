from uuid import UUID

from app.api.v1.schemas.base import Base


class FilmReviews(Base):
    text: str
    author_id: UUID
    film_rating: UUID
    draft: bool
