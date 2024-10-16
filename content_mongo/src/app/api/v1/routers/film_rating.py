from uuid import UUID

from fastapi import APIRouter

from app.api.v1.deps.user import UserData
from app.api.v1.schemas.film_rating import FilmRating as FilmRatingSchema
from app.repositories.film_rating import film_rating_repository

router = APIRouter()


@router.get(
    "/",
    summary='Список всех рейтингов фильмов',
    description='Список всех рейтингов фильмов',
    response_description='Выводит все рейтинги всех фильмов',
    response_model=list[FilmRatingSchema]
)
async def get_all_film_rating(user: UserData) -> list[FilmRatingSchema]:
    return await film_rating_repository.all_list()


@router.get(
    "/{rating_id}",
    summary='Поиск рейтинга фильмов по id',
    description='Выводит рейтинг фильмов по id',
    response_description='Выводит рейтинг фильмов по id',
    response_model=FilmRatingSchema
)
async def get_one_film_rating(rating_id: UUID, user: UserData) -> FilmRatingSchema:
    return await film_rating_repository.get(id=rating_id)


@router.post(
    "/",
    summary='Создание рейтинга фильмов',
    description='Создание рейтинга фильмов',
    response_description='Создание рейтинга фильмов',
    response_model=FilmRatingSchema,
)
async def create_film_rating(data: FilmRatingSchema, user: UserData) -> FilmRatingSchema:
    return await film_rating_repository.create(data=dict(data))


@router.put(
    "/{rating_id}",
    summary='Изменение рейтинга фильмов по id',
    description='Изменение рейтинга фильмов по id',
    response_description='Изменение рейтинга фильмов по id'
)
async def update_film_rating(rating_id: UUID, data: FilmRatingSchema, user: UserData) -> FilmRatingSchema:
    return await film_rating_repository.update(item_id=rating_id, data=dict(data))


@router.delete(
    "/{rating_id}",
    summary='Удаление рейтинга фильмов по id',
    description='Удаление рейтинга фильмов по id',
    response_description='Удаление рейтинга фильмов по id'
)
async def delete_film_rating(rating_id: UUID, user: UserData):
    await film_rating_repository.delete(item_id=rating_id)
    return f"Рейтинг с id {rating_id} удалён."


@router.get(
    "/filter",
    summary='Фильтр рейтинга фильмов',
    description='Позволяет фильтровать рейтинг фильмов по заданным параметрам',
    response_model=list[FilmRatingSchema]
)
async def filter_film_rating(filters: FilmRatingSchema, user: UserData) -> list[FilmRatingSchema]:
    return await film_rating_repository.filter(dict(filters))