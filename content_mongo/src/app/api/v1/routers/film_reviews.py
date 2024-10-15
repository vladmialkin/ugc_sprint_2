from uuid import UUID

from fastapi import APIRouter

from app.api.v1.deps.user import UserData
from app.api.v1.schemas.film_reviews import FilmReviews as FilmReviewsSchema
from app.repositories.film_reviews import FilmReviewsRepository

router = APIRouter()


@router.get(
    "/",
    summary='Список всех комментариев к фильмам',
    description='Список всех комментариев к фильмам',
    response_description='Выводит все комментарии ко всем фильмам',
    response_model=list[FilmReviewsSchema]
)
async def get_all_film_reviews(user: UserData) -> list[FilmReviewsSchema]:
    return await FilmReviewsRepository().get_all()


@router.get(
    "/{reviews_id}",
    summary='Поиск рейтинга фильмов по id',
    description='Выводит рейтинг фильмов по id',
    response_description='Выводит рейтинг фильмов по id',
    response_model=FilmReviewsSchema
)
async def get_one_film_reviews(reviews_id: UUID, user: UserData) -> FilmReviewsSchema:
    return await FilmReviewsRepository().get(data=reviews_id)


@router.post(
    "/",
    summary='Создание комментария к фильму',
    description='Создание комментария к фильму',
    response_description='Создание комментария к фильму',
    response_model=FilmReviewsSchema,
)
async def create_film_reviews(data: FilmReviewsSchema, user: UserData) -> FilmReviewsSchema:
    return await FilmReviewsRepository().create(data=data)


@router.put(
    "/{reviews_id}",
    summary='Изменение комментария к фильму по id',
    description='Изменение комментария к фильму по id',
    response_description='Изменение комментария к фильму по id'
)
async def update_film_reviews(reviews_id: UUID, data: FilmReviewsSchema, user: UserData) -> FilmReviewsSchema:
    return await FilmReviewsRepository().update(reviews_id=reviews_id, data=data)


@router.delete(
    "/{reviews_id}",
    summary='Удаление комментария к фильму по id',
    description='Удаление комментария к фильму по id',
    response_description='Удаление комментария к фильму по id'
)
async def delete_film_reviews(reviews_id: UUID, user: UserData):
    await FilmReviewsRepository().delete(reviews_id=reviews_id)
    return f"Комментарий к фильму с id {reviews_id} удалён."
