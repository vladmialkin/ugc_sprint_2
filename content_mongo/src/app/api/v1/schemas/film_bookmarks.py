from uuid import UUID

from pydantic import Field

from app.api.v1.schemas.base import Base


class FilmBookmarks(Base):
    type: str | None = Field(None, description="Тип закладки")
    user_id: UUID | None = Field(None, description="ID пользователя")
    film_id: UUID | None = Field(None, description="ID фильма")
