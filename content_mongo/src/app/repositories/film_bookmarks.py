from app.models.film_bookmarks import FilmBookmarks
from app.repositories.base import BeanieBaseRepository


class FilmBookmarksRepository(BeanieBaseRepository[FilmBookmarks]):
    pass


film_bookmarks_repository = FilmBookmarksRepository(FilmBookmarks)
