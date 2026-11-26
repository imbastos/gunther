from textual.containers import Container, Grid, Horizontal, Vertical
from textual.events import Click
from textual.widget import Widget
from textual.widgets import Static

from infra.nodes import NODES
from ui.widgets.game.arrows import Arrows
from ui.widgets.game.node import Node


class Diagram(Widget):
    def __init__(self):
        super().__init__(
            classes="hatch center h-full w-1--1",
        )
        self.selected_node: Node | None = None
        self.arrows = Arrows(diagram=self)

    def on_mount(self):
        self.call_after_refresh(self.arrows.update)

    def on_resize(self):
        self.arrows.update()

    def on_click(self, event: Click):
        target = event.widget
        if isinstance(target, Node):
            if self.selected_node is None:
                self.selected_node = target
                self.selected_node.select()
            elif self.selected_node is target:
                self.selected_node.deselect()
                self.selected_node = None
            else:
                source = self.selected_node
                source.deselect()
                self.selected_node = None

                # Evita duplicar seta idêntica
                if not self.arrows.has_connection(source, target):
                    self.arrows.add(source, target)
        else:
            if self.selected_node:
                self.selected_node.deselect()
                self.selected_node = None

    def compose(self):
        category = NODES["database"]
        nodes = category["nodes"]

        self.node_a = Node(text=nodes[0]["label"], color=category["color"])
        self.node_b = Node(text=nodes[1]["label"], color=category["color"])
        with Grid(classes="grid-5 gutter-1-1 hatch p-4 w-1--1"):
            yield self.node_a
            for _ in range(1, 13):
                node = category["nodes"][2]
                yield Node(text=node["label"], color=category["color"])
            yield self.node_b
        with (
            Horizontal(classes="h-5 bottom"),
            Container(classes="center-container hatch absolute"),
            Vertical(classes="w-auto center round-surface p-0-2"),
        ):
            yield Static("0", id="users", classes="w-full text-center")
            yield Static("[$foreground-muted]Usuários", classes="w-auto")
