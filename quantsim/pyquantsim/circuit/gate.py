from ..gates.gate import QuantumGate
from .component import Component


class GateComponent(Component):
    gate: QuantumGate

    def __init__(
        self,
        gate: QuantumGate,
        inputs: list[Component] | None = None,
        outputs: list[Component] | None = None,
    ) -> None:
        super().__init__(
            inputs if inputs is not None else [], outputs if outputs is not None else []
        )
        self.gate = gate

    def __array__(self):
        return self.gate.__array__()

    def __mul__(self, rhs):
        return self.gate.__mul__(rhs)
