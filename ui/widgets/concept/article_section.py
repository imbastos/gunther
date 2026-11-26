from textual.containers import Vertical
from textual.widgets import Static


class ArticleSection(Vertical):
    """Bloco visual de uma seção do artigo."""

    def __init__(
        self,
        title: str,
        content: str,
        border: str = "border-l-primary",
        widget_id: str | None = None,
    ):
        super().__init__(classes=f"w-full h-auto bg-surface {border} p-1-2 mb-2")

        self.title = title
        self.content = content
        self.widget_id = widget_id

    def compose(self):
        yield Static(self.title, classes="color-muted mb-1")
        yield Static(self.content, classes="w-full", id=self.widget_id)
