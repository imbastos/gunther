from datetime import datetime
from uuid import UUID, uuid4

from attrs import define, field

from utils.get_utc_now import get_utc_now


@define
class Profile:
    account_id: UUID

    username: str
    display_name: str
    photo: str | None = None
    following: list["Profile"] = field(factory=list)

    created_at: datetime = field(factory=get_utc_now)
    updated_at: datetime = field(factory=get_utc_now)

    id: UUID = field(factory=uuid4)
