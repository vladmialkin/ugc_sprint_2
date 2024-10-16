from uuid import UUID

from fastapi import APIRouter

from app.api.v1.deps.user import UserData
from app.api.v1.schemas.film_bookmarks import FilmBookmarks as FilmBookmarksSchema
from app.repositories.film_bookmarks import film_bookmarks_repository

router = APIRouter()


@router.get(
    "/",
    summary='Список всех закладок фильмов',
    description='Список всех закладок фильмов',
    response_description='Выводит все закладки фильмов',
    response_model=list[FilmBookmarksSchema]
)
async def get_all_film_bookmarks(user: UserData) -> list[FilmBookmarksSchema]:
    return await film_bookmarks_repository.all_list()


@router.get(
    "/{bookmarks_id}",
    summary='Поиск закладок фильмов по id',
    description='Выводит закладки фильмов по id',
    response_description='Выводит закладок фильмов по id',
    response_model=FilmBookmarksSchema
)
async def get_one_film_bookmarks(bookmark_id: UUID, user: UserData) -> FilmBookmarksSchema:
    return await film_bookmarks_repository.get(id=bookmark_id)


@router.post(
    "/",
    summary='Создание закладок фильмов',
    description='Создание закладок фильмов',
    response_description='Создание закладок фильмов',
    response_model=FilmBookmarksSchema,
)
async def create_film_bookmarks(data: FilmBookmarksSchema, user: UserData) -> FilmBookmarksSchema:
    return await film_bookmarks_repository.create(data=dict(data))


@router.put(
    "/{bookmarks_id}",
    summary='Изменение закладок фильмов по id',
    description='Изменение закладок фильмов по id',
    response_description='Изменение закладок фильмов по id'
)
async def update_film_bookmarks(bookmark_id: UUID, data: FilmBookmarksSchema, user: UserData) -> FilmBookmarksSchema:
    return await film_bookmarks_repository.update(item_id=bookmark_id, data=dict(data))


@router.delete(
    "/{bookmarks_id}",
    summary='Удаление закладок фильмов по id',
    description='Удаление закладок фильмов по id',
    response_description='Удаление закладок фильмов по id'
)
async def delete_film_bookmarks(bookmark_id: UUID, user: UserData):
    await film_bookmarks_repository.delete(item_id=bookmark_id)
    return f"Закладки фильмов с id {bookmark_id} удалёны."


@router.get(
    "/filter",
    summary='Фильтр закладок фильмов',
    description='Позволяет фильтровать закладки фильмов по заданным параметрам',
    response_model=list[FilmBookmarksSchema]
)
async def filter_film_rating(filters: FilmBookmarksSchema, user: UserData) -> list[FilmBookmarksSchema]:
    return await film_bookmarks_repository.filter(dict(filters))
