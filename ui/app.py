from textual.app import App
from textual.widgets import Input

from core.models.session import Session
from core.services import (
    ArticleService,
    GameService,
    PostService,
    UserService,
)
from core.services.auth import AuthService
from core.session import SessionManager
from ui.router import Router
from ui.screens import (
    AdminScreen,
    ArchKataScreen,
    ArticleScreen,
    ChallengeScreen,
    ConceptScreen,
    GameScreen,
    HeroScreen,
    OnboardingScreen,
    ProfileScreen,
    UserListScreen,
)
from ui.screens.auth import AuthScreen
from ui.screens.home import HomeScreen
from ui.widgets.alt_image import AltImage


class TextualApp(App):
    """Classe principal do aplicativo Textual"""

    SCREENS = {  # noqa: RUF012
        "admin": AdminScreen,
        "archkata": ArchKataScreen,
        "article": ArticleScreen,
        "auth": AuthScreen,
        "challenge": ChallengeScreen,
        "concept": ConceptScreen,
        "game": GameScreen,
        "hero": HeroScreen,
        "home": HomeScreen,
        "onboarding": OnboardingScreen,
        "profile": ProfileScreen,
        "user_list": UserListScreen,
    }

    CSS_PATH = "styles.tcss"

    def __init__(
        self,
        auth_service: AuthService,
        user_service: UserService,
        article_service: ArticleService | None = None,
        post_service: PostService | None = None,
        game_service: GameService | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.session_manager = SessionManager()
        self.router = Router(app=self, session_manager=self.session_manager)

        self.auth_service = auth_service
        self.user_service = user_service
        self.article_service = article_service
        self.post_service = post_service
        self.game_service = game_service

        self.use_images = True

    def set_use_images(self, value: bool) -> None:
        """Atualiza a preferência de exibição de imagens e recompõe os AltImage."""
        self.use_images = value

        for screen in self.screen_stack:
            for widget in screen.query(AltImage):
                widget.refresh(recompose=True)

    def on_click(self, event):
        # Remove o foco do input clicando fora dele
        if not isinstance(event.widget, Input):
            self.set_focus(None)

        # Fecha os resultados da busca ao clicar fora da searchbar/resultados
        from ui.widgets.header.search_results import SearchResultsDropdown
        from ui.widgets.header.searchbar import Searchbar

        if not any(
            isinstance(node, (Searchbar, SearchResultsDropdown))
            for node in event.widget.ancestors_with_self
        ):
            for box in self.screen.query(SearchResultsDropdown):
                box.hide()

    def on_mount(self):
        self.push_screen("hero")
        # self.session_manager.start(user_id="123e4567-e89b-12d3-a456-426614174000")
        # self.push_screen("archkata")
