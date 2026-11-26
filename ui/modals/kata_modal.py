from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Label

from core.models import Game
from ui.widgets.action_button import ActionButton


class KataModal(ModalScreen[bool]):
    """Modal de confirmação exibindo os dados do desafio antes de iniciar."""

    def __init__(self, game: Game):
        super().__init__()
        self.game = game

    def compose(self):
        dots = "●" * (self.game.difficulty or 1)

        with (
            Container(classes="center-container"),
            Vertical(
                id="kata-modal-dialog",
                classes="w-60 bg-surface round-panel p-1-2 h-auto",
            ),
        ):
            yield Label(
                self.game.name,
                id="kata-modal-title",
                classes="text-bold color-primary mb-1 w-full text-center",
            )
            if self.game.description:
                yield Label(
                    self.game.description,
                    id="kata-modal-description",
                    classes="color-muted mb-1 w-full text-center",
                )
            yield Label(
                f"Dificuldade: {dots} • {self.game.xp} XP",
                id="kata-modal-meta",
                classes="color-accent mb-1 w-full",
            )
            yield Label(
                "[$foreground-muted]Deseja iniciar o desafio ou voltar?",
                classes="mb-1 w-full",
            )
            with Horizontal(classes="w-full h-auto"):
                yield ActionButton(
                    "Começar",
                    action=lambda: self.dismiss(True),
                    id="kata-modal-start-btn",
                    variant="primary",
                    classes="h-3 p-0-2 mr-1 w-1--1",
                )
                yield ActionButton(
                    "Voltar",
                    action=lambda: self.dismiss(False),
                    id="kata-modal-back-btn",
                    classes="h-3 border-none bg-panel p-0-2 w-1--1 hover-tint-white",
                )
