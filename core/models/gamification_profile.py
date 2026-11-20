from datetime import datetime
from uuid import UUID, uuid4

from attrs import define, field

from utils.get_utc_now import get_utc_now


@define
class GamificationProfile:
    profile_id: UUID

    points: int = 0
    experience: int = 0
    streak: int = 0

    created_at: datetime = field(factory=get_utc_now)
    updated_at: datetime = field(factory=get_utc_now)
    id: UUID = field(factory=uuid4)
