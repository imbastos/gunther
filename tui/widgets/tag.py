from textual.widgets import Static


class Tag(Static):
    def __init__(self, content: str, color="$accent"):
        super().__init__(content, classes="tag")
        self.styles.background = color
