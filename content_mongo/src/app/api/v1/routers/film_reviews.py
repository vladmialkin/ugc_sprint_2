from beanie import PydanticObjectId
from fastapi import APIRouter, status

from app.api.v1.deps.user import UserData
from app.api.v1.schemas.film_reviews import FilmReviews as FilmReviewsSchema

from app.models import FilmReviews as FilmReviewsDocument
from app.repositories.film_reviews import film_reviews_repository

router = APIRouter()


@router.get(
    "/",
    summary="Список всех комментариев к фильмам",
    description="Список всех комментариев к фильмам",
    response_description="Выводит все комментарии ко всем фильмам",
    response_model=list[FilmReviewsDocument],
)
async def get_all_film_reviews(user: UserData) -> list[FilmReviewsDocument]:
    return await film_reviews_repository.all_list()


@router.get(
    "/{reviews_id}",
    summary="Поиск комментария к фильму по id",
    description="Выводит комментарий к фильму по id",
    response_description="Выводит комментарий к фильму по id",
    response_model=FilmReviewsDocument,
)
async def get_one_film_reviews(
        reviews_id: PydanticObjectId, user: UserData
) -> FilmReviewsDocument:
    return await film_reviews_repository.get(item_id=reviews_id)


@router.post(
    "/",
    summary="Создание комментария к фильму",
    description="Создание комментария к фильму",
    response_description="Создание комментария к фильму",
    response_model=FilmReviewsDocument,
)
async def create_film_reviews(
        data: FilmReviewsSchema, user: UserData
) -> FilmReviewsDocument:
    return await film_reviews_repository.create(data=data)


@router.put(
    "/{reviews_id}",
    summary="Изменение комментария к фильму по id",
    description="Изменение комментария к фильму по id",
    response_description="Изменение комментария к фильму по id",
)
async def update_film_reviews(
        reviews_id: PydanticObjectId, data: FilmReviewsSchema, user: UserData
) -> FilmReviewsDocument:
    return await film_reviews_repository.update(
        item_id=reviews_id, data=data
    )


@router.delete(
    "/{reviews_id}",
    summary="Удаление комментария к фильму по id",
    description="Удаление комментария к фильму по id",
    response_description="Удаление комментария к фильму по id",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_film_reviews(reviews_id: PydanticObjectId, user: UserData):
    await film_reviews_repository.delete(item_id=reviews_id)
