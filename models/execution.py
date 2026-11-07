from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class Execution(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    status: str = "EN_PROCESO"
    input_file: str | None = None
