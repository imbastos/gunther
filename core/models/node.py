from typing import Literal
from uuid import UUID, uuid4

from attrs import define, field


@define
class Node:
    name: str
    price: int

    category: UUID

    id: UUID = field(factory=uuid4)