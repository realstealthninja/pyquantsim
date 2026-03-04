from typing import override
from PySide6.QtCore import QPointF, Signal
from quantsim.circuit.component import Component
from quantsim.gates import PauliX
from quantsim.circuit import Observer
from .caditem import CADItem


class ObserverCADItem(CADItem):
    observer: Observer = Observer() 
    inputItems = []

    def __init__(self):
        super().__init__(
            "./assets/observer.svg",
            QPointF(2, 32),
            None,
        )
        self.setToolTip(
            str(self.observer.value) if self.observer.value else "Has not been observed"
        )

    @override
    def component(self) -> Component:
        return self.observer

    @override
    def toolTip(self, /) -> str:
        return (
            str(self.observer.value) if self.observer.value else "Has not been observed"
        )
