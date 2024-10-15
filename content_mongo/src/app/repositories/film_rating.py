from fastapi import Response
from app.models.film_rating import FilmRating


class FilmRatingRepository:

    async def create(self, data):
        try:
            await FilmRating(**data.__dict__).insert()
            return "Документ создан"
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def get(self, data):
        try:
            return await FilmRating.get(data)
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")
