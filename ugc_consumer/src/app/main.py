import asyncio
import json
import logging

import backoff
from aiokafka import AIOKafkaConsumer
from aiohttp import ClientSession
from aiochclient import ChClient

from app.schemas.events import Click, UsingSearchFilters, WatchToTheEnd, ChangeVideoQuality, TimeOnPage, PageView
from app.settings.kafka import settings as kafka_settings
from app.settings.clickhouse import settings as clickhouse_settings


BATCH_SIZE = 1000

tables = {
    'click': Click,
    'page_view': PageView,
    'time_on_page': TimeOnPage,
    'change_video_quality': ChangeVideoQuality,
    'watch_to_the_end': WatchToTheEnd,
    'using_search_filters': UsingSearchFilters,
}

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def insert_into_clickhouse(batch_data, client):
    for table, data in batch_data.items():
        if not data:
            continue

        fields = data[0].__dict__.keys()
        values = [tuple([getattr(values, field) for field in fields]) for values in data]

        query = f'INSERT INTO default.{table} VALUES'

        await client.execute(query, *values)
        data.clear()
    logging.info('Данные добавлены')



async def consume():
    consumer = AIOKafkaConsumer(
        *kafka_settings.TOPIC_NAMES.split(','),
        enable_auto_commit=False,
        bootstrap_servers=kafka_settings.KAFKA_BROKER,
        auto_offset_reset='earliest',
        group_id='my-group'
    )

    await consumer.start()
    async with ClientSession() as session:
        client = ChClient(session, url=clickhouse_settings.DSN)
        try:
            count = 0
            batch_data = {
                "click": [],
                "page_view": [],
                "time_on_page": [],
                "change_video_quality": [],
                "watch_to_the_end": [],
                "using_search_filters": [],
            }
            async for message in consumer:
                data = json.loads(message.value)
                table = data.get('event_type')
                schema = tables.get(table)(**data)
                batch_data.get(table).append(schema)
                count += 1

                if count >= BATCH_SIZE:
                    await insert_into_clickhouse(batch_data, client)

                await consumer.commit()
        finally:
            await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
