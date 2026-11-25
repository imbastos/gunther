from textual.containers import Container, Grid, Vertical
from textual.widgets import Label

from ui.templates import Shell
from ui.widgets.article_card import ArticleCard


class HomeScreen(Shell):
    """Tela principal do aplicativo"""

    group = "home"

    def compose(self):
        highlighted = (
            self.post_service.get_highlighted() if self.post_service else None
        )
        posts = self.post_service.get_all() if self.post_service else []
        other_posts = [
            post
            for post in posts
            if highlighted is None or str(post.id) != str(highlighted.id)
        ]

        yield from super().compose()
        with Container(classes="main"), Vertical(classes="w-full h-auto mb-2"):
            yield Label("[📄] Artigos", classes="color-muted mb-1")
            if highlighted is not None:
                yield ArticleCard(
                    article=highlighted,
                    highlighted=True,
                    classes="mb-2",
                )

            if other_posts:
                with Grid(classes="w-full h-auto cols-3 gutter-1"):
                    for post in other_posts:
                        yield ArticleCard(article=post, highlighted=False)
            elif highlighted is None:
                yield Label("Nenhum artigo cadastrado.", classes="color-muted")
