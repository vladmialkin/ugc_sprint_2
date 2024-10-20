from uuid import UUID

from beanie import PydanticObjectId
from pydantic import Field

from app.api.v1.schemas.base import Base


class  FilmReviews(Base):
    text: str | None = Field(None, description="Текст комментария")
    author_id: UUID | None = Field(None, description="Автор комментария")
    film_rating: PydanticObjectId | None = Field(None, description="Рейтинг фильма")
    draft: bool | None = Field(None, description="Черновик")
