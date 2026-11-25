from datetime import datetime
from uuid import UUID, uuid4

from attrs import define, field

from utils import date_now


@define
class Session:
    user_id: UUID

    created_at: datetime = field(factory=date_now)
    updated_at: datetime = field(factory=date_now)

    id: UUID = field(factory=uuid4)
