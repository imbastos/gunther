from textual.widgets import Static

from core.models import Article


class ConceptSidebarItem(Static):
    """Item de conceito na árvore hierárquica."""

    def __init__(self, article: Article, label: str, selected: bool = False):
        classes = (
            "w-full bg-background border-none mb-1 p-1-2 text-left hover-tint-white"
        )

        if not article.is_published:
            classes += " color-muted"

        if selected:
            classes += " tint-white-5 text-bold"

        super().__init__(
            label,
            id=f"sidebar-concept-{article.id}",
            classes=classes,
        )
        self.article = article

    def on_click(self) -> None:
        self.screen.router.navigate_to("concept", article_id=self.article.id)
