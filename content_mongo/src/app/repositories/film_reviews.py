from fastapi import Response, HTTPException
from app.models.film_reviews import FilmReviews


class FilmReviewsRepository:

    async def create(self, data):
        try:
            return await FilmReviews(**data.__dict__).insert()
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def get(self, data):
        try:
            return await FilmReviews.get(data)
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def get_all(self):
        try:
            return await FilmReviews.find().to_list()
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def update(self, reviews_id, data):
        reviews = await self.get(data=reviews_id)
        if reviews is None:
            raise HTTPException(status_code=404, detail="Item not found")
        reviews.text = data.text
        reviews.author_id = data.author_id
        reviews.film_rating = data.film_rating
        reviews.draft = data.draft
        return await reviews.save()

    async def delete(self, reviews_id):
        reviews = await self.get(data=reviews_id)
        if reviews is None:
            raise HTTPException(status_code=404, detail="Item not found")
        await reviews.delete()
