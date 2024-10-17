from datetime import UTC, datetime
from uuid import UUID, uuid4

from beanie import Document
from bson import ObjectId
from pydantic import Field


class BaseDocument(Document):
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
