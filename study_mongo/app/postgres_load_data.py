import functools
import logging
import random
import time
import asyncio
from logging.handlers import RotatingFileHandler
from multiprocessing import Process
from uuid import uuid1, UUID

from sqlalchemy import (create_engine, Column, Integer, String, ForeignKey, Text, select, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from faker import Faker

fake = Faker()

semaphore = asyncio.Semaphore(5)

logger = logging.getLogger('load_data_postgres')
logger.setLevel(logging.INFO)

fh = RotatingFileHandler('file_postgres.log', maxBytes=20_000_000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s'
)
fh.setFormatter(formatter)
logger.addHandler(fh)

Base = declarative_base()


class FilmBookmarks(Base):
    __tablename__ = 'film_bookmarks'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    user_id = Column(String(36))
    film_id = Column(String(36))


class FilmRating(Base):
    __tablename__ = 'film_ratings'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    user_id = Column(String(36))
    film_id = Column(String(36))


class FilmReviews(Base):
    __tablename__ = 'film_reviews'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    author_id = Column(String(36))
    film_rating_id = Column(Integer, ForeignKey('film_ratings.id'))
    draft = Column(Integer)


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
async def get_rating_user(session: AsyncSession, user_id: str):
    query = select(FilmRating).where(FilmRating.user_id == user_id)
    result = await session.execute(query)
    ratings = result.scalars().all()
    logger.info(f"Рейтинги пользователя {user_id}: {ratings}")


@timeit
async def get_rating_film(session: AsyncSession, rating: int):
    result = await session.execute(select(FilmRating).where(FilmRating.number == rating))
    ratings = result.scalars().all()
    logger.info(f"Количество полученных элементов с рейтингом {rating}: {len(ratings)}")


@timeit
async def get_bookmarks_list(session: AsyncSession):
    result = await session.execute(select(FilmBookmarks))
    bookmarks = result.scalars().all()
    logger.info(f"Количество полученных закладок: {len(bookmarks)}")


@timeit
async def get_avg_rating(session: AsyncSession, film_id: UUID):
    result = await session.execute(select(func.avg(FilmRating.number)).where(FilmRating.film_id == str(film_id)))
    average_rating = result.scalar() or 0
    logger.info(f"Средний рейтинг фильма {film_id}: {average_rating}")


async def insert_records(session: AsyncSession, batch_size):
    async with semaphore:
        bookmarks_records = []
        rating_records = []
        reviews_records = []

        for _ in range(batch_size // 3 + 1):
            user_id = str(uuid1())
            film_id = str(uuid1())

            bookmarks = FilmBookmarks(
                type=fake.company(),
                user_id=user_id,
                film_id=film_id
            )
            bookmarks_records.append(bookmarks)

            rating = FilmRating(
                number=random.randint(0, 10),
                user_id=user_id,
                film_id=film_id
            )
            rating_records.append(rating)

            reviews = FilmReviews(
                text=fake.text(max_nb_chars=200),
                author_id=film_id,
                draft=bool(random.randint(0, 1))
            )
            reviews_records.append(reviews)

        session.add_all(bookmarks_records)
        session.add_all(rating_records)
        session.add_all(reviews_records)

        await session.commit()
        logger.info(
            f"Добавлено ~{len(bookmarks_records)} закладок, {len(rating_records)} рейтингов и {len(reviews_records)} рецензий")


async def insert_to_db(session: AsyncSession, total_records, batch_size):
    logger.info("Начало загрузки данных")
    start_time = time.time()

    for _ in range(total_records // batch_size):
        await insert_records(session, batch_size)

    logger.info(f"Затраченное время {(time.time() - start_time) / 60} минут")


async def main(total_records, batch_size):
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # await insert_to_db(session, total_records, batch_size)

        await get_rating_user(session, user_id="9b5103de-8d49-11ef-ad95-7c70db5559dd")
        await get_rating_film(session, rating=8)
        await get_bookmarks_list(session)
        await get_avg_rating(session, film_id=UUID("f1fa9b48-8d33-11ef-a341-7c70db5559dd"))


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
    batch_size = 1000
    num_process = 5
    DATABASE_URL = "postgresql+asyncpg://user:123425426edfe@localhost/postgres_db"
    run_async_process(total_records, batch_size)
    # run_multiprocessing(total_records, batch_size, num_process)
