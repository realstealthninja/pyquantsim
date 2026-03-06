import numpy as np
from .gate import QuantumGate


class InverseS(QuantumGate):
    def __init__(self):
        mat = np.matrix([[1, 0],[0, -1j]], np.complex256)
        super().__init__(mat, "S-1")