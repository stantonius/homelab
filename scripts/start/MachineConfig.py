from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Container
from .MachineType import MachineType
from .VMImages import VMImages

class MachineConfig(Widget):

    def compose(self) -> ComposeResult:
        yield Container(
                MachineType(),
                VMImages(),
                classes="subsection-grid box"
            )