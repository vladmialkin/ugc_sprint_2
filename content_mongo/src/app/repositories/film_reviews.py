from typing import T

from fastapi import HTTPException
from beanie import PydanticObjectId

from app.models.film_rating import FilmRating
from app.models.film_reviews import FilmReviews
from app.repositories.base import BeanieBaseRepository


class FilmReviewsRepository(BeanieBaseRepository[FilmReviews]):
    async def create(self, data) -> [T]:
        try:
            if data.film_rating:
                film_rating = await FilmRating.get(data.film_rating)
                if not film_rating:
                    raise HTTPException(
                        status_code=404, detail="DoesNotExist film_rating"
                    )
            item = self._collection(**dict(data))
            await item.insert()
            return item
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error creating item: {str(e)}"
            )

    async def update(self, item_id: PydanticObjectId, data: T) -> [T]:
        try:
            existing_item = await self._collection.get(item_id)
            if existing_item:
                film_rating = await FilmRating.get(data.film_rating)
                if not film_rating:
                    raise HTTPException(status_code=404, detail="FilmRating item not found")
                data.film_rating = film_rating
                updated_item = existing_item.copy(update=dict(data))
                await updated_item.save()
                return updated_item
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error updating item: {str(e)}"
            )


film_reviews_repository = FilmReviewsRepository(FilmReviews)
