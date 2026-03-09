from ..core.qubit import Qubit
from .component import Component


class Observer(Component):
    """
    Observer Represents an observer, observes the given quantum state and collapses it into either zero or one
    """

    value: bool | None = None
    end_qubit: Qubit | None

    def __init__(self, inputs: list[Component] | None = None) -> None:
        super().__init__(inputs if inputs is not None else [], None)
        self.end_qubit = None
