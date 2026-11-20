from textual import on
from textual.app import App
from textual.widgets import Input

from core.exceptions.auth_exception import NotAuthorizedError
from core.models.session import Session
from core.services.auth_service import AuthService
from core.services.gamification_profile_service import GamificationProfileService
from core.services.profile_service import ProfileService
from tui.screens.auth import AuthScreen
from tui.screens.errors.not_found import NotFoundScreen
from tui.screens.errors.unauthorized import UnauthorizedScreen
from tui.screens.home import HomeScreen
from tui.screens.profile import ProfileScreen
from tui.screens.screen import Screen
from utils.validate_session import validate_session


class TextualApp(App):
    def __init__(
        self,
        auth_service: AuthService,
        profile_service: ProfileService,
        gamification_profile_service: GamificationProfileService,
    ):
        self.SCREENS = {
            "auth": AuthScreen(auth_service),
            "home": HomeScreen(),
            "profile": ProfileScreen(),
        }
        self.CSS_PATH = [
            "styles/screens/auth.tcss",
            "styles/widgets/alt_image.tcss",
            "styles/widgets/form.tcss",
            "styles/widgets/header.tcss",
            "styles/widgets/modal.tcss",
            "styles/widgets/profile.tcss",
            "styles/widgets/searchbar.tcss",
            "styles/widgets/sidebar.tcss",
            "styles/widgets/streak.tcss",
            "styles/widgets/title.tcss",
            "styles/styles.tcss",
        ]
        super().__init__()

        self.session: Session | None = None

        self.auth_service = auth_service
        self.profile_service = profile_service
        self.gamification_profile_service = gamification_profile_service

    @on(AuthScreen.Authenticated)
    def on_authenticated(self, event: AuthScreen.Authenticated) -> None:
        self.session = event.session
        self.navigate("home")

    def signout(self) -> None:
        self.session = None
        self.navigate("auth")

    def on_mount(self) -> None:
        self.push_screen("auth")
        self.set_focus(None)

    def on_click(self, event):
        if not isinstance(event.widget, Input):
            self.set_focus(None)

    def navigate(self, screen: str) -> None:
        """
        Altera a tela verificando se é uma tela protegida
        """

        try:
            target_screen: Screen = self.SCREENS[screen]
            if isinstance(screen, Screen) and screen.protected:
                validate_session(self.session)
        except NotAuthorizedError:
            self.push_screen(UnauthorizedScreen())
            return
        except KeyError:
            self.push_screen(NotFoundScreen())
            return
        self.push_screen(target_screen)
        self.set_focus(None)

    @property
    def profile(self):
        return self.profile_service.get_by_account_id(
            account_id=self.session.account.id
        )

    @property
    def gamification_profile(self):
        return self.gamification_profile_service.get_by_profile_id(
            profile_id=self.profile.id
        )
