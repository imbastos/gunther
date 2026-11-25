from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from attrs import define, field

import utils
from core.enums.article_area import ArticleArea


@define
class Article:
    """Modelo que representa um artigo/conceito educacional."""

    name: str
    slug: str
    description: str
    area: ArticleArea | str
    introduction: str
    explanation: str
    author: str

    parent_id: UUID | None = None
    order: int = 0
    examples: list[Any] | dict[str, Any] = field(factory=list)
    references: list[Any] | dict[str, Any] = field(factory=list)
    questions: list[dict[str, Any]] = field(factory=list)
    image: str | None = None
    is_published: bool = False

    created_at: datetime = field(factory=utils.date_now)
    updated_at: datetime = field(factory=utils.date_now)
    id: UUID = field(factory=uuid4)
