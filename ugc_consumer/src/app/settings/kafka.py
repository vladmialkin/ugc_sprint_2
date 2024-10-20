from app.settings.base import Base


class KafkaSettings(Base):
    KAFKA_BROKER: str
    TOPIC_NAMES: str


settings = KafkaSettings()
