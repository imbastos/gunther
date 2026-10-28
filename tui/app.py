from textual.app import App

from tui.screens.archkata.freeplay import ArchKataFreePlay
from tui.screens.archkata.home import ArchKataHome
from tui.screens.archkata.katas import ArchKataKatas


class TextualApp(App):
    def __init__(self):
        self.SCREENS = {
            "archkatahome": ArchKataHome,
            "archkatakatas": ArchKataKatas,
            "archkatafreeplay": ArchKataFreePlay,
        }
        self.CSS_PATH = "styles.tcss"

        super().__init__()

    def on_mount(self):
        self.theme = "tokyo-night"
        self.push_screen("archkatahome")

    def navigate(self, route: str):
        try:
            self.push_screen(route)
        except KeyError:
            self.notify(
                f'Não foi possível navegar para a rota "{route}"', severity="error"
            )
