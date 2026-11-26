from uuid import UUID

from textual.containers import Vertical, VerticalScroll
from textual.widget import Widget
from textual.widgets import Static

from core.models import Article
from ui.widgets.alt_image import AltImage
from ui.widgets.sidebar.concept_item import ConceptSidebarItem
from ui.widgets.sidebar.item import SidebarItem

SIDEBAR_MAX_LABEL_LEN = 24


def _truncate_sidebar_text(
    prefix: str,
    text: str,
    max_len: int = SIDEBAR_MAX_LABEL_LEN,
) -> str:
    """Limita o tamanho do texto na sidebar."""
    label = f"{prefix}{text}"

    if len(label) <= max_len:
        return label

    available = max_len - len(prefix) - 3
    return (
        f"{prefix}{text[:available]}..."
        if available > 0
        else f"{label[: max_len - 3]}..."
    )


class Sidebar(Widget):
    """Barra lateral de navegação."""

    ITEMS = [  # noqa: RUF012
        {"label": "🏠 Página Inicial", "screen": "home", "group": "home"},
        {"label": "🧩 ArchKata", "screen": "archkata", "group": "archkata"},
    ]

    def __init__(
        self,
        selected_group: str = "",
        selected_article_id: UUID | str | None = None,
        concepts_expanded: bool = True,
        **kwargs,
    ):
        super().__init__(
            classes="dock-left w-32 h-full align-center-top bg-background",
            **kwargs,
        )
        self.selected_group = selected_group
        self.selected_article_id = (
            str(selected_article_id) if selected_article_id else None
        )
        self.concepts_expanded = concepts_expanded

    def compose(self):
        yield AltImage(
            image="assets/gunther.png",
            alt="Gunther",
            classes="center h-3 m-1-6-2-6 text-bold",
        )

        with VerticalScroll(classes="w-full pl-3"):
            for item in self.ITEMS:
                yield SidebarItem(
                    id=f"sidebar-{item['group']}",
                    label=_truncate_sidebar_text("", item["label"]),
                    target_screen=item["screen"],
                    selected=item["group"] == self.selected_group,
                )

            if getattr(self.screen, "is_admin", False):
                yield self._admin_item()

            yield Static(
                "📚 Conceitos",
                id="concept",
                classes="w-full bg-background border-none mb-1 p-1-2 text-left hover-tint-white",
            )

            articles = self._load_articles()

            with Vertical(classes="w-full h-auto"):
                if articles:
                    yield from self._render_concept_tree(articles)
                else:
                    yield Static(
                        "Nenhum conceito cadastrado.",
                        classes="color-muted p-1-2",
                    )

    def _admin_item(self):
        return SidebarItem(
            id="sidebar-admin",
            label="🔨 Painel Admin",
            target_screen="admin",
            selected=self.selected_group == "admin",
        )

    def on_mount(self):
        self.update_concept_display()
        self.sync_admin_item()

    def on_screen_resume(self) -> None:
        self.sync_admin_item()

    def sync_admin_item(self) -> None:
        is_admin = bool(getattr(self.screen, "is_admin", False))
        existing = self.query("#sidebar-admin")

        if is_admin and not existing:
            scroll = self.query_one(VerticalScroll)
            home = self.query("#sidebar-home")
            scroll.mount(self._admin_item(), after=home.first() if home else None)

        elif not is_admin and existing:
            for item in existing:
                item.remove()

    def update_concept_display(self):
        for item in self.query(ConceptSidebarItem):
            item.display = self.concepts_expanded

    def _load_articles(self) -> list[Article]:
        service = getattr(self.screen, "article_service", None)
        return service.get_all() if service else []

    def _render_concept_tree(self, articles: list[Article]):
        known_ids = {str(article.id) for article in articles}
        children = {}

        for article in articles:
            parent_id = str(article.parent_id) if article.parent_id else None

            if parent_id not in known_ids:
                parent_id = None

            children.setdefault(parent_id, []).append(article)

        visited = set()

        def walk(parent_id: str | None, prefix: str):
            for article in children.get(parent_id, []):
                article_id = str(article.id)

                if article_id in visited:
                    continue

                visited.add(article_id)

                yield ConceptSidebarItem(
                    article=article,
                    label=_truncate_sidebar_text(prefix, article.name),
                    selected=(
                        self.selected_group == "concept"
                        and self.selected_article_id == article_id
                    ),
                )

                yield from walk(article_id, prefix + "    ")

        yield from walk(None, "    ")

    def on_click(self, event) -> None:
        if event.widget.id == "concept":
            self.concepts_expanded = not self.concepts_expanded
            self.update_concept_display()
            event.stop()

        elif isinstance(event.widget, ConceptSidebarItem):
            self.concepts_expanded = True
            self.update_concept_display()
            event.stop()
