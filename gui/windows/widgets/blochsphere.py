from math import atan2, degrees
from PySide6.QtCore import QUrl
from PySide6.QtQuickWidgets import QQuickWidget

from quantsim.circuit import Observer
from quantsim.core import Qubit


class BlochSphere(QQuickWidget):
    def __init__(self):
        super().__init__()
        self.setSource(QUrl("qml/bloch.qml"))

        self.set_qubit(Qubit())

    def set_qubit(self, qubit: Qubit):
        theta = degrees(atan2(qubit.alpha.imag, qubit.alpha.real))
        phi = degrees(atan2(qubit.beta.imag, qubit.beta.real))
        self.rootObject().setProperty("theta", phi)
        self.rootObject().setProperty("phi", theta)

    def set_observedvalue(self, observer: Observer):
        if observer.value is not None:
            if observer.value == True:
                theta = 90
                phi = 0
                self.rootObject().setProperty("theta", theta)
                self.rootObject().setProperty("phi", phi)
            else:
                theta = 180
                phi = 0
                self.rootObject().setProperty("theta", theta)
                self.rootObject().setProperty("phi", phi)
