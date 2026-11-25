from datetime import datetime
from uuid import UUID, uuid4

from attrs import define, field

import utils


@define
class Post:
    """Modelo que representa um artigo editorial exibido na página inicial."""

    name: str
    text: str = ""
    image: str | None = None
    is_highlighted: bool = False

    created_at: datetime = field(factory=utils.date_now)
    updated_at: datetime = field(factory=utils.date_now)
    id: UUID = field(factory=uuid4)
