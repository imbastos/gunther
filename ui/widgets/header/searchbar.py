from uuid import UUID

from textual.widget import Widget
from textual.widgets import Input, Static

from core.services.user import UserService
from ui.widgets.header.search_results import SearchResultsDropdown


class Searchbar(Widget):
    DEFAULT_CSS = """
    .icon{
        color: $surface;
        dock: right;
        offset: -4 1;
        position: absolute;
        width: auto;
    }
    """

    def __init__(self):
        super().__init__(classes="w-1--1", id="searchbar")

    def compose(self):
        yield Input(
            placeholder="Procurar",
            id="searchbar-input",
            classes="round-surface bg-background w-1--1",
        )
        yield Static("🔎︎", classes="icon")

    async def on_input_changed(self, event: Input.Changed) -> None:
        term = event.value.strip().lower()
        results_box = self.screen.query_one(SearchResultsDropdown)
        if not term:
            results_box.hide()
            return

        matches: list[tuple[str, str, UUID | str]] = []
        user_service: UserService = getattr(self.screen, "user_service", None)
        if user_service is not None:
            for user in user_service.get_all():
                if term in user.name.lower() or term in user.username.lower():
                    matches.append((f"👤 Usuário: {user.name}", "profile", {"user_id": user.id}))

        post_service = getattr(self.screen, "post_service", None)
        if post_service is not None:
            for post in post_service.get_all():
                if term in post.name.lower() or term in post.text.lower():
                    matches.append((f"📄 Artigo: {post.name}", "article", {"article_id": post.id}))

        article_service = getattr(self.screen, "article_service", None)
        if article_service is not None:
            for article in article_service.get_all():
                if (
                    term in article.name.lower()
                    or term in article.description.lower()
                    or term in article.slug.lower()
                ):
                    matches.append(
                        (f"📚 Conceito: {article.name}", "concept", {"article_id": article.id})
                    )

        await results_box.show_results(matches)
