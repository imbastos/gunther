from textual import on
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Switch


class SettingsModal(ModalScreen):
    """Modal de configurações do aplicativo."""

    def compose(self):
        with (
            Container(classes="center-container"),
            Vertical(
                id="settings-dialog",
                classes="w-48 h-auto bg-surface round-panel p-1-2 center",
            ),
        ):
            yield Label("Configurações", classes="text-center w-full mb-1 text-bold")
            with Horizontal(classes="w-full h-auto center mb-1"):
                yield Switch(value=self.app.use_images, id="images")
                yield Label("Utilizar imagens", classes="h-3 content-center ml-2")

            yield Button("Fechar", classes="w-full", id="dismiss")

    @on(Button.Pressed, "#dismiss")
    def handle_dismiss(self):
        self.dismiss()

    @on(Switch.Changed, "#images")
    def use_images(self, event: Switch.Changed):
        self.app.set_use_images(event.value)
