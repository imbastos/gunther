from typing import Literal
from uuid import UUID, uuid4

from attrs import define, field


@define
class Category:
    name: str
    color: str

    id: UUID = field(factory=uuid4)