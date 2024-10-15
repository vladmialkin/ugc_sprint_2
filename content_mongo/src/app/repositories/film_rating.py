from fastapi import Response, HTTPException
from app.models.film_rating import FilmRating


class FilmRatingRepository:

    async def create(self, data):
        try:
            return await FilmRating(**data.__dict__).insert()
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def get(self, data):
        try:
            return await FilmRating.get(data)
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def get_all(self):
        try:
            return await FilmRating.find().to_list()
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def update(self, rating_id, data):
        rating = await self.get(data=rating_id)
        if rating is None:
            raise HTTPException(status_code=404, detail="Item not found")
        rating.number = data.number
        rating.film_id = data.film_id
        rating.user_id = data.user_id
        return await rating.save()

    async def delete(self, rating_id):
        rating = await self.get(data=rating_id)
        if rating is None:
            raise HTTPException(status_code=404, detail="Item not found")
        await rating.delete()
