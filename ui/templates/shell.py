from uuid import UUID

from ui.base import BaseScreen
from ui.modals import ProfileDropdown
from ui.widgets import Header, Sidebar
from ui.widgets.header.search_results import SearchResultsDropdown


class Shell(BaseScreen):
    """Template base para páginas autenticadas."""

    protected = True
    group = ""

    def __init__(
        self,
        selected_article_id: UUID | str | None = None,
        concepts_expanded: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.selected_article_id = selected_article_id
        self.concepts_expanded = concepts_expanded

    def compose(self):
        yield ProfileDropdown()
        yield SearchResultsDropdown()
        yield Sidebar(
            selected_group=self.group,
            selected_article_id=self.selected_article_id,
            concepts_expanded=self.concepts_expanded,
        )
        yield Header(streak=self.current_user.streak)
