from fastapi import APIRouter, status

from app.api.v1.deps.user import UserData
from beanie import PydanticObjectId
from app.models import FilmRating as FilmRatingDocument
from app.repositories.film_rating import film_rating_repository

router = APIRouter()


@router.get(
    "/",
    summary="Список всех рейтингов фильмов",
    description="Список всех рейтингов фильмов",
    response_description="Выводит все рейтинги всех фильмов",
    response_model=list[FilmRatingDocument],
)
async def get_all_film_rating(user: UserData) -> list[FilmRatingDocument]:
    return await film_rating_repository.all_list()


@router.get(
    "/{rating_id}",
    summary="Поиск рейтинга фильмов по id",
    description="Выводит рейтинг фильмов по id",
    response_description="Выводит рейтинг фильмов по id",
    response_model=FilmRatingDocument,
)
async def get_one_film_rating(
        rating_id: PydanticObjectId, user: UserData
) -> FilmRatingDocument:
    return await film_rating_repository.get(item_id=rating_id)


@router.post(
    "/",
    summary="Создание рейтинга фильмов",
    description="Создание рейтинга фильмов",
    response_description="Создание рейтинга фильмов",
    response_model=FilmRatingDocument,
)
async def create_film_rating(data: FilmRatingDocument, user: UserData) -> FilmRatingDocument:
    return await film_rating_repository.create(data=dict(data))


@router.put(
    "/{rating_id}",
    summary="Изменение рейтинга фильмов по id",
    description="Изменение рейтинга фильмов по id",
    response_description="Изменение рейтинга фильмов по id",
    response_model=FilmRatingDocument
)
async def update_film_rating(
        rating_id: PydanticObjectId, data: FilmRatingDocument, user: UserData
) -> FilmRatingDocument:
    return await film_rating_repository.update(
        item_id=rating_id, data=dict(data)
    )


@router.delete(
    "/{rating_id}",
    summary="Удаление рейтинга фильмов по id",
    description="Удаление рейтинга фильмов по id",
    response_description="Удаление рейтинга фильмов по id",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_film_rating(rating_id: PydanticObjectId, user: UserData):
    await film_rating_repository.delete(item_id=rating_id)
