from uuid import UUID

from textual.containers import VerticalScroll
from textual.widgets import Static


class SearchResultItem(Static):
    """Item clicável na lista flutuante de resultados da busca."""

    def __init__(self, label: str, target_screen: str, item_id: UUID | str):
        super().__init__(
            label,
            classes="w-full p-0-2 bg-surface hover mb-1",
        )
        self.target_screen = target_screen
        self.item_id = item_id

    def on_click(self) -> None:
        self.screen.query_one(SearchResultsDropdown).hide()
        self.screen.router.navigate_to(
            self.target_screen,
            article_id=self.item_id,
        )


class SearchResultsDropdown(VerticalScroll):
    """Container flutuante com os resultados da barra de pesquisa."""

    def __init__(self):
        super().__init__(
            id="search-results",
            classes="modal bg-surface round-panel w-60 h-auto max-h-16 o-34-4 p-1",
        )
        self.display = False

    async def show_results(self, items: list[tuple[str, str, UUID | str]]) -> None:
        await self.remove_children()

        widgets = (
            [
                SearchResultItem(label, target, item_id)
                for label, target, item_id in items
            ]
            if items
            else [Static("Nenhum resultado encontrado.", classes="color-muted p-0-2")]
        )

        await self.mount(*widgets)
        self.display = True

    def hide(self) -> None:
        self.display = False
