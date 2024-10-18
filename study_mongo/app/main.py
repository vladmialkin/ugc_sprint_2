import functools
import logging
import random
import time
import asyncio
from logging.handlers import RotatingFileHandler
from multiprocessing import Process
from uuid import uuid4, uuid1, UUID

from beanie import init_beanie
from bson import Binary
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker

from app.models import FilmBookmarks, FilmReviews, FilmRating

fake = Faker()

semaphore = asyncio.Semaphore(5)

logger = logging.getLogger('load_data_mongodb')
logger.setLevel(logging.INFO)

fh = RotatingFileHandler('file.log', maxBytes=20_000_000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s'
)
fh.setFormatter(formatter)
logger.addHandler(fh)


def timeit(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"Функция {func.__name__} выполнена за {elapsed_time:.4f} секунд")
        return result

    return wrapper


@timeit
async def get_rating_user(user_id: UUID):
    ratings = await FilmRating.find(FilmRating.user_id == user_id).to_list()
    logger.info(f"Рейтинги пользователя {user_id}: {ratings}")


@timeit
async def get_rating_film(rating: int):
    ratings = await FilmRating.find(FilmRating.number == rating).to_list()
    logger.info(f"Количество полученных элементов с рейтингом {rating}: {len(ratings)}")


@timeit
async def get_bookmarks_list():
    bookmarks = await FilmRating.find().to_list()
    logger.info(f"Количество полученных закладок: {len(bookmarks)}")


@timeit
async def get_avg_rating(film_id: str):
    average_rating = await FilmRating.find(FilmRating.film_id == film_id).avg(FilmRating.number) or 0
    logger.info(f"Средний рейтинг фильма {film_id}: {average_rating}")


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


async def insert_to_db(total_records, batch_size):
    tasks = []
    logger.info("Начало загрузки данных")
    start_time = time.time()
    for count in range(total_records // batch_size):
        tasks.append(insert_records(batch_size, count * batch_size))

    await asyncio.gather(*tasks)
    logger.info(f"Затраченное время {(time.time() - start_time) / 60} минут")


async def main(total_records, batch_size):
    client = AsyncIOMotorClient('mongodb://localhost:27017', uuidRepresentation="standard")
    await init_beanie(
        database=client.test_db,
        document_models=[FilmBookmarks, FilmReviews, FilmRating],
    )

    # await insert_to_db(total_records, batch_size)

    tasks = []

    tasks.append(get_rating_user(user_id=UUID("f1fa9b48-8d33-11ef-a341-7c70db5559dd")))

    tasks.append(get_rating_film(rating=4))

    tasks.append(get_bookmarks_list())

    tasks.append(get_avg_rating(film_id="9b5104d8-8d49-11ef-ad95-7c70db5559dd"))
    await asyncio.gather(*tasks)


def run_async_process(total_records: int, batch_size: int):
    asyncio.run(main(total_records, batch_size))


def run_multiprocessing(total_records, batch_size, num_process):
    processes = []
    for _ in range(num_process):
        process = Process(target=run_async_process, args=(total_records // num_process, batch_size))
        processes.append(process)
        process.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    total_records = 10_000_000
    batch_size = 5000
    num_process = 5
    run_async_process(total_records, batch_size)
    # run_multiprocessing(total_records, batch_size, num_process)
