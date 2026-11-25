from uuid import UUID

from textual.containers import Container
from textual.widgets import Label, Static

from core.exceptions.post import NotFoundPostError
from core.models import Post
from ui.templates import Shell
from ui.widgets.action_button import ActionButton
from ui.widgets.alt_image import AltImage


class ArticleScreen(Shell):
    """Tela de leitura de artigo com conteúdo renderizado em Markdown."""

    group = ""

    def __init__(self, article_id: UUID | str | None = None, **kwargs):
        super().__init__(**kwargs)
        self._requested_id = article_id
        self.article: Post | None = self._resolve_article()

    def _resolve_article(self) -> Post | None:
        if self.post_service is None:
            return None
        try:
            if self._requested_id is not None:
                return self.post_service.get_by_id(self._requested_id)
        except NotFoundPostError:
            return None

        posts = self.post_service.get_all()
        return posts[0] if posts else None

    def compose(self):
        yield from super().compose()

        with Container(classes="main"):
            if self.article is None:
                yield Label("Artigo não encontrado", classes="text-bold mb-1")
                yield Label(
                    "Nenhum artigo disponível para exibição.",
                    classes="color-muted",
                )
                return

            yield ActionButton(
                "◀ Voltar",
                action=lambda: self.router.navigate_to("home"),
                id="article-back-btn",
                classes="h-3 border-none bg-surface p-0-2 mb-1 hover-tint-white",
            )
            yield Label(
                self.article.name,
                id="article-title",
                classes="text-bold color-primary mb-1 w-full",
            )
            if self.article.image:
                yield AltImage(
                    image=self.article.image,
                    alt=f"🖼 {self.article.image}",
                    classes="h-8 mb-1",
                )
            yield Static(
                self.article.text,
                id="article-markdown",
                classes="w-full h-auto mb-2",
            )
