from uuid import UUID

from app.api.v1.schemas.base import Base


class FilmBookmarks(Base):
    type: str
    user_id: UUID
    film_id: UUID
