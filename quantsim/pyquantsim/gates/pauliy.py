import numpy as np
from .gate import QuantumGate


class PauliY(QuantumGate):
    def __init__(self):
        mat = np.matrix([[0,  -1j],[1j, 0]], np.complex256)
        super().__init__(mat, "Y")


