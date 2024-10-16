from app.models.film_rating import FilmRating
from app.repositories.base import BeanieBaseRepository


class FilmRatingRepository(BeanieBaseRepository[FilmRating]):
    pass


film_rating_repository = FilmRatingRepository(FilmRating)
