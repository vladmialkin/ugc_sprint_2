from fastapi import Response, HTTPException
from app.models.film_bookmarks import FilmBookmarks


class FilmBookmarksRepository:

    async def create(self, data):
        try:
            return await FilmBookmarks(**data.__dict__).insert()
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def get(self, data):
        try:
            return await FilmBookmarks.get(data)
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def get_all(self):
        try:
            return await FilmBookmarks.find().to_list()
        except Exception as e:
            print(e)
            return Response(status_code=404, content="Ошибка")

    async def update(self, bookmark_id, data):
        bookmark = await self.get(data=bookmark_id)
        if bookmark is None:
            raise HTTPException(status_code=404, detail="Item not found")
        bookmark.type = data.type
        bookmark.user_id = data.user_id
        bookmark.film_id = data.film_id
        return await bookmark.save()

    async def delete(self, bookmark_id):
        bookmark = await self.get(data=bookmark_id)
        if bookmark is None:
            raise HTTPException(status_code=404, detail="Item not found")
        await bookmark.delete()
