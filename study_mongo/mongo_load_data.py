import functools
import logging
import random
import time
import asyncio
from logging.handlers import RotatingFileHandler
from multiprocessing import Process
from uuid import uuid1

from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from faker import Faker

from uuid import UUID

from beanie import Document, Link
from bson import UuidRepresentation
from pydantic import Field


class FilmBookmarks(Document):
    type: str
    user_id: UUID
    film_id: UUID

    class Settings:
        collection = "film_bookmarks"
        indexes = [
            ["user_id"],
            ["film_id"],
        ]


class FilmRating(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    number: int = Field(le=10, ge=0)
    film_id: UUID
    user_id: UUID

    class Settings:
        collection = "rating"
        uuid_representation = UuidRepresentation.STANDARD
        indexes = [
            ["film_id"],
            ["user_id"],
            ["number"],
        ]


class FilmReviews(Document):
    text: str
    author_id: UUID
    film_rating: Link[FilmRating] | None
    draft: bool

    class Settings:
        collection = "reviews"
        uuid_representation = UuidRepresentation.STANDARD
        indexes = [
            ["author_id"],
            ["film_rating"],
        ]


fake = Faker()

semaphore = asyncio.Semaphore(5)

logger = logging.getLogger('load_data_mongodb')
logger.setLevel(logging.INFO)

fh = RotatingFileHandler('file_mongo.log', maxBytes=20_000_000, backupCount=5)
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
async def get_rating_user(rating_collection, user_id: str):
    ratings = await rating_collection.find({"user_id": UUID(user_id)}).to_list(None)
    logger.info(f"Рейтинги пользователя {user_id}: {ratings}")


@timeit
async def get_rating_film(rating_collection, film_id: str, rating: int):
    ratings = await rating_collection.find({"number": rating, "film_id": UUID(film_id)}).to_list(None)
    logger.info(f"Количество полученных элементов фильма {film_id} с рейтингом {rating}: {len(ratings)}")


@timeit
async def get_bookmarks_count(bookmarks_collection):
    bookmarks = await bookmarks_collection.count_documents({})
    logger.info(f"Количество полученных закладок: {bookmarks}")


@timeit
async def get_reviews_user(reviews_collection, user_id: str):
    reviews = await reviews_collection.find({"user_id": UUID(user_id)}).to_list()
    logger.info(f"Получение комментариев пользователя {user_id}: {reviews}")


@timeit
async def get_avg_rating(rating_collection, film_id: str):
    pipeline = [
        {"$match": {"film_id": UUID(film_id)}},
        {"$group": {
            "_id": "$film_id",
            "average_rating": {"$avg": "$number"}
        }},
    ]

    result = await rating_collection.aggregate(pipeline).to_list(None)

    average_rating = result[0]['average_rating'] if result else 0
    logger.info(f"Средний рейтинг фильма {film_id}: {average_rating}")


async def insert_records(batch_size, count):
    async with semaphore:
        bookmarks_records = []
        rating_records = []
        reviews_records = []
        for _ in range(batch_size // 3 + 1):
            user_id = uuid1()
            film_id = uuid1()
            rating_id = PydanticObjectId()
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


async def insert_to_db(total_records, batch_size, **kwargs):
    tasks = []
    logger.info("Начало загрузки данных")
    start_time = time.time()
    for count in range(total_records // batch_size):
        tasks.append(insert_records(batch_size, count * batch_size))
        tasks.append(get_rating_user(kwargs["rating_collection"], user_id="be771ab0-8ec0-11ef-bab2-7c70db5559dd"))

        tasks.append(
            get_rating_film(kwargs["rating_collection"], rating=4, film_id="be771ab0-8ec0-11ef-bab2-7c70db5559dd"))

        tasks.append(get_bookmarks_count(kwargs["bookmarks_collection"]))

        tasks.append(get_avg_rating(kwargs["rating_collection"], film_id="be771ab0-8ec0-11ef-bab2-7c70db5559dd"))

    await asyncio.gather(*tasks)
    logger.info(f"Затраченное время {(time.time() - start_time) / 60} минут")


async def main(total_records, batch_size):
    client = AsyncIOMotorClient('mongodb://localhost:27017', uuidRepresentation="standard")
    await init_beanie(
        database=client.test_db,
        document_models=[FilmBookmarks, FilmReviews, FilmRating],
    )

    rating_collection = client.test_db.FilmRating
    bookmarks_collection = client.test_db.FilmBookmarks

    # await insert_to_db(total_records, batch_size, rating_collection=rating_collection,
    #                    bookmarks_collection=bookmarks_collection, reviews_collection=reviews_collection)

    tasks = []
    tasks.append(get_rating_user(rating_collection, user_id="be771ab0-8ec0-11ef-bab2-7c70db5559dd"))

    tasks.append(
        get_rating_film(rating_collection, rating=4, film_id="be771ab0-8ec0-11ef-bab2-7c70db5559dd"))

    tasks.append(get_bookmarks_count(bookmarks_collection))

    tasks.append(get_avg_rating(rating_collection, film_id="be771ab0-8ec0-11ef-bab2-7c70db5559dd"))

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
