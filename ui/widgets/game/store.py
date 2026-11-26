from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widget import Widget
from textual.widgets import Label

from infra.nodes import categories, nodes
from ui.widgets.game.diagram_node import DiagramNode


class Store(Widget):
    def __init__(self):
        super().__init__(
            classes="w-1--3 m-1 h-full",
        )

    def compose(self):
        with Container(classes="round-surface p-1 w-full h-full"):
            yield Label("[$text-muted]Loja", classes="mb-2")

            with VerticalScroll(classes="h-full w-full"):
                for category in categories:
                            with Vertical(classes="mb-1 w-full"):
                                yield Label(f"[{category.color}]•[$text] {category.name}", classes="mb-1")
                                for node in nodes:
                                    if node.category == category.id:
                                        yield NodeCard(node=node, category=category)
                            

class NodeCard(Widget):
    def __init__(self, category, node):
        super().__init__(classes="w-full")
        self.category = category
        self.node = node

    def compose(self):
        card = Vertical(classes="p-1 mb-1 w-full bg-background hover")
        card.styles.border_left = ("heavy", self.category.color)

        with card:
            yield Label(self.node.name)
            yield Label(f"[{self.category.color}]${self.node.price}")

    def on_click(self):
        node = DiagramNode(category=self.category, node=self.node)
        self.screen.query_one("#diagram").add_to_grid(node)