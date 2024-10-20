from app.settings.base import Base
from pydantic import field_validator, ClickHouseDsn
from pydantic_core.core_schema import FieldValidationInfo


class ClickHouseSettings(Base):
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_DATABASE: str
    DSN: str | None = None

    @field_validator("DSN", mode="before")
    @classmethod
    def assemble_dsn(
            cls, _: str | None, info: FieldValidationInfo
    ) -> ClickHouseDsn:
        host = info.data["CLICKHOUSE_HOST"]
        port = info.data["CLICKHOUSE_PORT"]

        url = f"http://{host}:{port}"
        return ClickHouseDsn(url).unicode_string()


settings = ClickHouseSettings()
