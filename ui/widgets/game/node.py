from textual.widget import Widget
from textual.widgets import Label


class Node(Widget):
    def __init__(self, text: str, color: str):
        super().__init__(classes="w-fill bg-background round-surface center h-auto")
        self.text = text
        self.color = color
        self.selected = False

        self.__update_style()

    def compose(self):
        yield Label(self.text, classes="w-auto")

    def __update_style(self):
        if self.selected:
            self.styles.background_tint = "white 10%"
            self.styles.border = ("round", "white")
        else:
            self.styles.background_tint = f"{self.color} 10%"
            self.styles.border = ("round", self.color)

    def select(self):
        self.selected = True
        self.__update_style()

    def deselect(self):
        self.selected = False
        self.__update_style()
