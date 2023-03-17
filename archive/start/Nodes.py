from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal, Container
from textual.widgets import Button
from textual.reactive import reactive

class Nodes(Widget):
    # provide the initial options from which the reactive state is set and the user can choose from
    options = ["Bigprox", "Miniprox"]

    # create a reactive value that sets an initial value and is updated according to user input
    node: reactive[str] = reactive(options[0].lower())

    # use the reactive value to set the value

    def compose(self) -> ComposeResult:
        yield Container(
            Button("Bigprox", id="bigprox-button-node", classes="button"),
            Button("Miniprox", id="miniprox-button-node", classes="button"),
            classes="horizontal-group remove",
            id="node_choice_container"
        )

    def watch_node(self, task: str) -> None:
        for option in self.options:
            self.query_one(f"#{option.lower()}-button-node").remove_class('selected')
        self.query_one(f"#{self.node}-button-node").add_class('selected')