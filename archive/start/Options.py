from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Container
from .Nodes import Nodes
from .Tasks import Tasks

class Options(Widget):

    def compose(self) -> ComposeResult:
        yield Container(
                Tasks(),
                Nodes(),
                classes="subsection-grid box"
            )