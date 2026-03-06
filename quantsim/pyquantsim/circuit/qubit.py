from ..core.qubit import Qubit
from .component import Component


class QubitComponent(Component):
    qubit: Qubit

    def __init__(self, outputs: list[Component] | None = None, qubit=Qubit()):
        super().__init__(None, outputs if outputs else [])
        self.qubit = qubit
