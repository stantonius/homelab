from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Button, Static, Checkbox, Label
from textual.reactive import reactive
from .Nodes import Nodes

class Tasks(Widget):

    options = ["Proxmox", "Other"]

    # create a reactive value that sets an initial value and is updated according to user input
    task: reactive[str] = reactive(options[0].lower())

    # use the reactive value to set the value

    def compose(self) -> ComposeResult:
        yield Container(
            Button("Proxmox", id="proxmox-button-task", classes=f"button {'selected' if self.task == 'proxmox' else ''}"),
            Button("Other", id="other-button-task", classes=f"button {'selected' if self.task == 'other' else ''}"),
            classes="horizontal-group",
            id="task_choice_container"
        )

