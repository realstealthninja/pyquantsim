from abc import ABC
import numpy as np


class QuantumGate(ABC):
    def __init__(self, matrix, symbol: str):
        self.matrix = matrix
        self.symbol: str = symbol

    def __array__(self):
        return np.matrix(self.matrix)

    def __mul__(self, rhs):
        return np.matrixlib.matrix(self.matrix) * np.matrixlib.matrix(rhs)
