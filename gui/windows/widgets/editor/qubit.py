from typing import override
from PySide6.QtCore import QPointF
from quantsim.circuit.component import Component
from quantsim.circuit.qubit import QubitComponent
from quantsim.core import Qubit
from .caditem import CADItem


class QubitCADItem(CADItem):
    qubit: Qubit
    qubitComp: QubitComponent
    outputItems = []

    def __init__(self, qubit: Qubit | None = None):
        super().__init__("./assets/qubit.svg", None, QPointF(64, 32))
        self.qubit = qubit if qubit else Qubit()
        self.qubitComp = QubitComponent(qubit=self.qubit)

        self.setToolTip(str(self.qubit))

    @override
    def component(self) -> Component:
        return self.qubitComp
