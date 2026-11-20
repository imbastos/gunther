import pyfiglet
from textual.widgets import Static


class Title(Static):
    def __init__(self, text: str):
        content = pyfiglet.figlet_format(text, font="rectangles").rstrip()
        super().__init__(content=content)
