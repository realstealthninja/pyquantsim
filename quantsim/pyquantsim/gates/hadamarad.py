import numpy as np
from math import sqrt
from .gate import QuantumGate


FACTOR = 1 / sqrt(2)

class Hadamarad(QuantumGate):

    def __init__(self):
        mat = np.matrix([[FACTOR,  FACTOR],[FACTOR, -FACTOR]], np.complex256)
        super().__init__(mat, "H")


