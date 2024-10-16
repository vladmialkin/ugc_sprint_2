from typing import T

from fastapi import HTTPException

from app.models.film_rating import FilmRating
from app.models.film_reviews import FilmReviews
from app.repositories.base import BeanieBaseRepository


class FilmReviewsRepository(BeanieBaseRepository[FilmReviews]):
    async def create(self, data: dict) -> [T]:
        try:
            film_rating = None
            film_rating_id = data.get('film_rating')
            if film_rating_id:
                film_rating = await FilmRating.get(film_rating_id)
                if not film_rating:
                    raise HTTPException(status_code=404, detail=f"DoesNotExist film_rating")
            data.pop('film_rating')
            item = self._collection(film_rating=film_rating, **data)
            await item.insert()
            return item
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating item: {str(e)}")


film_reviews_repository = FilmReviewsRepository(FilmReviews)
