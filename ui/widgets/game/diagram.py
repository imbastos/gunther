from textual.containers import Container, Grid, Horizontal, Vertical
from textual.events import Click
from textual.widget import Widget
from textual.widgets import Static

from ui.widgets.game.arrows import Arrows
from ui.widgets.game.diagram_node import DiagramNode


class Diagram(Widget):
    def __init__(self, multiplier):
        super().__init__(classes="hatch center h-full w-1--1", id="diagram")
        self.selected_diagram_node: DiagramNode | None = None
        self.arrows = Arrows(diagram=self)
        self.multiplier = multiplier

    def on_mount(self):
        self.call_after_refresh(self.arrows.update)

    def on_resize(self):
        self.arrows.update()

    def on_click(self, event: Click):
        target = event.widget
        if isinstance(target, DiagramNode):
            if self.selected_diagram_node is None:
                self.selected_diagram_node = target
                self.selected_diagram_node.select()
            elif self.selected_diagram_node is target:
                self.selected_diagram_node.deselect()
                self.selected_diagram_node = None
            else:
                source = self.selected_diagram_node
                source.deselect()
                self.selected_diagram_node = None

                # Evita duplicar seta idêntica
                if not self.arrows.has_connection(source, target):
                    self.arrows.add(source, target)
        else:
            if self.selected_diagram_node:
                self.selected_diagram_node.deselect()
                self.selected_diagram_node = None

    def compose(self):
        self.grid = Grid(
            classes="grid-5 gutter-grid hatch p-4 w-1--1", id="diagram_nodes"
        )

        yield self.grid

        with Container(classes="bottom h-8 absolute"):
            with Horizontal(classes="center-container hatch"):
                yield Static("oi", id="requirements_missing")
            with Horizontal(classes="center-container hatch"):
                with Vertical(classes="w-auto center round-surface p-0-2"):
                    yield Static("0", id="users", classes="w-full text-center")

                    with Horizontal():
                        yield Static("[$foreground-muted]Usuários", classes="w-auto")
                        yield Static(
                            "[$error]•", id="users-indicator", classes="ml-1 h-auto"
                        )

                with Vertical(classes="w-auto center round-surface p-0-2"):
                    yield Static("$1000", id="money", classes="w-full text-center")
                    yield Static("[$foreground-muted]Dinheiro", classes="w-auto")

    def add_to_grid(self, diagram_node: DiagramNode):
        self.grid.mount(diagram_node)