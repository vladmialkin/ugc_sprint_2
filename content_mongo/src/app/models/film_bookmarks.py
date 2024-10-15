from uuid import UUID

from app.models.base import BaseDocument


class FilmBookmarks(BaseDocument):
    type: str
    user_id: UUID
    film_id: UUID

    class Settings:
        collection = "bookmarks"
