from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Input, Label

from ui.base.screen import BaseScreen
from ui.modals.file_picker import FilePickerModal
from ui.utils import copy_user_photo
from ui.widgets.action_button import ActionButton


class OnboardingScreen(BaseScreen):
    """Tela pós-cadastro para definir nome e foto de perfil do computador."""

    protected = True

    def compose(self):
        user = self.current_user
        initial_name = ""
        if user is not None and user.name != "Sem nome":
            initial_name = user.name

        with (
            Container(classes="center-container"),
            Vertical(
                id="onboarding-card",
                classes="content-container w-1--3 bg-background round-surface p-1-2",
            ),
        ):
            yield Label(
                "Bem-vindo ao Gunther!",
                classes="text-bold text-center w-full color-primary mb-1",
            )
            yield Label(
                "Como devemos te chamar? Você também pode carregar uma foto do computador.",
                classes="color-muted mb-1 w-full",
            )
            yield Label("Seu nome:", classes="color-muted mb-1")
            yield Input(
                value=initial_name,
                placeholder="Digite seu nome completo",
                id="onboarding-name-input",
                classes="w-full mb-1",
            )
            yield Label("Foto de perfil (opcional):", classes="color-muted mb-1")
            with Horizontal(classes="w-full h-auto mb-2"):
                yield Input(
                    value="",
                    placeholder="Caminho da imagem no computador",
                    id="onboarding-photo-input",
                    classes="w-1--1 mr-1",
                )
                yield ActionButton(
                    "Procurar...",
                    action=lambda: self.app.push_screen(
                        FilePickerModal(),
                        callback=self._on_photo_picked,
                    ),
                    id="onboarding-pick-photo-btn",
                    classes="h-3 border-none bg-surface p-0-2 hover-tint-white",
                )
            with Horizontal(classes="w-full h-auto"):
                yield ActionButton(
                    "Continuar",
                    action=self._handle_save,
                    id="onboarding-save-btn",
                    classes="h-3 border-none bg-success p-0-2 mr-1 hover-tint-white",
                )
                yield ActionButton(
                    "Pular",
                    action=lambda: self.router.navigate_to("home"),
                    id="onboarding-skip-btn",
                    classes="h-3 border-none bg-surface p-0-2 hover-tint-white",
                )

    def _on_photo_picked(self, path: str | None) -> None:
        if path:
            self.query_one("#onboarding-photo-input", Input).value = path

    def _handle_save(self) -> None:
        user = self.current_user
        if user is None:
            self.router.navigate_to("home")
            return

        name = self.query_one("#onboarding-name-input", Input).value.strip()
        photo_path = self.query_one("#onboarding-photo-input", Input).value.strip()

        if name:
            user.name = name

        if photo_path:
            try:
                user.image = copy_user_photo(photo_path, user.id)
            except FileNotFoundError:
                self.app.notify("Arquivo de foto não encontrado.", severity="error")
                return

        self.user_service.update(user)
        self.app.notify("Perfil configurado!")
        self.router.navigate_to("home")
