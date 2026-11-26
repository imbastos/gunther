from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Label

from ui.widgets.action_button import ActionButton


class PauseModal(ModalScreen):
    def __init__(self, resume):
        super().__init__()
        self.resume = resume

    def compose(self):
        with Container(classes="center-container"), Vertical(classes="w-1--3"):
            yield Label("[$primary]Jogo pausado", classes="text-center w-1--1 mb-2")
            yield Label(
                "Aproveite para beber uma água", classes="text-center w-1--1 mb-1"
            )

            yield ActionButton(
                "Continuar", action=self.handle_dismiss, classes="w-full", id="dismiss"
            )

    def handle_dismiss(self):
        self.resume()
        self.dismiss()
