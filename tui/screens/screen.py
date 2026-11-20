from textual.screen import Screen as TScreen


class Screen(TScreen):
    def __init__(self, protected: bool = False):
        super().__init__()
        self.protected = protected
