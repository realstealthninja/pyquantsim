import numpy as np
from .gate import QuantumGate


class PauliX(QuantumGate):
    def __init__(self):
        mat = np.matrix([[0, 1],[1, 0]], np.complex256)
        super().__init__(mat, "X")



