from fastapi import APIRouter, status

from app.models import FilmBookmarks as FilmBookmarksDocument
from beanie import PydanticObjectId

from app.api.v1.deps.user import UserData
from app.repositories.film_bookmarks import film_bookmarks_repository

router = APIRouter()


@router.get(
    "/",
    summary="Список всех закладок фильмов",
    description="Список всех закладок фильмов",
    response_description="Выводит все закладки фильмов",
    response_model=list[FilmBookmarksDocument],
)
async def get_all_film_bookmarks(user: UserData) -> list[FilmBookmarksDocument]:
    return await film_bookmarks_repository.all_list()


@router.get(
    "/{bookmarks_id}",
    summary="Поиск закладок фильмов по id",
    description="Выводит закладки фильмов по id",
    response_description="Выводит закладок фильмов по id",
    response_model=FilmBookmarksDocument,
)
async def get_one_film_bookmarks(
        bookmark_id: PydanticObjectId, user: UserData
) -> FilmBookmarksDocument:
    return await film_bookmarks_repository.get(item_id=bookmark_id)


@router.post(
    "/",
    summary="Создание закладок фильмов",
    description="Создание закладок фильмов",
    response_description="Создание закладок фильмов",
    response_model=FilmBookmarksDocument,
)
async def create_film_bookmarks(
        data: FilmBookmarksDocument, user: UserData
) -> FilmBookmarksDocument:
    return await film_bookmarks_repository.create(data=dict(data))


@router.put(
    "/{bookmarks_id}",
    summary="Изменение закладок фильмов по id",
    description="Изменение закладок фильмов по id",
    response_description="Изменение закладок фильмов по id",
    response_model=FilmBookmarksDocument
)
async def update_film_bookmarks(
        bookmark_id: PydanticObjectId, data: FilmBookmarksDocument, user: UserData
) -> FilmBookmarksDocument:
    return await film_bookmarks_repository.update(
        item_id=bookmark_id, data=dict(data)
    )


@router.delete(
    "/{bookmarks_id}",
    summary="Удаление закладок фильмов по id",
    description="Удаление закладок фильмов по id",
    response_description="Удаление закладок фильмов по id",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_film_bookmarks(bookmark_id: PydanticObjectId, user: UserData):
    await film_bookmarks_repository.delete(item_id=bookmark_id)
