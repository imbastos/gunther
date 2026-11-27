from math import floor

from textual.binding import Binding
from textual.containers import Horizontal
from textual.timer import Timer
from textual.widgets import Footer

from ui.base.screen import BaseScreen
from ui.modals.game_modal import GameModal
from ui.modals.pause_modal import PauseModal
from ui.widgets.game.diagram import Diagram
from ui.widgets.game.store import Store

REQUIREMENTS = [
    {
        "name": "client_required",
        "message": "É obrigatório ter pelo menos um cliente",
        "multiplier": 0,
        "verify": lambda nodes: any(node.category.id == "client" for node in nodes),
    },
    {
        "name": "redis_required",
        "message": "É obrigatório ter pelo menos um banco cache",
        "multiplier": 0.8,
        "verify": lambda nodes: any(node.category.id == "client" for node in nodes),
    },
    {
        "name": "server_required",
        "message": "É obrigatório ter pelo menos um servidor",
        "multiplier": 0,
        "verify": lambda nodes: any(node.category.id == "compute" for node in nodes),
    },
]


class GameScreen(BaseScreen):
    """Tela base do simulador ArchKata."""

    BINDINGS = [  # noqa: RUF012
        Binding(key="escape", action="menu", description="Voltar ao menu"),
        Binding(key="f1", action="help", description="Ajuda"),
        Binding(key="p", action="pause", description="Pausar"),
    ]

    def __init__(self):
        super().__init__(classes="no-scroll")
        self.game_paused = False
        self.elapsed_seconds = 0
        self._timer: Timer | None = None
        self.multiplier = 0
        self.money = 1000
        self.missing_requirements = []

    def on_mount(self) -> None:
        self._timer = self.set_interval(1.0, self._on_tick, pause=self.game_paused)

    def _get_nodes(self):
        return self.query(".diagram_node")

    def _update_indicator(self):
        if len(self.missing_requirements) > 0:
            self.query_one("#users-indicator").display = True
        else:
            self.query_one("#users-indicator").display = False

    def _verify_requirements(self):
        nodes = self._get_nodes()
        missing_requirements = []

        for requirement in REQUIREMENTS:
            if not requirement["verify"](nodes):
                missing_requirements.append(requirement)

        self.missing_requirements = missing_requirements

        messages = "\n".join(
            f"[$error]• {requirement['message']}" for requirement in missing_requirements
        )

        self.query_one("#requirements_missing").update(messages)

    def _calc_multiplier(self):
        multiplier = 1
        for requirement in self.missing_requirements:
            multiplier *= requirement["multiplier"]
        self.multiplier = multiplier

    def _on_tick(self) -> None:
        self._verify_requirements()
        self._calc_multiplier()
        self._update_indicator()

        if len(self._get_nodes()) == 0:
            return
        if self.game_paused:
            return

        self.elapsed_seconds += 1
        self.update_simulation()

    def update_simulation(self):
        users = (
            floor(
                1**3
                * (10**6 * self.elapsed_seconds**3)
                / (600**3 + self.elapsed_seconds**3)
            )
            * self.multiplier
        )
        self.query_one("#users").update(str(users))

    def _set_paused(self, paused: bool) -> None:
        self.game_paused = paused
        if self._timer is not None:
            if paused:
                self._timer.pause()
            else:
                self._timer.resume()

    def action_menu(self):
        self.router.navigate_to("archkata")

    def action_pause(self):
        if self.game_paused:
            return
        self._set_paused(True)
        self.app.push_screen(PauseModal(lambda: self._set_paused(False)))

    def action_help(self):
        self.app.push_screen(GameModal())

    def compose(self):
        with Horizontal(classes="h-full"):
            yield Diagram(multiplier=self.multiplier)
            yield Store()
        yield Footer()
