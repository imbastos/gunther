import pyfiglet
from textual import on
from textual.containers import Center, Container
from textual.screen import Screen
from textual.widgets import Button, Static


class ArchKataHome(Screen):
    def compose(self):
        figlet = pyfiglet.Figlet(font="univers", width=150)
        title_art = figlet.renderText("ArchKata")

        options = [
            {"label": "► Resolver Katas", "id": "archkatakatas", "variant": "primary"},
            {"label": "► Modo Livre", "id": "archkatafreeplay", "variant": "primary"},
            {"label": "⚙ Configurações", "id": "archkatasettings", "variant": "default"},
            {"label": "⭐ Conquistas", "id": "archkataachievements", "variant": "default"},
            {"label": "🛒 Loja", "id": "archkatastore", "variant": "default"},
        ]

        with Container(classes="box"):
            yield Static(title_art, classes="title")

            with Center():
                for option in options:
                    yield Button(
                        option["label"],
                        classes="option w-50",
                        variant=option["variant"],
                        id=option["id"],
                    )

    @on(Button.Pressed, ".option")
    def on_click_option(self, event: Button.Pressed):
        self.app.navigate(event.button.id)
