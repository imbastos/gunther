from textual.widget import Widget
from textual.widgets import Static
from textual_image.widget import Image


class AltImage(Widget):
    def __init__(self, image: str, alt: str = "🖼"):
        super().__init__()
        self.image = image
        self.alt = alt

    def compose(self):
        try:
            yield Image(image=self.image)
        except FileNotFoundError:
            yield Static(content=self.alt, classes="alt-text")
