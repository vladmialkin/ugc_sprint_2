from pydantic import MongoDsn, SecretStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from app.settings.base import Settings


class MongoDBSettings(Settings):
    MONGODB_USER: str
    MONGODB_PASSWORD: SecretStr
    MONGODB_HOST: str
    MONGODB_PORT: str
    DSN: str | None = None

    @field_validator("DSN", mode="before")
    @classmethod
    def assemble_dsn(
        cls, _: str | None, info: FieldValidationInfo
    ) -> MongoDsn:
        scheme = "mongodb"
        user = info.data["MONGODB_USER"]
        password = info.data["MONGODB_PASSWORD"].get_secret_value()
        host = info.data["MONGODB_HOST"]
        port = info.data["MONGODB_PORT"]

        url = f"{scheme}://{user}:{password}@{host}:{port}"
        return MongoDsn(url).unicode_string()


settings = MongoDBSettings()
