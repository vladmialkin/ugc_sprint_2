from uuid import UUID

from app.api.v1.schemas.base import Base
from pydantic import Field


class FilmRating(Base):
    number: int = Field(le=10, ge=0)
    film_id: UUID
    user_id: UUID
