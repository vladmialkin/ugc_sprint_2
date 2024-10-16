from uuid import UUID

from app.api.v1.schemas.base import Base
from pydantic import Field


class FilmRating(Base):
    number: int | None = Field(le=10, ge=0, description="Оценка")
    film_id: UUID | None = Field(None, description="ID фильма")
    user_id: UUID | None = Field(None, description="ID пользователя")
