import logging
import random
import time
import asyncio
from logging.handlers import RotatingFileHandler
from multiprocessing import Process
from uuid import uuid4, uuid1

from beanie import init_beanie
from bson import Binary
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker

from app.models import FilmBookmarks, FilmReviews, FilmRating

fake = Faker()

semaphore = asyncio.Semaphore(5)

logger = logging.getLogger('etl_application')
logger.setLevel(logging.INFO)

fh = RotatingFileHandler('file.log', maxBytes=20_000_000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s'
)
fh.setFormatter(formatter)
logger.addHandler(fh)


async def insert_records(batch_size, count):
    async with semaphore:
        bookmarks_records = []
        rating_records = []
        reviews_records = []
        for _ in range(batch_size // 3 + 1):
            user_id = uuid1()
            film_id = uuid1()
            rating_id = Binary.from_uuid(uuid4())
            bookmarks = FilmBookmarks(
                type=fake.company(),
                user_id=user_id,
                film_id=film_id,
            )
            bookmarks_records.append(bookmarks)
            rating = FilmRating(
                id=rating_id,
                number=random.randint(0, 10),
                user_id=user_id,
                film_id=film_id,
            )
            rating_records.append(rating)
            reviews = FilmReviews(
                text=fake.text(max_nb_chars=200),
                author_id=film_id,
                film_rating=rating_id,
                draft=bool(random.randint(0, 1))
            )
            reviews_records.append(reviews)

        await FilmBookmarks.insert_many(bookmarks_records)
        await FilmRating.insert_many(rating_records)
        await FilmReviews.insert_many(reviews_records)
        logger.info(f"Добавлено ~{count} данных")


async def main(total_records, batch_size):
    client = AsyncIOMotorClient('mongodb://localhost:27017', uuidRepresentation="standard")
    await init_beanie(
        database=client.test_db,
        document_models=[FilmBookmarks, FilmReviews, FilmRating],
    )

    tasks = []

    start_time = time.time()
    logger.info("Начало загрузки данных")
    for count in range(total_records // batch_size):
        tasks.append(insert_records(batch_size, count * batch_size))

    await asyncio.gather(*tasks)

    end_time = time.time()
    logger.info(f"Затраченное время {(end_time - start_time) / 60} минут")


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
