from typing import Optional

from aiokafka import AIOKafkaConsumer

consumer: Optional[AIOKafkaConsumer] = None


async def get_consumer() -> AIOKafkaConsumer:
    return consumer
