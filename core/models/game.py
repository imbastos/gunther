from typing import Literal
from uuid import UUID, uuid4

from attrs import define, field


@define
class Game:
    name: str

    description: str = field(default="")
    # requirements: list[ChallengeRequirement] = field(factory=list)
    difficulty: Literal[1, 2, 3] | None = field(default=None)
    is_weekly: bool = field(default=False)

    id: UUID = field(factory=uuid4)

    @property
    def xp(self) -> int:
        xp_map = {1: 100, 2: 250, 3: 600}

        return xp_map.get(self.difficulty, 0)
