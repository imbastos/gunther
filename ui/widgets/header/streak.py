from textual.widget import Widget
from textual.widgets import Static


class Streak(Widget):
    def __init__(self, streak: int):
        super().__init__(classes="p-0-1 bg-background color-muted")
        self.streak = streak

    def _update_streak(self, streak: int):
        self.streak = streak
        active = self.streak > 0

        icon = "🔥" if active else "🧊"
        color = "color-accent" if active else "color-muted"

        if active:
            self.add_class("round-accent", "tint-accent")
        else:
            self.remove_class("round-accent", "tint-accent")

        self.label.update(f"{icon} {self.streak} dias")
        self.label.set_classes(color)

    def compose(self):
        self.label = Static()
        yield self.label
        self._update_streak(streak=self.streak)

    def refresh_streak(self, streak: int):
        self._update_streak(streak=streak)
