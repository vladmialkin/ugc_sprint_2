from datetime import UTC, datetime
from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class Base(BaseModel):
    id: PydanticObjectId = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
