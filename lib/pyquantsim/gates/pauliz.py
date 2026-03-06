import numpy as np
from .gate import QuantumGate


class PauliZ(QuantumGate):
    def __init__(self):
        mat = np.matrix([[1,  0],[0, -1]], np.complex256)
        super().__init__(mat, "Z")


