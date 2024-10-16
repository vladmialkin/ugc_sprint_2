from app.models.film_reviews import FilmReviews
from app.repositories.base import BeanieBaseRepository


class FilmReviewsRepository(BeanieBaseRepository[FilmReviews]):
    pass


film_reviews_repository = FilmReviewsRepository(FilmReviews)
