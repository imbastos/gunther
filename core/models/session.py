from datetime import datetime
from uuid import UUID, uuid4

from attrs import define, field

from core.models.account import Account
from utils.get_utc_now import get_utc_now


@define
class Session:
    account: Account

    created_at: datetime = field(factory=get_utc_now)
    updated_at: datetime = field(factory=get_utc_now)

    id: UUID = field(factory=uuid4)
