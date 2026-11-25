import datetime
from typing import Literal
from uuid import UUID, uuid4

from attrs import define, field

import utils


@define
class User:
    name: str
    username: str
    email: str
    hashed_password: str | None = None

    role: Literal["user", "admin"] = "user"
    image: str | None = None
    streak: int = 0
    last_activity_at: datetime.datetime | str | None = None
    completed_concepts: list[str] = field(factory=list)

    created_at: datetime = field(factory=utils.date_now)
    id: UUID = field(factory=uuid4)
