from textual.color import Color
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Label

from core.models import Post
from ui.widgets.tag import Tag


class ArticleCard(Widget):
    """Card clicável para exibir artigo na página inicial."""

    def __init__(
        self,
        article: Post,
        highlighted: bool | None = None,
        classes: str = "",
    ):
        super().__init__(classes=f"w-full h-auto {classes}".strip())
        self.article = article
        self.highlighted = (
            article.is_highlighted if highlighted is None else highlighted
        )

    def _build_preview(self) -> str:
        limit = 200 if self.highlighted else 56
        text = self.article.text.strip().replace("\n", " ")
        if len(text) > limit:
            return text[:limit] + "..."
        return text

    def compose(self):
        with Vertical(classes="p-1-2 bg-surface hover w-full h-auto"):
            if self.highlighted:
                yield Tag(
                    "💡 Sugestão de Leitura",
                    color=Color.parse(self.app.current_theme.primary).with_alpha(0.2),
                    classes="mb-2",
                )

            yield Label(self.article.name, classes="text-bold mb-1 w-full")
            yield Label(self._build_preview(), classes="color-muted w-full")

    def on_click(self):
        self.screen.router.navigate_to("article", article_id=self.article.id)
