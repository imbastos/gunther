from uuid import UUID

from textual.containers import VerticalScroll
from textual.widgets import Static


class SearchResultItem(Static):
    """Item clicável na lista flutuante de resultados da busca."""

    def __init__(self, label: str, target_screen: str, **kwargs):
        super().__init__(
            label,
            classes="w-full p-0-2 bg-surface hover mb-1",
        )
        self.target_screen = target_screen
        self.kwargs = kwargs

    def on_click(self) -> None:
        self.screen.query_one(SearchResultsDropdown).hide()
        self.screen.router.navigate_to(self.target_screen, **self.kwargs)


class SearchResultsDropdown(VerticalScroll):
    """Container flutuante com os resultados da barra de pesquisa."""

    def __init__(self):
        super().__init__(
            id="search-results",
            classes="modal bg-surface round-panel h-auto max-h-16 o-34-4 p-1",
        )
        self.display = False

    async def show_results(self, items: list[tuple[str, str, UUID | str]]) -> None:
        await self.remove_children()

        widgets = (
            [
                SearchResultItem(label, target, **kwargs)
                for label, target, kwargs in items
            ]
            if items
            else [
                Static(
                    "Nenhum resultado encontrado.",
                    classes="color-muted p-0-2",
                )
            ]
        )

        await self.mount(*widgets)
        self.display = True

    def on_mount(self):
        self.call_after_refresh(self.resize)

    def on_resize(self):
        self.resize()

    def resize(self):
        searchbar = self.screen.query_one("#searchbar")
        if searchbar is not None:
            self.styles.width = searchbar.region.width - 2

    def hide(self) -> None:
        self.display = False
