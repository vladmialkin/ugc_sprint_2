import time
import asyncio
from multiprocessing import Process
from uuid import UUID

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker

fake = Faker()

semaphore = asyncio.Semaphore(5)


class FilmBookmarks(Document):
    type: str
    user_id: UUID
    film_id: UUID

    class Settings:
        collection = "film_bookmarks"


async def insert_records(batch_size):
    async with semaphore:
        records = [
            FilmBookmarks(
                type=fake.company(),
                user_id=fake.uuid4(),
                film_id=fake.uuid4(),
            ) for _ in range(batch_size)
        ]
        await FilmBookmarks.insert_many(records)


async def main(total_records, batch_size):
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    await init_beanie(
        database=client.test_db,
        document_models=[FilmBookmarks],
    )

    tasks = []

    start_time = time.time()
    print("Начало загрузки данных")

    for count in range(total_records // batch_size):
        tasks.append(insert_records(batch_size))

    await asyncio.gather(*tasks)

    end_time = time.time()
    print((end_time - start_time) / 60)


def run_async_process(total_records: int, batch_size: int):
    asyncio.run(main(total_records, batch_size))


if __name__ == "__main__":
    total_records = 10_000_000
    batch_size = 5000
    num_process = 5

    processes = []
    for _ in range(num_process):
        process = Process(target=run_async_process, args=(total_records // num_process, batch_size))
        processes.append(process)
        process.start()

    for p in processes:
        p.join()
