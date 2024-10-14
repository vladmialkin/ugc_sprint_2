from typing import Optional

from aiochclient import ChClient
from aiohttp import ClientSession


client: Optional[ChClient] = None


async def get_async_session() -> ClientSession | None:
    async with ClientSession() as session:
        yield session
