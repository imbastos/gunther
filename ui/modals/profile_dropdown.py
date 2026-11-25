from ui.modals.settings_modal import SettingsModal
from ui.widgets.dropdown import Dropdown, DropdownAction


class ProfileDropdown(Dropdown):
    """Dropdown do perfil no cabeçalho."""

    def __init__(self):
        actions = {
            "profile": self._navigate_profile,
            "settings": lambda: self.app.push_screen(SettingsModal()),
            "signout": self.handle_signout,
        }
        super().__init__(actions, classes="right ox--2 oy-5")

    def _navigate_profile(self) -> None:
        """Navega para o perfil do usuário atual, passando o user_id explicitamente."""
        session = self.screen.session_manager.current_session
        self.screen.router.navigate_to("profile", user_id=session.user_id)

    def compose(self):
        yield DropdownAction(text="Perfil", id="profile")
        yield DropdownAction(text="Configurações", id="settings")
        yield DropdownAction(text="Sair", id="signout", caution=True)
