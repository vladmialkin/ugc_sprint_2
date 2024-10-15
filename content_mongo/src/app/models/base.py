from datetime import datetime, timezone
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field


class BaseDocument(Document):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
