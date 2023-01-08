from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button
from textual.containers import Container
from textual.reactive import reactive

class MachineType(Widget):
    # provide the initial options from which the reactive state is set and the user can choose from
    options = ["LXC", "VM"]

    # create a reactive value that sets an initial value and is updated according to user input
    machine_type: reactive[str] = reactive(options[0].lower())

    # use the reactive value to set the value

    def compose(self) -> ComposeResult:
        yield Container(
            Button("LXC", id="lxc-button-machinetype", classes="button"),
            Button("VM", id="vm-button-machinetype", classes="button"),
            classes="horizontal-group remove",
            id="machinetype_choice_container"
        )