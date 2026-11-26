from textual.widget import Widget
from textual.widgets import Label

from core.models.category import Category
from core.models.node import Node

from infra.nodes import categories

class DiagramNode(Widget):
    def __init__(self, node: Node, category: Category):
        super().__init__(classes="w-fill bg-background round-surface center h-auto diagram_node")
        self.node = node
        self.category = category
        self.selected = False

        self.__update_style()

        
    def compose(self):
        yield Label(self.node.name, classes="w-auto")

    def __update_style(self):
        if self.selected:
            self.styles.background_tint = "white 10%"
            self.styles.border = ("round", "white")
        else:
            category = next(
                (category for category in categories if category.id == self.node.category),
                None
            )
            self.styles.background_tint = f"{category.color} 10%"
            self.styles.border = ("round", category.color)

    def select(self):
        self.selected = True
        self.__update_style()

    def deselect(self):
        self.selected = False
        self.__update_style()
