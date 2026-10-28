from textual.containers import Container, Grid, Horizontal
from textual.screen import Screen
from textual.widgets import Static

from tui.widgets.tag import Tag


class Game(Screen):
    def compose(self):
        yield Grid(Main(), Sidebar(), id="game")


class Main(Container):
    def __init__(self):
        super().__init__(id="game_main")

    def compose(self):
        yield Node("Cliente")
        yield Node("Servidor")
        yield Node("Lorem")
        yield Node("Lorem")
        yield Node("Lorem")
        yield Node("Lorem")
        yield Node("Lorem")
        yield Node("Lorem")
        yield Node("Lorem")
        yield Node("Lorem")
        yield Node("Lorem")


class Node(Container):
    def __init__(self, label: str):
        super().__init__()
        self.label = label

    def compose(self):
        yield Static(self.label)


class Sidebar(Container):
    def __init__(self):
        super().__init__(id="game_sidebar", classes="box h-full")

    def compose(self):
        categories = [
            {
                "name": "Rede",
                "color": "#C7F799",
                "elements": [{"name": "Balanceador de Carga", "price": 500}],
            },
            {
                "name": "Dados",
                "color": "#99ABF7",
                "elements": [{"name": "DB Relacional", "price": 400}],
            },
        ]

        yield Static("[$foreground-muted]Nós", classes="helper")
        for category in categories:
            yield Static(
                f"[{category['color']}]•[/{category['color']}] {category['name']}"
            )
            for element in category["elements"]:
                with Container(classes="node") as container:
                    container.styles.background_tint = f"{category['color']} 10%"
                    container.styles.border_left = ("heavy", category["color"])

                    yield Static(element["name"])
                    yield Tag(f"${element['price']}", color=category["color"])
