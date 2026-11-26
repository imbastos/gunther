from math import floor

from textual.reactive import reactive
from textual.binding import Binding
from textual.containers import Horizontal
from textual.timer import Timer
from textual.widgets import Footer

from ui.base.screen import BaseScreen
from ui.modals.game_modal import GameModal
from ui.modals.pause_modal import PauseModal
from ui.widgets.game.diagram import Diagram
from ui.widgets.game.store import Store


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

    def on_mount(self) -> None:
        self._timer = self.set_interval(1.0, self._on_tick, pause=self.game_paused)

    def _get_nodes(self):
        return self.query(".diagram_node")

    def _calc_multiplier(self):
        has_client = False
        has_server = False

        CLIENT_CATEGORY = "f83e0f1e-cb44-4032-8142-76af0fb42ef5"
        SERVER_CATEGORY = "82a48b06-4aea-4e15-bffe-c5f9863e6dfb"

        for node in self._get_nodes():
            if node.category.id == CLIENT_CATEGORY:
                has_client = True
            if node.category.id == SERVER_CATEGORY:
                has_server = True

        if not has_client or not has_server:
            self.multiplier = 0
            self.query_one("#users-indicator").update("[$error]•")
            return 
        self.query_one("#users-indicator").update("")
        self.multiplier = 1
        return 

    def _on_tick(self) -> None:
        if len(self._get_nodes()) == 0:
            return
        if self.game_paused:
            return
        self._calc_multiplier()
    
        self.elapsed_seconds += 1
        self.update_simulation()

    def update_simulation(self):
        users = floor(
            1**3
            * (10**6 * self.elapsed_seconds**3)
            / (600**3 + self.elapsed_seconds**3)
        ) * self.multiplier
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
