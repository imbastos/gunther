from ui.widgets.game.arrow import Arrow
from ui.widgets.game.node import Node


class Arrows:
    def __init__(
        self,
        connections: tuple[tuple[Node, Node], ...] = (),
        diagram=None,
    ):
        self.diagram = diagram
        self.connections = [
            Arrow(source, target, diagram) for source, target in connections
        ]

    # def __iter__(self):
    #     for arrow in self.connections:
    #         yield arrow.widget

    def has_connection(self, source: Node, target: Node) -> bool:
        return any(a.source is source and a.target is target for a in self.connections)

    def add(self, source: Node, target: Node):
        arrow = Arrow(source, target, self.diagram)
        self.connections.append(arrow)

        if self.diagram and self.diagram.is_mounted:
            arrow.mount()

        return arrow

    def remove(self, arrow: "Arrow"):
        if arrow not in self.connections:
            return

        self.connections.remove(arrow)

        if arrow.widget.is_mounted:
            arrow.widget.remove()

    def update(self):
        for arrow in self.connections:
            arrow.update_position()
