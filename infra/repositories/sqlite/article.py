import json
from datetime import datetime
from uuid import UUID

from core.models import Article, ArticleArea
from core.repositories import ArticleRepo
from infra.db.sqlite.manager import SqliteManager

_COLUMNS = """
id, name, slug, description, area, parent_id, "order",
introduction, explanation, examples, "references", questions, image,
is_published, created_at, updated_at, author
"""


def _to_article(row: tuple) -> Article:
    return Article(
        id=UUID(row[0]),
        name=row[1],
        slug=row[2],
        description=row[3],
        area=ArticleArea(row[4])
        if row[4] in ArticleArea._value2member_map_
        else row[4],
        parent_id=UUID(row[5]) if row[5] else None,
        order=int(row[6]),
        introduction=row[7],
        explanation=row[8],
        examples=json.loads(row[9]) if row[9] else [],
        references=json.loads(row[10]) if row[10] else [],
        questions=json.loads(row[11]) if row[11] else [],
        image=row[12],
        is_published=bool(row[13]),
        created_at=row[14],
        updated_at=row[15],
        author=row[16],
    )


def _area_value(area: ArticleArea | str) -> str:
    return area.value if isinstance(area, ArticleArea) else str(area)


def _date_value(value: datetime | str) -> str:
    return value.isoformat() if isinstance(value, datetime) else str(value)


class SqliteArticleRepo(ArticleRepo):
    """Repositório de artigos usando SQLite."""

    def __init__(self, sqlite: SqliteManager):
        self.sqlite = sqlite

    def _select(self, where: str = "", params: tuple = ()) -> list[Article]:
        query = f"SELECT {_COLUMNS} FROM articles"
        if where:
            query += f" WHERE {where}"
        query += ' ORDER BY "order", created_at'

        with self.sqlite as db:
            rows = db.fetch_all(query, params)
        return [_to_article(row) for row in rows]

    def _select_one(self, where: str, params: tuple) -> Article | None:
        with self.sqlite as db:
            row = db.fetch_one(f"SELECT {_COLUMNS} FROM articles WHERE {where}", params)
        return _to_article(row) if row else None

    def get_all(self) -> list[Article]:
        return self._select()

    def get_published(self) -> list[Article]:
        return self._select("is_published = 1")

    def get_by_id(self, article_id: UUID | str) -> Article | None:
        return self._select_one("id = ?", (str(article_id),))

    def find_by_slug(self, slug: str) -> Article | None:
        return self._select_one("slug = ?", (slug,))

    def get_by_area(self, area: ArticleArea | str) -> list[Article]:
        return self._select("area = ?", (_area_value(area),))

    def get_children(self, parent_id: UUID | str | None) -> list[Article]:
        if parent_id is None:
            return self._select("parent_id IS NULL")
        return self._select("parent_id = ?", (str(parent_id),))

    def create(self, article: Article) -> Article:
        query = """
            INSERT INTO articles (
                id, name, slug, description, area, parent_id, "order",
                introduction, explanation, examples, "references", questions,
                image, is_published, created_at, updated_at, author
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            str(article.id),
            article.name,
            article.slug,
            article.description,
            _area_value(article.area),
            str(article.parent_id) if article.parent_id else None,
            int(article.order),
            article.introduction,
            article.explanation,
            json.dumps(article.examples, ensure_ascii=False),
            json.dumps(article.references, ensure_ascii=False),
            json.dumps(article.questions, ensure_ascii=False),
            article.image,
            int(bool(article.is_published)),
            _date_value(article.created_at),
            _date_value(article.updated_at),
            str(article.author),
        )
        with self.sqlite as db:
            db.execute(query, params)
        return article

    def update(self, article: Article) -> Article:
        query = """
            UPDATE articles SET
                name = ?, slug = ?, description = ?, area = ?, parent_id = ?,
                "order" = ?, introduction = ?, explanation = ?, examples = ?,
                "references" = ?, questions = ?, image = ?, is_published = ?,
                updated_at = ?, author = ?
            WHERE id = ?
        """
        params = (
            article.name,
            article.slug,
            article.description,
            _area_value(article.area),
            str(article.parent_id) if article.parent_id else None,
            int(article.order),
            article.introduction,
            article.explanation,
            json.dumps(article.examples, ensure_ascii=False),
            json.dumps(article.references, ensure_ascii=False),
            json.dumps(article.questions, ensure_ascii=False),
            article.image,
            int(bool(article.is_published)),
            _date_value(article.updated_at),
            str(article.author),
            str(article.id),
        )
        with self.sqlite as db:
            db.execute(query, params)
        return article

    def delete(self, article_id: UUID | str) -> None:
        with self.sqlite as db:
            db.execute("DELETE FROM articles WHERE id = ?", (str(article_id),))
