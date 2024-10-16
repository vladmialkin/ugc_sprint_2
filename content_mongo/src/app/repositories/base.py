from typing import TypeVar, List
from uuid import UUID

from fastapi import HTTPException

from app.models.base import BaseDocument

T = TypeVar("T", bound=BaseDocument)


class BeanieBaseRepository[T]:
    def __init__(self, collection: type[T]) -> None:
        self._collection = collection

    async def exists(self, **attrs) -> bool:
        try:
            return await self._collection.find_one(**attrs) is not None
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def all_list(self) -> list[T]:
        try:
            return await self._collection.find_all().to_list()
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def get(self, item_id) -> T | None:
        try:
            return await self._collection.get(item_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def create(self, data: dict) -> T:
        try:
            item = self._collection(**data)
            await item.insert()
            return item
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating item: {str(e)}")

    async def update(self, item_id: UUID, data: dict) -> T | None:
        try:
            existing_item = await self._collection.get(item_id)
            if existing_item:
                updated_item = existing_item.copy(update=data)
                await updated_item.save()
                return updated_item
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error updating item: {str(e)}")

    async def delete(self, item_id: UUID) -> bool:
        try:
            existing_item = await self._collection.get(item_id)
            if existing_item:
                await existing_item.delete()
                return True
            else:
                raise HTTPException(status_code=404, detail="Item not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def filter(self, attrs) -> List[T]:
        try:
            return await self._collection.find(**attrs).to_list()
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
