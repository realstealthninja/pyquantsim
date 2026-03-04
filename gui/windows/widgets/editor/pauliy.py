from typing import override
from PySide6.QtCore import QPointF
from quantsim.circuit.component import Component
from quantsim.gates import PauliY
from quantsim.circuit.gate import GateComponent
from .caditem import CADItem


class PauliYCADItem(CADItem):
    gate: PauliY = PauliY()
    gateComp: GateComponent = GateComponent(gate)
    inputItems = []
    outputItems = []

    def __init__(self):
        super().__init__(
            "./assets/pauliy.svg",
            QPointF(2, 32),
            QPointF(54, 32),
        )
        self.setToolTip(str(self.gate.__array__()))

    @override
    def component(self) -> Component:
        return self.gateComp

    @override
    def toolTip(self, /) -> str:
        return str(self.gate.__array__())
